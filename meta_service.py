"""
Facebook & Instagram Service (Meta Graph API)
"""
import os, httpx

GRAPH = "https://graph.facebook.com/v19.0"
TOKEN = os.getenv("META_ACCESS_TOKEN", "")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
IG_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")


# ── Post to Facebook Page ─────────────────────────────────────────────────────
def post_to_facebook(caption: str) -> str:
    """Post a text/photo to Facebook Page. Returns post_id."""
    url = f"{GRAPH}/{PAGE_ID}/feed"
    r = httpx.post(url, data={"message": caption, "access_token": TOKEN})
    data = r.json()
    return data.get("id", "")


# ── Post to Instagram ─────────────────────────────────────────────────────────
def post_to_instagram(caption: str, image_url: str = "") -> str:
    """Post to Instagram business account. Returns post_id."""
    if not image_url:
        # Instagram requires an image — use a default AmazingKSA banner
        image_url = "https://amazingksa.com/wp-content/uploads/amazingksa-banner.jpg"

    # Step 1: create container
    r1 = httpx.post(
        f"{GRAPH}/{IG_ID}/media",
        data={"image_url": image_url, "caption": caption, "access_token": TOKEN},
    )
    container_id = r1.json().get("id", "")
    if not container_id:
        return ""

    # Step 2: publish
    r2 = httpx.post(
        f"{GRAPH}/{IG_ID}/media_publish",
        data={"creation_id": container_id, "access_token": TOKEN},
    )
    return r2.json().get("id", "")


# ── Reply to Facebook Comment ─────────────────────────────────────────────────
def reply_to_fb_comment(comment_id: str, message: str):
    httpx.post(
        f"{GRAPH}/{comment_id}/comments",
        data={"message": message, "access_token": TOKEN},
    )


# ── Send Facebook DM ──────────────────────────────────────────────────────────
def send_fb_dm(recipient_id: str, message: str):
    httpx.post(
        f"{GRAPH}/{PAGE_ID}/messages",
        json={
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "access_token": TOKEN,
        },
    )


# ── Send Instagram DM ─────────────────────────────────────────────────────────
def send_ig_dm(recipient_id: str, message: str):
    httpx.post(
        f"{GRAPH}/{IG_ID}/messages",
        json={
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "access_token": TOKEN,
        },
    )


# ── Get Facebook Page Comments ────────────────────────────────────────────────
def get_fb_comments(post_id: str) -> list:
    r = httpx.get(
        f"{GRAPH}/{post_id}/comments",
        params={"access_token": TOKEN, "fields": "id,from,message"},
    )
    return r.json().get("data", [])
