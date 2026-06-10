# architecture.md — JarDIYn System Design

## Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | React + TypeScript + Tailwind | Type safety, componentization, design system |
| PWA | Service Worker + localStorage | Offline capability, local persistence |
| Backend | Python + FastAPI | Async-friendly, LLM integration ready |
| Database | SQLite (proto) → PostgreSQL (prod) | Lightweight initial, PostGIS for spatial |
| LLM Provider | Claude API (Opus/Sonnet/Haiku) | Model waterfall, cost-optimized routing |
| Storage | AWS S3 / local FS | Photos, depth maps, exports |
| Hosting | Vercel (frontend), Render (backend) | Serverless, scalable, free tier available |

## Data Flow

```
User Input (Profile, Photo, Text)
    ↓
Frontend Validation
    ↓
API Endpoint (7 core + 3 spatial)
    ↓
Orchestrator Agent (Opus) - Plans & Delegates
    ↓
Specialist Agents (Sonnet) - Domain Work
    ↓
Grounding Data (USDA zones, soil, frost dates)
    ↓
Claude API Call
    ↓
Reviewer Agent (Haiku) - Quality Gates
    ↓
Response Formatting
    ↓
Frontend Display
    ↓
User Exports (Markdown, JSON, GLB)
```

## 10 API Endpoints

### Core (7)
1. `POST /identify` — Photo → species + diagnosis
2. `POST /zone` — GPS → USDA hardiness zone
3. `POST /report` — Profile → seasonal DIY report
4. `POST /chat` — Message → context-aware response
5. `POST /design` — Text → 2D layout JSON
6. `POST /schedule` — Weather + soil → watering plan
7. `POST /calendar` — Zone + plants → 12-month timeline

### Spatial Intelligence (3) [v17]
8. `POST /depth` — Photo → depth map + segments
9. `POST /reconstruct` — Depth → scene graph
10. `POST /placement` — Scene graph → recommendations

## Product Lenses

| Lens | View | Data Perspective |
|---|---|---|
| **Dashboard** | Garden health at a glance | Summary metrics, today's actions |
| **Design** | 2D layout builder + AR | Spatial arrangement, plant placement |
| **Report** | Seasonal DIY brief | Calendar, tasks, soil amendments |
| **Chat** | Q&A interface | Conversational, profile-grounded |
| **History** | Timeline audit trail | Changes, observations, iterations |

## System Boundaries

- **In Scope (v25):** Profile, identify, design, report, chat, history, offline
- **Out of Scope (v25):** Real smart home control, community features, payment processing
- **Future (v26+):** Live AI, watering automation, mobile native

## Deployment Architecture

### v25 (Demo-Ready - Static)
- Frontend: GitHub Pages / Vercel free tier
- Backend: None (all mocked)
- Cost: $0

### v26 (Live AI)
- Frontend: Vercel ($0 free tier)
- Backend: Render ($7/month)
- Database: PostgreSQL managed ($10/month)
- Storage: AWS S3 ($5/month)
- **Total: ~$22/month infrastructure + $140/month AI**

### v2.0 (Mobile Native)
- iOS app: App Store ($99/year)
- Android app: Play Store ($25 one-time)
- Backend: Same as v26

## Intelligence Layers

### Layer 1: Grounding (RAG)
- USDA Plant Hardiness Zone data
- Soil type characteristics
- Frost dates by region
- Pest & disease management (organic)
- Native plant recommendations

### Layer 2: Reasoning (Claude)
- Agentic orchestration (Opus)
- Domain specialists (Sonnet)
- Quality review (Haiku)

### Layer 3: Spatial (v17)
- Depth estimation (monocular + LiDAR)
- Semantic segmentation (beds, plants, paths)
- Scene graph export

## Model Waterfall

```
High-Complexity Tasks
    ↓
Opus 4.5 (Orchestration, Evaluation)
    ↓ Delegates to
Medium-Complexity Tasks
    ↓
Sonnet 4.6 (Specialists: Plant ID, Design, Chat)
    ↓ References
Low-Complexity Tasks
    ↓
Haiku 4.5 (Review, Classification, Zone lookup)
```

**Cost Optimization:**
- Opus used ~10% of tasks (orchestration, evaluation)
- Sonnet used ~85% of tasks (core specialists)
- Haiku used ~5% of tasks (review, classification)
- **Result:** ~$140/month AI cost at 1K users × 50 calls/month

## Security

- No secrets in code (environment variables only)
- Prompts versioned in `prompts/` (never inline)
- Rate limiting: 100 req/hour per IP
- HTTPS enforced (production)
- GDPR/CCPA ready (no GPS storage, data deletion on request)
