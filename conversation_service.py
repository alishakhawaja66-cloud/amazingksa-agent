"""
Conversation Handler — manages DM conversations with candidates
"""
import json
from sqlalchemy.orm import Session
from app.models.database import Candidate, Conversation
from app.services.ai_service import get_next_reply
from app.services.notification_service import send_candidate_notification

# Maps conversation step → candidate field to save
STEP_FIELDS = {
    0: "full_name",
    1: "age",
    2: "city",
    3: "education",
    4: "experience",
    5: "phone",
    6: "email",
    7: "applied_job",
}


def handle_dm(platform: str, uid: str, user_message: str, db: Session) -> str:
    """
    Process an incoming DM and return the agent's reply.
    Creates/updates conversation and candidate records.
    """

    # Get or create conversation
    conv = db.query(Conversation).filter_by(platform=platform, platform_uid=uid).first()
    if not conv:
        conv = Conversation(platform=platform, platform_uid=uid, step=0, history="[]")
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # Get or create candidate
    candidate = None
    if conv.candidate_id:
        candidate = db.query(Candidate).filter_by(id=conv.candidate_id).first()
    if not candidate:
        candidate = Candidate(platform=platform, platform_uid=uid)
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        conv.candidate_id = candidate.id
        db.commit()

    # Load history
    history = json.loads(conv.history or "[]")

    # Get AI reply
    reply, is_complete = get_next_reply(conv.step, history, user_message)

    # Save user answer to candidate record
    field = STEP_FIELDS.get(conv.step - 1)  # previous step's field
    if field and user_message.strip():
        setattr(candidate, field, user_message.strip())
        db.commit()

    # Update history
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    conv.history = json.dumps(history[-20:])  # keep last 20

    # Advance step (only if not complete)
    if not is_complete:
        conv.step += 1
    else:
        candidate.is_complete = True
        db.commit()

        # Send notification
        send_candidate_notification({
            "platform":    candidate.platform,
            "full_name":   candidate.full_name,
            "age":         candidate.age,
            "city":        candidate.city,
            "education":   candidate.education,
            "experience":  candidate.experience,
            "phone":       candidate.phone,
            "email":       candidate.email,
            "applied_job": candidate.applied_job,
            "created_at":  str(candidate.created_at),
        })
        candidate.notified = True

    db.commit()
    return reply
