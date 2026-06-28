"""
AmazingKSA Recruitment Agent — Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from app.models.database import Base, engine
from app.api.routes import router

# Create all DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AmazingKSA Recruitment Agent",
    description="AI agent that posts jobs and manages candidates on Facebook, Instagram, TikTok",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "AmazingKSA Recruitment Agent is Live! 🇸🇦",
        "docs": "/docs",
        "health": "/api/health",
    }
