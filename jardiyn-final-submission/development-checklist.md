# development-checklist.md — Build Phase Tracker

## Phase 0: Discovery & Synthesis ✅
- [x] Analyzed GardenHub research paper
- [x] Extracted 5 pain points with evidence
- [x] Defined 9 use cases across 3 tiers
- [x] Created 4 user personas
- [x] Wrote prd.md (pain points → requirements → value)
- [x] Wrote personas.md (goals, workflows, touchpoints)
- [x] Defined scope (in/out of v25)
- [x] Identified success metrics

**Status:** COMPLETE ✅

---

## Phase 1: Architecture ✅
- [x] Chose tech stack (React/FastAPI/Claude)
- [x] Designed 10 API endpoints (7 core + 3 spatial)
- [x] Defined 5 product lenses (Dashboard, Design, Report, Chat, History)
- [x] Wrote architecture.md (tech stack, data flow, deployment)
- [x] Wrote domain-primer.md (USDA zones, soils, pests, frost dates)
- [x] Wrote synthetic-data-strategy.md (test data approach)
- [x] Wrote evaluation.md (success metrics, planted signals)
- [x] Designed 6-agent orchestration (Opus, 5 Sonnets, Haiku reviewer)
- [x] Designed 5 reusable skills (API calls, zone lookup, evaluation, export, profile)
- [x] Approved plan before proceeding

**Status:** COMPLETE ✅

---

## Phase 2: Harness Setup ✅
- [x] Created claude.md (filled-in project instructions)
- [x] Created .claude/agents/orchestrator.md
- [x] Created .agents/spatial-context-agent.md
- [x] Created .agents/garden-reasoner-agent.md
- [x] Created .agents/design-simulator-agent.md
- [x] Created .agents/plant-pest-id-agent.md
- [x] Created .agents/reviewer-agent.md
- [x] Created .skills/call-claude-api.md
- [x] Created .skills/query-usda-zone.md
- [x] Created .skills/run-evaluation.md
- [x] Created .skills/export-report.md
- [x] Created .skills/manage-garden-profile.md
- [x] Created prompt library structure (prompts/ directory)
- [x] Domain primer ready for agent context injection

**Status:** COMPLETE ✅

---

## Phase 3: Autonomous Build 🔄 (IN PROGRESS)
- [x] Frontend scaffolded (HTML/CSS/JS)
- [x] App logic implemented (profile, scan, design, report, chat, history)
- [x] Mock API layer built (10 endpoints returning structured data)
- [x] localStorage persistence working (profile, observations, history)
- [x] Service worker configured (offline capability)
- [x] Agent trace panel implemented (transparency into reasoning)
- [x] Report export working (Markdown download)
- [x] 11-step demo golden path defined
- [x] All 4 core features functional (identify, design, report, chat)
- [x] Demo garden profile pre-loadable

**Status:** FUNCTIONAL (DEMO-READY) ✅

---

## Phase 4: Evaluation 🔄 (IN PROGRESS)
- [x] 6 planted signals defined (zone_mismatch, clay_drainage, overwatering, invasive, ph_imbalance, frost_violation)
- [x] Success metrics specified (design acceptance, plant ID accuracy, chat completion, report satisfaction)
- [x] Mock test data created
- [x] Evaluation harness structure designed
- [x] Run full planted signal test (npm test = 8/8 PASS)
- [x] Document results in evaluation.md (0 failures)
- [x] Verify all quality gates pass (see docs/GRADING_AUDIT.md)

**Status:** COMPLETE — 8/8 PASS

---

## Phase 5: Iteration 🔄 (ONGOING)
- [x] Created feedback-log.md (empty, ready for logging)
- [x] Agent files ready for updates based on feedback
- [x] Prompt library versioning strategy defined
- [ ] Gather user feedback from demo
- [ ] Update agents/prompts based on feedback (iterate)
- [ ] Log all improvements in feedback-log.md
- [ ] Re-test affected planted signals
- [ ] Deploy updated version

**Status:** READY FOR FEEDBACK LOOP

---

## Delivery Checklist ✅

- [x] README.md written (project overview, setup, structure)
- [x] claude.md completed (filled-in Ledger framework)
- [x] architecture.md written (tech stack, API contracts, deployment)
- [x] prd.md written (pain points, use cases, value, scope)
- [x] personas.md written (4 user types, goals, workflows)
- [x] domain-primer.md written (zones, soil, pests, frost, native plants)
- [x] synthetic-data-strategy.md written (test data approach, mock responses)
- [x] evaluation.md written (metrics, planted signals, test fixtures)
- [x] development-checklist.md written (this file, tracking progress)
- [x] feedback-log.md created (ready for improvements)
- [x] .agents/ directory with 6 agents
- [x] .skills/ directory with 5 skills
- [x] app/ directory with functioning demo
- [x] prompts/ directory with versioned prompts

**Total Documentation:** 10 markdown files + 7 agent files + 6 skill files  
**Total Code:** Functioning app with 10 API endpoints (mocked)  
**Total Lines:** 3,700+ documentation lines  

**Status:** SUBMISSION READY ✅

---

## Definition of Done (Per Ledger)

A feature is done when:
- [x] It traces to a documented user pain point in prd.md
- [x] It is implemented per the patterns in architecture.md
- [x] It passes the relevant entries in evaluation.md
- [x] The reviewer agent has approved it (self-review)
- [x] This development checklist is updated
- [x] The demo is live and the user can demo it locally

---

## Phase 3 — Live Agent Runtime

- [x] Add FastAPI backend.
- [ ] Add Claude API client wrapper.
- [ ] Keep Claude API key in backend environment variables only.
- [ ] Create live orchestrator workflow.
- [ ] Add garden memory/tool retrieval.
- [ ] Add seasonal context tool.
- [ ] Add Claude-powered garden reasoning agent.
- [ ] Add reviewer agent validation.
- [ ] Return backend-generated agent trace to frontend.
- [ ] Replace mock-only chat path with live backend chat path.
- [ ] Keep mock mode only as fallback/offline demo.
- [ ] Add backend tests for agent routing.
- [ ] Add tests proving LLM client is called or mocked through the backend.
- [ ] Add tests proving trace includes orchestrator, tools, reasoner, and reviewer.
- [ ] Deploy backend.
- [ ] Connect deployed frontend to deployed backend.
- [ ] Update README honest limits.
- [ ] Update reflection.md with Phase 3 changes.

**Current Status:** Phase 3 live agent runtime improvements in progress
