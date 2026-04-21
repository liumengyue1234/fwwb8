@echo off
chcp 65001 >nul
echo.
echo ======================================
echo   审思明辨 · 智判法案双擎系统
echo   一键启动脚本
echo ======================================
echo.

:: 启动后端
echo [1/2] 正在启动后端服务 (http://localhost:8000)...
cd backend
pip install -r requirements.txt -q
start "后端服务 - 审思明辨" cmd /k "python main.py"
cd ..

:: 等待后端就绪
timeout /t 3 /nobreak >nul

:: 启动前端
echo [2/2] 正在启动前端服务 (http://localhost:3000)...
cd frontend
call npm install --silent
start "前端服务 - 审思明辨" cmd /k "npm run dev"
cd ..

echo.
echo ✅ 启动完成！
echo    前端访问地址: http://localhost:3000
echo    后端 API 文档: http://localhost:8000/docs
echo.
pause
