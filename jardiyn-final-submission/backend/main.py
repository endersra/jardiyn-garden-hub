from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="JarDIYn Agent Backend",
    description="Phase 3 live agent runtime backend for JarDIYn by Garden Hub.",
    version="0.1.0",
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


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "jardiyn-agent-backend",
        "phase": "phase-3-live-agent-runtime",
        "llm_mode": "not_connected_yet",
    }
