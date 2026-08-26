"""Email sending via the Resend HTTP API + result-email HTML builder.

Requires RESEND_API_KEY in the environment. If unset (local dev), the email
is logged server-side and send_email returns False.

The framework reference data below mirrors frontend/results.js so the email
can render the full MBTI / Holland / Big Five breakdown server-side.
"""
import html
import json
import os
import urllib.error
import urllib.request

FROM_ADDR = os.environ.get("SMTP_FROM") or "no-reply@theanitalmidproject.com"
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
BASE_URL = os.environ.get("ANITALMID_BASE_URL", "https://theanitalmidproject.com").rstrip("/")


# ---- Framework reference data (mirrors frontend/results.js) ----

MBTI_DICHOTOMIES = {
    "E": ("Extraversion", "Energized by the outer world of people and activity. Thinks out loud, thrives in collaborative, fast-paced settings: meetings, presentations, networking."),
    "I": ("Introversion", "Energized by the inner world of ideas and reflection. Thinks before speaking, excels at deep analysis, writing, and solo work; needs recharge time after socializing."),
    "S": ("Sensing", "Focuses on concrete, tangible information: facts, experience, detail. Excels at hands-on, practical, detail-oriented work and trusts proven methods."),
    "N": ("Intuition", "Focuses on patterns, possibilities, and the big picture. Trusts insight and theory. Excels at strategy, innovation, and systems thinking; comfortable with ambiguity."),
    "T": ("Thinking", "Decides with logic, consistency, and objective analysis. Excels in analytical roles: engineering, systems, data, security. Values correctness over consensus."),
    "F": ("Feeling", "Decides with personal values and impact on people. Excels in people-facing roles: counseling, HR, teaching, advocacy. Values harmony and outcomes for others."),
    "J": ("Judging", "Prefers structure, planning, and closure. Excels in project management, operations, and compliance; thrives on deadlines and clear expectations."),
    "P": ("Perceiving", "Prefers flexibility, adaptability, and open options. Excels in creative work, research, and crisis response; thrives on autonomy and emergent priorities."),
}

MBTI_TYPES = {
    "ISTJ": ("The Logistician", "Practical, fact-minded, and dependable. Values order, rules, and thoroughness; the steady backbone of any organization.", "Operations, compliance, accounting, law enforcement"),
    "ISFJ": ("The Defender", "Warm, conscientious, and quietly devoted. Protects and supports others with tireless, behind-the-scenes diligence.", "Healthcare, education, administrative support"),
    "INFJ": ("The Advocate", "Insightful, idealistic, and quietly determined. Sees meaning and potential in people and ideas, driven by a sense of purpose.", "Counseling, writing, non-profit leadership"),
    "INTJ": ("The Architect", "Strategic, analytical, and fiercely independent. Sees the system behind the system and designs the most efficient path forward.", "Systems architecture, strategic planning, research, engineering"),
    "ISTP": ("The Virtuoso", "Bold, hands-on, and pragmatic. Masters tools and systems through direct experimentation rather than theory.", "Engineering, trades, emergency response, field technician"),
    "ISFP": ("The Adventurer", "Gentle, artistic, and fully present. Expresses inner experience through action, craft, and aesthetics.", "Arts, design, healthcare, skilled trades"),
    "INFP": ("The Mediator", "Idealistic, empathetic, and values-driven. Seeks authenticity and meaning in every pursuit.", "Writing, counseling, creative arts, academia"),
    "INTP": ("The Logician", "Analytical, curious, and independent-minded. Deconstructs ideas to uncover the underlying truth.", "Research, software development, philosophy, systems analysis"),
    "ESTP": ("The Entrepreneur", "Energetic, perceptive, and action-oriented. Lives at full throttle, thriving on risk, variety, and real-time problem solving.", "Sales, emergency management, athletics, business"),
    "ESFP": ("The Entertainer", "Spontaneous, sociable, and enthusiastic. Brings warmth and energy to every room and every task.", "Performance, hospitality, sales, event planning"),
    "ENFP": ("The Campaigner", "Enthusiastic, creative, and sociable. Sees possibilities everywhere and connects people to them.", "Marketing, journalism, entrepreneurship, teaching"),
    "ENTP": ("The Debater", "Quick, ingenious, and intellectually fearless. Challenges convention to build better ideas.", "Law, consulting, engineering, entrepreneurship"),
    "ESTJ": ("The Executive", "Organized, direct, and dependable. Runs things efficiently and fairly, with clear standards and follow-through.", "Management, law, military, operations"),
    "ESFJ": ("The Consul", "Warm, conscientious, and cooperative. Keeps communities and teams running smoothly and harmoniously.", "Healthcare, teaching, hospitality, administration"),
    "ENFJ": ("The Protagonist", "Charismatic, inspiring, and empathetic. Helps others grow and reach their full potential.", "Teaching, counseling, politics, non-profit"),
    "ENTJ": ("The Commander", "Bold, strategic, and decisive. Leads with vision and drives execution at scale.", "Executive leadership, law, consulting, military"),
}

HOLLAND_TYPES = {
    "R": ("Realistic", "The Doers", "Drawn to things, tools, machines, and physical systems. Values practicality and tangible results. Prefers concrete problems and hands-on work over abstract theory.", "Engineering, skilled trades, agriculture, law enforcement, field tech, construction"),
    "I": ("Investigative", "The Thinkers", "Drawn to understanding, analyzing, and solving problems through ideas. Values knowledge and precision. Prefers research, analysis, and complex problem-solving.", "Scientist, researcher, software developer, systems analyst, data analyst, physician"),
    "A": ("Artistic", "The Creators", "Drawn to creating, expressing, and innovating through unstructured media. Values creativity and originality. Prefers writing, design, and performance over routine.", "Writer, designer, musician, architect, UX designer, creative director"),
    "S": ("Social", "The Helpers", "Drawn to helping, teaching, counseling, and developing others. Values service and empathy. Prefers teaching, counseling, and caregiving over isolated or mechanical work.", "Teacher, counselor, social worker, nurse, HR, coach"),
    "E": ("Enterprising", "The Persuaders", "Drawn to leading, persuading, selling, and achieving organizational goals. Values success and influence. Prefers sales, management, and entrepreneurship.", "Sales manager, executive, entrepreneur, lawyer, politician"),
    "C": ("Conventional", "The Organizers", "Drawn to organizing, managing data, and maintaining systems. Values accuracy, order, and efficiency. Prefers structured processes and record-keeping.", "Accountant, administrative assistant, compliance officer, auditor, bookkeeper"),
}

BIG5_TRAITS = {
    "O": {
        "name": "Openness",
        "High": "Curious, imaginative, creative, and abstract-thinking. Drawn to novelty, art, and ideas. Thrives with autonomy and intellectual challenge: creative, research, entrepreneurial, and strategic roles.",
        "Medium": "Balanced between the novel and the familiar: comfortable with a mix of routine and exploration, concrete and conceptual work.",
        "Low": "Practical, conventional, and grounded. Prefers routine and familiarity, trusts concrete facts. Thrives in structured, hands-on roles with clear expectations and proven methods.",
    },
    "C": {
        "name": "Conscientiousness",
        "High": "Organized, disciplined, methodical, and achievement-oriented. Plans ahead and follows through: the single best personality predictor of job performance across all occupations.",
        "Medium": "Reliable and structured where it counts, while staying comfortable with a degree of flexibility.",
        "Low": "Flexible, spontaneous, and adaptable. Prefers improvisation over rigid planning. Thrives in creative, crisis-response, and entrepreneurial roles that reward adaptability.",
    },
    "E": {
        "name": "Extraversion",
        "High": "Outgoing, energetic, talkative, and assertive. Gains energy from social interaction. Thrives in sales, management, teaching, and public-facing roles.",
        "Medium": "Comfortable in both social and solitary settings: adaptable to collaborative or independent work.",
        "Low": "Reserved, reflective, and prefers solitude. Gains energy from quiet and alone time. Thrives in research, analysis, writing, and independent work.",
    },
    "A": {
        "name": "Agreeableness",
        "High": "Cooperative, compassionate, trusting, and conflict-avoidant. Values harmony and helping others. Thrives in healthcare, counseling, customer service, and social work.",
        "Medium": "Cooperates when aligned, but will hold the line when the situation demands it.",
        "Low": "Competitive, skeptical, direct, and willing to challenge. Values truth over harmony. Thrives in law, security, auditing, and competitive business.",
    },
    "N": {
        "name": "Emotional Stability",
        "High": "Calm, resilient, confident, and emotionally steady. Handles pressure well and recovers quickly: suited to high-pressure roles like emergency response, leadership, trading, and critical operations.",
        "Medium": "Steady most of the time, with occasional stress responses under sustained pressure.",
        "Low": "More sensitive to stress and change. Performs best in predictable, supportive, lower-pressure environments.",
        "note": "Measured as emotional stability (the inverse of Neuroticism): higher stability = lower neuroticism.",
    },
}


def send_email(to_email: str, subject: str, html: str, text: str = "") -> bool:
    """Send an HTML email via Resend. Returns True on success."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print(f"[emailer] no RESEND_API_KEY — would email {to_email}: {subject}")
        return False

    payload = {
        "from": f"Anitalmid <{FROM_ADDR}>",
        "to": [to_email],
        "subject": subject,
        "html": html,
    }
    if text:
        payload["text"] = text

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": BROWSER_UA,
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[emailer] Resend API {e.code} {e.reason}: {body[:400]}")
        return False
    except Exception as e:
        print(f"[emailer] Resend API failed for {to_email}: {e}")
        return False


def _esc(s):
    return html.escape(str(s), quote=False) if s is not None else ""


def _card(inner):
    return f'<div style="background:#131a29;border:1px solid #2a3450;border-radius:10px;padding:14px 16px;margin:0 0 12px">{inner}</div>'


def _section(title, body):
    return (
        f'<div style="margin:0 0 28px">'
        f'<div style="font-size:18px;font-weight:700;color:#2dd4bf;margin:0 0 12px">{title}</div>'
        f'{body}'
        f'</div>'
    )


def _mbti_section(signals):
    t = (signals.get("mbti") or {}).get("inferred_type") or ""
    disp = t.replace("X", "·") or "—"
    info = MBTI_TYPES.get(t)

    head = f"Myers-Briggs &nbsp;<span style=\"color:#e9eef7\">{_esc(disp)}</span>"
    if info:
        head += f' &nbsp;<span style="color:#93a0b8;font-weight:400;font-size:14px">{_esc(info[0])}</span>'

    body = ""
    if info:
        body += f'<p style="color:#cdd4e0;font-size:14px;margin:0 0 8px;line-height:1.6">{_esc(info[1])}</p>'
        body += f'<p style="color:#93a0b8;font-size:13px;margin:0 0 14px"><b>Best-fit career clusters:</b> {_esc(info[2])}.</p>'
    elif t:
        body += '<p style="color:#93a0b8;font-size:13px;margin:0 0 14px">Some dichotomies were undetermined, so this is not a single classic type; the letters below still describe your strongest preferences.</p>'

    for ch in t:
        if ch == "X":
            continue
        d = MBTI_DICHOTOMIES.get(ch)
        if not d:
            continue
        body += _card(
            f'<b style="color:#38bdf8;font-size:15px">{_esc(ch)} &middot; {_esc(d[0])}</b>'
            f'<p style="color:#cdd4e0;font-size:14px;margin:6px 0 0;line-height:1.6">{_esc(d[1])}</p>'
        )
    return _section(head, body)


def _holland_section(signals):
    code = (signals.get("holland") or {}).get("inferred_code") or ""
    labels = ["primary", "secondary", "tertiary"]
    body = ""
    if code:
        parts = []
        for i, ch in enumerate(code):
            h = HOLLAND_TYPES.get(ch)
            if h:
                parts.append(f'<b>{_esc(h[0])}</b>-{labels[i]}')
        if parts:
            body += f'<p style="color:#cdd4e0;font-size:14px;margin:0 0 14px">A three-letter interest signature, strongest first: {", ".join(parts)}.</p>'

    for ch in code:
        h = HOLLAND_TYPES.get(ch)
        if not h:
            continue
        body += _card(
            f'<b style="color:#38bdf8;font-size:15px">{_esc(ch)} &middot; {_esc(h[0])} &nbsp;<span style="color:#93a0b8;font-weight:400">{_esc(h[1])}</span></b>'
            f'<p style="color:#cdd4e0;font-size:14px;margin:6px 0;line-height:1.6">{_esc(h[2])}</p>'
            f'<p style="color:#93a0b8;font-size:13px;margin:0"><b>Best fit:</b> {_esc(h[3])}.</p>'
        )
    return _section(f'Holland Code &nbsp;<span style="color:#e9eef7">{_esc(code) or "—"}</span>', body)


def _big5_section(signals):
    profile = (signals.get("big_five") or {}).get("inferred_profile") or {}
    body = ""
    for k, v in profile.items():
        t = BIG5_TRAITS.get(k) or {"name": k, "High": "", "Medium": "", "Low": ""}
        key = "High" if "High" in str(v) else ("Medium" if v == "Medium" else "Low")
        level = str(v)
        note = f'<p style="color:#93a0b8;font-size:13px;margin:8px 0 0">{_esc(t.get("note"))}</p>' if t.get("note") else ""
        body += _card(
            f'<b style="color:#38bdf8;font-size:15px">{_esc(k)} &middot; {_esc(t["name"])} '
            f'<span style="background:#1a2234;border:1px solid #2a3450;color:#e9eef7;border-radius:999px;padding:2px 10px;font-size:12px">{_esc(level)}</span></b>'
            f'<p style="color:#cdd4e0;font-size:14px;margin:6px 0 0;line-height:1.6">{_esc(t.get(key) or t.get("Medium") or "")}</p>'
            f'{note}'
        )
    return _section("Big Five &nbsp;<span style=\"color:#93a0b8;font-size:14px;font-weight:400\">OCEAN</span>", body)


def build_metrics_email(metrics: dict) -> str:
    """Build the HTML for the admin metrics digest."""
    total_users = metrics.get("total_users", 0)
    total_analyses = metrics.get("total_analyses", 0)
    analyses_24h = metrics.get("analyses_24h", 0)
    new_users = metrics.get("new_users_24h", [])

    if new_users:
        user_rows = "".join(
            '<tr><td style="padding:10px 14px;border-bottom:1px solid #2a3450">'
            f'<div style="font-size:14px;font-weight:700;color:#e9eef7">{_esc(u["username"])}</div>'
            f'<div style="font-size:12px;color:#93a0b8">{_esc(u["email"])}</div>'
            "</td></tr>"
            for u in new_users
        )
    else:
        user_rows = (
            '<tr><td style="padding:10px 14px;color:#93a0b8;font-size:14px">'
            "No new registrations in the last 24 hours.</td></tr>"
        )

    per_day = metrics.get("analyses_per_day", [])
    day_rows = "".join(
        '<tr><td style="padding:8px 14px;border-bottom:1px solid #1a2234;font-size:13px;color:#cdd4e0">'
        f'<b style="color:#e9eef7">{_esc(d["date"])}</b></td>'
        f'<td style="padding:8px 14px;border-bottom:1px solid #1a2234;font-size:13px;color:#2dd4bf;text-align:right">{d["count"]}</td>'
        "</tr>"
        for d in reversed(per_day)
    )

    stat = (
        '<div style="display:flex;gap:12px;margin:0 0 24px">'
        f'<div style="flex:1;background:#131a29;border:1px solid #2a3450;border-radius:10px;padding:16px;text-align:center">'
        f'<div style="font-size:28px;font-weight:800;color:#2dd4bf">{total_users}</div>'
        f'<div style="font-size:12px;color:#93a0b8;margin-top:2px">Total users</div></div>'
        f'<div style="flex:1;background:#131a29;border:1px solid #2a3450;border-radius:10px;padding:16px;text-align:center">'
        f'<div style="font-size:28px;font-weight:800;color:#38bdf8">{total_analyses}</div>'
        f'<div style="font-size:12px;color:#93a0b8;margin-top:2px">Total analyses</div></div>'
        f'<div style="flex:1;background:#131a29;border:1px solid #2a3450;border-radius:10px;padding:16px;text-align:center">'
        f'<div style="font-size:28px;font-weight:800;color:#4ade80">{analyses_24h}</div>'
        f'<div style="font-size:12px;color:#93a0b8;margin-top:2px">Analyses (24h)</div></div>'
        "</div>"
    )

    return f"""<!DOCTYPE html><html><body style="margin:0;padding:0;background:#0b0f1a;font-family:Arial,Helvetica,sans-serif">
<div style="max-width:600px;margin:0 auto;padding:32px 20px">
  <h1 style="color:#e9eef7;font-size:24px;margin:0 0 4px">Anitalmid — daily metrics</h1>
  <p style="color:#93a0b8;font-size:14px;margin:0 0 24px">Automated digest from theanitalmidproject.com</p>

  {stat}

  <div style="font-size:18px;font-weight:700;color:#2dd4bf;margin:0 0 12px">New registrations (24h)</div>
  <table style="width:100%;border-collapse:collapse;background:#131a29;border:1px solid #2a3450;border-radius:12px;overflow:hidden;margin:0 0 28px">
    {user_rows}
  </table>

  <div style="font-size:18px;font-weight:700;color:#2dd4bf;margin:0 0 12px">Analyses — last 7 days</div>
  <table style="width:100%;border-collapse:collapse;background:#131a29;border:1px solid #2a3450;border-radius:12px;overflow:hidden">
    {day_rows}
  </table>

  <p style="color:#93a0b8;font-size:13px;margin:24px 0 0">Sent by the Anitalmid admin digest.</p>
</div>
</body></html>"""


def _pivot_section(pivot: dict) -> str:
    """Render the Career Pivot Journey section (the matches currently in view)."""
    matches = pivot.get("matches") or []
    education = pivot.get("education") or []
    hobbies = pivot.get("hobbies") or []
    summary_parts = []
    if education:
        summary_parts.append("degrees: " + ", ".join(_esc(e) for e in education))
    if hobbies:
        summary_parts.append("hobbies: " + ", ".join(_esc(h) for h in hobbies))
    summary = "; ".join(summary_parts)

    rows = ""
    for m in matches:
        title = _esc(m.get("title") or "")
        category = _esc(m.get("category") or "")
        holland = _esc(m.get("holland_code") or "")
        pivot_cost = _esc(m.get("pivot_cost") or "")
        meta = " &middot; ".join(x for x in (category, holland, f"pivot: {pivot_cost}") if x)
        rows += (
            '<tr><td style="padding:12px 16px;border-bottom:1px solid #2a3450">'
            f'<div style="font-size:15px;font-weight:700;color:#e9eef7">{title}</div>'
            + (f'<div style="font-size:12px;color:#93a0b8;margin-top:3px">{meta}</div>' if meta else "")
            + "</td></tr>"
        )

    body = ""
    if summary:
        body += f'<p style="color:#cdd4e0;font-size:14px;margin:0 0 12px;line-height:1.6">{summary}</p>'
    if rows:
        body += (
            '<table style="width:100%;border-collapse:collapse;background:#131a29;'
            'border:1px solid #2a3450;border-radius:12px;overflow:hidden">' + rows + "</table>"
        )
    else:
        body += '<p style="color:#93a0b8;font-size:14px">No pivot matches were generated.</p>'
    return _section("Career Pivot Journey", body)


def _job_section(ja: dict) -> str:
    """Render the job-match section (overall alignment + keyword coverage)."""
    job = ja.get("job") or {}
    title = _esc(job.get("title") or "Job posting")
    company = _esc(job.get("company") or "")
    heading = title + (f" @ {company}" if company else "")
    kw = ja.get("keyword_alignment") or {}
    psych = ja.get("psychometric_alignment") or {}
    overall = psych.get("overall")
    kw_score = kw.get("score")

    body = f'<p style="color:#cdd4e0;font-size:15px;font-weight:700;margin:0 0 10px">{heading}</p>'
    if overall is not None:
        body += f'<p style="color:#cdd4e0;font-size:14px;margin:0 0 6px"><b>Overall psychometric alignment:</b> {int(round(float(overall)))}%</p>'
    if kw_score is not None:
        body += f'<p style="color:#cdd4e0;font-size:14px;margin:0 0 6px"><b>Keyword coverage:</b> {int(round(float(kw_score)))}%</p>'
    return _section("Job match", body)


def build_results_email(username: str, signals: dict, top_matches: list, pivot: dict | None = None, job_alignment: dict | None = None) -> str:
    """Build the HTML for the individualized-results email, scaling with completed sections."""
    rows = ""
    for m in (top_matches or [])[:6]:
        title = _esc(m.get("title") or "")
        score = int(round(float(m.get("composite_score") or 0)))
        desc = _esc(m.get("description") or "")
        salary = _esc(m.get("salary_range") or "")
        fits = m.get("salary_fits")
        if fits is True:
            fits_html = '<div style="font-size:12px;color:#4ade80;margin-top:4px">&#10003; within your range</div>'
        elif fits is False:
            fits_html = '<div style="font-size:12px;color:#93a0b8;margin-top:4px">outside your range</div>'
        else:
            fits_html = ""
        rows += (
            '<tr><td style="padding:14px 16px;border-bottom:1px solid #2a3450">'
            f'<div style="font-size:16px;font-weight:700;color:#e9eef7">{title} '
            f'<span style="color:#2dd4bf">({score}%)</span></div>'
            + (f'<div style="font-size:14px;color:#93a0b8;margin-top:3px">{desc}</div>' if desc else "")
            + (f'<div style="font-size:12px;color:#38bdf8;margin-top:4px">{salary}</div>' if salary else "")
            + fits_html
            + "</td></tr>"
        )

    pivot_html = _pivot_section(pivot) if pivot else ""
    job_html = _job_section(job_alignment) if (job_alignment and not job_alignment.get("error")) else ""

    return f"""<!DOCTYPE html><html><body style="margin:0;padding:0;background:#0b0f1a;font-family:Arial,Helvetica,sans-serif">
<div style="max-width:600px;margin:0 auto;padding:32px 20px">
  <h1 style="color:#e9eef7;font-size:24px;margin:0 0 4px">Your Anitalmid career map</h1>
  <p style="color:#93a0b8;font-size:14px;margin:0 0 24px">Hi {_esc(username)}, here's the individualized breakdown generated from your resume.</p>

  {_mbti_section(signals)}
  {_holland_section(signals)}
  {_big5_section(signals)}

  <div style="font-size:18px;font-weight:700;color:#2dd4bf;margin:0 0 12px">Top career matches</div>
  <table style="width:100%;border-collapse:collapse;background:#131a29;border:1px solid #2a3450;border-radius:12px;overflow:hidden">
    {rows}
  </table>

  {pivot_html}
  {job_html}

  <p style="color:#93a0b8;font-size:14px;margin:24px 0 0">
    <a href="{BASE_URL}" style="color:#2dd4bf;text-decoration:none;font-weight:700">Return to The Anitalmid Project &rarr;</a>
  </p>
</div>
</body></html>"""
