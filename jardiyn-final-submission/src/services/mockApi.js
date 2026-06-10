/*
 * mockApi.js — JarDIYn mock service layer
 *
 * Per CLAUDE.md: LLM_MODE defaults to mock. The browser must NEVER call an LLM
 * provider directly. In production these functions are replaced by calls to the
 * FastAPI proxy (architecture.md). The mock responses are deterministic so the
 * golden demo path and the evaluation harness behave predictably.
 *
 * Every mock response runs the deterministic rule engine first, then attaches a
 * narrative — exactly the order a live build would use.
 */

import { evaluateGarden } from "./ruleEngine.js";

const AGENT_TRACE = [];

function trace(agent, model, action) {
  AGENT_TRACE.push({ ts: new Date().toISOString(), agent, model, action });
}

export function getTrace() { return AGENT_TRACE.slice(); }
export function clearTrace() { AGENT_TRACE.length = 0; }

/* POST /identify — photo -> species + diagnosis */
export function identify(profile, observation) {
  trace("orchestrator", "opus", "route /identify -> garden-reasoner");
  trace("garden-reasoner", "sonnet", "run rule engine + identify prompt");
  const recs = evaluateGarden(profile, observation);
  const invasive = recs.find(r => r.signal === "invasive_species_photo");
  let result;
  if (invasive) {
    result = {
      species: "Likely invasive species (visual match)",
      confidence: 0.71,
      status: "invasive",
      diagnosis: "Aggressive growth habit consistent with an invasive vine.",
      remedies: [invasive.message],
      invasive: true
    };
  } else {
    result = {
      species: "Solanum lycopersicum (tomato)",
      confidence: 0.9,
      status: /spot/.test(observation.note || "") ? "diseased" : "healthy",
      diagnosis: /spot/.test(observation.note || "")
        ? "Early blight — dark concentric spots on lower leaves."
        : null,
      remedies: /spot/.test(observation.note || "")
        ? ["Remove affected lower leaves", "Apply copper fungicide (organic)",
           "Water at soil level, not foliage", "Improve airflow between plants"]
        : []
    };
  }
  trace("reviewer", "haiku", "quality gate: pass");
  return { recommendations: recs, result };
}

/* POST /report — profile -> seasonal DIY report */
export function report(profile) {
  trace("orchestrator", "opus", "route /report -> garden-reasoner");
  trace("garden-reasoner", "sonnet", "run rule engine + report prompt");
  const recs = evaluateGarden(profile, {});
  const tasks = [
    "Test soil moisture 2 inches down before watering.",
    "Add 2-3 inches of mulch to retain moisture and suppress weeds.",
    "Scout weekly for aphids and beetles; treat organically if found.",
    "Deadhead spent blooms to extend the flowering season.",
    "Top-dress beds with finished compost."
  ];
  trace("reviewer", "haiku", "quality gate: pass");
  return {
    recommendations: recs,
    season: "Late Spring",
    zone: profile.zone,
    tasks,
    watering: (profile.soil_type || "").toLowerCase() === "clay"
      ? "Clay soil holds moisture — water deeply but less often."
      : "Provide about 1-1.5 inches of water per week."
  };
}

/* POST /design — natural language -> 2D layout */
export function design(profile, observation) {
  trace("orchestrator", "opus", "route /design -> ui-engineer + garden-reasoner");
  trace("garden-reasoner", "sonnet", "run rule engine + design prompt");
  const recs = evaluateGarden(profile, observation);
  const blocked = recs.find(r => r.signal === "zone_mismatch_plant");
  const palette = [
    { name: "Black-eyed Susan", qty: 8, spacing_in: 18, native: true },
    { name: "Purple coneflower", qty: 6, spacing_in: 24, native: true },
    { name: "Bee balm", qty: 4, spacing_in: 36, native: true }
  ];
  trace("reviewer", "haiku", "quality gate: pass");
  return {
    recommendations: recs,
    concept: "Pollinator-friendly native perennial border",
    plants: palette,
    layout: "Curved bed along the sunniest fence line",
    rationale: `Zone ${profile.zone}, ${profile.sun_exposure}, native and long-blooming for pollinators.`,
    blocked_plant: blocked ? blocked.message : null
  };
}

/* POST /chat — message -> context-aware reply */
export function chat(profile, observation, message) {
  trace("orchestrator", "opus", "route /chat -> garden-reasoner");
  trace("garden-reasoner", "sonnet", "run rule engine + chat prompt");
  const recs = evaluateGarden(profile, observation);
  let reply;
  if (recs.length) {
    reply = recs.map(r => r.message).join(" ");
  } else {
    reply = `Based on your Zone ${profile.zone} ${profile.soil_type} soil, that should work well. ` +
            `Keep an eye on watering and sunlight for best results.`;
  }
  trace("reviewer", "haiku", "quality gate: pass");
  return { recommendations: recs, reply };
}

/* POST /calendar — zone + plant -> seasonal timeline */
export function calendar(profile, observation) {
  trace("orchestrator", "opus", "route /calendar -> garden-reasoner");
  trace("garden-reasoner", "sonnet", "run rule engine + calendar logic");
  const recs = evaluateGarden(profile, observation);
  trace("reviewer", "haiku", "quality gate: pass");
  return {
    recommendations: recs,
    last_spring_frost: profile.last_spring_frost,
    first_fall_frost: profile.first_fall_frost,
    note: "Frost-tender crops should go outdoors only after the last spring frost."
  };
}
