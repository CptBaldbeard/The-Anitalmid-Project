"""Career map generator — builds a JSON graph for the frontend to render.

Graph shape:
    profile -> signal (MBTI / Holland / Big Five)
    signal  -> role   (weighted by that role's framework contribution)
    role    -> role   (progression edges, e.g. Systems Admin -> Cloud Admin)
"""
from typing import Dict, List

# Known progression edges between role titles (Systems Admin -> Cloud Admin, etc.)
PROGRESSION_EDGES = [
    ("Systems Administrator", "Cloud Administrator"),
    ("Systems Administrator", "Security Analyst / SOC Analyst"),
    ("Cloud Administrator", "Systems Architect"),
    ("Security Analyst / SOC Analyst", "GRC Analyst / Compliance Engineer"),
    ("Data Analyst / Security Analytics", "Security Analyst / SOC Analyst"),
]


def _slug(s: str) -> str:
    return "".join(c for c in s if c.isalnum()).lower()


def build_career_map(ranking: list, signals: dict, expanded: list | None = None) -> Dict:
    nodes: List[Dict] = []
    edges: List[Dict] = []

    # Profile node
    nodes.append({"id": "profile", "label": "You", "type": "profile", "data": {}})

    # Signal nodes
    mbti_type = signals["mbti"].get("inferred_type", "N/A")
    holland_code = signals["holland"].get("inferred_code", "N/A")
    big5 = signals["big_five"].get("inferred_profile", {})

    signal_nodes = [
        ("sig-mbti", f"MBTI: {mbti_type}", "signal"),
        ("sig-holland", f"Holland: {holland_code}", "signal"),
        ("sig-big5", "Big Five", "signal"),
    ]
    for sid, label, stype in signal_nodes:
        nodes.append({"id": sid, "label": label, "type": stype, "data": {}})

    for sid, _, _ in signal_nodes:
        edges.append({"source": "profile", "target": sid, "label": "infers", "weight": 1.0})

    # Role nodes (top 6)
    top = ranking[:6]
    role_ids = {}
    for role in top:
        rid = "role-" + _slug(role["title"])
        role_ids[role["title"]] = rid
        nodes.append(
            {
                "id": rid,
                "label": role["title"],
                "type": "role",
                "data": {
                    "score": role["composite_score"],
                    "validation": role["validation"],
                    "category": role["category"],
                    "pivot_cost": role["pivot_cost"],
                    "salary_range": role["salary_range"],
                },
            }
        )

    # signal -> role edges (weighted by composite score, capped)
    max_score = max((r["composite_score"] for r in top), default=1.0) or 1.0
    for role in top:
        rid = role_ids[role["title"]]
        w = round(role["composite_score"] / max_score, 2)
        # Attach to the most relevant signal (Holland is the primary matching key)
        edges.append({"source": "sig-holland", "target": rid, "label": "", "weight": w})
        edges.append({"source": "sig-mbti", "target": rid, "label": "", "weight": round(w * 0.6, 2)})

    # role -> role progression edges (only if both roles are in the top 6)
    for src, dst in PROGRESSION_EDGES:
        if src in role_ids and dst in role_ids:
            edges.append({"source": role_ids[src], "target": role_ids[dst], "label": "→", "weight": 0.8})

    # Expanded (web-discovered) roles — attach to the Holland signal node
    if expanded:
        for e in expanded[:5]:
            eid = "exp-" + _slug(e["title"])
            nodes.append(
                {
                    "id": eid,
                    "label": e["title"],
                    "type": "expanded",
                    "data": {
                        "category": e.get("category", ""),
                        "salary_range": e.get("salary_range") or "",
                        "source_url": e.get("source_url", ""),
                        "holland_code": e.get("holland_code", ""),
                    },
                }
            )
            edges.append({"source": "sig-holland", "target": eid, "label": "expands", "weight": 0.6})

    return {"nodes": nodes, "edges": edges}
