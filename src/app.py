import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.agents import analyze_message
from src.ml_engine import ml_predict_label
from src.feedback import save_feedback

app = FastAPI(title="VeriPhish Engine")

class AnalyzeRequest(BaseModel):
    content: str
    input_type: str = "LINE"

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")

class FeedbackRequest(BaseModel):
    content: str
    input_type: str
    predicted_label: str
    correct_label: str
    reason: str = ""

def get_html_content():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: Template not found</h1>"

HTML_CONTENT = get_html_content()

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):

    result = analyze_message(req.content, req.input_type)

    ml_label, ml_scores = ml_predict_label(req.content, req.input_type)

    if ml_label:
        if ml_label == "RED" and result["classification"] != "RED":
            result["classification"] = "RED"
            result["risk_label"] = "紅色魚：高風險詐騙"
            result["fish"] = "🔴🐟"
            result["short_title"] = "高風險，請勿操作"
            result["risk_score"] = max(result["risk_score"], 7.5)
            result["evidence"].insert(0, "訓練模型判斷此訊息接近高風險詐騙樣本。")

        elif ml_label == "YELLOW" and result["classification"] == "GREEN":
            result["classification"] = "YELLOW"
            result["risk_label"] = "黃色魚：中風險可疑訊息"
            result["fish"] = "🟡🐟"
            result["short_title"] = "可疑，建議先查證"
            result["risk_score"] = max(result["risk_score"], 4.5)
            result["evidence"].insert(0, "訓練模型判斷此訊息接近可疑訊息樣本。")

        result["agents"].append({
            "name": "資料訓練分類模型代理",
            "score": round(result["risk_score"], 1),
            "finding": "使用 TF-IDF + Logistic Regression 輔助判斷。",
            "reasoning": f"模型預測結果：{ml_label}；信心分數：{ml_scores}"
        })

        result["summary"] = f"多代理系統綜合規則式代理與訓練模型結果後，判定總風險分數為 {result['risk_score']}/10，因此釣出：{result['risk_label']}。"

    return result

@app.post("/api/feedback")
def feedback(req: FeedbackRequest):
    save_feedback(
        req.content, 
        req.input_type, 
        req.predicted_label, 
        req.correct_label, 
        req.reason
    )
    return {"status": "ok", "message": "Feedback saved"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=HTML_CONTENT)
