#!/bin/bash
echo "======================================="
echo "  审思明辨 · 智判法案双擎系统"
echo "  启动脚本"
echo "======================================="

# 后端
echo "[1/2] 启动后端..."
cd backend
pip install -r requirements.txt -q
python main.py &
BACKEND_PID=$!
cd ..

sleep 2

# 前端
echo "[2/2] 启动前端..."
cd frontend
npm install --silent
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 启动完成！"
echo "   前端: http://localhost:3000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
wait
