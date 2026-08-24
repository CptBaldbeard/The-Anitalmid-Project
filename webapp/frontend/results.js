/* Anitalmid — individualized results breakdown (MBTI / Holland / Big Five). */

const MBTI_DICHOTOMIES = {
  E: { letter: "E", name: "Extraversion", desc: "Energized by the outer world of people and activity. Thinks out loud, thrives in collaborative, fast-paced settings — meetings, presentations, networking." },
  I: { letter: "I", name: "Introversion", desc: "Energized by the inner world of ideas and reflection. Thinks before speaking, excels at deep analysis, writing, and solo work — needs recharge time after socializing." },
  S: { letter: "S", name: "Sensing", desc: "Focuses on concrete, tangible information — facts, experience, detail. Excels at hands-on, practical, detail-oriented work and trusts proven methods." },
  N: { letter: "N", name: "Intuition", desc: "Focuses on patterns, possibilities, and the big picture. Trusts insight and theory. Excels at strategy, innovation, and systems thinking — comfortable with ambiguity." },
  T: { letter: "T", name: "Thinking", desc: "Decides with logic, consistency, and objective analysis. Excels in analytical roles — engineering, systems, data, security. Values correctness over consensus." },
  F: { letter: "F", name: "Feeling", desc: "Decides with personal values and impact on people. Excels in people-facing roles — counseling, HR, teaching, advocacy. Values harmony and outcomes for others." },
  J: { letter: "J", name: "Judging", desc: "Prefers structure, planning, and closure. Excels in project management, operations, and compliance — thrives on deadlines and clear expectations." },
  P: { letter: "P", name: "Perceiving", desc: "Prefers flexibility, adaptability, and open options. Excels in creative work, research, and crisis response — thrives on autonomy and emergent priorities." },
};

const MBTI_TYPES = {
  ISTJ: { name: "The Logistician", desc: "Practical, fact-minded, and dependable. Values order, rules, and thoroughness — the steady backbone of any organization.", careers: "Operations, compliance, accounting, law enforcement" },
  ISFJ: { name: "The Defender", desc: "Warm, conscientious, and quietly devoted. Protects and supports others with tireless, behind-the-scenes diligence.", careers: "Healthcare, education, administrative support" },
  INFJ: { name: "The Advocate", desc: "Insightful, idealistic, and quietly determined. Sees meaning and potential in people and ideas, driven by a sense of purpose.", careers: "Counseling, writing, non-profit leadership" },
  INTJ: { name: "The Architect", desc: "Strategic, analytical, and fiercely independent. Sees the system behind the system and designs the most efficient path forward.", careers: "Systems architecture, strategic planning, research, engineering" },
  ISTP: { name: "The Virtuoso", desc: "Bold, hands-on, and pragmatic. Masters tools and systems through direct experimentation rather than theory.", careers: "Engineering, trades, emergency response, field technician" },
  ISFP: { name: "The Adventurer", desc: "Gentle, artistic, and fully present. Expresses inner experience through action, craft, and aesthetics.", careers: "Arts, design, healthcare, skilled trades" },
  INFP: { name: "The Mediator", desc: "Idealistic, empathetic, and values-driven. Seeks authenticity and meaning in every pursuit.", careers: "Writing, counseling, creative arts, academia" },
  INTP: { name: "The Logician", desc: "Analytical, curious, and independent-minded. Deconstructs ideas to uncover the underlying truth.", careers: "Research, software development, philosophy, systems analysis" },
  ESTP: { name: "The Entrepreneur", desc: "Energetic, perceptive, and action-oriented. Lives at full throttle, thriving on risk, variety, and real-time problem solving.", careers: "Sales, emergency management, athletics, business" },
  ESFP: { name: "The Entertainer", desc: "Spontaneous, sociable, and enthusiastic. Brings warmth and energy to every room and every task.", careers: "Performance, hospitality, sales, event planning" },
  ENFP: { name: "The Campaigner", desc: "Enthusiastic, creative, and sociable. Sees possibilities everywhere and connects people to them.", careers: "Marketing, journalism, entrepreneurship, teaching" },
  ENTP: { name: "The Debater", desc: "Quick, ingenious, and intellectually fearless. Challenges convention to build better ideas.", careers: "Law, consulting, engineering, entrepreneurship" },
  ESTJ: { name: "The Executive", desc: "Organized, direct, and dependable. Runs things efficiently and fairly, with clear standards and follow-through.", careers: "Management, law, military, operations" },
  ESFJ: { name: "The Consul", desc: "Warm, conscientious, and cooperative. Keeps communities and teams running smoothly and harmoniously.", careers: "Healthcare, teaching, hospitality, administration" },
  ENFJ: { name: "The Protagonist", desc: "Charismatic, inspiring, and empathetic. Helps others grow and reach their full potential.", careers: "Teaching, counseling, politics, non-profit" },
  ENTJ: { name: "The Commander", desc: "Bold, strategic, and decisive. Leads with vision and drives execution at scale.", careers: "Executive leadership, law, consulting, military" },
};

const HOLLAND_TYPES = {
  R: { name: "Realistic", tag: "The Doers", desc: "Drawn to things, tools, machines, and physical systems. Values practicality and tangible results. Prefers concrete problems and hands-on work over abstract theory.", careers: "Engineering, skilled trades, agriculture, law enforcement, field tech, construction" },
  I: { name: "Investigative", tag: "The Thinkers", desc: "Drawn to understanding, analyzing, and solving problems through ideas. Values knowledge and precision. Prefers research, analysis, and complex problem-solving.", careers: "Scientist, researcher, software developer, systems analyst, data analyst, physician" },
  A: { name: "Artistic", tag: "The Creators", desc: "Drawn to creating, expressing, and innovating through unstructured media. Values creativity and originality. Prefers writing, design, and performance over routine.", careers: "Writer, designer, musician, architect, UX designer, creative director" },
  S: { name: "Social", tag: "The Helpers", desc: "Drawn to helping, teaching, counseling, and developing others. Values service and empathy. Prefers teaching, counseling, and caregiving over isolated or mechanical work.", careers: "Teacher, counselor, social worker, nurse, HR, coach" },
  E: { name: "Enterprising", tag: "The Persuaders", desc: "Drawn to leading, persuading, selling, and achieving organizational goals. Values success and influence. Prefers sales, management, and entrepreneurship.", careers: "Sales manager, executive, entrepreneur, lawyer, politician" },
  C: { name: "Conventional", tag: "The Organizers", desc: "Drawn to organizing, managing data, and maintaining systems. Values accuracy, order, and efficiency. Prefers structured processes and record-keeping.", careers: "Accountant, administrative assistant, compliance officer, auditor, bookkeeper" },
};

const BIG5_TRAITS = {
  O: {
    name: "Openness",
    High: "Curious, imaginative, creative, and abstract-thinking. Drawn to novelty, art, and ideas. Thrives with autonomy and intellectual challenge — creative, research, entrepreneurial, and strategic roles.",
    Medium: "Balanced between the novel and the familiar — comfortable with a mix of routine and exploration, concrete and conceptual work.",
    Low: "Practical, conventional, and grounded. Prefers routine and familiarity, trusts concrete facts. Thrives in structured, hands-on roles with clear expectations and proven methods.",
  },
  C: {
    name: "Conscientiousness",
    High: "Organized, disciplined, methodical, and achievement-oriented. Plans ahead and follows through — the single best personality predictor of job performance across all occupations.",
    Medium: "Reliable and structured where it counts, while staying comfortable with a degree of flexibility.",
    Low: "Flexible, spontaneous, and adaptable. Prefers improvisation over rigid planning. Thrives in creative, crisis-response, and entrepreneurial roles that reward adaptability.",
  },
  E: {
    name: "Extraversion",
    High: "Outgoing, energetic, talkative, and assertive. Gains energy from social interaction. Thrives in sales, management, teaching, and public-facing roles.",
    Medium: "Comfortable in both social and solitary settings — adaptable to collaborative or independent work.",
    Low: "Reserved, reflective, and prefers solitude. Gains energy from quiet and alone time. Thrives in research, analysis, writing, and independent work.",
  },
  A: {
    name: "Agreeableness",
    High: "Cooperative, compassionate, trusting, and conflict-avoidant. Values harmony and helping others. Thrives in healthcare, counseling, customer service, and social work.",
    Medium: "Cooperates when aligned, but will hold the line when the situation demands it.",
    Low: "Competitive, skeptical, direct, and willing to challenge. Values truth over harmony. Thrives in law, security, auditing, and competitive business.",
  },
  N: {
    name: "Emotional Stability",
    High: "Calm, resilient, confident, and emotionally steady. Handles pressure well and recovers quickly — suited to high-pressure roles like emergency response, leadership, trading, and critical operations.",
    Medium: "Steady most of the time, with occasional stress responses under sustained pressure.",
    Low: "More sensitive to stress and change. Performs best in predictable, supportive, lower-pressure environments.",
    note: "Measured as emotional stability (the inverse of Neuroticism): higher stability = lower neuroticism.",
  },
};

const LEVEL_LABEL = { High: "high", Medium: "medium", Low: "low" };

function resultsPageBody(s) {
  const mbtiRaw = (s.mbti?.inferred_type || "").replace(/X/g, "·");
  const holland = s.holland?.inferred_code || "";
  const big5 = s.big_five?.inferred_profile || {};

  /* ---- MBTI ---- */
  const type = (s.mbti?.inferred_type || "");
  const typeInfo = MBTI_TYPES[type];
  let mbtiHtml = `<h3 class="rs-h">Myers-Briggs <span class="rs-big">${mbtiRaw || "—"}</span>${typeInfo ? ` <span class="rs-tag">${typeInfo.name}</span>` : ""}</h3>`;
  if (typeInfo) {
    mbtiHtml += `<p class="rs-desc">${typeInfo.desc}</p><p class="rs-careers"><b>Best-fit career clusters:</b> ${typeInfo.careers}.</p>`;
  } else if (type) {
    mbtiHtml += `<p class="rs-desc muted">Some dichotomies were undetermined ("·"), so this isn't a single classic type — the letters below still describe your strongest preferences.</p>`;
  }
  mbtiHtml += `<div class="rs-grid">`;
  for (const ch of type) {
    if (ch === "X") continue;
    const d = MBTI_DICHOTOMIES[ch];
    if (d) mbtiHtml += `<div class="rs-item"><b class="rs-letter">${ch}</b><div><span class="rs-name">${d.name}</span><p>${d.desc}</p></div></div>`;
  }
  mbtiHtml += `</div>`;

  /* ---- Holland ---- */
  let hollandHtml = `<h3 class="rs-h">Holland Code <span class="rs-big">${holland || "—"}</span></h3>`;
  if (holland) {
    hollandHtml += `<p class="rs-desc">A three-letter interest signature, strongest first. ${holland.split("").map((c, i) => HOLLAND_TYPES[c] ? (i === 0 ? `<b>${HOLLAND_TYPES[c].name}</b>-primary` : i === 1 ? `<b>${HOLLAND_TYPES[c].name}</b>-secondary` : `<b>${HOLLAND_TYPES[c].name}</b>-tertiary`) : "").join(", ")}.</p>`;
  }
  hollandHtml += `<div class="rs-grid">`;
  for (const ch of holland) {
    const h = HOLLAND_TYPES[ch];
    if (h) hollandHtml += `<div class="rs-item"><b class="rs-letter">${ch}</b><div><span class="rs-name">${h.name} <em>— ${h.tag}</em></span><p>${h.desc}</p><p class="rs-careers"><b>Best fit:</b> ${h.careers}.</p></div></div>`;
  }
  hollandHtml += `</div>`;

  /* ---- Big Five ---- */
  const big5Summary = Object.entries(big5).map(([k, v]) => {
    const t = BIG5_TRAITS[k] || { name: k };
    const lvl = v.includes("High") ? "High" : v === "Medium" ? "Medium" : "Low";
    return `${lvl} ${t.name}`;
  }).join(" · ");
  const big5Html = `<h3 class="rs-h">Big Five <span class="rs-tag">OCEAN</span></h3>
    <p class="rs-desc"><b>Your lean:</b> ${big5Summary}.</p>
    <div class="rs-grid">` +
    Object.entries(big5).map(([k, v]) => {
      const t = BIG5_TRAITS[k] || { name: k, High: "", Medium: "", Low: "" };
      const key = v.includes("High") ? "High" : v === "Medium" ? "Medium" : "Low";
      const lvl = LEVEL_LABEL[key] || key;
      return `<div class="rs-item"><b class="rs-letter">${k}</b><div>
        <span class="rs-name">${t.name} <span class="rs-level ${lvl}">${v}</span></span>
        <p>${t[key] || t.Medium || ""}</p>
        ${t.note ? `<p class="rs-careers">${t.note}</p>` : ""}
      </div></div>`;
    }).join("") +
    `</div>`;

  return `<div class="rs-section">${mbtiHtml}</div>
    <div class="rs-section">${hollandHtml}</div>
    <div class="rs-section">${big5Html}</div>`;
}

function renderResultsPage(s) {
  const body = document.getElementById("resultsPageBody");
  if (!body) return;
  body.innerHTML = resultsPageBody(s || {});
  document.getElementById("resultsPage").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closeResultsPage() {
  document.getElementById("resultsPage").classList.add("hidden");
  document.body.style.overflow = "";
}

document.getElementById("closeResultsBtn").addEventListener("click", closeResultsPage);
document.getElementById("resultsPage").addEventListener("click", (e) => {
  if (e.target === e.currentTarget) closeResultsPage();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeResultsPage();
});
