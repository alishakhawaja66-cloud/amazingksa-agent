"""
AI Service — uses Claude to generate replies and captions
"""
import os, json
import anthropic
from app.prompts.agent_prompts import SYSTEM_PROMPT, CAPTION_PROMPT, QUESTIONS, COMPLETION_MESSAGE

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_next_reply(step: int, history: list, user_message: str) -> tuple[str, bool]:
    """
    Returns (reply_text, is_complete)
    step = which question we're currently on (0-7)
    """
    is_complete = False

    # All questions answered
    if step >= len(QUESTIONS):
        return COMPLETION_MESSAGE, True

    # Build conversation history for Claude
    messages = []
    for h in history[-10:]:   # last 10 messages for context
        messages.append({"role": h["role"], "content": h["content"]})

    # Add current user message
    messages.append({"role": "user", "content": user_message})

    # Next question to ask
    next_question = QUESTIONS[step] if step < len(QUESTIONS) else None

    system = SYSTEM_PROMPT + f"\n\nCURRENT STEP: {step + 1} of {len(QUESTIONS)}"
    if next_question:
        system += f"\n\nNEXT QUESTION TO ASK: {next_question}"
        system += "\nAcknowledge their answer warmly, then ask the next question."

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system,
        messages=messages,
    )

    reply = response.content[0].text

    # Check if this was the last answer
    if step == len(QUESTIONS) - 1:
        reply = COMPLETION_MESSAGE
        is_complete = True

    return reply, is_complete


def generate_job_caption(job: dict) -> str:
    """Generate AI caption for a job posting"""
    prompt = f"""Create a job posting caption for this position:

Job Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Salary: {job['salary']}
Requirements: {job['requirements']}
Description: {job['description']}
Contact: {job['contact']}

Website: amazingksa.com
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=CAPTION_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def answer_faq(question: str) -> str:
    """Answer frequently asked questions about AmazingKSA"""
    faq_system = """You are a helpful assistant for AmazingKSA job portal.
Answer questions about the platform, jobs in Saudi Arabia, Iqama, Ajeer system, etc.
Be brief, friendly, and accurate. Reply in same language as question.
Website: amazingksa.com"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=faq_system,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text
