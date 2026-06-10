/*
 * ruleEngine.js — JarDIYn deterministic recommendation engine
 *
 * Per architecture.md: recommendation logic is DETERMINISTIC FIRST (rule-based),
 * LLM SECOND (narrative wording only). Every recommendation cites its trigger.
 * This is what makes the six planted signals reliably detectable by the
 * evaluation harness.
 */

// --- domain reference data (mirrors domain-primer.md) ---
const ZONE_MIN_HARDINESS = { mango: 10, banana: 9, citrus: 9, tomato: 2, lavender: 5, blueberry: 3 };
const ACID_LOVING_PLANTS = ["blueberry", "azalea", "rhododendron"];
const INVASIVE_KEYWORDS = ["kudzu", "knotweed", "english ivy", "purple loosestrife",
  "garlic mustard", "climbing aggressively", "spreading vine"];

function zoneNumber(zone) {
  // "6a" -> 6, "5b" -> 5
  const m = String(zone).match(/\d+/);
  return m ? parseInt(m[0], 10) : null;
}

function monthOf(dateStr) {
  return new Date(dateStr).getMonth() + 1; // 1-12
}

/**
 * Evaluate a garden profile + optional observation and return a list of
 * recommendation objects. Each carries the triggering signal so the
 * evaluation harness can trace it.
 */
export function evaluateGarden(profile, observation = {}) {
  const recs = [];

  // Signal 1: zone_mismatch_plant
  const requested = (observation.requested_plant || "").toLowerCase();
  if (requested && ZONE_MIN_HARDINESS[requested] != null) {
    const zn = zoneNumber(profile.zone);
    if (zn != null && zn < ZONE_MIN_HARDINESS[requested]) {
      recs.push({
        signal: "zone_mismatch_plant",
        severity: "major",
        message: `${requested} needs USDA Zone ${ZONE_MIN_HARDINESS[requested]}+ but your garden is Zone ${profile.zone}. Choose a cold-hardy alternative instead.`,
        trigger: `requested_plant=${requested}, profile.zone=${profile.zone}`
      });
    }
  }

  // Signal 2: clay_soil_drainage
  if ((profile.soil_type || "").toLowerCase() === "clay") {
    recs.push({
      signal: "clay_soil_drainage",
      severity: "major",
      message: "Clay soil drains poorly. Amend with grit and compost, or use a rain garden for moisture-loving plants.",
      trigger: `profile.soil_type=${profile.soil_type}`
    });
  }

  // Signal 3: overwatering_pattern
  const note = (observation.note || "").toLowerCase();
  if (/3 times per day|3x daily|three times a day/.test(note)) {
    recs.push({
      signal: "overwatering_pattern",
      severity: "major",
      message: "Watering 3x daily is overwatering and risks root rot. Most plants need about 1-1.5 inches of water per week.",
      trigger: `observation.note="${observation.note}"`
    });
  }

  // Signal 4: invasive_species_photo
  if (INVASIVE_KEYWORDS.some(k => note.includes(k) ||
      (observation.subject || "").toLowerCase().includes(k))) {
    recs.push({
      signal: "invasive_species_photo",
      severity: "critical",
      message: "This looks like an invasive species. Remove it promptly: cut back growth, dig out roots/rhizomes, and dispose of it in the trash, not compost.",
      trigger: `observation.subject="${observation.subject || ''}", note="${observation.note || ''}"`
    });
  }

  // Signal 5: ph_imbalance_blueberry
  const wantsAcidPlant = ACID_LOVING_PLANTS.some(p =>
    requested.includes(p) ||
    (profile.goals || []).join(" ").toLowerCase().includes(p) ||
    (profile.existing_plants || []).join(" ").toLowerCase().includes(p));
  if (wantsAcidPlant && profile.soil_ph != null && profile.soil_ph > 6.0) {
    recs.push({
      signal: "ph_imbalance_blueberry",
      severity: "major",
      message: `Blueberries (and other acid-loving plants) need soil pH 4.5-5.5, but your soil is pH ${profile.soil_ph}. Add elemental sulfur or use a raised bed with peat moss.`,
      trigger: `acid_loving plant requested, profile.soil_ph=${profile.soil_ph}`
    });
  }

  // Signal 6: frost_date_violation
  if (observation.planting_date && profile.last_spring_frost) {
    const plantM = monthOf(observation.planting_date);
    const frostM = monthOf(profile.last_spring_frost);
    if (plantM < frostM) {
      recs.push({
        signal: "frost_date_violation",
        severity: "major",
        message: `Planting on ${observation.planting_date} is before your last spring frost (${profile.last_spring_frost}). Frost-tender crops risk damage. Wait until after the last frost date.`,
        trigger: `planting_date=${observation.planting_date}, last_spring_frost=${profile.last_spring_frost}`
      });
    }
  }

  return recs;
}

/** Convenience: which planted signals fired, as a plain list. */
export function detectedSignals(profile, observation = {}) {
  return evaluateGarden(profile, observation).map(r => r.signal);
}
