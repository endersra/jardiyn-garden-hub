/*
 * app.js — JarDIYn prototype controller
 * Wires the five lenses and five UX primitives to the mock service layer.
 * No secrets, no direct LLM calls — mock mode only (see CLAUDE.md).
 */
import { identify, report, design, chat, calendar, getTrace, clearTrace } from "./services/mockApi.js";

// --- in-memory state (localStorage persistence) ---
let state = { profile: null, history: [], lastReport: null };

const DEMO_PROFILE = {
  profile_id: "demo-grand-rapids",
  owner: "Sarah (novice homeowner)",
  zone: "6a",
  last_spring_frost: "2026-05-05",
  first_fall_frost: "2026-10-15",
  soil_type: "loam",
  soil_ph: 6.7,
  sun_exposure: "full sun",
  garden_size_sqft: 800,
  existing_plants: ["tomato", "basil", "lavender"],
  goals: ["pollinator friendly", "low water"]
};

function save() {
  try { localStorage.setItem("jardiyn_state", JSON.stringify(state)); } catch (e) {}
}
function load() {
  try {
    const s = localStorage.getItem("jardiyn_state");
    if (s) state = JSON.parse(s);
  } catch (e) {}
}
function logHistory(entry) {
  state.history.unshift({ ts: new Date().toLocaleString(), entry });
  save(); renderHistory();
}

// --- lens navigation ---
document.getElementById("lensNav").addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  const lens = btn.dataset.lens;
  document.querySelectorAll("#lensNav button").forEach(b => b.classList.toggle("active", b === btn));
  document.querySelectorAll(".lens").forEach(s =>
    s.classList.toggle("active", s.dataset.lens === lens));
  if (lens === "trace") renderTrace();
});

// --- signal rendering helper ---
function renderSignals(recs) {
  if (!recs || !recs.length) return "";
  return recs.map(r => `
    <div class="signal ${r.severity === "critical" ? "critical" : ""}">
      <div>${r.message}</div>
      <span class="sig-name">signal: ${r.signal} (${r.severity})</span>
      <span class="sig-trigger">trigger: ${r.trigger}</span>
    </div>`).join("");
}

// --- PRIMITIVE 1: Profile (Load demo garden) ---
document.getElementById("loadDemo").addEventListener("click", () => {
  state.profile = DEMO_PROFILE;
  save();
  renderProfile();
  logHistory("Loaded demo garden: Grand Rapids, Zone 6a, loam soil.");
  // surface profile-level signals immediately
  const r = report(state.profile);
  document.getElementById("dashSignals").innerHTML =
    r.recommendations.length
      ? "<h3>Profile signals detected</h3>" + renderSignals(r.recommendations)
      : "";
});

function renderProfile() {
  const p = state.profile;
  const card = document.getElementById("profileCard");
  if (!p) { card.className = "card muted"; card.textContent = "No garden loaded."; return; }
  card.className = "card";
  card.innerHTML = `<h3>${p.owner}</h3>
    <div class="kv">
      <span>USDA Zone</span><span>${p.zone}</span>
      <span>Soil type</span><span>${p.soil_type} (pH ${p.soil_ph})</span>
      <span>Sun</span><span>${p.sun_exposure}</span>
      <span>Size</span><span>${p.garden_size_sqft} sq ft</span>
      <span>Plants</span><span>${p.existing_plants.join(", ")}</span>
      <span>Goals</span><span>${p.goals.join(", ")}</span>
      <span>Frost dates</span><span>${p.last_spring_frost} &rarr; ${p.first_fall_frost}</span>
    </div>`;
}

// --- PRIMITIVE 2: Design ---
document.getElementById("designRun").addEventListener("click", () => {
  if (!requireProfile()) return;
  const text = document.getElementById("designInput").value.toLowerCase();
  const observation = {};
  ["mango", "banana", "citrus"].forEach(p => { if (text.includes(p)) observation.requested_plant = p; });
  const d = design(state.profile, observation);
  let html = renderSignals(d.recommendations);
  if (d.blocked_plant) html += `<div class="signal">${d.blocked_plant}</div>`;
  html += `<div class="card"><h3>${d.concept}</h3>
    <p>${d.rationale}</p>
    <ul class="palette">${d.plants.map(pl =>
      `<li>${pl.qty}x ${pl.name} (${pl.spacing_in}" spacing)${pl.native ? " &middot; native" : ""}</li>`).join("")}</ul>
    <p class="hint">Layout: ${d.layout}</p></div>`;
  document.getElementById("designOut").innerHTML = html;
  logHistory(`Generated design: "${document.getElementById("designInput").value || "pollinator border"}".`);
});

// --- PRIMITIVE 3: Report ---
document.getElementById("reportRun").addEventListener("click", () => {
  if (!requireProfile()) return;
  const r = report(state.profile);
  state.lastReport = r; save();
  document.getElementById("reportOut").innerHTML =
    renderSignals(r.recommendations) +
    `<div class="card"><h3>${r.season} report &middot; Zone ${r.zone}</h3>
      <ul class="tasks">${r.tasks.map(t => `<li>${t}</li>`).join("")}</ul>
      <p class="hint">Watering: ${r.watering}</p></div>`;
  document.getElementById("reportExport").hidden = false;
  logHistory("Generated seasonal DIY report.");
});

document.getElementById("reportExport").addEventListener("click", () => {
  const r = state.lastReport;
  if (!r) return;
  const md = `# JarDIYn Seasonal Report\n\n**Zone:** ${r.zone} | **Season:** ${r.season}\n\n` +
    `## Priority Tasks\n${r.tasks.map(t => `- ${t}`).join("\n")}\n\n` +
    `## Watering\n${r.watering}\n\n` +
    (r.recommendations.length
      ? `## Warnings\n${r.recommendations.map(x => `- ${x.message}`).join("\n")}\n`
      : "");
  const blob = new Blob([md], { type: "text/markdown" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "jardiyn-report.md";
  a.click();
  logHistory("Exported report as Markdown.");
});

// --- PRIMITIVE 4: Chat ---
document.getElementById("chatSend").addEventListener("click", sendChat);
document.getElementById("chatInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendChat();
});
function sendChat() {
  if (!requireProfile()) return;
  const input = document.getElementById("chatInput");
  const msg = input.value.trim();
  if (!msg) return;
  addMsg("user", msg);
  input.value = "";
  const lower = msg.toLowerCase();
  const observation = {};
  if (/3 times per day|3x|three times a day/.test(lower)) observation.note = "watered 3 times per day";
  if (lower.includes("blueberry")) observation.requested_plant = "blueberry";
  const c = chat(state.profile, observation, msg);
  addMsg("bot", c.reply);
  logHistory(`Chat: "${msg}"`);
}
function addMsg(who, text) {
  const log = document.getElementById("chatLog");
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

// --- History + Trace renderers ---
function renderHistory() {
  const ul = document.getElementById("historyList");
  ul.innerHTML = state.history.length
    ? state.history.map(h => `<li><strong>${h.ts}</strong> &mdash; ${h.entry}</li>`).join("")
    : '<li class="muted">No activity yet.</li>';
}
function renderTrace() {
  const ul = document.getElementById("traceList");
  const t = getTrace();
  ul.innerHTML = t.length
    ? t.map(x => `<li><span class="t-agent">${x.agent}</span> ` +
        `<span class="t-model">[${x.model}]</span> ${x.action}</li>`).join("")
    : '<li class="muted">Run any feature to see the trace.</li>';
}

function requireProfile() {
  if (!state.profile) { alert('Click "Load demo garden" first.'); return false; }
  return true;
}

// --- boot ---
load();
renderProfile();
renderHistory();
