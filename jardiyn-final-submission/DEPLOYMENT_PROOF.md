# JarDIYn Project 3 Deployment Proof

## Deployed Frontend

The browser-based Phase 3 agent demo is available through GitHub Pages:

https://endersra.github.io/jardiyn-garden-hub/jardiyn-final-submission/src/phase3-agent-demo.html

## Deployed Backend

The FastAPI backend is deployed on Render:

https://jardiyn-agent-backend-api.onrender.com

## Health Check

The deployed backend health endpoint confirms live mode:

https://jardiyn-agent-backend-api.onrender.com/api/health

Expected response includes:

status: ok  
service: jardiyn-agent-backend  
phase: phase-3-live-agent-runtime  
llm_mode: live  

## Live Agent Chat Endpoint

The deployed backend exposes the Project 3 agent workflow at:

https://jardiyn-agent-backend-api.onrender.com/api/agent/chat

## Agent Workflow Proven

The deployed workflow routes requests through:

Frontend browser demo  
→ FastAPI backend  
→ orchestrator  
→ garden memory tool  
→ seasonal context tool  
→ Claude-powered garden reasoner  
→ structured reviewer validation  
→ returned agent trace  

## Security Note

The Anthropic API key is not committed to GitHub. It is stored only as a Render environment variable.
