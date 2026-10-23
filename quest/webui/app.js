// Python Developer Quest -- GUI frontend. Vanilla JS, no build step
// (consistent with the CLI's stdlib-only design). Talks to the JSON API
// in quest/gui.py, which wraps the same engine/registry/state functions
// the `quest` CLI itself uses.

const state = { data: null, activeMissionId: null };

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function escapeHtml(str) {
  return str.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// Minimal markdown renderer for scenario.md: headers, bold, inline code,
// fenced code blocks, bullet lists, paragraphs. Covers exactly the subset
// the curriculum authors actually use.
function renderMarkdown(md) {
  const lines = md.split("\n");
  let html = "";
  let inCode = false;
  let inList = false;
  const closeList = () => { if (inList) { html += "</ul>"; inList = false; } };

  for (const raw of lines) {
    if (raw.trim().startsWith("```")) {
      if (!inCode) { closeList(); html += "<pre>"; inCode = true; }
      else { html += "</pre>"; inCode = false; }
      continue;
    }
    if (inCode) { html += escapeHtml(raw) + "\n"; continue; }

    const line = raw;
    if (/^####\s+/.test(line)) { closeList(); html += `<h4>${inline(line.replace(/^####\s+/, ""))}</h4>`; continue; }
    if (/^###\s+/.test(line)) { closeList(); html += `<h4>${inline(line.replace(/^###\s+/, ""))}</h4>`; continue; }
    if (/^##\s+/.test(line)) { closeList(); html += `<h3>${inline(line.replace(/^##\s+/, ""))}</h3>`; continue; }
    if (/^-\s+/.test(line)) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${inline(line.replace(/^-\s+/, ""))}</li>`;
      continue;
    }
    closeList();
    if (line.trim() === "") { continue; }
    html += `<p>${inline(line)}</p>`;
  }
  closeList();
  if (inCode) html += "</pre>";
  return html;
}

function inline(text) {
  let t = escapeHtml(text);
  t = t.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
  return t;
}

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok && res.status !== 404) throw new Error(`API error ${res.status}`);
  return res.json();
}

async function loadState() {
  state.data = await api("/api/state");
  renderPlayerSummary();
  renderCampaignMap();
  renderProgress();
  if (state.data.player.current_mission) {
    state.activeMissionId = state.data.player.current_mission;
  }
}

function renderPlayerSummary() {
  const p = state.data.player;
  const el = $("#player-summary");
  const pct = p.xp_to_next !== null
    ? Math.min(100, Math.round((p.xp_into_current / (p.xp_into_current + p.xp_to_next)) * 100))
    : 100;
  el.innerHTML = `
    <span class="rank">Lv.${p.level} ${escapeHtml(p.rank)}</span>
    <span>${p.xp} XP</span>
    <span class="xpbar"><span class="xpbar-fill" style="width:${pct}%"></span></span>
    <span>${p.completed_count} Missionen &middot; ${p.achievements_count} Achievements</span>
  `;
  if (state.data.warning) {
    el.innerHTML += ` <span style="color:var(--warn)">[WARNUNG] ${escapeHtml(state.data.warning)}</span>`;
  }
}

function missionIcon(m) {
  if (m.done) return "&#10003;"; // check
  if (!m.unlocked) return "&#128274;"; // lock
  if (m.is_active) return "&#9654;"; // play
  return "&#9675;"; // circle
}

function renderCampaignMap() {
  const root = $("#campaign-list");
  root.innerHTML = "";
  for (const c of state.data.campaigns) {
    const card = document.createElement("div");
    card.className = "campaign-card" + (!c.unlocked ? " locked" : "");
    const statusClass = c.status === "available" ? (c.unlocked ? "available" : "locked") : "planned";
    const statusLabel = c.status === "available" ? (c.unlocked ? "verfuegbar" : "gesperrt") : "geplant";

    let missionsHtml = "";
    if (c.missions.length) {
      const pct = c.total ? Math.round((c.done / c.total) * 100) : 0;
      missionsHtml += `
        <div class="progressbar-row">
          <span>${c.done}/${c.total} Missionen</span>
          <span class="progressbar"><span class="progressbar-fill" style="width:${pct}%"></span></span>
        </div>`;
      for (const m of c.missions) {
        missionsHtml += `
          <div class="mission-row ${m.unlocked ? "" : "locked"} ${m.is_active ? "active-mission" : ""}"
               data-mission-id="${m.id}">
            <span class="icon">${missionIcon(m)}</span>
            <span class="title">${escapeHtml(m.title)}</span>
            <span class="xp">+${m.xp_reward} XP</span>
          </div>`;
      }
    } else if (c.topics && c.topics.length) {
      missionsHtml = `<div class="muted">Themen: ${c.topics.slice(0, 6).map(escapeHtml).join(", ")}${c.topics.length > 6 ? "..." : ""}</div>`;
    }

    card.innerHTML = `
      <h3>${escapeHtml(c.title)} <span class="campaign-status ${statusClass}">${statusLabel}</span></h3>
      <div class="campaign-summary">${escapeHtml(c.summary)}</div>
      ${missionsHtml}
    `;
    root.appendChild(card);
  }

  $$(".mission-row:not(.locked)", root).forEach((row) => {
    row.addEventListener("click", () => openMission(row.dataset.missionId));
  });
}

async function openMission(missionId) {
  state.activeMissionId = missionId;
  switchTab("mission");
  const panel = $("#mission-detail");
  panel.innerHTML = `<p class="muted">Laedt Mission...</p>`;
  const m = await api(`/api/mission?id=${encodeURIComponent(missionId)}`);
  if (m.error) { panel.innerHTML = `<p class="muted">${escapeHtml(m.error)}</p>`; return; }
  renderMissionDetail(m);
}

function renderMissionDetail(m) {
  const panel = $("#mission-detail");
  const hintsHtml = m.hints_revealed.map((h, i) => `<div class="hint-box"><strong>Hint ${i + 1}:</strong> ${inline(h)}</div>`).join("");
  const moreHints = m.hints_used < m.hints_total;

  panel.innerHTML = `
    <h2>${escapeHtml(m.title)} ${m.done ? "&#10003;" : ""}</h2>
    <div class="mission-meta">
      <span>Schwierigkeit: ${m.difficulty}/5</span>
      <span>~${m.estimated_minutes} min</span>
      <span>+${m.xp_reward} XP</span>
    </div>
    <div class="workspace-path">${escapeHtml(m.workspace_dir)}</div>
    <div class="scenario-body">${renderMarkdown(m.scenario)}</div>
    <div class="btn-row">
      ${m.is_active ? "" : `<button class="action" id="btn-start">Als aktive Mission setzen</button>`}
      <button class="action secondary" id="btn-hint" ${moreHints ? "" : "disabled"}>
        Hint zeigen (${m.hints_used}/${m.hints_total})
      </button>
      <button class="action" id="btn-check">Check ausfuehren</button>
    </div>
    <div id="hints-container">${hintsHtml}</div>
    <div id="check-result-container"></div>
  `;

  $("#btn-start")?.addEventListener("click", async () => {
    await api(`/api/start?id=${encodeURIComponent(m.id)}`, { method: "POST" });
    await loadState();
    openMission(m.id);
  });
  $("#btn-hint").addEventListener("click", async () => {
    const updated = await api(`/api/hint?id=${encodeURIComponent(m.id)}`, { method: "POST" });
    renderMissionDetail(updated);
  });
  $("#btn-check").addEventListener("click", async () => {
    const btn = $("#btn-check");
    btn.disabled = true;
    btn.textContent = "Pruefe...";
    try {
      const result = await api(`/api/check?id=${encodeURIComponent(m.id)}`, { method: "POST" });
      renderCheckResult(result);
      await loadState();
    } finally {
      btn.disabled = false;
      btn.textContent = "Check ausfuehren";
    }
  });
}

function renderCheckResult(result) {
  const container = $("#check-result-container");
  const cls = result.passed ? "pass" : "fail";
  let verdict;
  if (result.passed) {
    verdict = result.already_completed
      ? "Bestanden (bereits vorher abgeschlossen, keine erneute XP)."
      : `BESTANDEN -- +${result.xp_awarded} XP`;
  } else {
    verdict = `NICHT BESTANDEN (score=${result.score.toFixed(2)})` + (result.xp_awarded ? ` -- Teil-XP: +${result.xp_awarded} XP` : "");
  }
  let achievementHtml = "";
  if (result.achievement) {
    achievementHtml = `<div class="achievement-banner">Achievement freigeschaltet: ${escapeHtml(result.achievement.title)} -- ${escapeHtml(result.achievement.description)}</div>`;
  }
  container.innerHTML = `
    <div class="check-result ${cls}">
      <div class="verdict">${verdict}</div>
      <pre>${escapeHtml(result.detail)}</pre>
      ${achievementHtml}
    </div>
  `;
}

function renderProgress() {
  const root = $("#progress-content");
  const campaignRows = state.data.campaigns
    .filter((c) => c.total > 0)
    .map((c) => {
      const pct = Math.round((c.done / c.total) * 100);
      return `
        <div class="progressbar-row">
          <span style="width:220px">${escapeHtml(c.title)}</span>
          <span class="progressbar"><span class="progressbar-fill" style="width:${pct}%"></span></span>
          <span>${c.done}/${c.total}</span>
        </div>`;
    }).join("");

  const skillRows = state.data.skill_tree.map((s) => `
    <div class="skill-row">
      <span class="label">${escapeHtml(s.label)}</span>
      <span class="progressbar"><span class="progressbar-fill" style="width:${(s.level / 5) * 100}%"></span></span>
      <span class="pts">Lv.${s.level}/5 (${s.points} pts)</span>
    </div>`).join("");

  const weaknesses = Object.entries(state.data.player.weaknesses || {})
    .map(([topic, note]) => `<li><strong>${escapeHtml(topic)}:</strong> ${escapeHtml(note)}</li>`).join("");

  root.innerHTML = `
    <h3>Campaign-Fortschritt</h3>
    ${campaignRows || '<p class="muted">Keine Daten.</p>'}
    <h3 style="margin-top:24px">Skill Tree</h3>
    ${skillRows}
    ${weaknesses ? `<h3 style="margin-top:24px">Schwachstellen</h3><ul>${weaknesses}</ul>` : ""}
  `;
}

async function renderAchievements() {
  const root = $("#achievements-content");
  root.innerHTML = `<p class="muted">Laedt...</p>`;
  const data = await api("/api/achievements");
  root.innerHTML = data.achievements.map((a) => `
    <div class="achv-row ${a.unlocked ? "" : "locked"}">
      <span class="icon">${a.unlocked ? "&#10003;" : "&#9675;"}</span>
      <span><strong>${escapeHtml(a.title)}</strong>${a.unlocked ? " -- " + escapeHtml(a.description) : ""}</span>
    </div>
  `).join("") || `<p class="muted">Keine Achievements im Katalog.</p>`;
}

async function renderReview() {
  const root = $("#review-content");
  root.innerHTML = `<p class="muted">Laedt...</p>`;
  const data = await api("/api/review");
  const bucketLabel = { strong: "Stark", developing: "Im Aufbau", weak: "Schwach", untouched: "Unberuehrt" };
  const skillRows = data.skills
    .filter((s) => s.bucket !== "untouched")
    .map((s) => `
      <div class="skill-row">
        <span class="label">${escapeHtml(s.label)}</span>
        <span class="bucket-tag bucket-${s.bucket}">${bucketLabel[s.bucket]}</span>
      </div>`).join("");

  const weaknesses = Object.entries(data.weaknesses || {})
    .map(([topic, note]) => `<li><strong>${escapeHtml(topic)}:</strong> ${escapeHtml(note)}</li>`).join("");

  const failedRows = data.failed_recent.map((h) => `
    <div class="history-row">
      <span class="icon fail">&#10007;</span>
      <span>${escapeHtml(h.mission_id)}</span>
      <span>score=${h.score.toFixed(2)}</span>
    </div>`).join("");

  root.innerHTML = `
    ${skillRows ? `<h3>Skill-Einschaetzung</h3>${skillRows}` : '<p class="muted">Noch keine Missionen abgeschlossen.</p>'}
    ${weaknesses ? `<h3 style="margin-top:24px">Empfohlene Wiederholung</h3><ul>${weaknesses}</ul>` : ""}
    ${failedRows ? `<h3 style="margin-top:24px">Zuletzt gescheiterte Versuche</h3>${failedRows}` : ""}
  `;
}

function renderHistory() {
  const root = $("#history-content");
  const rows = state.data.history.map((h) => `
    <div class="history-row">
      <span class="icon ${h.passed ? "ok" : "fail"}">${h.passed ? "&#10003;" : "&#10007;"}</span>
      <span>${escapeHtml(h.mission_id)}</span>
      <span>score=${h.score.toFixed(2)}</span>
      <span>+${h.xp_awarded} XP</span>
      <span class="ts">${escapeHtml(h.timestamp)}</span>
    </div>
  `).join("");
  root.innerHTML = rows || `<p class="muted">Noch keine Versuche.</p>`;
}

function switchTab(name) {
  $$(".tab-btn").forEach((b) => b.classList.toggle("active", b.dataset.tab === name));
  $$(".tab-panel").forEach((p) => p.classList.toggle("active", p.id === `tab-${name}`));
  if (name === "achievements") renderAchievements();
  if (name === "review") renderReview();
  if (name === "history") renderHistory();
  if (name === "mission" && state.activeMissionId && !$("#mission-detail h2")) {
    openMission(state.activeMissionId);
  }
}

$$(".tab-btn").forEach((btn) => btn.addEventListener("click", () => switchTab(btn.dataset.tab)));

loadState().then(() => {
  if (state.activeMissionId) openMission(state.activeMissionId);
}).catch((err) => {
  $("#player-summary").textContent = `Fehler beim Laden: ${err.message}`;
});
