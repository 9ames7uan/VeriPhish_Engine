import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.agents import analyze_message
from src.utils import clamp, has_any, extract_urls, extract_domains

app = FastAPI(title="VeriPhish Engine")

class AnalyzeRequest(BaseModel):
    content: str
    input_type: str = "LINE"

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")

def get_html_content():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: Template not found</h1>"

HTML_CONTENT = get_html_content()

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    return analyze_message(req.content, req.input_type)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def index():
    """
    Serves the main application dashboard.
    """
    return HTMLResponse(content=HTML_CONTENT)
