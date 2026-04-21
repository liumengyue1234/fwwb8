"""
审思明辨 - 智判法案双擎系统
后端主入口 FastAPI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import json
import httpx
import asyncio
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="审思明辨 - 智判法案双擎系统 API",
    description="面向法律从业者的智能辅助平台",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== 配置 =====================
DELI_APPID = "QthdBErlyaYvyXul"
DELI_SECRET = "EC5D455E6BD348CE8E18BE05926D2EBE"
DELI_BASE = "https://openapi.delilegal.com/api/qa/v3/search"

# 元器 Yuanqi AI Agent（用户可替换为自己的 appid/appkey）
YUANQI_APPID = os.getenv("YUANQI_APPID", "YOUR_YUANQI_APPID")
YUANQI_APPKEY = os.getenv("YUANQI_APPKEY", "YOUR_YUANQI_APPKEY")
YUANQI_URL = "https://yuanqi.tencent.com/openapi/v1/agent/chat/completions"

# ===================== 数据模型 =====================
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_id: Optional[str] = "user_default"
    stream: Optional[bool] = False

class CaseSearchRequest(BaseModel):
    query: str
    page_no: Optional[int] = 1
    page_size: Optional[int] = 5
    court_level: Optional[List[str]] = None
    year_start: Optional[str] = None
    year_end: Optional[str] = None

class LawSearchRequest(BaseModel):
    query: str
    page_no: Optional[int] = 1
    page_size: Optional[int] = 5
    field_name: Optional[str] = "semantic"

class StrategyRequest(BaseModel):
    case_text: str
    user_id: Optional[str] = "user_default"

# ===================== 健康检查 =====================
@app.get("/")
def root():
    return {"status": "ok", "system": "审思明辨 - 智判法案双擎系统", "version": "1.0.0"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

# ===================== 类案检索 =====================
@app.post("/api/case/search")
async def search_cases(req: CaseSearchRequest):
    """
    调用得理开放平台 API 进行类案检索
    """
    condition = {
        "keywordArr": [req.query]
    }
    if req.court_level:
        condition["courtLevelArr"] = req.court_level
    if req.year_start:
        condition["caseYearStart"] = req.year_start
    if req.year_end:
        condition["caseYearEnd"] = req.year_end

    payload = {
        "pageNo": req.page_no,
        "pageSize": req.page_size,
        "sortField": "correlation",
        "sortOrder": "desc",
        "condition": condition
    }

    headers = {
        "Content-Type": "application/json",
        "appid": DELI_APPID,
        "secret": DELI_SECRET
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{DELI_BASE}/queryListCase",
                json=payload,
                headers=headers
            )
            data = resp.json()
            return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"类案检索失败: {str(e)}")


# ===================== 法规检索 =====================
@app.post("/api/law/search")
async def search_laws(req: LawSearchRequest):
    """
    调用得理开放平台 API 进行法规检索
    """
    payload = {
        "pageNo": req.page_no,
        "pageSize": req.page_size,
        "sortField": "correlation",
        "sortOrder": "desc",
        "condition": {
            "keywords": [req.query],
            "fieldName": req.field_name
        }
    }

    headers = {
        "Content-Type": "application/json",
        "appid": DELI_APPID,
        "secret": DELI_SECRET
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{DELI_BASE}/queryListLaw",
                json=payload,
                headers=headers
            )
            data = resp.json()
            return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"法规检索失败: {str(e)}")


# ===================== 法规详情 =====================
@app.get("/api/law/detail/{law_id}")
async def get_law_detail(law_id: str):
    """
    获取法规详情
    """
    headers = {
        "Content-Type": "application/json",
        "appid": DELI_APPID,
        "secret": DELI_SECRET
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                f"{DELI_BASE}/lawInfo?lawId={law_id}&merge=true",
                headers=headers
            )
            data = resp.json()
            return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取法规详情失败: {str(e)}")


# ===================== 智能问答（直连 Demo 模式）=====================
@app.post("/api/chat")
async def chat(req: ChatRequest):
    """
    智能法律问答 - 调用腾讯元器 AI Agent
    若未配置 YUANQI_APPID，则返回 Demo 响应
    """
    if YUANQI_APPID == "YOUR_YUANQI_APPID":
        # Demo 模式：直接调用得理 API 检索后汇总
        query = req.messages[-1].content if req.messages else ""
        return await demo_chat_response(query)

    messages_payload = []
    for msg in req.messages:
        messages_payload.append({
            "role": msg.role,
            "content": [{"type": "text", "text": msg.content}]
        })

    payload = {
        "assistant_id": YUANQI_APPID,
        "user_id": req.user_id,
        "stream": False,
        "messages": messages_payload
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YUANQI_APPKEY}",
        "X-Source": "openapi"
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(YUANQI_URL, json=payload, headers=headers)
            data = resp.json()
            content = ""
            if data.get("choices"):
                content = data["choices"][0].get("message", {}).get("content", "")
            return {"success": True, "content": content, "raw": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 问答失败: {str(e)}")


async def demo_chat_response(query: str):
    """Demo 模式：组合检索法条和案例并生成摘要"""
    results = []

    # 法规检索
    law_req = LawSearchRequest(query=query, page_size=3)
    try:
        law_data = await search_laws(law_req)
        laws = []
        if law_data.get("data", {}).get("body", {}).get("data"):
            for item in law_data["data"]["body"]["data"][:3]:
                laws.append(f"📜 {item.get('title', '未知法规')} ({item.get('levelName', '')})")
        results.append("**相关法律法规：**\n" + "\n".join(laws) if laws else "")
    except:
        pass

    # 案例检索
    case_req = CaseSearchRequest(query=query, page_size=3)
    try:
        case_data = await search_cases(case_req)
        cases = []
        if case_data.get("data", {}).get("body", {}).get("data"):
            for item in case_data["data"]["body"]["data"][:3]:
                case_name = item.get("name") or item.get("title") or "未知案例"
                court = item.get("court") or item.get("courtName") or ""
                cases.append(f"⚖️ {case_name}（{court}）")
        results.append("**相关类案参考：**\n" + "\n".join(cases) if cases else "")
    except:
        pass

    content = f"您好！关于「{query}」，以下是智能检索结果：\n\n"
    content += "\n\n".join([r for r in results if r])
    if not any(results):
        content += "暂未检索到直接相关内容，建议调整关键词或联系专业律师进一步咨询。"
    content += "\n\n> *注：当前为演示模式，配置元器 AI Agent 后可获得更深度的智能分析。*"

    return {"success": True, "content": content}


# ===================== 诉讼策略推演 =====================
@app.post("/api/strategy")
async def generate_strategy(req: StrategyRequest):
    """
    诉讼策略推演 - 基于案情生成对方律师视角的质证意见和风险提示
    """
    query = req.case_text[:200]

    # 并发检索法条 + 案例
    law_req = LawSearchRequest(query=query, page_size=5)
    case_req = CaseSearchRequest(query=query, page_size=5)

    law_result = None
    case_result = None
    try:
        law_result = await search_laws(law_req)
    except:
        pass
    try:
        case_result = await search_cases(case_req)
    except:
        pass

    # 提取数据
    relevant_laws = []
    if law_result and law_result.get("data", {}).get("body", {}).get("data"):
        for item in law_result["data"]["body"]["data"][:5]:
            relevant_laws.append({
                "title": item.get("title", ""),
                "level": item.get("levelName", ""),
                "id": item.get("id") or item.get("lawsId", "")
            })

    relevant_cases = []
    if case_result and case_result.get("data", {}).get("body", {}).get("data"):
        for item in case_result["data"]["body"]["data"][:5]:
            relevant_cases.append({
                "name": item.get("name") or item.get("title") or "",
                "court": item.get("court") or item.get("courtName") or "",
                "date": item.get("judgeDate") or item.get("caseYear") or ""
            })

    # 生成策略报告
    report = generate_strategy_report(req.case_text, relevant_laws, relevant_cases)

    return {
        "success": True,
        "report": report,
        "relevant_laws": relevant_laws,
        "relevant_cases": relevant_cases
    }


def generate_strategy_report(case_text: str, laws: list, cases: list) -> dict:
    """生成诉讼策略分析报告"""
    law_names = "、".join([l["title"] for l in laws[:3]]) if laws else "暂无检索到相关法规"
    case_names = "、".join([c["name"] for c in cases[:3] if c["name"]]) if cases else "暂无检索到相关案例"

    return {
        "overview": f"基于您提交的案情材料，系统已从法律知识库中检索到 {len(laws)} 条相关法规、{len(cases)} 件类似案例，以下为综合分析报告。",
        "opponent_perspective": {
            "title": "对方律师视角 · 质证意见",
            "points": [
                "📌 **程序合规性审查**：检查起诉材料是否满足《民事诉讼法》规定的形式要件，包括管辖权、诉讼主体资格、诉讼时效等。",
                "📌 **证据链完整性质疑**：对提交证据的真实性、关联性和合法性提出异议，要求对方举证证明证据来源合法。",
                "📌 **法律适用争议**：就案件适用的法律条文提出不同解释，援引对己方有利的司法解释或典型案例。",
                f"📌 **相关法规参考**：{law_names}"
            ]
        },
        "risk_assessment": {
            "title": "风险评估",
            "risks": [
                {"level": "高", "item": "诉讼时效风险", "desc": "请确认起诉时效未届满，否则存在被驳回诉讼请求的风险。"},
                {"level": "中", "item": "举证责任分配", "desc": "根据现有材料，建议进一步完善书证和电子证据，确保证据链条完整。"},
                {"level": "低", "item": "程序瑕疵风险", "desc": "材料形式基本完备，注意送达程序合规性。"}
            ]
        },
        "strategy_suggestions": {
            "title": "诉讼策略建议",
            "suggestions": [
                "1. **证据补强**：在开庭前补充完善证据材料，特别是电子数据和书面合同原件。",
                "2. **类案研究**：参考类似案例裁判规律，预判法院倾向性意见。",
                f"3. **法条援引**：重点关注 {law_names if law_names != '暂无检索到相关法规' else '相关法律规定'}，构建法律论证逻辑。",
                "4. **和解评估**：综合考量诉讼成本与胜诉概率，评估庭前调解可行性。",
                "5. **备选方案**：准备诉讼外争议解决预案（仲裁/调解），降低诉讼风险。"
            ]
        },
        "similar_cases_summary": f"检索到 {len(cases)} 件类案：{case_names}" if cases else "未检索到高度相似案例，建议扩大关键词范围重新检索。"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
