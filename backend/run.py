#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python后端服务启动脚本
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Python在线编译器后端服务")
    print("=" * 60)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 启动服务
    print("服务启动中...")
    print("访问地址: http://localhost:5000")
    print("API文档: http://localhost:5000/")
    print("健康检查: http://localhost:5000/health")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )