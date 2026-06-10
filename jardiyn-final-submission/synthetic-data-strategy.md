# synthetic-data-strategy.md — Test Data Strategy

## Overview

Test data must be structured identically to production data, with planted signals that the evaluation harness can verify.

---

## Garden Profile (Test Data)

```json
{
  "profile_id": "demo-grand-rapids-2026",
  "zone": "Zone 6a",
  "soil_type": "loam",
  "sun_exposure": "full sun",
  "existing_plants": ["tomatoes", "basil", "lavender"],
  "garden_goals": ["pollinator friendly", "low water"],
  "garden_size": "800 sq ft"
}
```

---

## Test Fixtures (Planted Signals)

| Signal | Test Case | Expected Behavior |
|---|---|---|
| `zone_mismatch_plant` | Recommend mango for Zone 6a | System warns: "Not hardy for your zone" + suggests alternatives |
| `clay_soil_drainage` | Clay soil + moisture-heavy plant | Report flags: "May suffer from poor drainage" + recommends amendment |
| `overwatering_pattern` | Log shows 3× daily watering | Chat assistant flags root rot risk |
| `invasive_species_photo` | Photo of kudzu or Japanese knotweed | Plant ID flags invasive + removal guidance |
| `ph_imbalance_blueberry` | pH 7.5 soil + recommend blueberries | Report: "Your soil is too alkaline" + recommend acidification |
| `frost_date_violation` | Tomatoes planted 6 weeks before frost | Calendar alerts: "Risk of frost damage" |

---

## Test Photos (For Plant ID)

**Needed for evaluation:**
- Healthy tomato plant
- Tomato with late blight
- Japanese beetle infestation
- Kudzu vine (invasive)
- Healthy lavender
- Slug damage

**Real-world analogs:**
- Source from USDA Plant Disease Database
- Source from iNaturalist
- Source from extension service websites

---

## Test Scenarios (For Chat)

### Scenario 1: Zone Warning
**Input:** "Can I grow mangoes in my Zone 6a garden?"  
**Expected:** "Mangoes need Zone 10-11. For your zone, try hardy alternatives like..."

### Scenario 2: Soil Correction
**Input:** "I want to plant blueberries but I'm not sure if my soil is right"  
**Expected:** "Blueberries need acidic soil (pH 4.5-5.5). Your soil is pH 7.5. I recommend sulfur amendment or a raised bed with peat."

### Scenario 3: Pest Management
**Input:** "I see white powder on my leaves"  
**Expected:** "That's powdery mildew. Remove affected areas and apply baking soda spray (1 tsp per gallon water). Improve airflow."

---

## Mock API Responses

### /identify (Plant ID)
```json
{
  "species": "Solanum lycopersicum (tomato)",
  "confidence": 0.92,
  "status": "healthy",
  "diagnosis": null,
  "remedies": []
}
```

### /identify (with diagnosis)
```json
{
  "species": "Solanum lycopersicum (tomato)",
  "confidence": 0.87,
  "status": "diseased",
  "diagnosis": "Late blight detected",
  "remedies": [
    "Remove affected leaves and tissue",
    "Apply copper fungicide",
    "Improve air circulation",
    "Water at soil level, not foliage"
  ]
}
```

### /design
```json
{
  "concept": "Pollinator-friendly perennial border",
  "plants": [
    { "name": "Black-eyed Susan", "qty": 8, "spacing": 18 },
    { "name": "Purple coneflower", "qty": 6, "spacing": 24 },
    { "name": "Bee balm", "qty": 4, "spacing": 36 }
  ],
  "layout": "curved bed along north fence",
  "rationale": "Zone 6a, full sun, native, long blooming"
}
```

---

## Data Persistence (v25 Demo)

**localStorage keys:**
- `jardiyn_profile` — Garden profile
- `jardiyn_observations` — Photos, scans, notes
- `jardiyn_history` — Timeline of changes
- `jardiyn_reports` — Generated reports

---

## Production Data (v26+)

**Database tables:**
- `users` — Authentication, preferences
- `gardens` — Garden profiles, zone, soil
- `observations` — Photos, scans, metadata
- `recommendations` — AI-generated outputs
- `conversations` — Chat history
- `evaluations` — Quality metrics

