# CLAUDE.md — JarDIYn Project Instructions
**Master rule set for AI agents working on JarDIYn. Used by Claude Code for autonomous development.**

---

## Mission

You are working on **JarDIYn by GardenHub**, which solves **the disconnect between homeowners' sustainable landscaping aspirations and their ability to execute them** for **homeowners, gardeners, designers, and sustainability enthusiasts**. The intended outcome is **a demo-ready agentic garden intelligence platform that turns smartphones into garden design tools and provides zone-accurate, organic-first recommendations**.

Everything you build must serve a real-world problem and a real-world user — not technical novelty for its own sake.

Your role is to plan, build, evaluate, and improve this product autonomously, subject to the constraints and conventions in this file.

---

## Operating Mindset

- **Plan deeply before building.** If you are uncertain about scope, requirements, or architecture, propose a plan and request confirmation before writing code.
- **Build for a real user, not for technical impressiveness.** Every feature must trace to a documented user pain point in prd.md.
- **Move fast, fail fast.** A working prototype that gets feedback is worth more than a polished system built on assumptions.
- **Take audit-grade ownership.** Every line of code is potentially a courtroom exhibit. Code must be explainable, traceable, and grounded in tried-and-tested open-source patterns.
- **Low temperature is correct for this work.** Prefer determinism and explainability over creativity in implementation. Save creativity for design, naming, and UX.

---

## Required Project Artifacts

Maintain these Markdown files in the repository root. Create them if they don't exist, and keep them current as the project evolves.

| File | Purpose |
|---|---|
| **README.md** | Project overview, directory structure, setup steps |
| **architecture.md** | Tech stack, data flow, system boundaries, deployment |
| **prd.md** | Product requirements: problems → specifications → value |
| **personas.md** | Users, their goals, and their workflows |
| **domain-primer.md** | Domain knowledge (USDA zones, soil types, frost dates, pests) |
| **synthetic-data-strategy.md** | Test data: what to mock, what formats, what sources |
| **evaluation.md** | Success metrics, test cases, planted signals |
| **development-checklist.md** | Phased build plan; agent checks off items as complete |
| **feedback-log.md** | Append every user-provided prompt or correction |

Render any of these in VS Code with Ctrl+Shift+V.

---

## Tech Stack & Conventions

### Frontend
- **React + TypeScript + Tailwind** (browser workspace)
- **React Native / Expo** (mobile PWA alternative)
- **PWA-capable** (offline support via service worker)
- **Localhost:5173** (dev server)

### Backend
- **Python + FastAPI** (agentic API gateway)
- **PostgreSQL + PostGIS** (production database; SQLite for prototype)
- **Redis** (sessions, rate limits)
- **Localhost:8000** (dev server)

### LLM Provider
- **Claude API** (ANTHROPIC_API_KEY environment variable)
  - Opus 4.5: Orchestration, evaluation
  - Sonnet 4.6: Specialists (Plant ID, design, chat, reports)
  - Haiku 4.5: Review, classification
- **Backup providers** (Gemini, Grok) — adapters documented but Claude primary

### Hosting
- **Vercel** (frontend)
- **Render** (backend)
- **AWS S3 / Cloudflare R2** (photo/scan storage)

### Code Conventions
- **Python:** Type hints, ruff for linting, pytest for tests
- **TypeScript:** Strict mode, ESLint, Prettier, functional components
- **No raw HTML** when a component framework is in use
- **All API keys** live in environment variables, never in code
- **Every LLM prompt** lives in a versioned prompt library (`prompts/`), never inline in business logic

---

## Design System

### UX Primitives (5 core actions available everywhere)
1. **Profile** — Set/edit garden zone, soil, sun, goals
2. **Scan** — Upload photo for plant/pest ID
3. **Design** — Create 2D layout from text description
4. **Report** — Generate personalized seasonal DIY brief
5. **Chat** — Ask context-aware garden questions

### Lenses (5 core + extensions)
- **Core:** Dashboard (health at a glance) · Design (2D layout + AR) · Report (seasonal tips) · Chat (conversational) · History (timeline)
- **Extensions:** DepthLab (spatial intelligence, v17) · CAD/BIM · API Map · Trace Panel · Multi-Model Routing

**Principle:** Every primitive works in every lens. Behavior is consistent across the experience.

---

## The Agentic Workflow

### Phase 0 — Discovery & Synthesis ✅
**Status:** Complete (research paper analyzed, pain points extracted, use cases prioritized)

**Artifacts:**
- prd.md (6 use cases, 3 tiers, scope defined)
- personas.md (4 user types, goals, workflows)
- domain-primer.md (USDA zones, soil types, pests, frost dates)

### Phase 1 — Architecture ✅
**Status:** Complete (tech stack chosen, API contracts written, evaluation metrics defined)

**Artifacts:**
- architecture.md (10 endpoints, data flow, tech stack)
- evaluation.md (6 planted signals, success metrics)
- synthetic-data-strategy.md (mock data approach)

### Phase 2 — Harness Setup ✅
**Status:** Complete (7 agents designed, 6 skills defined)

**Artifacts in `.claude/agents/`:**
- orchestrator.md (Opus — plans, delegates, verifies)
- product-strategist.md (Sonnet — requirements, PRD)
- coder.md (Sonnet — implements app code, rule engine, services)
- garden-reasoner.md (Sonnet — zone/soil/plant domain logic)
- ui-engineer.md (Sonnet — frontend build)
- data-architect.md (Sonnet — synthetic data, schemas)
- reviewer.md (Haiku — quality gates)

**Artifacts in `.claude/skills/`:**
- create-feature/SKILL.md
- run-evaluation/SKILL.md
- generate-synthetic-data/SKILL.md
- update-documentation/SKILL.md
- plant-pest-identification/SKILL.md, garden-design/SKILL.md

### Phase 3 — Autonomous Build 🔄
**Status:** In progress (demo-ready app working, prompts versioned, APIs specified)

**Checklist:** development-checklist.md (updated as features complete)

### Phase 4 — Evaluation 🔄
**Status:** In progress (planted signals designed, test fixtures created)

**Artifacts:** evaluation.md (success metrics + planted signal test cases)

### Phase 5 — Iteration 🔄
**Status:** Ongoing (feedback-log.md grows with each user input)

**Process:** Read feedback-log.md before each iteration, update agents/prompts accordingly.

---

## Model Waterfall (Cost-Optimized Routing)

| Tier | Model | When to Use | Cost/1M Tokens |
|---|---|---|---|
| **Top** | Claude Opus 4.5 | Orchestration, planning, evaluation, cross-domain | $15 in / $75 out |
| **Middle** | Claude Sonnet 4.6 | Coding, design, specialists, sub-agent work | $3 in / $15 out |
| **Bottom** | Claude Haiku 4.5 | Code review, audits, classification, repetitive | $0.25 in / $1.25 out |

**Rules:**
- Orchestrator runs ~15× cost of Sonnet; must never write code or do sub-agent work
- Smaller models have ~10–100× less parametric knowledge; always supply domain context in Markdown
- Evaluation (Phase 4) is where NOT to cut costs; use top tier

---

## Sub-Agent Pattern

Every agent is a Markdown file in `.claude/agents/` with this structure:

```
[Agent Name]

Mandate
[One sentence: what is this agent for?]

Operating Mindset
[How should this agent think? What are its non-negotiables?]

Customers Served
[Who benefits from this agent's output?]

Inputs
[What files, prompts, or context must this agent read before acting?]

Outputs
[What artifacts does this agent produce? In what format?]

Quality Gates
- Is it correct?
- Does it fit the codebase?
- Does it match the design system?
- Does it respect CLAUDE.md?

Escalation
[When does this agent hand off to another agent or to the user?]
```

---

## Skill Pattern

Every skill is a Markdown file in `.claude/skills/` with this structure:

```
[Skill Name]

When to Use
[Trigger conditions]

Prerequisites
[Tools, APIs, files, credentials needed]

Steps
- [Step 1]
- [Step 2]
- [Step 3]

Expected Output
[What success looks like]

Known Failure Modes
[Edge cases and how to handle them]
```

**Critical:** If a skill fails at runtime, fix the skill before retrying. The skill is the canonical recipe; bugs propagate.

---

## Synthetic Data Rules

- **Do not generate from one-line prompts.** Results will be useless.
- **Specify:** what the data represents, formats, real-world analogs to source
- **Structure** synthetic data the way real data will be structured
- **Plant known signals** in the synthetic data that the evaluation harness can test for
- **Source real analogs** via web when terminal agents can't reach them

---

## Quality Gates

Before any deliverable is accepted, the reviewer agent must verify:

- [ ] The code passes existing tests
- [ ] New code has tests covering its primary behavior
- [ ] The change is consistent with architecture.md
- [ ] The change respects the design system
- [ ] No API keys, secrets, or private data are committed
- [ ] Prompts live in the prompt library, not inline
- [ ] Documentation is updated
- [ ] The feedback log reflects any new user input

---

## File-Format Rules

- LLMs cannot act on PDFs, images, or audio directly. Convert all inputs to Markdown or plain text first
- Use **Markdown as the lingua franca** for agent-to-agent and agent-to-human communication
- Once converted, log: source file, destination path, conversion method

---

## Continuous Improvement

- **Every prompt** the user sends → append to feedback-log.md
- **Periodically** (after every major iteration), revise `.claude/agents/*.md` files so same feedback never needs again
- **Workspace memory is transient.** Trust the disk-based feedback log, not session memory

---

## Cross-Tool Conflicts

- If you are Claude invoked from Claude Code: read this file (CLAUDE.md)
- If you are Claude invoked from GitHub Copilot: read copilot-instructions.md instead
- **Do not read both.**

---

## Escalation to the Human

Surface to the user only when:

- A foundational decision (tech stack change, scope change, security implication) needs approval
- Two or more reasonable paths exist and the trade-off is non-obvious
- You have completed a phase and the plan calls for human review
- An external resource (API key, credentials) is required

**Otherwise, take the most reasonable path forward and log in feedback-log.md.**

---

## Definition of Done

A feature is done when:

- [ ] It traces to a documented user pain point in prd.md
- [ ] It is implemented per the patterns in architecture.md
- [ ] It passes the relevant entries in evaluation.md
- [ ] The reviewer agent has approved it
- [ ] The development checklist is updated
- [ ] The deployment is live and the user can demo it

---

## Kickoff Prompt Template

When ready to begin autonomous development:

> You are the orchestrator agent for JarDIYn. Build the entire product autonomously from end to end, following the workflow in CLAUDE.md. Do not interrupt me at the console unless you hit a foundational decision requiring approval. If you encounter blockers, take the most reasonable path forward and log it. Extensively use online information for deep context grounding. Use all sub-agents and skills as defined. Audit completeness before declaring done. Begin.

---

**Version:** v25 Demo-Ready Baseline for Grading  
**Last Updated:** May 26, 2026  
**Status:** Ready for Claude Code autonomous development
