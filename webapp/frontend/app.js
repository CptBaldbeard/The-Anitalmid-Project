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
    const unverified = currentUser.email_verified === false;
    $("verifyBanner").classList.toggle("hidden", !unverified);
  } else {
    $("authLoggedOut").classList.remove("hidden");
    $("authLoggedIn").classList.add("hidden");
    $("verifyBanner").classList.add("hidden");
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
$("resendBtn").addEventListener("click", async () => {
  const s = $("verifyStatus");
  s.textContent = "";
  try {
    await apiFetch("/auth/resend-verification", { method: "POST" });
    s.textContent = "Sent! Check your inbox.";
  } catch (e) {
    s.textContent = e.message;
  }
});

/* Restore session on load */
(async () => {
  if (token) {
    try {
      const me = await apiFetch("/auth/me");
      currentUser = me;
      renderAuth();
    } catch { logout(); }
  }
})();

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
  renderExpanded(data.expanded_matches || []);
}

function renderExpanded(items) {
  const box = $("expanded");
  if (!items || !items.length) {
    box.innerHTML = '<p class="muted">No expanded results (web search unavailable or no matches).</p>';
    return;
  }
  box.innerHTML = items
    .map((r) => {
      const meta = [r.category, r.holland_code, r.salary_range, r.pivot_cost ? "pivot: " + r.pivot_cost : ""]
        .filter(Boolean)
        .join(" · ");
      return `
    <div class="expanded-item">
      <div class="top"><a href="${r.source_url}" target="_blank" rel="noopener">${r.title}</a></div>
      <div class="meta">${meta}</div>
      <div class="muted small">${r.snippet}</div>
    </div>`;
    })
    .join("");
}

function renderSignals(s) {
  const box = $("signalsBox");
  const mbti = s.mbti?.inferred_type || "N/A";
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

function renderMap(map) {
  const nodes = map.nodes.map((n) => {
    const color = n.type === "profile" ? "#d4a24e" : n.type === "signal" ? "#5b8def" : n.type === "role" ? "#57b87e" : n.type === "expanded" ? "#e0884a" : "#9b6cf0";
    const shape = n.type === "profile" ? "star" : (n.type === "role" || n.type === "expanded") ? "box" : "ellipse";
    return {
      id: n.id,
      label: n.label,
      title: n.label,
      color: { background: color, border: "#0e0f13", highlight: { background: color, border: "#fff" } },
      font: { color: "#e8e6df", size: n.type === "role" ? 13 : 15 },
      shape,
      margin: 8,
    };
  });
  const edges = map.edges.map((e) => ({
    from: e.source,
    to: e.target,
    label: e.label,
    value: e.weight,
    color: { color: "#3a3d4a", highlight: "#d4a24e" },
    font: { color: "#8a8f9c", size: 10 },
  }));
  const container = $("map");
  const network = new vis.Network(container, { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) }, {
    physics: { stabilization: true, barnesHut: { gravitationalConstant: -8000, springLength: 120 } },
    interaction: { hover: true, tooltipDelay: 150 },
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

  const typeLabel = { profile: "Your profile", signal: "Detected signal", role: "Career role", expanded: "Web-expanded role" }[node.type] || node.type;

  let dataHtml = "";
  if (node.type === "profile") dataHtml = `<p class="muted">${node.data?.note || ""}</p>`;
  else if (node.type === "signal") dataHtml = signalDetailsHtml(node);
  else if (node.type === "role") dataHtml = roleDetailsHtml(node);
  else if (node.type === "expanded") dataHtml = expandedDetailsHtml(node);

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

function expandedDetailsHtml(node) {
  const d = node.data || {};
  const rows = [["Category", d.category], ["Holland", d.holland_code], ["Salary", d.salary_range]]
    .filter(([, v]) => v)
    .map(([k, v]) => `<li><span class="k">${k}</span><span>${v}</span></li>`).join("");
  const link = d.source_url ? `<p><a href="${d.source_url}" target="_blank" rel="noopener">Source ↗</a></p>` : "";
  return `<ul class="nd-kv">${rows}</ul>${link}`;
}

function mbtiDecode(t) {
  const map = { I: "Introverted", E: "Extraverted", N: "Intuitive", S: "Sensing", T: "Thinking", F: "Feeling", J: "Judging", P: "Perceiving" };
  return (t || "").split("").map((c) => map[c] || c).join(", ");
}

function hollandName(c) {
  return { R: "Realistic", I: "Investigative", A: "Artistic", S: "Social", E: "Enterprising", C: "Conventional" }[c] || c;
}
