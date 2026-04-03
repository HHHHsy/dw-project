#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版Python在线编译器后端API
解决编码问题，使用更简单的启动方式
"""

import sys
import os
import subprocess
import tempfile
import uuid
import json
from datetime import datetime

# 检查是否安装了必要的库
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json as json_module
    print("✅ 使用内置库启动服务")
except ImportError as e:
    print(f"❌ 缺少必要的库: {e}")
    sys.exit(1)

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
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def preprocess_code(self, code, user_inputs=None):
        """预处理代码，处理用户输入"""
        
        if not user_inputs:
            user_inputs = []
        
        # 添加输入处理逻辑
        input_processor = '''
# 输入处理函数
import sys

class InputProcessor:
    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0
    
    def readline(self):
        if self.index < len(self.inputs):
            result = self.inputs[self.index]
            self.index += 1
            return result
        return '用户输入模拟'

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
                timeout=30,  # 30秒超时
                encoding='utf-8'
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # 处理输出
            output = result.stdout
            error = result.stderr
            
            # 限制输出长度
            if len(output) > 10000:
                output = output[:10000] + '\n... (输出过长，已截断)'
            
            if len(error) > 10000:
                error = error[:10000] + '\n... (错误信息过长，已截断)'
            
            return {
                'output': output,
                'error': error,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'output': '',
                'error': f'代码执行超时（超过30秒）',
                'execution_time': execution_time
            }
        
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'output': '',
                'error': f'执行过程错误: {str(e)}',
                'execution_time': execution_time
            }

class PythonAPIHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self.send_health()
        elif self.path == '/':
            self.send_index()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/execute':
            self.execute_code()
        else:
            self.send_error(404, "Not Found")
    
    def send_health(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def send_index(self):
        """首页信息"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'message': 'Python在线编译器API',
            'version': '1.0',
            'endpoints': {
                '/execute': '执行Python代码',
                '/health': '服务健康检查'
            }
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def execute_code(self):
        """执行Python代码"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            data = json.loads(post_data.decode('utf-8'))
            
            if 'code' not in data:
                self.send_error(400, "缺少代码参数")
                return
            
            code = data['code']
            session_id = data.get('session_id')
            user_inputs = data.get('user_inputs', [])
            
            # 执行代码
            result = compiler.execute_code(code, session_id, user_inputs)
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"服务器错误: {str(e)}")
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

# 创建编译器实例
compiler = PythonCompiler()

def main():
    """主函数"""
    print("=" * 60)
    print("Python在线编译器后端服务（简化版）")
    print("=" * 60)
    print(f"Python版本: {sys.version}")
    print("服务地址: http://localhost:5000")
    print("API文档: http://localhost:5000/")
    print("健康检查: http://localhost:5000/health")
    print("=" * 60)
    
    try:
        # 启动HTTP服务器
        server = HTTPServer(('0.0.0.0', 5000), PythonAPIHandler)
        print("服务启动成功！")
        print("按 Ctrl+C 停止服务")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == '__main__':
    main()