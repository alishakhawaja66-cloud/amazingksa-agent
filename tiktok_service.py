"""
TikTok Service (TikTok Content Posting API)
Note: TikTok API only supports video posting, not text posts.
We post job videos or use their Direct Message API.
"""
import os, httpx

TIKTOK_API = "https://open.tiktokapis.com/v2"
ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
OPEN_ID = os.getenv("TIKTOK_OPEN_ID", "")


def post_tiktok_video(caption: str, video_url: str = "") -> str:
    """
    Post a video to TikTok with job caption.
    video_url: publicly accessible URL of the job video/image slideshow.
    Returns post_id.
    """
    if not video_url:
        # TikTok requires video — skip if no video available
        return "no_video_provided"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8",
    }

    # Initialize upload
    r1 = httpx.post(
        f"{TIKTOK_API}/post/publish/video/init/",
        headers=headers,
        json={
            "post_info": {
                "title": caption[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000,
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url,
            },
        },
    )
    data = r1.json()
    return data.get("data", {}).get("publish_id", "")


def send_tiktok_dm(recipient_open_id: str, message: str):
    """Send a DM on TikTok (requires special API access)."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    httpx.post(
        f"{TIKTOK_API}/dm/conversation/message/create/",
        headers=headers,
        json={
            "conversation_id": recipient_open_id,
            "message_type": "TEXT",
            "content": {"text": message},
        },
    )
