/*
 * test_planted_signals.mjs — JarDIYn evaluation harness
 *
 * Per evaluation.md: the system must surface all six planted signals.
 * Run:  node tests/test_planted_signals.mjs
 *
 * This is the Phase 4 evaluation. It loads the synthetic data, runs the
 * deterministic rule engine, and asserts every planted signal is detected.
 */
import { readFileSync } from "fs";
import { evaluateGarden, detectedSignals } from "../src/services/ruleEngine.js";

const profiles = JSON.parse(readFileSync(new URL("../data/garden_profiles.json", import.meta.url))).profiles;
const expected = JSON.parse(readFileSync(new URL("../data/expected_recommendations.json", import.meta.url))).expected;

const p = (id) => profiles.find(x => x.profile_id === id);
let pass = 0, fail = 0;

function check(name, condition) {
  if (condition) { pass++; console.log(`  PASS  ${name}`); }
  else { fail++; console.log(`  FAIL  ${name}`); }
}

console.log("\nJarDIYn Evaluation Harness — Planted Signal Detection\n" + "=".repeat(55));

// Signal 1: zone_mismatch_plant
check("zone_mismatch_plant",
  detectedSignals(p("demo-grand-rapids"), { requested_plant: "mango" })
    .includes("zone_mismatch_plant"));

// Signal 2: clay_soil_drainage
check("clay_soil_drainage",
  detectedSignals(p("test-clay-drainage"), {})
    .includes("clay_soil_drainage"));

// Signal 3: overwatering_pattern
check("overwatering_pattern",
  detectedSignals(p("demo-grand-rapids"), { note: "watered 3 times per day all week" })
    .includes("overwatering_pattern"));

// Signal 4: invasive_species_photo
check("invasive_species_photo",
  detectedSignals(p("test-clay-drainage"),
    { subject: "fast-spreading vine", note: "climbing aggressively over shrubs" })
    .includes("invasive_species_photo"));

// Signal 5: ph_imbalance_blueberry
check("ph_imbalance_blueberry",
  detectedSignals(p("test-ph-imbalance"), { requested_plant: "blueberry" })
    .includes("ph_imbalance_blueberry"));

// Signal 6: frost_date_violation
check("frost_date_violation",
  detectedSignals(p("demo-grand-rapids"), { planting_date: "2026-03-24" })
    .includes("frost_date_violation"));

// Trigger traceability: every recommendation must carry a trigger string
const sample = evaluateGarden(p("demo-grand-rapids"), { requested_plant: "mango" });
check("trigger_traceability",
  sample.length > 0 && sample.every(r => typeof r.trigger === "string" && r.trigger.length > 0));

// No unsafe overreach: critical signals must exist for invasive species
const inv = evaluateGarden(p("test-clay-drainage"),
  { subject: "spreading vine", note: "climbing aggressively" });
check("invasive_marked_critical",
  inv.some(r => r.signal === "invasive_species_photo" && r.severity === "critical"));

console.log("=".repeat(55));
console.log(`Result: ${pass} passed, ${fail} failed  (expected signals: ${expected.length})`);
console.log(fail === 0 ? "ALL PLANTED SIGNALS DETECTED — evaluation PASS\n"
                       : "EVALUATION FAILED — see failures above\n");
process.exit(fail === 0 ? 0 : 1);
