"""Anitalmid signal detection — enriched framework detectors (MBTI, Holland, Big Five).

Each detector scans resume text against a broad, field-spanning lexicon using
word-boundary prefix matching (a stem like "collaborat" catches collaborate /
collaboration / collaborative). Keyword lists deliberately cover vocabulary from
healthcare, trades, education, creative, science, legal, public safety, finance,
and technology so non-IT resumes produce real signal instead of defaulting to a
guess.
"""
import re


def _scan(text_lower: str, keywords) -> int:
    """Count keyword hits via word-boundary prefix matching."""
    hits = 0
    for kw in keywords:
        if re.search(rf"\b{re.escape(kw)}", text_lower):
            hits += 1
    return hits


def detect_mbti_signals(text: str) -> dict:
    """Detect MBTI (I/E, N/S, T/F, J/P) signals across a broad lexicon."""
    text_lower = text.lower()
    signals = {"I": 0, "E": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    i_keywords = [
        "independen", "autonom", "self-direct", "individual contributor",
        "deep work", "solitar", "solo", "remote", "focused", "concentrat",
        "research", "analys", "writ", "document", "quiet", "introspect",
        "reflect", "behind the scenes", "lab", "library", "archiv",
        "coding", "programm", "scholar", "contemplat", "stud", "data entry",
    ]
    signals["I"] += _scan(text_lower, i_keywords)

    e_keywords = [
        "team", "collaborat", "present", "meeting", "leadership", "lead",
        "client-facing", "stakeholder", "train", "workshop", "facilitat",
        "sales", "network", "public speak", "outreach", "community",
        "teaching", "coach", "group", "social", "customer", "hospitalit",
        "business development", "field", "persuad", "energetic", "engag",
        "campaign", "fundrais", "presentation", "interfac",
    ]
    signals["E"] += _scan(text_lower, e_keywords)

    n_keywords = [
        "strateg", "innov", "design", "architect", "future", "concept",
        "pattern", "abstract", "vision", "creativ", "big picture", "theor",
        "imagin", "novel", "possibilit", "forward", "ideat", "brainstorm",
        "forecast", "trend", "hypothes", "explor", "conceptual", "philosoph",
        "insight", "scenario", "transform",
    ]
    signals["N"] += _scan(text_lower, n_keywords)

    s_keywords = [
        "detail", "hands-on", "practic", "concret", "procedure", "process",
        "implement", "execut", "maintenance", "routine", "realist", "specific",
        "tangible", "step-by-step", "precis", "accur", "measur", "inspect",
        "assembl", "physical", "equipment", "current", "established",
        "experienc", "observ", "applied", "operat", "install", "repair",
        "build", "fabricat", "technic",
    ]
    signals["S"] += _scan(text_lower, s_keywords)

    t_keywords = [
        "analysis", "analys", "logical", "logic", "system", "technical",
        "data", "objective", "investigat", "troubleshoot", "engineer",
        "security", "rational", "critical think", "problem-solv", "quantitativ",
        "metric", "evaluat", "decision", "efficien", "diagnos", "repair",
        "mechanic", "financial", "comput", "programm", "calculat", "reason",
        "skeptic", "technical", "systemat",
    ]
    signals["T"] += _scan(text_lower, t_keywords)

    f_keywords = [
        "empath", "relationship", "customer", "client", "support",
        "team harmony", "collaborat", "people", "help", "service",
        "compassion", "care", "patient", "counsel", "advocac", "understand",
        "interperson", "emotion", "nurtur", "community", "humanitar", "teach",
        "mentor", "wellbeing", "wellness", "assist", "guid", "listen",
        "warm", "sensitive",
    ]
    signals["F"] += _scan(text_lower, f_keywords)

    j_keywords = [
        "organiz", "plann", "plan", "deadline", "project management",
        "structur", "systematic", "methodical", "schedul", "complianc",
        "disciplin", "order", "checklist", "timeline", "goal", "complet",
        "control", "regulat", "polic", "standard", "procedure", "punctual",
        "prepar", "decisive", "firm", "scheduled", "coordina",
    ]
    signals["J"] += _scan(text_lower, j_keywords)

    p_keywords = [
        "flexib", "adaptab", "spontan", "explor", "agile", "iterativ",
        "open-ended", "emergent", "improvis", "adapt", "responsiv",
        "multitask", "variety", "fast-paced", "dynamic", "chang",
        "opportunis", "creative freedom", "on the fly", "juggl", "versatil",
        "curious", "improvis", "open-minded",
    ]
    signals["P"] += _scan(text_lower, p_keywords)

    # Dominant dichotomy per pair ("X" when there's no clear signal)
    def _pick(a_key, b_key):
        if signals[a_key] > signals[b_key]:
            return a_key
        if signals[b_key] > signals[a_key]:
            return b_key
        return "X"

    result = {}
    result["I_vs_E"] = _pick("I", "E")
    result["N_vs_S"] = _pick("N", "S")
    result["T_vs_F"] = _pick("T", "F")
    result["J_vs_P"] = _pick("J", "P")
    result["inferred_type"] = (
        result["I_vs_E"] + result["N_vs_S"] +
        result["T_vs_F"] + result["J_vs_P"]
    )
    result["signal_strength"] = sum(signals.values())
    result["raw_signals"] = signals
    return result


def detect_holland_signals(text: str) -> dict:
    """Detect Holland (RIASEC) signals across a broad lexicon."""
    text_lower = text.lower()
    signals = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

    r_keywords = [
        "build", "repair", "install", "configur", "deploy", "operat",
        "hardware", "equipment", "tool", "hands-on", "technic", "system",
        "network", "server", "infrastructure", "machine", "mechanic",
        "electr", "construction", "plumb", "weld", "carpent", "automot",
        "hvac", "manufactur", "assembl", "maintenance", "physical", "outdoor",
        "driv", "pilot", "farm", "landscap", "warehous", "fabricat",
        "machin", "vehicl", "circuit", "appliance",
    ]
    signals["R"] += _scan(text_lower, r_keywords)

    i_keywords = [
        "research", "analys", "analysis", "investigat", "troubleshoot",
        "diagnos", "problem-solv", "scientif", "data", "evaluat", "assess",
        "security", "test", "audit", "examin", "stud", "experiment",
        "laborator", "hypothes", "theor", "math", "statist", "model", "cod",
        "biolog", "chemistr", "physic", "engineer", "forens", "clinical",
        "scholar", "observ", "analyt", "algorithm", "genetic",
    ]
    signals["I"] += _scan(text_lower, i_keywords)

    a_keywords = [
        "design", "creat", "write", "writing", "visual", "content",
        "documentation", "graphic", "media", "video", "music", "artistic",
        "innov", "imagin", "illustrat", "photograph", "film", "animat",
        "perform", "literar", "editorial", "storytell", "aesthetic", "fashion",
        "culinar", "compos", "choreograph", "craft", "draw", "paint", "poet",
        "novel", "brand", "logo",
    ]
    signals["A"] += _scan(text_lower, a_keywords)

    s_keywords = [
        "teach", "train", "instruct", "mentor", "coach", "help", "support",
        "customer", "client", "patient", "service", "care", "assist", "guid",
        "counsel", "therap", "nurs", "healthcar", "social work", "educat",
        "community", "advocac", "outreach", "volunteer", "hospitalit",
        "childcare", "eldercare", "advis", "listen", "empathetic", "wellness",
        "rehabilit",
    ]
    signals["S"] += _scan(text_lower, s_keywords)

    e_keywords = [
        "lead", "manag", "sales", "persuad", "negotiat", "business",
        "entrepreneur", "revenue", "growth", "market", "influenc", "execut",
        "director", "strateg", "initiativ", "startup", "fundrais",
        "public relation", "campaign", "promot", "business development",
        "politic", "lobby", "leadership", "authorit", "ambition", "pitch",
        "proposal", "negotiat", "account exec", "close deal",
    ]
    signals["E"] += _scan(text_lower, e_keywords)

    c_keywords = [
        "organiz", "administr", "record", "data entry", "schedul", "process",
        "procedure", "complianc", "polic", "standard", "document", "fil",
        "bookkeep", "account", "audit", "spreadsheet", "database", "cleric",
        "office", "report", "regulat", "tax", "payroll", "inventor",
        "quality control", "record", "transact", "budget", "reconcil",
        "catalog", "coordina", "logistic",
    ]
    signals["C"] += _scan(text_lower, c_keywords)

    sorted_types = sorted(signals.items(), key=lambda x: x[1], reverse=True)
    inferred_code = "".join(t[0] for t in sorted_types[:3])

    return {
        "inferred_code": inferred_code,
        "signal_strength": sum(signals.values()),
        "raw_signals": signals,
        "primary": sorted_types[0][0],
        "secondary": sorted_types[1][0] if len(sorted_types) > 1 else "",
        "tertiary": sorted_types[2][0] if len(sorted_types) > 2 else "",
    }


def detect_big_five_signals(text: str) -> dict:
    """Detect Big Five (OCEAN) trait signals across a broad lexicon."""
    text_lower = text.lower()
    signals = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}

    o_keywords = [
        "creativ", "innov", "curious", "design", "research", "learn",
        "new technolog", "explor", "abstract", "conceptual", "intellectual",
        "artistic", "cultural", "imagin", "novel", "philosoph", "theor",
        "diverse", "unconvention", "experiment", "forward", "literar",
        "travel", "multilingual", "aesthetic", "visionar", "insight",
        "invent", "idea",
    ]
    signals["O"] += _scan(text_lower, o_keywords)

    c_keywords = [
        "organiz", "detail", "thorough", "methodic", "systemat", "plan",
        "schedul", "deadlin", "reliab", "accur", "qualit", "standard",
        "procedure", "complianc", "responsib", "disciplin", "diligent",
        "punctual", "prepar", "careful", "meticulous", "structur", "goal",
        "follow-through", "dependab", "accountab", "consisten", "order",
        "document", "deliver",
    ]
    signals["C"] += _scan(text_lower, c_keywords)

    e_keywords = [
        "team", "collaborat", "present", "lead", "meeting", "network",
        "social", "outgoing", "energetic", "communicat", "interperson",
        "public speak", "stakeholder", "client", "talkat", "assertiv",
        "sociab", "gregarious", "enthusiast", "charismat", "sales", "facilitat",
        "public-facing", "group", "engag", "outreach", "connect",
    ]
    signals["E"] += _scan(text_lower, e_keywords)

    a_keywords = [
        "cooperat", "helpful", "support", "team player", "empathetic",
        "patient", "trust", "kind", "generous", "collaborat", "service",
        "customer", "client", "assist", "compassion", "caring", "diplomat",
        "tactful", "agreeab", "nurtur", "supportiv", "altruist", "courteous",
        "harmoni", "conflict", "respect", "friendly", "teamwork",
    ]
    signals["A"] += _scan(text_lower, a_keywords)

    # Neuroticism is measured inversely via emotional-stability signals
    n_keywords = [
        "calm", "resilien", "stabl", "compos", "pressure", "stress", "crisis",
        "emergenc", "critical", "urgent", "steady", "unflappab", "level-head",
        "pois", "adaptab", "stress management", "crisis management",
        "high-pressure", "under pressure", "composed", "grace under",
    ]
    signals["N"] += _scan(text_lower, n_keywords)

    def _level(count, high, mid):
        return "High" if count > high else "Medium" if count > mid else "Low"

    return {
        "raw_signals": signals,
        "signal_strength": sum(signals.values()),
        "inferred_profile": {
            "O": _level(signals["O"], 8, 3),
            "C": _level(signals["C"], 8, 3),
            "E": _level(signals["E"], 8, 3),
            "A": _level(signals["A"], 8, 3),
            "N": "High (Stable)" if signals["N"] > 4 else
                 "Medium" if signals["N"] > 1 else "Low",
        },
    }
