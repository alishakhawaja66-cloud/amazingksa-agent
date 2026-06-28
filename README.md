# AmazingKSA Recruitment Agent — Setup Guide

## Project Structure
```
amazingksa-recruitment/
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Python packages
├── .env.example                     # Environment variables template
└── app/
    ├── api/
    │   └── routes.py                # All API endpoints & webhooks
    ├── models/
    │   └── database.py              # SQLite database models
    ├── services/
    │   ├── ai_service.py            # Claude AI integration
    │   ├── meta_service.py          # Facebook & Instagram API
    │   ├── tiktok_service.py        # TikTok API
    │   ├── conversation_service.py  # DM conversation handler
    │   └── notification_service.py  # Email notifications
    └── prompts/
        └── agent_prompts.py         # AI prompts & messages
```

---

## STEP 1 — Install Python & Setup

```bash
# Install Python 3.11+
# Then run:
pip install -r requirements.txt

# Copy env file
cp .env.example .env
```

---

## STEP 2 — Fill in .env file

Open `.env` and fill in:

### Claude API Key (already have this!)
```
ANTHROPIC_API_KEY=sk-ant-...  ← your key from console.anthropic.com
```

### Facebook/Instagram
After creating Meta App (next step):
```
META_APP_ID=...
META_APP_SECRET=...
META_ACCESS_TOKEN=...        ← Page Access Token
FACEBOOK_PAGE_ID=...         ← Amazing KSA page ID
INSTAGRAM_ACCOUNT_ID=...     ← Amazing KSA Instagram ID
```

### Your notification email
```
NOTIFY_EMAIL=amazingksa9@gmail.com
SMTP_USER=amazingksa9@gmail.com
SMTP_PASS=your_gmail_app_password   ← Google App Password (not regular password)
```

---

## STEP 3 — Get Facebook API Keys

1. Go to **developers.facebook.com**
2. Click **My Apps → Create App**
3. Choose **Business** type
4. Add products: **Messenger** + **Instagram Graph API** + **Webhooks**
5. Go to **Messenger Settings → Access Tokens**
6. Select your **Amazing KSA** page → Generate token
7. Copy **Page Access Token** → paste in `.env`
8. Copy **Page ID** → paste in `.env`

---

## STEP 4 — Setup Webhooks

Your server URL will be: `https://yourdomain.com/api/webhook/facebook`

In Meta Developer Console:
1. Webhooks → Add Callback URL: `https://yourdomain.com/api/webhook/facebook`
2. Verify Token: `amazingksa_verify_2024`
3. Subscribe to: `messages`, `messaging_postbacks`, `feed`

---

## STEP 5 — Get TikTok API Keys

1. Go to **developers.tiktok.com**
2. Create App → Content Posting API
3. Get Access Token
4. Paste in `.env`

---

## STEP 6 — Run the Server

```bash
# Development
uvicorn main:app --reload --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000/docs to see all APIs

---

## STEP 7 — Post a Job (API call)

```bash
curl -X POST http://localhost:8000/api/post-job \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Driver Needed in Riyadh",
    "company": "AmazingKSA",
    "location": "Riyadh, Saudi Arabia",
    "salary": "2000-3000 SAR",
    "requirements": "Valid driving license, 2 years experience",
    "description": "We need experienced drivers for daily commute service",
    "contact": "amazingksa9@gmail.com",
    "platforms": ["facebook", "instagram"]
  }'
```

---

## HOW IT WORKS

### Comment Detection
When someone comments "Interested", "job", "salary", etc. on your post:
→ Agent auto-replies: "Thank you! Please check your DMs 📩"
→ Sends them a DM automatically

### DM Conversation
When someone DMs Amazing KSA:
→ Agent asks 8 questions one by one
→ Saves all answers to database
→ Sends you complete info by email when done

### Job Posting
You call the API → Agent generates AI caption → Posts to Facebook + Instagram + TikTok

---

## VIEW ALL CANDIDATES

Open: http://localhost:8000/api/candidates

Or connect to WordPress via REST API for dashboard view.

---

## DEPLOY TO SERVER (Hostinger/VPS)

```bash
# Install on server
pip install -r requirements.txt

# Run with PM2 (keep alive)
pip install uvicorn
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name amazingksa-agent

# Or use systemd service
```

---

## NEED HELP?
Contact: amazingksa9@gmail.com
Website: amazingksa.com
