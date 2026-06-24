import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import run_chat_workflow


app = FastAPI(
    title="JarDIYn Agent Backend",
    description="Phase 3 live agent runtime backend for JarDIYn by Garden Hub.",
    version="0.2.0",
)


DEFAULT_CORS_ORIGINS = (
    "http://127.0.0.1:5500,"
    "http://localhost:5500,"
    "https://endersra.github.io"
)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGIN", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://endersra.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "demo-user"


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "jardiyn-agent-backend",
        "phase": "phase-3-live-agent-runtime",
        "llm_mode": os.getenv("LLM_MODE", "mock").lower(),
    }


@app.post("/api/agent/chat")
def agent_chat(request: ChatRequest):
    return run_chat_workflow(
        user_message=request.message,
        user_id=request.user_id,
    )