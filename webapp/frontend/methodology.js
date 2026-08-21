/* Methodology page — interactive vault graph + creation timelapse. */
const $ = (id) => document.getElementById(id);

let data = null;
let nodesData, edgesData, network;
let timeline = [];   // notes sorted by creation order
let allEdges = [];   // vis-network edge objects
let addedCount = 0;
let playing = false;
let playTimer = null;

const KEY_NODES = new Set([
  "Capstone - Career Aptitude Synthesis",
  "Frameworks Overview",
  "Myers-Briggs MBTI",
  "Big Five OCEAN",
  "Holland Codes RIASEC",
]);

function visNode(n) {
  const key = KEY_NODES.has(n.id);
  const isCapstone = n.id.startsWith("Capstone");
  return {
    id: n.id,
    label: key ? n.label : "",
    title: n.label,
    shape: "dot",
    size: isCapstone ? 18 : key ? 11 : 7,
    color: {
      background: n.color,
      border: n.color,
      highlight: { background: n.color, border: "#ffffff" },
      hover: { background: n.color, border: "#ffffff" },
    },
    font: { color: "#9aa4b8", size: key ? 11 : 0, face: "system-ui, -apple-system, sans-serif" },
  };
}

function visEdge(e) {
  return {
    from: e.source,
    to: e.target,
    width: 0.5,
    selectionWidth: 0,
    color: { color: "rgba(147,160,184,0.12)", highlight: "#2dd4bf", hover: "#2dd4bf" },
  };
}

function fmtDate(ts) {
  return new Date(ts * 1000).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function buildLegend() {
  const counts = data.meta.folders;
  const colorFor = (folder) => {
    const n = data.nodes.find((x) => x.folder === folder);
    return n ? n.color : "#8b98b0";
  };
  const names = {
    "Frameworks": "Frameworks", "Claims": "Claims", "Role Profiles": "Role Profiles",
    "synthesis": "Synthesis", "Birkman Insights": "Birkman", "Birkman Colors": "Birkman",
    "Birkman Symbols": "Birkman", "Birkman Interests": "Birkman",
    "Birkman Career Exploration Overview": "Birkman", "Career History": "Career History",
    "Enneagram Report": "Enneagram", "Parachute": "Parachute", "Memories": "Other",
    "Projects": "Other", "Reflections": "Other", "Resume": "Resume", "root": "Core",
  };
  const merged = {};
  for (const [folder, cnt] of Object.entries(counts)) {
    const label = names[folder] || folder;
    if (!merged[label]) merged[label] = { cnt: 0, color: colorFor(folder) };
    merged[label].cnt += cnt;
  }
  $("legend").innerHTML = Object.entries(merged)
    .map(([label, m]) => `<span><i style="background:${m.color}"></i>${label} (${m.cnt})</span>`)
    .join("");
}

function visibleEdges(count) {
  const visible = new Set(timeline.slice(0, count).map((n) => n.id));
  return allEdges.filter((e) => visible.has(e.from) && visible.has(e.to));
}

/* Clear and re-render the first `count` notes (used for scrub / reset). */
function resetTo(count) {
  stopPlay();
  count = Math.max(0, Math.min(count, timeline.length));
  nodesData.clear();
  edgesData.clear();
  addedCount = 0;
  for (let i = 0; i < count; i++) {
    nodesData.add(visNode(timeline[i]));
    addedCount++;
  }
  visibleEdges(count).forEach((e) => edgesData.add(e));
  updateLabel(count);
}

function renderUpTo(count) {
  while (addedCount < count && addedCount < timeline.length) {
    nodesData.add(visNode(timeline[addedCount]));
    addedCount++;
  }
  visibleEdges(addedCount).forEach((e) => {
    if (!edgesData.get(e.id)) edgesData.add({ ...e, id: e.from + "→" + e.to });
  });
}

function updateLabel(count) {
  const slider = $("timeline");
  slider.value = count;
  $("timelineLabel").textContent =
    count === 0
      ? "Empty"
      : count >= timeline.length
        ? "All notes"
        : `${count} notes · ${fmtDate(timeline[count - 1].created)}`;
}

function play() {
  if (playing) {
    stopPlay();
    return;
  }
  playing = true;
  $("playBtn").textContent = "⏸ Pause";
  nodesData.clear();
  edgesData.clear();
  addedCount = 0;
  const DURATION = 12000; // ms to reveal everything
  const start = performance.now();
  playTimer = setInterval(() => {
    const elapsed = performance.now() - start;
    const target = Math.min(timeline.length, Math.floor((elapsed / DURATION) * timeline.length));
    renderUpTo(target);
    updateLabel(target);
    if (target >= timeline.length) stopPlay();
  }, 80);
}

function stopPlay() {
  playing = false;
  if (playTimer) { clearInterval(playTimer); playTimer = null; }
  $("playBtn").textContent = "▶ Play timelapse";
}

async function init() {
  const resp = await fetch("vault_graph.json");
  data = await resp.json();
  timeline = data.nodes.slice().sort((a, b) => a.seq - b.seq);
  allEdges = data.edges.map(visEdge);

  $("noteCount").textContent = data.meta.note_count;
  $("edgeCount").textContent = data.meta.edge_count;

  const slider = $("timeline");
  slider.max = timeline.length;
  slider.value = timeline.length;

  nodesData = new vis.DataSet();
  edgesData = new vis.DataSet();
  const container = $("vaultGraph");
  network = new vis.Network(container, { nodes: nodesData, edges: edgesData }, {
    physics: {
      stabilization: { enabled: false },
      forceAtlas2Based: {
        gravitationalConstant: -55,
        centralGravity: 0.005,
        springLength: 95,
        springConstant: 0.05,
        damping: 0.4,
        avoidOverlap: 0.5,
      },
    },
    interaction: { hover: true, tooltipDelay: 120 },
  });

  buildLegend();
  resetTo(timeline.length); // show the full graph initially
}

$("playBtn").addEventListener("click", play);
$("resetBtn").addEventListener("click", () => resetTo(timeline.length));
$("timeline").addEventListener("input", (e) => resetTo(parseInt(e.target.value, 10)));

init();
