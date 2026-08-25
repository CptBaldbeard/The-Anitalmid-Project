const $ = (id) => document.getElementById(id);

let resumeFile = null;
let resumeText = "";
let token = localStorage.getItem("anitalmid_token") || "";
let currentUser = null;

/* ---------- Auth ---------- */
function authHeaders() {
  return token ? { Authorization: "Bearer " + token } : {};
}

async function apiFetch(url, opts = {}) {
  const headers = { ...authHeaders(), ...(opts.headers || {}) };
  const resp = await fetch(url, { ...opts, headers });
  if (resp.status === 401) {
    logout();
    throw new Error("Please sign in first.");
  }
  if (!resp.ok) {
    let msg = resp.status;
    try { const d = await resp.json(); msg = d.detail || msg; } catch {}
    throw new Error(msg);
  }
  return resp.json();
}

async function login(email, password) {
  const d = await apiFetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  setSession(d);
}

async function register(email, username, password) {
  const d = await apiFetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, username, password }),
  });
  setSession(d);
}

function setSession(d) {
  token = d.access_token;
  currentUser = d.user;
  localStorage.setItem("anitalmid_token", token);
  renderAuth();
}

function logout() {
  token = "";
  currentUser = null;
  localStorage.removeItem("anitalmid_token");
  renderAuth();
}

function renderAuth() {
  if (currentUser) {
    $("authLoggedOut").classList.add("hidden");
    $("authLoggedIn").classList.remove("hidden");
    $("authUser").textContent = currentUser.email;
  } else {
    $("authLoggedOut").classList.remove("hidden");
    $("authLoggedIn").classList.add("hidden");
  }
}

$("loginBtn").addEventListener("click", async () => {
  $("authStatus").textContent = "";
  try {
    await login($("authEmail").value.trim(), $("authPassword").value);
  } catch (e) { $("authStatus").textContent = e.message; }
});
$("registerBtn").addEventListener("click", async () => {
  $("authStatus").textContent = "";
  try {
    await register($("authEmail").value.trim(), $("authUsername").value.trim(), $("authPassword").value);
  } catch (e) { $("authStatus").textContent = e.message; }
});
$("logoutBtn").addEventListener("click", logout);
/* ---------- Landing / app view toggle ---------- */
$("startQuizBtn").addEventListener("click", startQuiz);
$("signInBtn").addEventListener("click", showSignIn);
$("methodologyBtn").addEventListener("click", () => { window.location.href = "/methodology.html"; });
$("brandHome").addEventListener("click", showLanding);

function startQuiz() {
  showApp();
  setTimeout(() => $("wizard").scrollIntoView({ behavior: "smooth" }), 60);
}

function showSignIn() {
  showApp();
  setTimeout(() => $("auth").scrollIntoView({ behavior: "smooth" }), 60);
}

function showApp() {
  $("landing").classList.add("hidden");
  $("appView").classList.remove("hidden");
}

function showLanding() {
  $("appView").classList.add("hidden");
  $("landing").classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* Refresh the user session (e.g. after email verification completes in another tab) */
async function refreshUser() {
  if (!token) return;
  try {
    currentUser = await apiFetch("/auth/me");
    renderAuth();
  } catch { /* apiFetch logs out on 401 */ }
}

/* Re-check whenever the user returns to this tab — they may have just verified */
window.addEventListener("focus", refreshUser);
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") refreshUser();
});

/* Restore session on load */
refreshUser();

/* ---------- Dropzone ---------- */
const dz = $("dropzone");
dz.addEventListener("click", () => $("resumeFile").click());
$("browseBtn").addEventListener("click", (e) => { e.stopPropagation(); $("resumeFile").click(); });

["dragover", "dragenter"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("dragover"); }));
["dragleave", "drop"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.remove("dragover"); }));

dz.addEventListener("drop", (e) => {
  const f = e.dataTransfer.files[0];
  if (f) setFile(f);
});
$("resumeFile").addEventListener("change", (e) => {
  if (e.target.files[0]) setFile(e.target.files[0]);
});

function setFile(f) {
  resumeFile = f;
  dz.querySelector("strong").textContent = f.name;
  resumeText = "";
  if (/\.(txt|md|rtf)$/i.test(f.name)) {
    const r = new FileReader();
    r.onload = () => { resumeText = r.result; };
    r.readAsText(f);
  }
}

/* ---------- Input mode toggle ---------- */
let inputMode = "resume"; // "resume" | "signals"

function setInputMode(mode) {
  inputMode = mode;
  $("resumeMode").classList.toggle("hidden", mode !== "resume");
  $("signalsMode").classList.toggle("hidden", mode !== "signals");
  $("modeResume").classList.toggle("active", mode === "resume");
  $("modeSignals").classList.toggle("active", mode === "signals");
}

$("modeResume").addEventListener("click", () => setInputMode("resume"));
$("modeSignals").addEventListener("click", () => setInputMode("signals"));

function buildHollandCode() {
  const seen = new Set();
  const code = [];
  ["holland1", "holland2", "holland3"].forEach((id) => {
    const v = $(id).value;
    if (v && !seen.has(v)) { seen.add(v); code.push(v); }
  });
  return code.join("");
}

async function loadMajors() {
  try {
    const d = await fetch("/majors").then((r) => r.json());
    const sel = $("majorSelect");
    (d.majors || []).forEach((m) => {
      const o = document.createElement("option");
      o.value = m;
      o.textContent = m;
      sel.appendChild(o);
    });
  } catch { /* majors dropdown left with the placeholder only */ }
}
loadMajors();

/* ---------- Analyze ---------- */
$("analyzeBtn").addEventListener("click", async () => {
  const status = $("status");
  const btn = $("analyzeBtn");
  const jobUrl = $("jobUrl").value.trim();

  if (!currentUser) { status.textContent = "Sign in first."; return; }

  // Signals mode: no resume — send MBTI / Holland / major directly.
  if (inputMode === "signals") {
    const holland = buildHollandCode();
    if (!holland) { status.textContent = "Pick your top three interests."; return; }
    btn.disabled = true;
    status.textContent = "Analyzing…";
    try {
      const data = await apiFetch("/analyze-signals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mbti: $("mbtiSelect").value.trim(),
          holland,
          major: $("majorSelect").value.trim(),
          job_url: jobUrl,
        }),
      });
      render(data);
      status.textContent = "Done.";
      refreshUser();
    } catch (err) {
      status.textContent = "Error: " + err.message;
    } finally {
      btn.disabled = false;
    }
    return;
  }

  // Resume mode
  const text = buildAnalysisText();
  if (!resumeFile && !text.trim()) { status.textContent = "Add a resume or some experience text first."; return; }

  btn.disabled = true;
  status.textContent = "Analyzing…";

  try {
    let data;
    if (resumeFile && /\.pdf$/i.test(resumeFile.name)) {
      const fd = new FormData();
      fd.append("resume", resumeFile);
      if (jobUrl) fd.append("job_url", jobUrl);
      data = await apiFetch("/analyze", { method: "POST", body: fd });
    } else {
      data = await apiFetch("/analyze-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, job_url: jobUrl }),
      });
    }
    render(data);
    status.textContent = "Done.";
    refreshUser();
  } catch (err) {
    status.textContent = "Error: " + err.message;
  } finally {
    btn.disabled = false;
  }
});

function buildAnalysisText() {
  const parts = [];
  if (resumeText.trim()) parts.push(resumeText.trim());
  const exp = $("experience").value.trim();
  const certs = $("certifications").value.trim();
  const skills = $("skills").value.trim();
  if (exp) parts.push("WORK EXPERIENCE:\n" + exp);
  if (certs) parts.push("CERTIFICATIONS:\n" + certs);
  if (skills) parts.push("SKILLS:\n" + skills);
  return parts.join("\n\n");
}

/* ---------- Render ---------- */
function render(data) {
  currentAnalysis = data;
  currentJobAlignment = data.job_alignment || null;
  $("wizard").classList.add("hidden");
  $("results").classList.remove("hidden");
  renderSignals(data.signals);
  renderMatches(data.top_matches);
  renderMap(data.career_map);
  renderPie(data.top_matches);
}

function restart() {
  // Reset resume form
  resumeFile = null;
  resumeText = "";
  $("resumeFile").value = "";
  dz.querySelector("strong").textContent = "Drop a resume here";
  $("experience").value = "";
  $("certifications").value = "";
  $("skills").value = "";

  // Reset signals form
  $("mbtiSelect").value = "";
  $("holland1").value = "";
  $("holland2").value = "";
  $("holland3").value = "";
  $("majorSelect").value = "";

  $("status").textContent = "";
  currentAnalysis = null;
  currentMatches = [];
  currentJobAlignment = null;
  $("nodeDetails").classList.add("hidden");

  $("results").classList.add("hidden");
  $("wizard").classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
  $("wizard").scrollIntoView({ behavior: "smooth" });
}
$("restartBtn").addEventListener("click", restart);

/* ---------- Job alignment (rendered from the main analyze result) ---------- */
function jobLevelLabel(v) {
  if (!v) return "—";
  if (v.includes("High")) return "High";
  if (v.includes("Medium")) return "Medium";
  return "Low";
}

function renderJobResults(d) {
  const job = d.job || {};
  const kw = d.keyword_alignment || {};
  const psych = d.psychometric_alignment || {};
  const userS = d.user_signals || {};
  const jobS = d.job_signals || {};

  const userMbti = (userS.mbti?.inferred_type || "").replace(/X/g, "·") || "—";
  const jobMbti = (jobS.mbti?.inferred_type || "").replace(/X/g, "·") || "—";
  const userHolland = userS.holland?.inferred_code || "—";
  const jobHolland = jobS.holland?.inferred_code || "—";

  const overall = psych.overall;
  const overallCls = overall == null ? "" : overall >= 66 ? "good" : overall >= 40 ? "mid" : "bad";

  let kwHtml = "";
  if (kw.score != null) {
    kwHtml += `<p><b>Keyword coverage:</b> ${kw.score}% of the posting's signal terms appear in your background.</p>`;
  }
  if (kw.aligned && kw.aligned.length) {
    kwHtml += `<p><b class="good">✓ Aligns (${kw.aligned_count})</b> — ${kw.aligned.join(", ")}</p>`;
  }
  if (kw.gaps && kw.gaps.length) {
    kwHtml += `<p><b class="bad">✗ Missing (${kw.gap_count})</b> — ${kw.gaps.join(", ")}</p>`;
  }
  if (kw.extra && kw.extra.length) {
    kwHtml += `<p><b class="extra">+ Beyond the posting (${kw.extra_count})</b> — ${kw.extra.join(", ")}</p>`;
  }

  const bfTraits = psych.big_five?.traits || {};
  const bfNames = { O: "Openness", C: "Conscientiousness", E: "Extraversion", A: "Agreeableness", N: "Emotional Stability" };
  const bfRows = Object.entries(bfTraits).map(([k, v]) => {
    const name = bfNames[k] || k;
    const mark = v.match ? '<span class="good">✓</span>' : '<span class="muted">·</span>';
    return `<div class="rs-item"><b class="rs-letter">${k}</b><div><span class="rs-name">${name}</span>
      <p>You <b>${jobLevelLabel(v.user)}</b> · Job <b>${jobLevelLabel(v.job)}</b> ${mark}</p></div></div>`;
  }).join("");

  $("jobModalTitle").textContent = `${job.title || "Job posting"}${job.company ? " @ " + job.company : ""}`;

  $("jobModalBody").innerHTML = `
    <div class="job-score ${overallCls}">
      <div class="job-score-num">${overall != null ? overall + "%" : "—"}</div>
      <div class="job-score-label">overall psychometric alignment</div>
    </div>

    <h3 class="rs-h">Keyword &amp; experience alignment</h3>
    <p class="muted">${d.explanation || ""}</p>
    ${kwHtml}

    <h3 class="rs-h">Psychometric mapping</h3>
    <div class="rs-grid">
      <div class="rs-item"><b class="rs-letter">M</b><div>
        <span class="rs-name">Myers-Briggs</span>
        <p>You <b>${userMbti}</b> · Job <b>${jobMbti}</b> · <b>${psych.mbti?.match_pct != null ? psych.mbti.match_pct + "%" : "—"}</b></p>
      </div></div>
      <div class="rs-item"><b class="rs-letter">H</b><div>
        <span class="rs-name">Holland code</span>
        <p>You <b>${userHolland}</b> · Job <b>${jobHolland}</b> · Overlap <b>${(psych.holland?.overlap || []).join("") || "—"}</b></p>
      </div></div>
      ${bfRows}
    </div>

    <p class="muted small" style="margin-top:16px">Alignment is inferred from the language of the posting versus your resume/signals — a heuristic, not a guarantee.</p>
  `;

  $("jobModal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closeJobModal() {
  $("jobModal").classList.add("hidden");
  document.body.style.overflow = "";
}
$("closeJobModalBtn").addEventListener("click", closeJobModal);
$("jobModal").addEventListener("click", (e) => { if (e.target === e.currentTarget) closeJobModal(); });

function renderSignals(s) {
  const box = $("signalsBox");
  const mbtiRaw = (s.mbti?.inferred_type || "").replace(/X/g, "·");
  const mbti = mbtiRaw && mbtiRaw !== "····" ? mbtiRaw : "—";
  const holland = s.holland?.inferred_code || "N/A";
  const big5 = s.big_five?.inferred_profile || {};
  const big5Txt = Object.entries(big5).map(([k, v]) => `${k}: ${v}`).join(" · ") || "N/A";
  const jobBtnHtml = currentJobAlignment && !currentJobAlignment.error
    ? `<button id="jobMatchBtn" class="results-btn job-btn">Job match: ${currentJobAlignment.job?.title || "view"} →</button>`
    : "";
  box.innerHTML = `
    <div class="chip"><b>MBTI</b>${mbti}</div>
    <div class="chip"><b>Holland</b>${holland}</div>
    <div class="chip"><b>Big Five</b>${big5Txt}</div>
    <button id="resultsBtn" class="results-btn">Results →</button>
    <button id="emailResultsBtn" class="results-btn email-btn">Email my results</button>
    <button id="exportApplyPilotBtn" class="results-btn export-btn">Export for ApplyPilot</button>
    ${jobBtnHtml}`;
  $("resultsBtn").addEventListener("click", () => renderResultsPage(s));
  $("emailResultsBtn").addEventListener("click", emailResults);
  $("exportApplyPilotBtn").addEventListener("click", exportApplyPilot);
  if (currentJobAlignment && !currentJobAlignment.error) {
    $("jobMatchBtn").addEventListener("click", () => renderJobResults(currentJobAlignment));
  }
}

async function emailResults() {
  const btn = $("emailResultsBtn");
  if (!currentAnalysis) return;
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Sending…";
  try {
    const d = await apiFetch("/analyze/email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ signals: currentAnalysis.signals, top_matches: currentAnalysis.top_matches }),
    });
    btn.textContent = "✓ Sent to " + (d.to || "your email");
  } catch (err) {
    btn.textContent = "Failed, try again";
    btn.disabled = false;
    setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 3000);
  }
}

async function exportApplyPilot() {
  const btn = $("exportApplyPilotBtn");
  if (!currentAnalysis) return;
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Exporting…";
  try {
    const resp = await fetch("/export/applypilot", {
      method: "POST",
      headers: { ...authHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({
        top_matches: currentAnalysis.full_ranking || currentAnalysis.top_matches,
        location: localStorage.getItem("anitalmid_location") || "",
      }),
    });
    if (resp.status === 401) { logout(); throw new Error("Please sign in first."); }
    if (!resp.ok) {
      let msg = resp.status;
      try { const d = await resp.json(); msg = d.detail || msg; } catch {}
      throw new Error(msg);
    }
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "applypilot_config.zip";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    btn.textContent = "✓ Downloaded";
    setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 3000);
  } catch (err) {
    btn.textContent = "Failed, try again";
    btn.disabled = false;
    setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 3000);
  }
}

let currentMatches = [];
let currentAnalysis = null;
let currentJobAlignment = null;
function renderMatches(matches) {
  currentMatches = matches || [];
  const box = $("matches");
  box.innerHTML = currentMatches
    .map(
      (r, i) => `
    <div class="match clickable" data-idx="${i}">
      <div class="top">
        <span><span class="rank">#${r.rank}</span><span class="title">${r.title}</span></span>
        <span class="score">${r.composite_score}</span>
      </div>
      <div>
        <span class="badge ${r.validation}">${r.validation.replace("-", " ")}</span>
        <span class="meta">${r.category} · ${r.holland_code} · pivot: ${r.pivot_cost}</span>
      </div>
      <div class="meta">${r.salary_range}</div>
      <div class="desc">${r.description}</div>
      <div class="match-cta">View full description &amp; search jobs →</div>
    </div>`
    )
    .join("");
  box.querySelectorAll(".match").forEach((el) => {
    el.addEventListener("click", () => openRoleModal(parseInt(el.dataset.idx, 10)));
  });
}

let matchesPie = null;
function renderPie(matches) {
  const canvas = $("matchesPie");
  if (!canvas || !window.Chart) return;
  if (matchesPie) { matchesPie.destroy(); matchesPie = null; }

  const COLORS = ["#2dd4bf", "#38bdf8", "#4ade80", "#a78bfa", "#fbbf24", "#f87171"];
  const items = (matches || []).slice(0, 6);
  const pct = (m) => Math.min(100, Math.round(m.composite_score));

  matchesPie = new Chart(canvas.getContext("2d"), {
    type: "pie",
    data: {
      labels: items.map((m) => m.title),
      datasets: [{
        data: items.map((m) => Math.max(0, m.composite_score)),
        backgroundColor: COLORS.slice(0, items.length),
        borderColor: "#0b0f1a",
        borderWidth: 2,
        hoverOffset: 30,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: { padding: 14 },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#131a29",
          titleColor: "#e9eef7",
          bodyColor: "#93a0b8",
          borderColor: "#2a3450",
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: (c) => {
              const m = items[c.dataIndex];
              return ` ${pct(m)}% aligned · ${(m.validation || "").replace("-", " ")}`;
            },
          },
        },
      },
    },
  });

  $("pieLegend").innerHTML = items
    .map((m, i) => `<span class="pie-item clickable" data-idx="${i}"><i style="background:${COLORS[i]}"></i>${m.title} <b>${pct(m)}%</b></span>`)
    .join("");
  $("pieLegend").querySelectorAll(".pie-item").forEach((el) => {
    el.addEventListener("click", () => openRoleModal(parseInt(el.dataset.idx, 10)));
  });
}

/* ---------- Role detail modal ---------- */
function indeedUrl(title, location) {
  let url = "https://www.indeed.com/jobs?q=" + encodeURIComponent(title);
  if (location) url += "&l=" + encodeURIComponent(location);
  return url;
}

function openRoleModal(idx) {
  const role = currentMatches[idx];
  if (!role) return;
  $("roleModalTitle").textContent = role.title;
  $("roleModalBody").innerHTML = roleModalHtml(role);
  $("roleModalLocation").value = localStorage.getItem("anitalmid_location") || "";
  $("roleModal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
  $("roleModalIndeedBtn").addEventListener("click", () => {
    const loc = $("roleModalLocation").value.trim();
    localStorage.setItem("anitalmid_location", loc);
    window.open(indeedUrl(role.title, loc), "_blank", "noopener");
  });
}

function closeRoleModal() {
  $("roleModal").classList.add("hidden");
  document.body.style.overflow = "";
}

function roleModalHtml(role) {
  const rows = [
    ["Category", role.category],
    ["Holland code", role.holland_code],
    ["Typical MBTI", role.mbti_type],
    ["O*NET", role.o_net_code],
    ["Salary", role.salary_range],
    ["Experience", role.experience_required],
    ["Pivot cost", role.pivot_cost],
  ].filter(([, v]) => v).map(([k, v]) => `<li><span class="k">${k}</span><span>${v}</span></li>`).join("");

  const skills = (role.keywords_strong || []).slice(0, 8).map((k) => `<span class="skill-tag">${k}</span>`).join("");

  return `
    <div class="role-badges">
      <span class="badge ${role.validation}">${(role.validation || "").replace("-", " ")}</span>
      <span class="badge score-badge">${Math.round(role.composite_score)}% aligned</span>
    </div>
    <p class="role-desc">${role.description || ""}</p>
    <ul class="nd-kv">${rows}</ul>
    ${skills ? `<div class="role-skills"><b>Key skills &amp; responsibilities</b><div>${skills}</div></div>` : ""}
    <div class="role-scoring muted">How it's scored: keyword ${role.keyword_score} · framework ${role.framework_score} · boost +${role.experience_boost}.</div>
    <div class="role-location">
      <label for="roleModalLocation">Location <span class="muted">(optional)</span></label>
      <input type="text" id="roleModalLocation" placeholder="City, State or Remote" />
    </div>
    <button id="roleModalIndeedBtn" class="indeed-btn" type="button">Search "${role.title}" on Indeed ↗</button>
  `;
}

let careerNetwork = null;
function renderMap(map) {
  const TYPE_STYLE = {
    profile: { color: "#2dd4bf", glow: "rgba(45,212,191,0.45)", size: 17 },
    signal: { color: "#38bdf8", glow: "rgba(56,189,248,0.45)", size: 12 },
    role: { color: "#4ade80", glow: "rgba(74,222,128,0.45)", size: 10 },
  };

  const nodes = map.nodes.map((n) => {
    const s = TYPE_STYLE[n.type] || { color: "#a78bfa", glow: "rgba(167,139,250,0.45)", size: 9 };
    return {
      id: n.id,
      label: n.label,
      title: n.label,
      shape: "dot",
      size: s.size,
      borderWidth: 2,
      color: {
        background: s.color,
        border: s.color,
        highlight: { background: s.color, border: "#ffffff" },
        hover: { background: s.color, border: "#ffffff" },
      },
      shadow: { enabled: true, color: s.glow, size: 10, x: 0, y: 0 },
      font: { color: "#9aa4b8", size: 11, face: "system-ui, -apple-system, sans-serif" },
    };
  });

  const edges = map.edges.map((e) => ({
    from: e.source,
    to: e.target,
    value: e.weight,
    width: 0.5,
    color: { color: "rgba(147,160,184,0.15)", highlight: "#2dd4bf", hover: "#2dd4bf" },
  }));

  const container = $("map");
  if (careerNetwork) { careerNetwork.destroy(); careerNetwork = null; }
  const nodesData = new vis.DataSet(nodes);
  const edgesData = new vis.DataSet(edges);
  const network = new vis.Network(container, { nodes: nodesData, edges: edgesData }, {
    physics: {
      stabilization: { iterations: 250, updateInterval: 25 },
      forceAtlas2Based: {
        gravitationalConstant: -60,
        centralGravity: 0.005,
        springLength: 110,
        springConstant: 0.06,
        damping: 0.4,
        avoidOverlap: 0.6,
      },
    },
    interaction: { hover: true, tooltipDelay: 120 },
  });

  careerNetwork = network;

  network.on("click", (params) => {
    const nodeId = params.nodes[0];
    if (nodeId) {
      const node = map.nodes.find((n) => n.id === nodeId);
      renderNodeDetails(node, map.nodes, map.edges);
    }
  });
}

// Re-fit the career map on resize / orientation change (mobile).
let _mapResizeTimer = null;
window.addEventListener("resize", () => {
  clearTimeout(_mapResizeTimer);
  _mapResizeTimer = setTimeout(() => {
    if (careerNetwork) {
      const c = $("map");
      if (c) careerNetwork.setSize(c.clientWidth + "px", c.clientHeight + "px");
    }
  }, 200);
});

// Live GitHub star count for the header badge.
fetch("https://api.github.com/repos/CptBaldbeard/The-Anitalmid-Project")
  .then((r) => r.json())
  .then((d) => { if (d && typeof d.stargazers_count === "number") $("starCount").textContent = d.stargazers_count; })
  .catch(() => {});

function renderNodeDetails(node, nodes, edges) {
  const box = $("nodeDetails");
  if (!node) {
    box.classList.add("hidden");
    return;
  }
  box.classList.remove("hidden");

  const conns = edges
    .filter((e) => e.source === node.id || e.target === node.id)
    .map((e) => {
      const otherId = e.source === node.id ? e.target : e.source;
      const other = nodes.find((n) => n.id === otherId);
      const dir = e.source === node.id ? "→" : "←";
      const lbl = e.label ? ` (${e.label})` : "";
      return `<li>${dir} ${other ? other.label : otherId}${lbl}</li>`;
    });

  const typeLabel = { profile: "Your profile", signal: "Detected signal", role: "Career role" }[node.type] || node.type;

  let dataHtml = "";
  if (node.type === "profile") dataHtml = `<p class="muted">${node.data?.note || ""}</p>`;
  else if (node.type === "signal") dataHtml = signalDetailsHtml(node);
  else if (node.type === "role") dataHtml = roleDetailsHtml(node);

  box.innerHTML = `
    <div class="nd-head"><span class="nd-type">${typeLabel}</span><b>${node.label}</b></div>
    ${dataHtml}
    <div class="nd-conns"><b>Connections</b><ul>${conns.join("")}</ul></div>`;
}

function signalDetailsHtml(node) {
  const d = node.data || {};
  if (node.id === "sig-mbti") {
    const t = d.inferred_type || "N/A";
    return `<p>Type <b>${t}</b> — ${mbtiDecode(t)}.</p>`;
  }
  if (node.id === "sig-holland") {
    const code = d.inferred_code || "N/A";
    const parts = [d.primary, d.secondary, d.tertiary].filter(Boolean).map((c) => `${hollandName(c)} (${c})`);
    return `<p>Code <b>${code}</b></p><p class="muted">${parts.join(" · ") || "—"}</p>`;
  }
  if (node.id === "sig-big5") {
    const prof = d.inferred_profile || {};
    const entries = Object.entries(prof).map(([k, v]) => `<li><span class="k">${k}</span><span>${v}</span></li>`).join("");
    return `<p class="muted">Trait profile (Low → High):</p><ul class="nd-kv">${entries || "<li>—</li>"}</ul>`;
  }
  return "";
}

function roleDetailsHtml(node) {
  const d = node.data || {};
  const rows = [
    ["Score", d.score != null ? Math.round(d.score) : "—"],
    ["Validation", d.validation],
    ["Category", d.category],
    ["Holland", d.holland_code],
    ["O*NET", d.o_net_code],
    ["Salary", d.salary_range],
    ["Pivot cost", d.pivot_cost],
    ["Experience", d.experience_required],
  ].filter(([, v]) => v).map(([k, v]) => `<li><span class="k">${k}</span><span>${v}</span></li>`).join("");

  const breakdown = d.keyword_score != null
    ? `<p class="muted">How it's scored: keyword ${d.keyword_score} · framework ${d.framework_score} · experience boost +${d.experience_boost}.</p>`
    : "";
  return `<ul class="nd-kv">${rows}</ul>${breakdown}${d.description ? `<p class="muted">${d.description}</p>` : ""}<a class="indeed-btn" href="${indeedUrl(node.label)}" target="_blank" rel="noopener">Search on Indeed ↗</a>`;
}

function mbtiDecode(t) {
  const map = { I: "Introverted", E: "Extraverted", N: "Intuitive", S: "Sensing", T: "Thinking", F: "Feeling", J: "Judging", P: "Perceiving" };
  const parts = (t || "").split("").map((c) => map[c]).filter(Boolean);
  return parts.length ? parts.join(", ") : "Not enough signal to infer a type";
}

function hollandName(c) {
  return { R: "Realistic", I: "Investigative", A: "Artistic", S: "Social", E: "Enterprising", C: "Conventional" }[c] || c;
}

/* ---------- Role modal close ---------- */
$("closeRoleModalBtn").addEventListener("click", closeRoleModal);
$("roleModal").addEventListener("click", (e) => {
  if (e.target === e.currentTarget) closeRoleModal();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeRoleModal();
});

/* ---------- How-it-works info modal ---------- */
$("infoBtn").addEventListener("click", () => {
  $("infoModal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
});
function closeInfoModal() {
  $("infoModal").classList.add("hidden");
  document.body.style.overflow = "";
}
$("closeInfoBtn").addEventListener("click", closeInfoModal);
$("infoModal").addEventListener("click", (e) => {
  if (e.target === e.currentTarget) closeInfoModal();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeInfoModal();
});
