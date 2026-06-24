# JarDIYn Garden Hub

---

## Project 3 Final Deployment Summary

JarDIYn now includes a deployed Phase 3 agent workflow that connects a browser-based frontend to a live FastAPI backend.

### Live Links

- Frontend demo: https://endersra.github.io/jardiyn-garden-hub/jardiyn-final-submission/src/phase3-agent-demo.html
- Backend health check: https://jardiyn-agent-backend-api.onrender.com/api/health
- Backend agent endpoint: https://jardiyn-agent-backend-api.onrender.com/api/agent/chat

### Phase 3 Agent Workflow

The deployed backend routes a gardening question through:

Frontend browser demo  
→ FastAPI backend  
→ orchestrator  
→ garden memory tool  
→ seasonal context tool  
→ Claude-powered garden reasoner  
→ structured reviewer validation  
→ agent trace returned to the frontend  

### Project 3 Evidence

This version demonstrates:

- A deployed frontend URL that can be opened in a browser.
- A deployed backend API running in live mode.
- A Claude-powered reasoning step through the Anthropic API.
- A structured reviewer validation step.
- A returned agent trace showing the workflow path.
- Backend tests for health, runtime mode, agent chat, LLM client behavior, and reviewer validation.
- Environment-based secret handling so the Anthropic API key is not committed to GitHub.

Additional proof is documented in `jardiyn-final-submission/DEPLOYMENT_PROOF.md`.

