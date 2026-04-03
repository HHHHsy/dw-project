@echo off
chcp 65001 > nul
echo ========================================
echo Python在线编译器后端服务启动脚本
echo ========================================
echo.

cd /d %~dp0

:: 使用-S参数绕过site模块问题
echo 正在启动后端服务...
python -S no_site.py

pause