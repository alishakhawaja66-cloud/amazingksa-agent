"""
AmazingKSA Recruitment Agent — Main Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, httpx, json
import anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
FACEBOOK_PAGE_ID  = os.getenv("FACEBOOK_PAGE_ID", "")
IG_ACCOUNT_ID     = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
GRAPH             = "https://graph.facebook.com/v19.0"

claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

app = FastAPI(title="AmazingKSA Recruitment Agent", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "AmazingKSA Recruitment Agent is Live! 🇸🇦", "docs": "/docs", "health": "/health"}

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "AmazingKSA"}

@app.post("/post-job")
async def post_job(request: Request):
    body = await request.json()
    prompt = f"""Create a professional job posting in Arabic and English:
Job Title: {body.get('title','')}
Location: {body.get('location','Saudi Arabia')}
Salary: {body.get('salary','')}
Requirements: {body.get('requirements','')}
Website: amazingksa.com
Make it attractive with emojis."""
    response = claude.messages.create(model="claude-sonnet-4-6", max_tokens=500, messages=[{"role":"user","content":prompt}])
    caption = response.content[0].text
    r = httpx.post(f"{GRAPH}/{FACEBOOK_PAGE_ID}/feed", data={"message": caption, "access_token": META_ACCESS_TOKEN})
    result = r.json()
    return {"success": "id" in result, "post_id": result.get("id",""), "caption": caption}

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == os.getenv("SECRET_KEY","amazingksa2024secretkey"):
        return int(params.get("hub.challenge", 0))
    return {"error": "Invalid token"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    body = await request.json()
    try:
        for entry in body.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging.get("sender", {}).get("id")
                message = messaging.get("message", {}).get("text", "")
                if sender_id and message:
                    reply = get_ai_reply(message)
                    httpx.post(f"{GRAPH}/{FACEBOOK_PAGE_ID}/messages", json={"recipient":{"id":sender_id},"message":{"text":reply},"access_token":META_ACCESS_TOKEN})
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if value.get("item") == "comment":
                    comment_id = value.get("comment_id","")
                    comment = value.get("message","")
                    if comment_id and comment:
                        reply = get_ai_reply(comment)
                        httpx.post(f"{GRAPH}/{comment_id}/comments", data={"message":reply,"access_token":META_ACCESS_TOKEN})
    except Exception as e:
        print(f"Webhook error: {e}")
    return {"status": "ok"}

def get_ai_reply(message: str) -> str:
    response = claude.messages.create(model="claude-sonnet-4-6", max_tokens=300,
        system="You are a helpful recruitment assistant for AmazingKSA job portal. Help with job inquiries, Saudi Arabia work info, Iqama, Ajeer. Be friendly and brief. Reply in same language as message. Website: amazingksa.com",
        messages=[{"role":"user","content":message}])
    return response.content[0].text

@app.get("/test-ai")
async def test_ai():
    reply = get_ai_reply("What jobs are available in Saudi Arabia?")
    return {"reply": reply}
