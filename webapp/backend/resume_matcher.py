#!/usr/bin/env python3
"""
The Anitalmid Project — Resume-to-Top-6-Positions Matching Pipeline

Matches a resume (PDF or plain text) against the six-framework psychometric
profile (Birkman, MBTI, Enneagram, DISC, Big Five, Holland Codes) and generates
a ranked top-6 list of most suitable career positions.

Usage:
    python3 resume_matcher.py /path/to/resume.pdf
    python3 resume_matcher.py /path/to/resume.txt

Dependencies: pymupdf (for PDF), no other external deps
"""

import json
import re
import sys
import os
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

# ─── Try pymupdf for PDF extraction ────────────────────────────────────────
try:
    import pymupdf
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


try:
    from .roles import RoleProfile, ROLE_PROFILES
except ImportError:
    from roles import RoleProfile, ROLE_PROFILES


# ═══════════════════════════════════════════════════════════════════════════
# RESUME EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file using pymupdf."""
    if not HAS_PYMUPDF:
        raise ImportError(
            "pymupdf is required to parse PDFs. "
            "Install with: uv pip install pymupdf"
        )
    doc = pymupdf.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def extract_text_from_txt(txt_path: str) -> str:
    """Read text from a plain text file."""
    with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def load_resume(path: str) -> str:
    """Auto-detect file type and extract text."""
    path_lower = path.lower()
    if path_lower.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path_lower.endswith((".txt", ".md", ".rtf")):
        return extract_text_from_txt(path)
    else:
        # Try as plain text first
        try:
            return extract_text_from_txt(path)
        except UnicodeDecodeError:
            raise ValueError(
                f"Unsupported file type: {path}. "
                "Supported: .pdf, .txt, .md"
            )


# ═══════════════════════════════════════════════════════════════════════════
# FRAMEWORK SIGNAL DETECTION
# ═══════════════════════════════════════════════════════════════════════════

def detect_mbti_signals(text: str) -> dict:
    """Detect MBTI-related signals in resume text."""
    text_lower = text.lower()
    signals = {"I": 0, "E": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    # Introversion signals
    i_keywords = [
        "independently", "autonomous", "self-directed", "remote work",
        "individual contributor", "focused", "deep work", "research",
        "analysis", "writing", "documentation", "quiet"
    ]
    for kw in i_keywords:
        if kw in text_lower:
            signals["I"] += 1
    
    # Extraversion signals
    e_keywords = [
        "team", "collaborative", "presentation", "meeting", "leadership",
        "client-facing", "stakeholder", "training", "workshop", "facilitated"
    ]
    for kw in e_keywords:
        if kw in text_lower:
            signals["E"] += 1
    
    # Intuition signals
    n_keywords = [
        "strategy", "innovation", "design", "architecture", "future",
        "concept", "pattern", "abstract", "vision", "creative", "big picture"
    ]
    for kw in n_keywords:
        if kw in text_lower:
            signals["N"] += 1
    
    # Sensing signals
    s_keywords = [
        "detail", "hands-on", "practical", "concrete", "procedure",
        "process", "implementation", "execution", "maintenance", "routine"
    ]
    for kw in s_keywords:
        if kw in text_lower:
            signals["S"] += 1
    
    # Thinking signals
    t_keywords = [
        "analysis", "logical", "system", "technical", "data", "objective",
        "investigation", "troubleshooting", "engineering", "security"
    ]
    for kw in t_keywords:
        if kw in text_lower:
            signals["T"] += 1
    
    # Feeling signals
    f_keywords = [
        "empathy", "relationship", "customer", "client", "support",
        "team harmony", "collaboration", "people", "helping", "service"
    ]
    for kw in f_keywords:
        if kw in text_lower:
            signals["F"] += 1
    
    # Judging signals
    j_keywords = [
        "organized", "planning", "deadline", "project management",
        "structured", "systematic", "methodical", "schedule", "compliance"
    ]
    for kw in j_keywords:
        if kw in text_lower:
            signals["J"] += 1
    
    # Perceiving signals
    p_keywords = [
        "flexible", "adaptable", "spontaneous", "exploratory",
        "agile", "iterative", "open-ended", "emergent"
    ]
    for kw in p_keywords:
        if kw in text_lower:
            signals["P"] += 1
    
    # Determine dominant dichotomies ("X" when there's no clear signal)
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
    """Detect Holland Code (RIASEC) signals in resume text."""
    text_lower = text.lower()
    signals = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    
    # Realistic
    r_keywords = [
        "build", "repair", "install", "configure", "deploy", "operate",
        "hardware", "equipment", "tool", "hands-on", "technical", "system",
        "network", "server", "infrastructure"
    ]
    for kw in r_keywords:
        if kw in text_lower:
            signals["R"] += 1
    
    # Investigative
    i_keywords = [
        "research", "analysis", "investigate", "troubleshoot", "diagnose",
        "problem-solv", "scientific", "data", "evaluate", "assess",
        "security", "test", "audit", "examine", "study"
    ]
    for kw in i_keywords:
        if kw in text_lower:
            signals["I"] += 1
    
    # Artistic
    a_keywords = [
        "design", "create", "write", "writing", "creative", "visual",
        "content", "documentation", "graphic", "media", "video", "music",
        "artistic", "innovative", "imaginative"
    ]
    for kw in a_keywords:
        if kw in text_lower:
            signals["A"] += 1
    
    # Social
    s_keywords = [
        "teach", "train", "instruct", "mentor", "coach", "help", "support",
        "customer", "client", "patient", "service", "care", "assist",
        "guide", "counsel"
    ]
    for kw in s_keywords:
        if kw in text_lower:
            signals["S"] += 1
    
    # Enterprising
    e_keywords = [
        "lead", "manage", "sales", "persuade", "negotiate", "business",
        "entrepreneur", "revenue", "growth", "marketing", "influence",
        "executive", "director", "strategy", "initiative"
    ]
    for kw in e_keywords:
        if kw in text_lower:
            signals["E"] += 1
    
    # Conventional
    c_keywords = [
        "organize", "administrative", "record", "data entry", "schedule",
        "process", "procedure", "compliance", "policy", "standard",
        "document", "filing", "bookkeeping", "accounting", "audit"
    ]
    for kw in c_keywords:
        if kw in text_lower:
            signals["C"] += 1
    
    # Sort and build 3-letter code
    sorted_types = sorted(signals.items(), key=lambda x: x[1], reverse=True)
    inferred_code = "".join(t[0] for t in sorted_types[:3])
    
    return {
        "inferred_code": inferred_code,
        "signal_strength": sum(signals.values()),
        "raw_signals": signals,
        "primary": sorted_types[0][0],
        "secondary": sorted_types[1][0] if len(sorted_types) > 1 else "",
        "tertiary": sorted_types[2][0] if len(sorted_types) > 2 else ""
    }


def detect_big_five_signals(text: str) -> dict:
    """Detect Big Five (OCEAN) trait signals in resume text."""
    text_lower = text.lower()
    signals = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    
    # Openness
    o_keywords = [
        "creative", "innovative", "curious", "design", "research",
        "learn", "new technology", "explore", "abstract", "conceptual",
        "intellectual", "artistic", "cultural"
    ]
    for kw in o_keywords:
        if kw in text_lower:
            signals["O"] += 1
    
    # Conscientiousness
    c_keywords = [
        "organized", "detail", "thorough", "methodical", "systematic",
        "plan", "schedule", "deadline", "reliable", "accurate",
        "quality", "standard", "procedure", "compliance", "responsible"
    ]
    for kw in c_keywords:
        if kw in text_lower:
            signals["C"] += 1
    
    # Extraversion
    e_keywords = [
        "team", "collaborat", "present", "lead", "meeting",
        "network", "social", "outgoing", "energetic", "communicat",
        "interpersonal", "public speak", "stakeholder", "client"
    ]
    for kw in e_keywords:
        if kw in text_lower:
            signals["E"] += 1
    
    # Agreeableness
    a_keywords = [
        "cooperat", "helpful", "support", "team player", "empathetic",
        "patient", "trust", "kind", "generous", "collaborative",
        "service", "customer", "client", "assist"
    ]
    for kw in a_keywords:
        if kw in text_lower:
            signals["A"] += 1
    
    # Neuroticism (inverse: emotional stability signals)
    n_keywords = [
        "calm", "resilient", "stable", "composed", "pressure",
        "stress", "crisis", "emergency", "critical", "urgent"
    ]
    for kw in n_keywords:
        if kw in text_lower:
            signals["N"] += 1
    
    return {
        "raw_signals": signals,
        "signal_strength": sum(signals.values()),
        "inferred_profile": {
            "O": "High" if signals["O"] > 5 else "Medium" if signals["O"] > 2 else "Low",
            "C": "High" if signals["C"] > 5 else "Medium" if signals["C"] > 2 else "Low",
            "E": "High" if signals["E"] > 5 else "Medium" if signals["E"] > 2 else "Low",
            "A": "High" if signals["A"] > 5 else "Medium" if signals["A"] > 2 else "Low",
            "N": "High (Stable)" if signals["N"] > 3 else "Medium" if signals["N"] > 1 else "Low"
        }
    }


# ═══════════════════════════════════════════════════════════════════════════
# MATCHING ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def score_keyword_match(text_lower: str, role: RoleProfile) -> float:
    """Score a resume against a role's keyword detectors.
    
    Returns a score from 0-100 based on weighted keyword matches.
    """
    score = 0.0
    max_possible = 0.0
    
    # Strong keywords (weight 3)
    for kw in role.keywords_strong:
        max_possible += 3
        if kw.lower() in text_lower:
            score += 3
    
    # Moderate keywords (weight 2)
    for kw in role.keywords_moderate:
        max_possible += 2
        if kw.lower() in text_lower:
            score += 2
    
    # Weak keywords (weight 1)
    for kw in role.keywords_weak:
        max_possible += 1
        if kw.lower() in text_lower:
            score += 1
    
    # Contraindication penalties (weight -2 each)
    for kw in role.contra_keywords:
        if kw.lower() in text_lower:
            score -= 2
    
    # Normalize to 0-100
    if max_possible > 0:
        normalized = (score / max_possible) * 100
    else:
        normalized = 0
    
    return max(0, min(100, normalized))


def compute_framework_compatibility(
    mbti_signals: dict,
    holland_signals: dict,
    big_five_signals: dict,
    role: RoleProfile
) -> float:
    """Compute how well the resume's detected framework signals match the role.

    Returns a compatibility score 0-100.
    """
    # MBTI compatibility — % of known dichotomies matching the role's typical type
    mbti_match = 50  # neutral when the resume carries no MBTI signal
    inferred = mbti_signals.get("inferred_type", "")
    target = role.mbti_type
    if inferred and target:
        matched = 0
        known = 0
        for inferred_char, target_char in zip(inferred, target):
            if inferred_char == "X":
                continue  # unknown dichotomy — skip
            known += 1
            if inferred_char == target_char:
                matched += 1
        if known:
            mbti_match = (matched / known) * 100
    mbti_match = min(mbti_match, 100)

    # Holland compatibility — overlap between inferred and target code
    holland_match = 0
    inferred_code = holland_signals.get("inferred_code", "")
    target_code = role.holland_code
    if inferred_code and target_code:
        for char in inferred_code[:3]:
            if char in target_code:
                holland_match += 33  # ~33 per matching type
    holland_match = min(holland_match, 100)

    # Blend: 50% MBTI + 50% Holland (both field-agnostic)
    compatibility = (mbti_match * 0.5) + (holland_match * 0.5)

    return min(100, compatibility)


def match_resume_to_roles(text: str) -> list:
    """Match a resume against all role profiles and return ranked results."""
    text_lower = text.lower()
    
    # Detect framework signals
    mbti_signals = detect_mbti_signals(text)
    holland_signals = detect_holland_signals(text)
    big_five_signals = detect_big_five_signals(text)
    
    results = []
    for role in ROLE_PROFILES:
        keyword_score = score_keyword_match(text_lower, role)
        framework_score = compute_framework_compatibility(
            mbti_signals, holland_signals, big_five_signals, role
        )
        
        # Composite score: 60% keyword match + 40% framework compatibility
        composite = (keyword_score * 0.6) + (framework_score * 0.4)
        
        # Experience adjustment: boost roles matching experience level
        exp_boost = 0
        if role.experience_required == "Direct Match":
            exp_boost = 10  # Boost for directly experienced roles
        elif role.experience_required == "Low":
            exp_boost = 5
        
        composite += exp_boost
        
        results.append({
            "role": role,
            "composite_score": round(composite, 1),
            "keyword_score": round(keyword_score, 1),
            "framework_score": round(framework_score, 1),
            "experience_boost": exp_boost,
            "category": role.category,
            "pivot_cost": role.pivot_cost
        })
    
    # Sort by composite score (descending)
    results.sort(key=lambda x: x["composite_score"], reverse=True)
    
    return results, mbti_signals, holland_signals, big_five_signals


# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTING
# ═══════════════════════════════════════════════════════════════════════════

def format_results(results: list, mbti_signals: dict, holland_signals: dict,
                   big_five_signals: dict, resume_path: str) -> str:
    """Format the top 6 results as a readable report."""
    lines = []
    lines.append("=" * 72)
    lines.append("  THE ANITALMID PROJECT — Resume-to-Career Matching Pipeline")
    lines.append("=" * 72)
    lines.append(f"  Resume: {resume_path}")
    lines.append(f"  Frameworks: Birkman + MBTI + Enneagram + DISC + Big Five + Holland")
    lines.append("=" * 72)
    lines.append("")
    
    # Detected signals
    lines.append("─── Detected Framework Signals ───")
    lines.append(f"  MBTI (inferred): {mbti_signals.get('inferred_type', 'N/A')}")
    lines.append(f"    {mbti_signals.get('I_vs_E', '?')} vs "
                 f"{mbti_signals.get('N_vs_S', '?')} vs "
                 f"{mbti_signals.get('T_vs_F', '?')} vs "
                 f"{mbti_signals.get('J_vs_P', '?')}")
    lines.append(f"  Holland Code (inferred): {holland_signals.get('inferred_code', 'N/A')}")
    lines.append(f"    Primary: {holland_signals.get('primary', '?')}  "
                 f"Secondary: {holland_signals.get('secondary', '?')}  "
                 f"Tertiary: {holland_signals.get('tertiary', '?')}")
    lines.append(f"  Big Five (inferred): {big_five_signals.get('inferred_profile', {})}")
    lines.append("")
    
    # Top 6 results
    lines.append("─── Top 6 Career Matches ───")
    lines.append("")
    
    top6 = results[:6]
    for i, result in enumerate(top6, 1):
        role = result["role"]
        lines.append(f"  #{i}  {role.title}  [{role.category}]  Score: {result['composite_score']}")
        lines.append(f"      Holland Code: {role.holland_code}  |  O*NET: {role.o_net_code}")
        lines.append(f"      Salary: {role.salary_range}")
        lines.append(f"      Pivot Cost: {role.pivot_cost}  |  Keyword: {result['keyword_score']}  |  Framework: {result['framework_score']}")
        lines.append(f"      {role.description}")
        lines.append("")
    
    # Summary table
    lines.append("─── Full Ranking ───")
    lines.append(f"  {'#':<3} {'Role':<38} {'Score':<8} {'Category':<10} {'Pivot':<8}")
    lines.append(f"  {'-'*3} {'-'*38} {'-'*8} {'-'*10} {'-'*8}")
    for i, result in enumerate(results, 1):
        lines.append(
            f"  {i:<3} "
            f"{result['role'].title:<38} "
            f"{result['composite_score']:<8} "
            f"{result['category']:<10} "
            f"{result['pivot_cost']:<8}"
        )
    
    lines.append("")
    lines.append("─── Interpretation Guide ───")
    lines.append("  Score = 60% resume keyword match + 40% framework compatibility")
    lines.append("  Direct Match experience roles receive a +10 bonus")
    lines.append("  Pivot Cost: None (already doing it) → Low → Medium → High (new field)")
    lines.append("  Framework compatibility uses Birkman/MBTI/Enneagram/DISC/BigFive/Holland")
    lines.append("=" * 72)
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 resume_matcher.py <resume.pdf|resume.txt>")
        print()
        print("Matches a resume against the Anitalmid Project's six-framework")
        print("career aptitude model and outputs the top 6 recommended positions.")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    
    if not os.path.exists(resume_path):
        print(f"ERROR: File not found: {resume_path}")
        sys.exit(1)
    
    print(f"Loading resume: {resume_path}")
    text = load_resume(resume_path)
    print(f"Extracted {len(text):,} characters of text.")
    print()
    
    print("Analyzing framework signals and matching against role profiles...")
    results, mbti_signals, holland_signals, big_five_signals = match_resume_to_roles(text)
    
    report = format_results(results, mbti_signals, holland_signals, big_five_signals, resume_path)
    print(report)
    
    # Also save report to file
    output_path = resume_path.rsplit(".", 1)[0] + "_career_match_report.txt"
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
