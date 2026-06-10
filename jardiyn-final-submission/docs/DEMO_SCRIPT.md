# Demo Script — JarDIYn Golden Path

A 9-step walkthrough graders can follow in about 5 minutes.

## Setup
```bash
npm run dev          # serves the app at http://localhost:8080
```

## Steps
1. **Open the app** at http://localhost:8080 — the Dashboard lens loads.
2. **Click "Load demo garden"** — loads Sarah's Grand Rapids Zone 6a profile.
   The Dashboard renders the profile card.
3. **Open the Design lens.** Type: `add a mango tree to a pollinator border`.
   Click *Generate design*. JarDIYn surfaces the **zone_mismatch_plant** signal
   (mango needs Zone 10+) and still returns a zone-correct native palette.
4. **Open the Report lens.** Click *Generate seasonal report*. A Zone 6a Late
   Spring report appears with 5 prioritized tasks and soil-correct watering advice.
5. **Click "Export report (Markdown)."** A `jardiyn-report.md` file downloads.
6. **Open the Chat lens.** Ask: `I watered 3 times per day this week, is that ok?`
   The assistant flags the **overwatering_pattern** signal and root-rot risk.
7. **Ask in Chat:** `Can I grow blueberries here?` — the assistant flags the
   **ph_imbalance_blueberry** signal (soil pH 6.7 is too high for blueberries).
8. **Open the History lens** — every action above is recorded with a timestamp.
9. **Open the Agent Trace lens** — see which agent and model (orchestrator/Opus,
   garden-reasoner/Sonnet, reviewer/Haiku) handled each request.

## Evaluation
```bash
npm test             # runs the planted-signal harness — expect 8/8 PASS
```

## Main message
JarDIYn is a functioning agentic garden intelligence app. The deterministic rule
engine guarantees the six planted signals are caught; the agent trace makes the
reasoning transparent.
