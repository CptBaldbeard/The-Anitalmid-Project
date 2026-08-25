"""Hobby → career mapping for the Career Pivot pane.

Each hobby is GRADED (a strength) and MATCHED against the psychometric frameworks:
it carries a Holland (RIASEC) hint, Big Five (OCEAN) leanings, and MBTI dichotomy
leanings, plus the career fields it points at. Hobbies integrate into the pivot by
marking those fields relevant and nudging the framework matching within a field.

Deterministic, curated lexicon — no LLM.
"""

from __future__ import annotations

from dataclasses import dataclass

STRENGTH_WEIGHT: dict[str, float] = {"strong": 3.0, "moderate": 2.0, "weak": 1.0}


@dataclass(frozen=True)
class Hobby:
    name: str
    categories: tuple[str, ...]          # career fields this hobby points at
    strength: str                        # "strong" | "moderate" | "weak"
    holland: str = ""                    # 1-3 RIASEC letters
    big_five: tuple[tuple[str, str], ...] = ()  # ((trait, "High"/"Medium"/"Low"), ...)
    mbti: str = ""                       # hinted dichotomies, e.g. "NP" or ""


# --- Curated hobby catalog (~170 hobbies) ------------------------------------
_H = Hobby  # short alias for readability below

HOBBIES: tuple[Hobby, ...] = (
    # Creative / making
    _H("drone flying", ("Creative & Media", "Real Estate", "Aviation"), "strong", "RIA", (("O", "High"),), "P"),
    _H("photography", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "P"),
    _H("videography", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "P"),
    _H("filmmaking", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "NP"),
    _H("painting", ("Arts & Entertainment",), "strong", "A", (("O", "High"),), "FP"),
    _H("drawing", ("Arts & Entertainment", "Creative & Media"), "strong", "A", (("O", "High"),), "FP"),
    _H("sculpture", ("Arts & Entertainment",), "strong", "A", (("O", "High"),), "FP"),
    _H("graphic design", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "NP"),
    _H("digital art", ("Creative & Media", "Arts & Entertainment", "Technology"), "strong", "A", (("O", "High"),), "NP"),
    _H("animation", ("Creative & Media", "Arts & Entertainment", "Technology"), "strong", "A", (("O", "High"),), "NP"),
    _H("illustration", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "FP"),
    _H("creative writing", ("Arts & Entertainment", "Creative & Media"), "strong", "A", (("O", "High"),), "NP"),
    _H("blogging", ("Creative & Media", "Arts & Entertainment"), "moderate", "A", (("O", "High"),), "NP"),
    _H("journaling", ("Arts & Entertainment", "Social Services"), "weak", "A", (("O", "High"),), "IF"),
    _H("knitting", ("Arts & Entertainment", "Manufacturing & Production"), "moderate", "AC", (("C", "Medium"),), "SJ"),
    _H("crocheting", ("Arts & Entertainment", "Manufacturing & Production"), "moderate", "AC", (("C", "Medium"),), "SJ"),
    _H("sewing", ("Arts & Entertainment", "Manufacturing & Production"), "moderate", "AC", (("C", "Medium"),), "SJ"),
    _H("embroidery", ("Arts & Entertainment",), "moderate", "AC", (("C", "Medium"),), "SJ"),
    _H("pottery", ("Arts & Entertainment",), "strong", "A", (("O", "High"),), "FP"),
    _H("woodworking", ("Skilled Trades", "Manufacturing & Production", "Arts & Entertainment"), "strong", "R", (("O", "Medium"),), "SP"),
    _H("carpentry", ("Skilled Trades", "Architecture & Construction"), "strong", "R", (), "SP"),
    _H("metalworking", ("Skilled Trades", "Manufacturing & Production"), "strong", "R", (), "SP"),
    _H("blacksmithing", ("Skilled Trades", "Arts & Entertainment"), "strong", "R", (("O", "Medium"),), "SP"),
    _H("leatherworking", ("Skilled Trades", "Manufacturing & Production"), "moderate", "RC", (), "SP"),
    _H("3d printing", ("Manufacturing & Production", "Technology", "Engineering"), "strong", "RI", (("O", "High"),), "NP"),
    _H("model building", ("Manufacturing & Production", "Engineering"), "moderate", "RI", (("C", "Medium"),), "SP"),
    _H("diy projects", ("Skilled Trades", "Architecture & Construction"), "moderate", "R", (), "SP"),
    _H("home improvement", ("Architecture & Construction", "Skilled Trades"), "strong", "R", (), "SP"),
    _H("gardening", ("Agriculture & Environment", "Science"), "strong", "R", (), "SP"),
    _H("landscaping", ("Agriculture & Environment", "Architecture & Construction"), "strong", "R", (), "SP"),
    _H("beekeeping", ("Agriculture & Environment", "Science"), "moderate", "R", (("O", "Medium"),), "SP"),
    _H("cooking", ("Hospitality & Tourism", "Arts & Entertainment"), "strong", "AS", (("O", "Medium"),), "SP"),
    _H("baking", ("Hospitality & Tourism", "Arts & Entertainment"), "strong", "AC", (("C", "Medium"),), "SJ"),
    _H("brewing", ("Manufacturing & Production", "Science"), "moderate", "RI", (("O", "Medium"),), "SP"),
    _H("winemaking", ("Agriculture & Environment", "Manufacturing & Production"), "moderate", "RI", (("O", "Medium"),), "SP"),
    _H("coffee roasting", ("Hospitality & Tourism", "Manufacturing & Production"), "moderate", "RC", (), "SJ"),
    _H("grilling", ("Hospitality & Tourism",), "moderate", "R", (), "SP"),
    _H("fermenting", ("Science", "Manufacturing & Production"), "weak", "RI", (("O", "Medium"),), "SP"),
    _H("cosplay", ("Arts & Entertainment", "Manufacturing & Production"), "moderate", "A", (("O", "High"),), "FP"),
    _H("makeup artistry", ("Arts & Entertainment", "Creative & Media"), "strong", "A", (("O", "Medium"),), "FP"),
    _H("fashion design", ("Arts & Entertainment", "Creative & Media"), "strong", "A", (("O", "High"),), "NP"),
    _H("interior decorating", ("Architecture & Construction", "Arts & Entertainment"), "strong", "A", (("O", "Medium"),), "FP"),
    # Technology / analytical
    _H("coding", ("Technology", "Engineering"), "strong", "IC", (("O", "Medium"),), "NT"),
    _H("programming", ("Technology", "Engineering"), "strong", "IC", (("O", "Medium"),), "NT"),
    _H("web development", ("Technology",), "strong", "IC", (("O", "Medium"),), "NT"),
    _H("game development", ("Technology", "Arts & Entertainment"), "strong", "IA", (("O", "High"),), "NP"),
    _H("gaming", ("Technology", "Arts & Entertainment"), "strong", "I", (("O", "High"),), "NP"),
    _H("video games", ("Technology", "Arts & Entertainment"), "strong", "I", (("O", "High"),), "NP"),
    _H("board games", ("Arts & Entertainment", "Business & Finance"), "moderate", "I", (("O", "High"),), "NT"),
    _H("tabletop roleplaying", ("Arts & Entertainment", "Creative & Media"), "moderate", "IA", (("O", "High"),), "NP"),
    _H("robotics", ("Engineering", "Technology", "Manufacturing & Production"), "strong", "RI", (("O", "High"),), "NT"),
    _H("electronics", ("Engineering", "Technology", "Skilled Trades"), "strong", "RI", (("O", "Medium"),), "NT"),
    _H("tinkering", ("Engineering", "Technology", "Skilled Trades"), "strong", "RI", (("O", "High"),), "NP"),
    _H("ham radio", ("Technology", "Engineering"), "moderate", "RI", (), "NT"),
    _H("drones", ("Aviation", "Technology", "Creative & Media"), "strong", "RI", (("O", "High"),), "NP"),
    _H("model rocketry", ("Engineering", "Aviation"), "moderate", "RI", (("O", "High"),), "NT"),
    _H("astronomy", ("Science", "Engineering"), "strong", "I", (("O", "High"),), "NT"),
    _H("astrophotography", ("Science", "Creative & Media"), "moderate", "IA", (("O", "High"),), "NT"),
    _H("chess", ("Science", "Business & Finance"), "moderate", "I", (("C", "Medium"),), "NT"),
    _H("puzzles", ("Science", "Technology"), "weak", "I", (), "NT"),
    _H("data analysis", ("Technology", "Science", "Business & Finance"), "strong", "IC", (("C", "Medium"),), "NT"),
    _H("machine learning", ("Technology", "Science"), "strong", "IC", (("O", "High"),), "NT"),
    _H("cryptocurrency", ("Business & Finance", "Technology"), "moderate", "IC", (("O", "High"),), "NT"),
    _H("investing", ("Business & Finance", "Real Estate"), "strong", "CE", (), "NT"),
    _H("stock trading", ("Business & Finance",), "strong", "CE", (("C", "Medium"),), "NT"),
    _H("personal finance", ("Business & Finance",), "moderate", "C", (("C", "High"),), "SJ"),
    _H("budgeting", ("Business & Finance",), "weak", "C", (("C", "High"),), "SJ"),
    _H("fantasy sports", ("Sports & Fitness", "Technology"), "moderate", "IC", (), "NT"),
    _H("genealogy", ("Science", "Government & Nonprofit"), "moderate", "I", (("C", "Medium"),), "SJ"),
    _H("archaeology", ("Science", "Agriculture & Environment"), "moderate", "I", (("O", "High"),), "NT"),
    _H("birdwatching", ("Agriculture & Environment", "Science"), "moderate", "I", (), "SP"),
    _H("insect collecting", ("Science", "Agriculture & Environment"), "weak", "I", (), "SP"),
    _H("rock collecting", ("Science", "Agriculture & Environment"), "weak", "I", (), "SP"),
    # Physical / outdoors
    _H("hiking", ("Agriculture & Environment", "Sports & Fitness"), "strong", "R", (), "SP"),
    _H("backpacking", ("Agriculture & Environment", "Sports & Fitness"), "strong", "R", (), "SP"),
    _H("camping", ("Agriculture & Environment", "Sports & Fitness"), "moderate", "R", (), "SP"),
    _H("running", ("Sports & Fitness",), "strong", "R", (), "SP"),
    _H("marathon running", ("Sports & Fitness",), "strong", "R", (("C", "Medium"),), "SJ"),
    _H("cycling", ("Sports & Fitness", "Transportation"), "strong", "R", (), "SP"),
    _H("mountain biking", ("Sports & Fitness", "Agriculture & Environment"), "strong", "R", (), "SP"),
    _H("swimming", ("Sports & Fitness",), "moderate", "R", (), "SP"),
    _H("rock climbing", ("Sports & Fitness", "Agriculture & Environment"), "strong", "R", (), "SP"),
    _H("weightlifting", ("Sports & Fitness", "Healthcare"), "moderate", "R", (("C", "Medium"),), "SJ"),
    _H("bodybuilding", ("Sports & Fitness", "Healthcare"), "moderate", "R", (("C", "Medium"),), "SJ"),
    _H("yoga", ("Sports & Fitness", "Healthcare", "Social Services"), "strong", "S", (("A", "Medium"),), "IF"),
    _H("pilates", ("Sports & Fitness", "Healthcare"), "moderate", "S", (), "IF"),
    _H("martial arts", ("Sports & Fitness", "Public Safety"), "strong", "RS", (), "SP"),
    _H("boxing", ("Sports & Fitness", "Public Safety"), "moderate", "R", (), "SP"),
    _H("fencing", ("Sports & Fitness",), "moderate", "R", (), "SP"),
    _H("team sports", ("Sports & Fitness",), "moderate", "ES", (("E", "High"),), "ES"),
    _H("soccer", ("Sports & Fitness",), "moderate", "ES", (("E", "High"),), "ES"),
    _H("basketball", ("Sports & Fitness",), "moderate", "ES", (("E", "High"),), "ES"),
    _H("baseball", ("Sports & Fitness",), "moderate", "RS", (), "ES"),
    _H("football", ("Sports & Fitness",), "moderate", "ES", (("E", "High"),), "ES"),
    _H("golf", ("Sports & Fitness", "Business & Finance"), "moderate", "R", (), "SJ"),
    _H("tennis", ("Sports & Fitness",), "moderate", "R", (), "SP"),
    _H("skiing", ("Sports & Fitness", "Hospitality & Tourism"), "moderate", "R", (), "SP"),
    _H("snowboarding", ("Sports & Fitness", "Hospitality & Tourism"), "moderate", "R", (), "SP"),
    _H("surfing", ("Sports & Fitness", "Hospitality & Tourism"), "moderate", "R", (), "SP"),
    _H("kayaking", ("Sports & Fitness", "Agriculture & Environment"), "moderate", "R", (), "SP"),
    _H("fishing", ("Agriculture & Environment", "Sports & Fitness"), "strong", "R", (), "SP"),
    _H("hunting", ("Agriculture & Environment", "Public Safety"), "moderate", "R", (), "SP"),
    _H("horseback riding", ("Agriculture & Environment", "Veterinary"), "strong", "R", (), "SP"),
    _H("equestrian", ("Agriculture & Environment", "Veterinary"), "strong", "R", (), "SP"),
    _H("scuba diving", ("Sports & Fitness", "Public Safety"), "moderate", "R", (), "SP"),
    _H("sailing", ("Transportation", "Sports & Fitness", "Hospitality & Tourism"), "moderate", "R", (), "SP"),
    # Music / performance
    _H("playing guitar", ("Arts & Entertainment",), "strong", "A", (("O", "High"),), "FP"),
    _H("playing piano", ("Arts & Entertainment",), "strong", "A", (("O", "High"),), "FP"),
    _H("music", ("Arts & Entertainment",), "strong", "A", (("O", "High"),), "FP"),
    _H("singing", ("Arts & Entertainment",), "strong", "A", (("E", "Medium"),), "EF"),
    _H("songwriting", ("Arts & Entertainment", "Creative & Media"), "strong", "A", (("O", "High"),), "NP"),
    _H("djing", ("Arts & Entertainment", "Creative & Media"), "moderate", "A", (("E", "Medium"),), "EP"),
    _H("producing music", ("Arts & Entertainment", "Technology", "Creative & Media"), "strong", "A", (("O", "High"),), "NP"),
    _H("dancing", ("Arts & Entertainment", "Sports & Fitness"), "strong", "A", (("E", "Medium"),), "EP"),
    _H("theater", ("Arts & Entertainment",), "strong", "A", (("E", "High"),), "EF"),
    _H("acting", ("Arts & Entertainment",), "strong", "A", (("E", "High"),), "EF"),
    _H("improv", ("Arts & Entertainment",), "moderate", "A", (("E", "High"),), "EP"),
    _H("stand-up comedy", ("Arts & Entertainment", "Creative & Media"), "moderate", "A", (("E", "High"),), "EP"),
    _H("magic", ("Arts & Entertainment",), "weak", "A", (), "EP"),
    _H("photography editing", ("Creative & Media", "Arts & Entertainment"), "moderate", "A", (), "NP"),
    # Learning / intellectual
    _H("reading", ("Education", "Creative & Media"), "moderate", "I", (("O", "High"),), "IN"),
    _H("learning languages", ("Education", "Government & Nonprofit", "Hospitality & Tourism"), "strong", "IS", (("O", "High"),), "NP"),
    _H("history", ("Education", "Government & Nonprofit", "Arts & Entertainment"), "moderate", "I", (("O", "High"),), "IN"),
    _H("philosophy", ("Education", "Government & Nonprofit"), "moderate", "I", (("O", "High"),), "IN"),
    _H("writing essays", ("Creative & Media", "Education"), "moderate", "A", (("O", "High"),), "IN"),
    _H("studying science", ("Science", "Education"), "moderate", "I", (("O", "High"),), "IN"),
    _H("math puzzles", ("Science", "Education"), "moderate", "I", (), "IN"),
    _H("debate", ("Legal", "Government & Nonprofit", "Education"), "moderate", "E", (("E", "Medium"),), "ET"),
    _H("public speaking", ("Government & Nonprofit", "Education", "Business & Finance"), "moderate", "E", (("E", "High"),), "EJ"),
    _H("teaching others", ("Education", "Social Services"), "strong", "S", (("A", "Medium"),), "EF"),
    _H("tutoring", ("Education", "Social Services"), "strong", "S", (("A", "Medium"),), "EF"),
    _H("mentoring", ("Education", "Social Services", "Business & Finance"), "strong", "S", (("A", "Medium"),), "EF"),
    _H("studying psychology", ("Social Services", "Science"), "moderate", "IS", (("O", "High"),), "IN"),
    _H("watching documentaries", ("Science", "Education", "Creative & Media"), "weak", "I", (("O", "High"),), "IN"),
    # Social / community / care
    _H("volunteering", ("Social Services", "Government & Nonprofit"), "strong", "S", (("A", "High"),), "EF"),
    _H("community service", ("Social Services", "Government & Nonprofit"), "strong", "S", (("A", "High"),), "EF"),
    _H("charity work", ("Social Services", "Government & Nonprofit"), "strong", "S", (("A", "High"),), "EF"),
    _H("coaching", ("Sports & Fitness", "Education"), "strong", "S", (("E", "Medium"),), "ES"),
    _H("coaching sports", ("Sports & Fitness", "Education"), "strong", "S", (("E", "Medium"),), "ES"),
    _H("babysitting", ("Education", "Social Services"), "moderate", "S", (("A", "Medium"),), "EF"),
    _H("pet care", ("Veterinary", "Social Services"), "moderate", "S", (("A", "Medium"),), "EF"),
    _H("dog training", ("Veterinary", "Social Services", "Agriculture & Environment"), "strong", "S", (), "EF"),
    _H("animal rescue", ("Veterinary", "Social Services"), "strong", "S", (("A", "High"),), "EF"),
    _H("fostering animals", ("Veterinary", "Social Services"), "strong", "S", (("A", "High"),), "EF"),
    _H("fundraising", ("Government & Nonprofit", "Business & Finance"), "moderate", "E", (("E", "Medium"),), "ES"),
    _H("organizing events", ("Hospitality & Tourism", "Operations", "Business & Finance"), "strong", "EC", (("E", "Medium"),), "EJ"),
    _H("hosting parties", ("Hospitality & Tourism",), "moderate", "ES", (("E", "High"),), "ES"),
    _H("networking", ("Business & Finance", "Government & Nonprofit"), "moderate", "E", (("E", "High"),), "ES"),
    _H("social media", ("Creative & Media", "Business & Finance"), "moderate", "EA", (("E", "Medium"),), "EP"),
    _H("content creation", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "NP"),
    _H("podcasting", ("Creative & Media", "Arts & Entertainment"), "strong", "A", (("O", "High"),), "NP"),
    _H("streaming", ("Creative & Media", "Technology"), "moderate", "EA", (("E", "Medium"),), "EP"),
    # Collecting / misc
    _H("collecting", ("Business & Finance", "Arts & Entertainment"), "weak", "C", (("C", "Medium"),), "SJ"),
    _H("coin collecting", ("Business & Finance", "Government & Nonprofit"), "weak", "C", (("C", "Medium"),), "SJ"),
    _H("stamp collecting", ("Government & Nonprofit",), "weak", "C", (("C", "Medium"),), "SJ"),
    _H("card collecting", ("Business & Finance",), "weak", "C", (("C", "Medium"),), "SJ"),
    _H("antiquing", ("Business & Finance", "Arts & Entertainment"), "weak", "C", (("O", "Medium"),), "SJ"),
    _H("restoring furniture", ("Skilled Trades", "Arts & Entertainment"), "strong", "R", (("O", "Medium"),), "SP"),
    _H("restoring cars", ("Skilled Trades", "Manufacturing & Production"), "strong", "R", (("O", "Medium"),), "SP"),
    _H("auto repair", ("Skilled Trades", "Manufacturing & Production"), "strong", "R", (), "SP"),
    _H("car detailing", ("Skilled Trades", "Operations"), "moderate", "RC", (("C", "Medium"),), "SJ"),
    _H("travel", ("Hospitality & Tourism", "Transportation"), "moderate", "E", (("O", "High"),), "EP"),
    _H("backpacking travel", ("Hospitality & Tourism", "Transportation"), "moderate", "E", (("O", "High"),), "EP"),
    _H("geocaching", ("Agriculture & Environment", "Technology"), "weak", "RI", (), "SP"),
    _H("urban exploration", ("Architecture & Construction", "Public Safety"), "weak", "RI", (("O", "High"),), "NP"),
    _H("food blogging", ("Creative & Media", "Hospitality & Tourism"), "moderate", "A", (("O", "High"),), "NP"),
    _H("wine tasting", ("Hospitality & Tourism", "Agriculture & Environment"), "weak", "A", (("O", "Medium"),), "SP"),
    _H("craft beer tasting", ("Hospitality & Tourism", "Manufacturing & Production"), "weak", "A", (("O", "Medium"),), "SP"),
)

_BY_NAME: dict[str, Hobby] = {h.name.lower(): h for h in HOBBIES}
_HOBBY_NAMES: list[str] = sorted(h.name for h in HOBBIES)


def hobby_names() -> list[str]:
    """Sorted list of hobby names for the frontend typeahead/datalist."""
    return list(_HOBBY_NAMES)


def resolve_hobby(text: str) -> Hobby | None:
    """Resolve a free-text hobby to a catalog entry, or None if unknown."""
    key = (text or "").strip()
    if not key:
        return None
    h = _BY_NAME.get(key.lower())
    if h is not None:
        return h
    low = key.lower()
    for name, hobby in _BY_NAME.items():
        if name in low or low in name:
            return hobby
    return None


def map_hobbies_to_categories(hobbies: list[str]) -> dict[str, float]:
    """Aggregate hobbies into {career category: summed strength weight}."""
    out: dict[str, float] = {}
    for raw in hobbies or []:
        h = resolve_hobby(raw)
        if h is None:
            continue
        weight = STRENGTH_WEIGHT.get(h.strength, 1.0)
        for cat in h.categories:
            out[cat] = out.get(cat, 0.0) + weight
    return out


def hobby_signals(hobbies: list[str]) -> dict:
    """Aggregate hobby framework hints into a single signal dict.

    Returns {holland: str, big_five: {trait: level}, mbti: str}.
    """
    holland_order = "RIASEC"
    holland_counts: dict[str, int] = {}
    big_five: dict[str, str] = {}
    mbti_seen: set[str] = set()

    for raw in hobbies or []:
        h = resolve_hobby(raw)
        if h is None:
            continue
        for letter in h.holland:
            holland_counts[letter] = holland_counts.get(letter, 0) + 1
        for trait, level in h.big_five:
            big_five.setdefault(trait, level)
        for letter in h.mbti:
            mbti_seen.add(letter)

    holland = "".join(
        sorted(holland_counts, key=lambda c: (-holland_counts[c], holland_order.index(c) if c in holland_order else 9))
    )
    mbti = "".join(sorted(mbti_seen))
    return {"holland": holland, "big_five": big_five, "mbti": mbti}
