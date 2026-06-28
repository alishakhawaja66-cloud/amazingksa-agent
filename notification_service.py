"""
Notification Service — sends candidate info via email when they complete the form
"""
import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "amazingksa9@gmail.com")


def send_candidate_notification(candidate: dict):
    """Send email notification when a candidate completes all questions."""

    subject = f"🎉 New Candidate: {candidate.get('full_name', 'Unknown')} — {candidate.get('applied_job', '')}"

    body = f"""
=== NEW CANDIDATE APPLICATION ===
AmazingKSA Recruitment Agent

Platform:    {candidate.get('platform', '').upper()}
Date/Time:   {candidate.get('created_at', '')}

── PERSONAL INFO ──────────────────
Full Name:   {candidate.get('full_name', '')}
Age:         {candidate.get('age', '')}
City:        {candidate.get('city', '')}

── EDUCATION & EXPERIENCE ─────────
Education:   {candidate.get('education', '')}
Experience:  {candidate.get('experience', '')}

── CONTACT INFO ───────────────────
Phone:       {candidate.get('phone', '')}
Email:       {candidate.get('email', '')}

── JOB APPLIED ────────────────────
Job:         {candidate.get('applied_job', '')}

==================================
Login to amazingksa.com/wp-admin to view all candidates.
"""

    print(f"[NOTIFICATION] New candidate: {candidate.get('full_name')} — {candidate.get('applied_job')}")
    print(body)

    # Try sending email via Gmail SMTP
    try:
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASS", "")

        if smtp_user and smtp_pass:
            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = NOTIFY_EMAIL
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, NOTIFY_EMAIL, msg.as_string())
                print(f"[EMAIL] Sent to {NOTIFY_EMAIL}")
        else:
            print("[EMAIL] SMTP credentials not set — email not sent")

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
