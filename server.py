#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Python教学平台后端服务器
"""

import sys
import os
import subprocess
import tempfile
import uuid
import json
import time
import socket
import threading
import pymysql
import hashlib

# 项目根目录（server.py所在的目录）
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class SimpleServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.running = False
    
    def handle_request(self, client_socket):
        try:
            request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            if not request_data:
                return
            
            lines = request_data.split('\r\n')
            if not lines:
                return
            
            request_line = lines[0]
            parts = request_line.split(' ')
            if len(parts) < 3:
                return
            
            method, path, _ = parts
            
            print(f"[REQUEST] {method} {path}")
            
            if method == 'OPTIONS':
                response = self.cors_response()
                client_socket.send(response.encode('utf-8'))
                return
            
            if path == '/health':
                response = self.health_check()
                client_socket.send(response.encode('utf-8'))
                return
            
            if (path == '/execute' or path == '/api/login' or path == '/api/register') and method == 'POST':
                content_length = 0
                for line in lines:
                    if line.startswith('Content-Length:'):
                        try:
                            content_length = int(line.split(':')[1].strip())
                        except:
                            pass
                        break
                
                body = ''
                parts = request_data.split('\r\n\r\n', 1)
                if len(parts) > 1:
                    body = parts[1]
                
                remaining = content_length - len(body.encode('utf-8'))
                while remaining > 0:
                    chunk = client_socket.recv(min(remaining, 4096)).decode('utf-8', errors='ignore')
                    if not chunk:
                        break
                    body += chunk
                    remaining -= len(chunk.encode('utf-8'))
                
                if path == '/execute':
                    response = self.execute_code(body)
                elif path == '/api/login':
                    response = self.handle_login(body)
                elif path == '/api/register':
                    response = self.handle_register(body)
                    
                if isinstance(response, bytes):
                    client_socket.send(response)
                else:
                    client_socket.send(response.encode('utf-8'))
                return
            
            response = self.serve_file(path)
            if isinstance(response, bytes):
                client_socket.send(response)
            else:
                client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"[ERROR] {e}")
            error_resp = "HTTP/1.1 500 Internal Server Error\r\n"
            error_resp += "Content-Type: text/plain\r\n"
            error_resp += "Access-Control-Allow-Origin: *\r\n"
            error_resp += "\r\nServer Error"
            client_socket.send(error_resp.encode('utf-8'))
        
        finally:
            client_socket.close()
    
    def cors_response(self):
        resp = "HTTP/1.1 200 OK\r\n"
        resp += "Access-Control-Allow-Origin: *\r\n"
        resp += "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        resp += "Access-Control-Allow-Headers: Content-Type\r\n"
        resp += "Access-Control-Max-Age: 86400\r\n"
        resp += "\r\n"
        return resp
    
    def health_check(self):
        data = {'status': 'ok', 'time': time.time()}
        resp = "HTTP/1.1 200 OK\r\n"
        resp += "Content-Type: application/json\r\n"
        resp += "Access-Control-Allow-Origin: *\r\n"
        resp += "\r\n"
        resp += json.dumps(data)
        return resp
    
    def get_db_connection(self):
        return pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='hrxcy31.',
            database='python_edu',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
        
    def handle_login(self, body):
        try:
            data = json.loads(body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return self.json_response({'success': False, 'message': '用户名或密码不能为空'})
                
            conn = self.get_db_connection()
            try:
                with conn.cursor() as cursor:
                    sql = "SELECT id, username, password FROM users WHERE username = %s"
                    cursor.execute(sql, (username,))
                    user = cursor.fetchone()
                    
                    if user and user['password'] == self.hash_password(password):
                        return self.json_response({
                            'success': True, 
                            'message': '登录成功',
                            'user': {'id': user['id'], 'username': user['username']}
                        })
                    else:
                        return self.json_response({'success': False, 'message': '用户名或密码错误'})
            finally:
                conn.close()
        except Exception as e:
            return self.json_response({'success': False, 'message': str(e)})

    def handle_register(self, body):
        try:
            data = json.loads(body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return self.json_response({'success': False, 'message': '用户名或密码不能为空'})
                
            conn = self.get_db_connection()
            try:
                with conn.cursor() as cursor:
                    # Check if username exists
                    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                    if cursor.fetchone():
                        return self.json_response({'success': False, 'message': '用户名已存在'})
                        
                    # Insert new user
                    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                    cursor.execute(sql, (username, self.hash_password(password)))
                    conn.commit()
                    
                    return self.json_response({'success': True, 'message': '注册成功，请登录'})
            finally:
                conn.close()
        except Exception as e:
            return self.json_response({'success': False, 'message': str(e)})
            
    def json_response(self, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        resp = "HTTP/1.1 200 OK\r\n"
        resp += "Content-Type: application/json; charset=utf-8\r\n"
        resp += f"Content-Length: {len(body)}\r\n"
        resp += "Access-Control-Allow-Origin: *\r\n"
        resp += "\r\n"
        return resp.encode('utf-8') + body

    def execute_code(self, body):
        try:
            data = json.loads(body)
            code = data.get('code', '')
            inputs = data.get('inputs', [])
            
            # 将前端传来的输入数组转换为字符串，供标准输入使用
            input_str = '\n'.join(inputs) + '\n' if inputs else ''
            
            temp_file = os.path.join(tempfile.gettempdir(), f"py_{uuid.uuid4().hex}.py")
            
            try:
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # 在 Windows 下，Python 默认输出编码可能不是 utf-8，强制指定 PYTHONIOENCODING
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                
                result = subprocess.run(
                    [sys.executable, '-S', temp_file],
                    input=input_str,
                    capture_output=True,
                    text=True,
                    timeout=5,  # 将超时时间缩短，避免长时间卡死
                    encoding='utf-8',
                    errors='replace',
                    env=env
                )
                
                output = {
                    'success': True,
                    'output': result.stdout,
                    'error': result.stderr
                }
            finally:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            
            # 必须指定 charset=utf-8，否则浏览器可能解析错误
            body = json.dumps(output, ensure_ascii=False).encode('utf-8')
            
            resp = "HTTP/1.1 200 OK\r\n"
            resp += "Content-Type: application/json; charset=utf-8\r\n"
            resp += f"Content-Length: {len(body)}\r\n"
            resp += "Access-Control-Allow-Origin: *\r\n"
            resp += "\r\n"
            
            return resp.encode('utf-8') + body
            
        except Exception as e:
            body = json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8')
            
            resp = "HTTP/1.1 200 OK\r\n"
            resp += "Content-Type: application/json; charset=utf-8\r\n"
            resp += f"Content-Length: {len(body)}\r\n"
            resp += "Access-Control-Allow-Origin: *\r\n"
            resp += "\r\n"
            
            return resp.encode('utf-8') + body
    
    def serve_file(self, path):
        if path == '/' or path == '':
            path = '/index.html'
        
        file_path = os.path.join(PROJECT_ROOT, path.lstrip('/'))
        print(f"[FILE] Serving: {file_path}")
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found"
        
        content_type = 'text/html'
        if path.endswith('.css'):
            content_type = 'text/css'
        elif path.endswith('.js'):
            content_type = 'application/javascript'
        elif path.endswith('.json'):
            content_type = 'application/json'
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            header = f"HTTP/1.1 200 OK\r\n"
            header += f"Content-Type: {content_type}\r\n"
            header += f"Content-Length: {len(content)}\r\n"
            header += "Access-Control-Allow-Origin: *\r\n"
            header += "\r\n"
            
            return header.encode('utf-8') + content
            
        except Exception as e:
            print(f"[ERROR] Read file: {e}")
            return f"HTTP/1.1 500 Error\r\nContent-Type: text/plain\r\n\r\n{str(e)}"
    
    def start(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            self.running = True
            
            print("=" * 60)
            print("Python教学平台 - 后端服务器")
            print("=" * 60)
            print(f"项目根目录: {PROJECT_ROOT}")
            print(f"服务地址: http://localhost:{self.port}")
            print("按 Ctrl+C 停止服务")
            print("=" * 60)
            
            while self.running:
                try:
                    client_socket, addr = server_socket.accept()
                    thread = threading.Thread(target=self.handle_request, args=(client_socket,))
                    thread.daemon = True
                    thread.start()
                except KeyboardInterrupt:
                    print("\n正在停止...")
                    break
                except Exception as e:
                    print(f"[ERROR] {e}")
            
            server_socket.close()
            print("服务器已停止")
            
        except Exception as e:
            print(f"启动失败: {e}")

if __name__ == '__main__':
    server = SimpleServer()
    server.start()
