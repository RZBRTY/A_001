@echo off
chcp 65001 >nul
echo ========================================
echo   智能招聘多Agent系统 - 演示
echo ========================================
echo.
cd /d "%~dp0"
python demo.py
if errorlevel 1 (
    echo.
    echo 尝试使用 py 命令...
    py demo.py
)
if errorlevel 1 (
    echo.
    echo 尝试使用 python3 命令...
    python3 demo.py
)
echo.
pause
