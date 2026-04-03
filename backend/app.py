#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python在线编译器后端API
支持完整的Python功能，包括文件操作、用户输入等
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import tempfile
import uuid
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 代码执行配置
MAX_EXECUTION_TIME = 30  # 最大执行时间（秒）
MAX_OUTPUT_LENGTH = 10000  # 最大输出长度

class PythonCompiler:
    """Python代码编译器"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.sessions = {}
    
    def execute_code(self, code, session_id=None, user_inputs=None):
        """执行Python代码"""
        
        # 生成临时文件名
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # 创建临时文件
        temp_file = os.path.join(self.temp_dir, f"python_{session_id}.py")
        
        try:
            # 预处理代码（处理用户输入）
            processed_code = self.preprocess_code(code, user_inputs)
            
            # 写入临时文件
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(processed_code)
            
            # 执行Python代码
            result = self.run_python_code(temp_file)
            
            return {
                'success': True,
                'output': result['output'],
                'error': result['error'],
                'execution_time': result['execution_time'],
                'session_id': session_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'执行错误: {str(e)}',
                'session_id': session_id
            }
        
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def preprocess_code(self, code, user_inputs=None):
        """预处理代码，处理用户输入"""
        
        if not user_inputs:
            user_inputs = []
        
        # 添加输入处理逻辑
        input_processor = '''
# 输入处理函数
import sys
import io

class InputProcessor:
    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0
    
    def readline(self):
        if self.index < len(self.inputs):
            result = self.inputs[self.index]
            self.index += 1
            return result
        return ''

# 替换标准输入
input_processor = InputProcessor({})
original_input = __builtins__.input

def simulated_input(prompt=''):
    if prompt:
        print(prompt, end='')
    return input_processor.readline()

__builtins__.input = simulated_input

'''.format(json.dumps(user_inputs))
        
        return input_processor + code
    
    def run_python_code(self, file_path):
        """运行Python代码"""
        
        start_time = datetime.now()
        
        try:
            # 使用subprocess执行，设置超时
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=MAX_EXECUTION_TIME,
                encoding='utf-8'
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # 处理输出
            output = result.stdout
            error = result.stderr
            
            # 限制输出长度
            if len(output) > MAX_OUTPUT_LENGTH:
                output = output[:MAX_OUTPUT_LENGTH] + '\n... (输出过长，已截断)'
            
            if len(error) > MAX_OUTPUT_LENGTH:
                error = error[:MAX_OUTPUT_LENGTH] + '\n... (错误信息过长，已截断)'
            
            return {
                'output': output,
                'error': error,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'output': '',
                'error': f'代码执行超时（超过{MAX_EXECUTION_TIME}秒）',
                'execution_time': execution_time
            }
        
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'output': '',
                'error': f'执行过程错误: {str(e)}',
                'execution_time': execution_time
            }

# 创建编译器实例
compiler = PythonCompiler()

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': 'Python在线编译器API',
        'version': '1.0',
        'endpoints': {
            '/execute': '执行Python代码',
            '/health': '服务健康检查'
        }
    })

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version
    })

@app.route('/execute', methods=['POST'])
def execute_code():
    """执行Python代码"""
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': '缺少代码参数'
            }), 400
        
        code = data['code']
        session_id = data.get('session_id')
        user_inputs = data.get('user_inputs', [])
        
        # 执行代码
        result = compiler.execute_code(code, session_id, user_inputs)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/execute/batch', methods=['POST'])
def execute_batch():
    """批量执行代码（用于测试）"""
    
    try:
        data = request.get_json()
        
        if not data or 'codes' not in data:
            return jsonify({
                'success': False,
                'error': '缺少代码列表参数'
            }), 400
        
        codes = data['codes']
        results = []
        
        for i, code in enumerate(codes):
            result = compiler.execute_code(code, f"batch_{i}")
            results.append(result)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

if __name__ == '__main__':
    # 启动服务器
    print("Python在线编译器后端服务启动中...")
    print(f"Python版本: {sys.version}")
    print("服务地址: http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )