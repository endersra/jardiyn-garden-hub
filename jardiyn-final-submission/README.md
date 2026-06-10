# JarDIYn by GardenHub

**An agentic garden intelligence platform that gives homeowners zone-accurate, organic-first landscaping recommendations.**

Course project for AI402/502 (Generative AI), built with the Ledger agentic methodology and Claude Code.

> This project uses Claude Code. The main Claude instruction file is `CLAUDE.md`. Claude agents are stored in `.claude/agents/`. Claude skills are stored in `.claude/skills/`.

---

## What the project does

JarDIYn turns a smartphone and a garden profile into a design tool. A user sets up their garden (USDA zone, soil, sun, goals), and JarDIYn's agentic AI engine provides:

- **Plant & pest identification** from photos, with organic remedies
- **Garden design** — natural language to a zone-correct plant palette
- **Personalized seasonal reports** with prioritized DIY tasks
- **A conversational assistant** grounded in the user's garden profile
- **A history timeline** and an **agent trace** for full transparency

## Who it is for

Novice homeowners, eco-minded gardeners, and landscape designers — see `personas.md`.

## Problem it solves

Traditional landscaping has a precision gap, a visualization deficit, and a knowledge barrier. Homeowners want sustainable gardens but lack zone-accurate guidance. JarDIYn closes that gap — see `prd.md`.

---

## Main features

| Feature | Lens | Traces to |
|---|---|---|
| Garden profile setup | Dashboard | UC-01..04 |
| Garden design copilot | Design | UC-01 |
| Personalized DIY report | Report | UC-02 |
| Conversational assistant | Chat | UC-04 |
| Garden history timeline | History | all |
| Agent trace transparency | Agent Trace | methodology |

## Tech stack

- **Frontend:** HTML + CSS + ES modules (prototype); React + TypeScript planned for production
- **Service layer:** mock API (v25) then Python + FastAPI (v26)
- **AI:** Claude API — Opus (orchestration), Sonnet (specialists), Haiku (review)
- **Data:** localStorage (v25) then PostgreSQL (production)
- **Recommendation core:** deterministic rule engine first, LLM narrative second

Full detail in `architecture.md`.

---

## How to run the project

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd jardiyn-final-submission

# 2. (Optional) create a local env file — the demo runs without it
cp .env.example .env

# 3. Start the development server (no dependencies needed)
npm run dev

# 4. Open the app
#    http://localhost:8080
```

Then follow the 9-step walkthrough in `docs/DEMO_SCRIPT.md`.

## How to test the project

```bash
npm test
```

This runs the evaluation harness (`tests/test_planted_signals.mjs`), which verifies all six planted signals are detected. Expected result: **8 passed, 0 failed**.

---

## Project structure

```
jardiyn-final-submission/
├── CLAUDE.md                   Master Claude Code instruction file
├── README.md                   This file
├── prd.md                      Product requirements
├── personas.md                 User personas
├── architecture.md             Tech stack, data flow, system design
├── domain-primer.md            Garden domain knowledge for agents
├── synthetic-data-strategy.md  Test data approach + planted signals
├── evaluation.md               Success metrics + planted-signal tests
├── development-checklist.md    Phased build progress
├── feedback-log.md             Decisions and iterations
│
├── .claude/
│   ├── agents/                 6 sub-agents (orchestrator + 5 specialists)
│   └── skills/                 6 skills, each <name>/SKILL.md
│
├── src/                        Application code
│   ├── index.html              App shell — 6 lenses
│   ├── app.js                  UI controller
│   ├── styles.css              Design system
│   ├── services/
│   │   ├── ruleEngine.js       Deterministic recommendation engine
│   │   └── mockApi.js          Mock service layer + agent trace
│   └── prompts/                Versioned LLM prompts (4)
│
├── tests/
│   └── test_planted_signals.mjs   Evaluation harness (8 checks)
│
├── data/                       Synthetic data (3 JSON, 6 planted signals)
│   ├── garden_profiles.json
│   ├── site_observations.json
│   └── expected_recommendations.json
│
├── docs/
│   ├── DEMO_SCRIPT.md          9-step golden path
│   └── GRADING_AUDIT.md        Self-audit checklist
│
├── server.mjs                  Zero-dependency dev server
├── package.json                Scripts: dev, test, evaluate
├── .env.example                Env var template (no real secrets)
└── .gitignore                  Excludes .env and secrets
```

## Claude Code setup

This project follows the Ledger agentic workflow:

- **`CLAUDE.md`** is the persistent project instruction file Claude Code reads on every call.
- **`.claude/agents/`** holds 6 sub-agents: `orchestrator` (Opus) plans and delegates; `product-strategist`, `garden-reasoner`, `ui-engineer`, `data-architect` (Sonnet) do specialist work; `reviewer` (Haiku) gates quality.
- **`.claude/skills/`** holds 6 skills, each a `<name>/SKILL.md` recipe.

## Evaluation

`evaluation.md` defines 6 planted signals and success metrics. The harness in `tests/` proves all signals are caught. Current result: **8/8 PASS**. See also `docs/GRADING_AUDIT.md`.

## Synthetic data

The `data/` folder contains structured synthetic garden profiles and observations, each carrying a documented planted signal. The approach is described in `synthetic-data-strategy.md`.

## Notes for the grader

- The project runs entirely in **mock mode** — no API key required to demo or test.
- **No real API keys** are committed. `.env.example` holds only placeholders; `.env` is gitignored.
- Recommendation logic is **deterministic-first** (rule engine), which is why the evaluation harness is reliable.
- Start with `docs/DEMO_SCRIPT.md`, then run `npm test`.

## License

MIT.

---

## Build Log

### Tools used to build this
- **Claude (Anthropic)** — primary AI for planning, agent design, and code generation
- **Claude Code methodology** — agentic workflow with orchestrator + specialist sub-agents
- **VS Code / browser editing** for final polish

### System prompts (verbatim)

#### Plant & Pest Identification prompt (`src/prompts/identify.md`)

#### Garden Design prompt (`src/prompts/design.md`)

(Full prompts in `src/prompts/`.)

### Prompting techniques used
- **Role + constraints** — every agent starts with a clear role and non-negotiables (see `.claude/agents/*.md`)
- **Structured output** — every prompt specifies required JSON shape, so the app can parse responses reliably
- **Grounding** — `domain-primer.md` (USDA zones, soils, frost dates, pests) is injected as context on every domain call
- **Deterministic-first** — recommendation logic runs a rule engine (`src/services/ruleEngine.js`) *before* any LLM narrative, so the six planted signals are caught reliably
- **Model waterfall** — Opus for orchestration, Sonnet for specialists, Haiku for review (per `CLAUDE.md`)

### Evaluation

**What "good" means here:** the system must surface all six planted signals
(zone mismatch, clay drainage, overwatering, invasive species, pH imbalance,
frost date violation) on the synthetic test profiles.

**How I tested:** ran `npm test`, which executes
`tests/test_planted_signals.mjs` against the synthetic fixtures in `data/`.

**Result: 8 / 8 checks PASS** — all six planted signals detected, plus
trigger-traceability and severity-gating checks. See `evaluation.md` for
the full table.

### Honest limits
- The v25 build runs in **mock mode** — no live LLM calls. Live mode (v26)
  is fully spec'd in `architecture.md` and the service layer is structured
  for a drop-in swap.
- Plant ID accuracy is only as good as the synthetic test set; a real
  deployment would need a labeled image corpus.
- Smart-home control is mocked for safety; real integration requires an
  OAuth flow and a security review.

### What I'd do next (v26)
- Replace `src/services/mockApi.js` calls with real Claude API calls via
  a small FastAPI backend (specified in `architecture.md`)
- Deploy backend to Render, swap `LLM_MODE=mock` for `LLM_MODE=anthropic_api`
- Build a labeled test set for plant ID precision/recall measurement

- Add build log to README
  
