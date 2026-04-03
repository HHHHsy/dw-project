#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的Python后端API
完全绕过site模块问题
"""

import sys
import os

# 设置环境变量避免site模块问题
os.environ['PYTHONNOUSERSITE'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# 检查基础模块
try:
    import subprocess
    import tempfile
    import uuid
    import json
    import time
    import socket
    import threading
    print("✅ 基础模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

class SimpleHTTPServer:
    """简单的HTTP服务器"""
    
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.running = False
    
    def handle_request(self, client_socket):
        """处理HTTP请求"""
        try:
            # 接收请求数据
            request_data = client_socket.recv(1024).decode('utf-8')
            
            if not request_data:
                return
            
            # 解析请求行
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, _ = request_line.split(' ')
            
            # 处理不同路径
            if path == '/health':
                response = self.health_check()
            elif path == '/execute' and method == 'POST':
                # 读取POST数据
                content_length = 0
                for line in lines:
                    if line.startswith('Content-Length:'):
                        content_length = int(line.split(':')[1].strip())
                        break
                
                # 读取POST body
                body = ''
                if content_length > 0:
                    body = client_socket.recv(content_length).decode('utf-8')
                
                response = self.execute_code(body)
            else:
                response = self.not_found()
            
            # 发送响应
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            error_response = f"HTTP/1.1 500 Internal Server Error\r\n"
            error_response += f"Content-Type: text/plain\r\n"
            error_response += f"Access-Control-Allow-Origin: *\r\n"
            error_response += f"\r\nServer Error: {str(e)}"
            client_socket.send(error_response.encode('utf-8'))
        
        finally:
            client_socket.close()
    
    def health_check(self):
        """健康检查"""
        response_data = {
            'status': 'healthy',
            'timestamp': time.time(),
            'python_version': sys.version
        }
        
        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: application/json\r\n"
        response += f"Access-Control-Allow-Origin: *\r\n"
        response += f"\r\n{json.dumps(response_data)}"
        
        return response
    
    def execute_code(self, body):
        """执行Python代码"""
        try:
            # 解析JSON数据
            data = json.loads(body)
            code = data.get('code', '')
            
            if not code:
                return self.bad_request('缺少代码参数')
            
            # 执行代码
            result = self.run_python_code(code)
            
            response = f"HTTP/1.1 200 OK\r\n"
            response += f"Content-Type: application/json\r\n"
            response += f"Access-Control-Allow-Origin: *\r\n"
            response += f"\r\n{json.dumps(result)}"
            
            return response
            
        except Exception as e:
            return self.internal_error(str(e))
    
    def run_python_code(self, code):
        """运行Python代码"""
        # 创建临时文件
        temp_file = os.path.join(tempfile.gettempdir(), f"python_{uuid.uuid4()}.py")
        
        try:
            # 写入代码文件
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 执行代码
            start_time = time.time()
            
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'output': result.stdout,
                'error': result.stderr,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '代码执行超时（超过30秒）',
                'execution_time': 30
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'执行错误: {str(e)}'
            }
        
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def not_found(self):
        """404响应"""
        response = f"HTTP/1.1 404 Not Found\r\n"
        response += f"Content-Type: text/plain\r\n"
        response += f"Access-Control-Allow-Origin: *\r\n"
        response += f"\r\nNot Found"
        return response
    
    def bad_request(self, message):
        """400响应"""
        response = f"HTTP/1.1 400 Bad Request\r\n"
        response += f"Content-Type: text/plain\r\n"
        response += f"Access-Control-Allow-Origin: *\r\n"
        response += f"\r\n{message}"
        return response
    
    def internal_error(self, message):
        """500响应"""
        response = f"HTTP/1.1 500 Internal Server Error\r\n"
        response += f"Content-Type: text/plain\r\n"
        response += f"Access-Control-Allow-Origin: *\r\n"
        response += f"\r\n{message}"
        return response
    
    def start(self):
        """启动服务器"""
        try:
            # 创建socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            self.running = True
            
            print(f"服务器启动成功！")
            print(f"服务地址: http://{self.host}:{self.port}")
            print(f"健康检查: http://{self.host}:{self.port}/health")
            print("按 Ctrl+C 停止服务")
            
            while self.running:
                try:
                    # 接受客户端连接
                    client_socket, addr = server_socket.accept()
                    
                    # 在新线程中处理请求
                    thread = threading.Thread(target=self.handle_request, args=(client_socket,))
                    thread.daemon = True
                    thread.start()
                    
                except KeyboardInterrupt:
                    print("\\n收到停止信号...")
                    break
                except Exception as e:
                    print(f"连接错误: {e}")
            
            server_socket.close()
            print("服务器已停止")
            
        except Exception as e:
            print(f"启动失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("Python在线编译器后端服务（简单版）")
    print("=" * 60)
    print(f"Python版本: {sys.version}")
    
    # 启动服务器
    server = SimpleHTTPServer()
    server.start()

if __name__ == '__main__':
    main()