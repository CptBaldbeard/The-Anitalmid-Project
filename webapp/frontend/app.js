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

/* ---------- Analyze ---------- */
$("analyzeBtn").addEventListener("click", async () => {
  const status = $("status");
  const btn = $("analyzeBtn");
  const text = buildAnalysisText();

  if (!currentUser) { status.textContent = "Sign in first."; return; }
  if (!resumeFile && !text.trim()) { status.textContent = "Add a resume or some experience text first."; return; }

  btn.disabled = true;
  status.textContent = "Analyzing…";

  try {
    let data;
    if (resumeFile && /\.pdf$/i.test(resumeFile.name)) {
      const fd = new FormData();
      fd.append("resume", resumeFile);
      data = await apiFetch("/analyze", { method: "POST", body: fd });
    } else {
      data = await apiFetch("/analyze-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
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
  $("wizard").classList.add("hidden");
  $("results").classList.remove("hidden");
  renderSignals(data.signals);
  renderMatches(data.top_matches);
  renderMap(data.career_map);
  renderPie(data.top_matches);
}

function renderSignals(s) {
  const box = $("signalsBox");
  const mbtiRaw = (s.mbti?.inferred_type || "").replace(/X/g, "·");
  const mbti = mbtiRaw && mbtiRaw !== "····" ? mbtiRaw : "—";
  const holland = s.holland?.inferred_code || "N/A";
  const big5 = s.big_five?.inferred_profile || {};
  const big5Txt = Object.entries(big5).map(([k, v]) => `${k}: ${v}`).join(" · ") || "N/A";
  box.innerHTML = `
    <div class="chip"><b>MBTI</b>${mbti}</div>
    <div class="chip"><b>Holland</b>${holland}</div>
    <div class="chip"><b>Big Five</b>${big5Txt}</div>`;
}

function renderMatches(matches) {
  const box = $("matches");
  box.innerHTML = matches
    .map(
      (r) => `
    <div class="match">
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
    </div>`
    )
    .join("");
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
    .map((m, i) => `<span class="pie-item"><i style="background:${COLORS[i]}"></i>${m.title} <b>${pct(m)}%</b></span>`)
    .join("");
}

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

  network.on("click", (params) => {
    const nodeId = params.nodes[0];
    if (nodeId) {
      const node = map.nodes.find((n) => n.id === nodeId);
      renderNodeDetails(node, map.nodes, map.edges);
    }
  });
}

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
  return `<ul class="nd-kv">${rows}</ul>${breakdown}${d.description ? `<p class="muted">${d.description}</p>` : ""}`;
}

function mbtiDecode(t) {
  const map = { I: "Introverted", E: "Extraverted", N: "Intuitive", S: "Sensing", T: "Thinking", F: "Feeling", J: "Judging", P: "Perceiving" };
  const parts = (t || "").split("").map((c) => map[c]).filter(Boolean);
  return parts.length ? parts.join(", ") : "Not enough signal to infer a type";
}

function hollandName(c) {
  return { R: "Realistic", I: "Investigative", A: "Artistic", S: "Social", E: "Enterprising", C: "Conventional" }[c] || c;
}
