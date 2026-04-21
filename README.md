# 审思明辨 · 智判法案双擎系统

> 面向法律从业者的智能辅助平台 | 腾讯服创赛 D06 赛道

## ✨ 功能特性

| 模块 | 说明 |
|------|------|
| 💬 **智能问答** | 自然语言咨询法律问题，实时检索法条与案例 |
| 📚 **法条检索** | 语义/关键词双模式检索，覆盖全量法律法规 |
| 🔍 **类案匹配** | 海量司法裁判文书检索，快速定位类案要旨 |
| 🎯 **策略推演** | 对方律师视角分析，生成质证意见与风险报告 |

## 🛠️ 技术架构

- **前端**：Vue 3 + Vite + Vue Router
- **后端**：Python FastAPI
- **AI 引擎**：腾讯混元大模型（通过元器 Agent API）
- **法律数据**：得理开放平台 API（案例检索 + 法规检索）

## 🚀 快速启动

### 方式一：一键启动脚本（Windows）

```bash
start.bat
```

### 方式二：手动启动

**启动后端：**
```bash
cd backend
pip install -r requirements.txt
python main.py
# 服务运行在 http://localhost:8000
```

**启动前端：**
```bash
cd frontend
npm install
npm run dev
# 页面访问 http://localhost:3000
```

## ⚙️ 配置说明

### 得理开放平台（已内置）
- AppID: `QthdBErlyaYvyXul`
- Secret: 已配置在后端

### 腾讯元器 AI Agent（可选）
若需要更智能的问答能力，在 `backend/.env` 中配置：
```
YUANQI_APPID=您的元器智能体AppID
YUANQI_APPKEY=您的元器智能体AppKey
```

> 未配置时系统将使用演示模式，直接调用得理 API 返回法规和案例摘要。

## 📦 项目结构

```
ssmb/
├── backend/          # FastAPI 后端
│   ├── main.py       # 主入口
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # Vue3 前端
│   ├── src/
│   │   ├── views/    # 四大功能页面
│   │   │   ├── Chat.vue        # 智能问答
│   │   │   ├── LawSearch.vue   # 法条检索
│   │   │   ├── CaseSearch.vue  # 类案匹配
│   │   │   └── Strategy.vue    # 策略推演
│   │   ├── App.vue   # 主布局
│   │   └── main.js
│   ├── index.html
│   └── package.json
├── start.bat         # Windows 一键启动
├── start.sh          # Linux/Mac 启动
└── README.md
```

## 🏆 赛事信息

- 赛道：腾讯服创赛 D06
- 项目名：**审思明辨 · 智判法案双擎系统**
- 核心价值：推动法律服务智能化、普惠化

---

*Powered by 腾讯混元 × 得理科技*
