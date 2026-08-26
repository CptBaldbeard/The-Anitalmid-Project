"""Post-graduate degree catalog -> career-category mapping for the Career Pivot pane.

Mirrors ``majors.py`` (which maps undergrad majors -> category) but for
post-graduate degrees. Each degree maps to one or more of the 24 role-catalog
categories (see ``roles.py``), so an education pick acts as a coarse
field-level boost on the pivot ranking while MBTI + Holland supply the finer
signal. Degrees that don't match the catalog fall through gracefully (the
frontend also lets users type their own).
"""

from __future__ import annotations

from dataclasses import dataclass

# The 24 canonical role categories (must match roles.py exactly).
CATEGORIES: frozenset[str] = frozenset(
    {
        "Technology",
        "Engineering",
        "Healthcare",
        "Business & Finance",
        "Science",
        "Creative & Media",
        "Education",
        "Architecture & Construction",
        "Skilled Trades",
        "Hospitality & Tourism",
        "Legal",
        "Public Safety",
        "Operations",
        "Agriculture & Environment",
        "Government & Nonprofit",
        "Energy & Utilities",
        "Arts & Entertainment",
        "Aviation",
        "Sports & Fitness",
        "Manufacturing & Production",
        "Transportation",
        "Social Services",
        "Veterinary",
        "Real Estate",
    }
)


@dataclass(frozen=True)
class Degree:
    name: str
    level: str  # "Masters" | "Doctoral" | "Professional"
    categories: tuple[str, ...]


# --- Post-graduate fields that sensibly take "MS/MA/PhD in {field}" ----------
# field -> category. Professional-terminal fields (Medicine, Law, etc.) live in
# PROFESSIONAL below and are deliberately NOT generated here (no "MS in Medicine").
FIELDS: dict[str, str] = {
    # Technology
    "Computer Science": "Technology",
    "Software Engineering": "Technology",
    "Information Technology": "Technology",
    "Cybersecurity": "Technology",
    "Data Science": "Technology",
    "Information Systems": "Technology",
    "Computer Engineering": "Technology",
    "Artificial Intelligence": "Technology",
    "Machine Learning": "Technology",
    "Robotics": "Technology",
    "Human-Computer Interaction": "Technology",
    "Cloud Computing": "Technology",
    "Network Engineering": "Technology",
    "Web Development": "Technology",
    "Game Development": "Technology",
    "Blockchain Technology": "Technology",
    "Health Informatics": "Technology",
    "Geographic Information Science": "Technology",
    # Engineering
    "Mechanical Engineering": "Engineering",
    "Electrical Engineering": "Engineering",
    "Civil Engineering": "Engineering",
    "Chemical Engineering": "Engineering",
    "Aerospace Engineering": "Engineering",
    "Biomedical Engineering": "Engineering",
    "Industrial Engineering": "Engineering",
    "Materials Science & Engineering": "Engineering",
    "Nuclear Engineering": "Engineering",
    "Environmental Engineering": "Engineering",
    "Petroleum Engineering": "Engineering",
    "Structural Engineering": "Engineering",
    "Systems Engineering": "Engineering",
    "Automotive Engineering": "Engineering",
    "Marine Engineering": "Engineering",
    "Mining Engineering": "Engineering",
    "Optical Engineering": "Engineering",
    "Mechatronics": "Engineering",
    # Healthcare (non-terminal fields)
    "Nursing": "Healthcare",
    "Physical Therapy": "Healthcare",
    "Physician Assistant Studies": "Healthcare",
    "Public Health": "Healthcare",
    "Health Administration": "Healthcare",
    "Medical Laboratory Science": "Healthcare",
    "Radiologic Science": "Healthcare",
    "Occupational Therapy": "Healthcare",
    "Speech-Language Pathology": "Healthcare",
    "Nutrition & Dietetics": "Healthcare",
    "Genetic Counseling": "Healthcare",
    "Epidemiology": "Healthcare",
    "Biostatistics": "Healthcare",
    "Healthcare Management": "Healthcare",
    "Athletic Training": "Healthcare",
    "Nurse Practitioner": "Healthcare",
    "Nurse Anesthesia": "Healthcare",
    # Science
    "Biology": "Science",
    "Chemistry": "Science",
    "Physics": "Science",
    "Biochemistry": "Science",
    "Mathematics": "Science",
    "Statistics": "Science",
    "Environmental Science": "Science",
    "Geology": "Science",
    "Astronomy & Astrophysics": "Science",
    "Neuroscience": "Science",
    "Microbiology": "Science",
    "Genetics": "Science",
    "Immunology": "Science",
    "Molecular Biology": "Science",
    "Pharmacology": "Science",
    "Toxicology": "Science",
    "Marine Biology": "Science",
    "Atmospheric Science": "Science",
    "Materials Science": "Science",
    # Business & Finance
    "Business Administration": "Business & Finance",
    "Accounting": "Business & Finance",
    "Finance": "Business & Finance",
    "Marketing": "Business & Finance",
    "Economics": "Business & Finance",
    "Management": "Business & Finance",
    "Entrepreneurship": "Business & Finance",
    "Human Resources": "Business & Finance",
    "International Business": "Business & Finance",
    "Supply Chain Management": "Business & Finance",
    "Actuarial Science": "Business & Finance",
    "Business Analytics": "Business & Finance",
    "Organizational Leadership": "Business & Finance",
    # Creative & Media
    "Graphic Design": "Creative & Media",
    "Journalism": "Creative & Media",
    "Communications": "Creative & Media",
    "Digital Media": "Creative & Media",
    "Film & Video Production": "Creative & Media",
    "Photography": "Creative & Media",
    "Advertising": "Creative & Media",
    "Public Relations": "Creative & Media",
    "Animation": "Creative & Media",
    "Game Design": "Creative & Media",
    # Education
    "Education": "Education",
    "Early Childhood Education": "Education",
    "Special Education": "Education",
    "Secondary Education": "Education",
    "Educational Leadership": "Education",
    "Curriculum & Instruction": "Education",
    "Higher Education": "Education",
    "School Counseling": "Education",
    "Educational Technology": "Education",
    # Architecture & Construction
    "Architecture": "Architecture & Construction",
    "Interior Design": "Architecture & Construction",
    "Landscape Architecture": "Architecture & Construction",
    "Urban Planning": "Architecture & Construction",
    "Construction Management": "Architecture & Construction",
    "Historic Preservation": "Architecture & Construction",
    # Skilled Trades (management-adjacent post-grad programs)
    "Construction Technology": "Skilled Trades",
    "Industrial Technology": "Skilled Trades",
    "Aviation Maintenance": "Skilled Trades",
    # Hospitality & Tourism
    "Hospitality Management": "Hospitality & Tourism",
    "Tourism Management": "Hospitality & Tourism",
    "Event Management": "Hospitality & Tourism",
    "Culinary Arts": "Hospitality & Tourism",
    "Food Service Management": "Hospitality & Tourism",
    # Legal (non-terminal)
    "Legal Studies": "Legal",
    "Paralegal Studies": "Legal",
    "International Law": "Legal",
    "Intellectual Property Law": "Legal",
    "Tax Law": "Legal",
    "Environmental Law": "Legal",
    # Public Safety
    "Criminal Justice": "Public Safety",
    "Criminology": "Public Safety",
    "Fire Science": "Public Safety",
    "Emergency Management": "Public Safety",
    "Homeland Security": "Public Safety",
    "Forensic Science": "Public Safety",
    # Operations
    "Operations Management": "Operations",
    "Logistics Management": "Operations",
    "Project Management": "Operations",
    "Quality Management": "Operations",
    "Industrial Management": "Operations",
    # Agriculture & Environment
    "Agriculture & Agribusiness": "Agriculture & Environment",
    "Forestry": "Agriculture & Environment",
    "Horticulture": "Agriculture & Environment",
    "Animal Science": "Agriculture & Environment",
    "Soil Science": "Agriculture & Environment",
    "Plant Science": "Agriculture & Environment",
    "Agricultural Engineering": "Agriculture & Environment",
    "Conservation": "Agriculture & Environment",
    # Government & Nonprofit
    "Public Administration": "Government & Nonprofit",
    "Public Policy": "Government & Nonprofit",
    "International Relations": "Government & Nonprofit",
    "Political Science": "Government & Nonprofit",
    "Nonprofit Management": "Government & Nonprofit",
    "Public Affairs": "Government & Nonprofit",
    "Development Studies": "Government & Nonprofit",
    "Urban Policy": "Government & Nonprofit",
    # Energy & Utilities
    "Energy Management": "Energy & Utilities",
    "Renewable Energy": "Energy & Utilities",
    "Energy Systems": "Energy & Utilities",
    "Power Systems": "Energy & Utilities",
    # Arts & Entertainment
    "Fine Arts": "Arts & Entertainment",
    "Music": "Arts & Entertainment",
    "Theater": "Arts & Entertainment",
    "Dance": "Arts & Entertainment",
    "Art History": "Arts & Entertainment",
    "Creative Writing": "Arts & Entertainment",
    "Musicology": "Arts & Entertainment",
    "Arts Management": "Arts & Entertainment",
    # Aviation
    "Aviation": "Aviation",
    "Aviation Management": "Aviation",
    "Air Traffic Management": "Aviation",
    "Unmanned Systems": "Aviation",
    # Sports & Fitness
    "Sports Management": "Sports & Fitness",
    "Kinesiology & Exercise Science": "Sports & Fitness",
    "Recreation Management": "Sports & Fitness",
    "Sports Medicine": "Sports & Fitness",
    # Manufacturing & Production
    "Manufacturing Engineering": "Manufacturing & Production",
    "Industrial Technology Management": "Manufacturing & Production",
    "Quality Engineering": "Manufacturing & Production",
    # Transportation
    "Transportation Management": "Transportation",
    "Urban Transportation": "Transportation",
    "Transportation Planning": "Transportation",
    # Social Services
    "Social Work": "Social Services",
    "Counseling": "Social Services",
    "Psychology": "Social Services",
    "Sociology": "Social Services",
    "Human Services": "Social Services",
    "Marriage & Family Therapy": "Social Services",
    "Clinical Mental Health Counseling": "Social Services",
    "School Psychology": "Social Services",
    # Veterinary
    "Veterinary Science": "Veterinary",
    "Animal Welfare": "Veterinary",
    # Real Estate
    "Real Estate Development": "Real Estate",
    "Real Estate Finance": "Real Estate",
}

# Categories whose fields also get an "MA in {field}" form (humanities/social/arts).
MA_CATEGORIES: frozenset[str] = frozenset(
    {
        "Creative & Media",
        "Education",
        "Social Services",
        "Government & Nonprofit",
        "Arts & Entertainment",
        "Legal",
        "Business & Finance",
        "Architecture & Construction",
        "Hospitality & Tourism",
    }
)

# Categories whose fields also get an "MFA in {field}" form.
MFA_CATEGORIES: frozenset[str] = frozenset({"Creative & Media", "Arts & Entertainment"})

# Canonical degree levels, in display order.
LEVELS: tuple[str, ...] = ("Undergraduate", "Masters", "Doctoral")

# Undergraduate categories: which fields take a "B.S. in {field}" vs "B.A. in {field}".
BS_CATEGORIES: frozenset[str] = frozenset(
    {
        "Technology", "Engineering", "Healthcare", "Science", "Business & Finance",
        "Agriculture & Environment", "Energy & Utilities", "Manufacturing & Production",
        "Operations", "Skilled Trades", "Aviation", "Transportation", "Sports & Fitness",
        "Public Safety", "Real Estate", "Veterinary",
    }
)
BA_CATEGORIES: frozenset[str] = frozenset(
    {
        "Creative & Media", "Education", "Architecture & Construction",
        "Hospitality & Tourism", "Legal", "Government & Nonprofit",
        "Arts & Entertainment", "Social Services",
    }
)

# Named undergraduate degrees that aren't simply "B.S./B.A. in <field>".
UNDERGRAD_PROFESSIONAL: list[tuple[str, str, tuple[str, ...]]] = [
    ("BBA", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Business Administration", "Undergraduate", ("Business & Finance",)),
    ("BSBA", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Accounting", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Finance", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Marketing", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Economics", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of International Business", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Human Resources", "Undergraduate", ("Business & Finance",)),
    ("Bachelor of Management", "Undergraduate", ("Business & Finance",)),
    ("BEng", "Undergraduate", ("Engineering",)),
    ("BSE", "Undergraduate", ("Engineering",)),
    ("BTech", "Undergraduate", ("Engineering",)),
    ("Bachelor of Engineering", "Undergraduate", ("Engineering",)),
    ("Bachelor of Technology", "Undergraduate", ("Engineering",)),
    ("BSN", "Undergraduate", ("Healthcare",)),
    ("Bachelor of Nursing", "Undergraduate", ("Healthcare",)),
    ("BPharm", "Undergraduate", ("Healthcare",)),
    ("Bachelor of Pharmacy", "Undergraduate", ("Healthcare",)),
    ("Bachelor of Dental Science", "Undergraduate", ("Healthcare",)),
    ("Bachelor of Medical Laboratory Science", "Undergraduate", ("Healthcare",)),
    ("Bachelor of Radiography", "Undergraduate", ("Healthcare",)),
    ("Bachelor of Science in Health Science", "Undergraduate", ("Healthcare",)),
    ("LLB", "Undergraduate", ("Legal",)),
    ("Bachelor of Laws", "Undergraduate", ("Legal",)),
    ("BEd", "Undergraduate", ("Education",)),
    ("Bachelor of Education", "Undergraduate", ("Education",)),
    ("Bachelor of Early Childhood Education", "Undergraduate", ("Education",)),
    ("BFA", "Undergraduate", ("Arts & Entertainment",)),
    ("Bachelor of Fine Arts", "Undergraduate", ("Arts & Entertainment",)),
    ("Bachelor of Music", "Undergraduate", ("Arts & Entertainment",)),
    ("BMus", "Undergraduate", ("Arts & Entertainment",)),
    ("Bachelor of Design", "Undergraduate", ("Arts & Entertainment",)),
    ("BArch", "Undergraduate", ("Architecture & Construction",)),
    ("Bachelor of Architecture", "Undergraduate", ("Architecture & Construction",)),
    ("Bachelor of Landscape Architecture", "Undergraduate", ("Architecture & Construction",)),
    ("Bachelor of Interior Design", "Undergraduate", ("Architecture & Construction",)),
    ("Bachelor of Urban Planning", "Undergraduate", ("Architecture & Construction",)),
    ("BSW", "Undergraduate", ("Social Services",)),
    ("Bachelor of Social Work", "Undergraduate", ("Social Services",)),
    ("Bachelor of Counseling", "Undergraduate", ("Social Services",)),
    ("Bachelor of Journalism", "Undergraduate", ("Creative & Media",)),
    ("Bachelor of Communications", "Undergraduate", ("Creative & Media",)),
    ("Bachelor of Graphic Design", "Undergraduate", ("Creative & Media",)),
    ("Bachelor of Digital Media", "Undergraduate", ("Creative & Media",)),
    ("Bachelor of Aviation", "Undergraduate", ("Aviation",)),
    ("Bachelor of Hospitality Management", "Undergraduate", ("Hospitality & Tourism",)),
    ("Bachelor of Tourism Management", "Undergraduate", ("Hospitality & Tourism",)),
    ("Bachelor of Agriculture", "Undergraduate", ("Agriculture & Environment",)),
    ("Bachelor of Veterinary Science", "Undergraduate", ("Veterinary",)),
    ("Bachelor of Criminal Justice", "Undergraduate", ("Public Safety",)),
    ("Bachelor of Emergency Management", "Undergraduate", ("Public Safety",)),
    ("Bachelor of Public Administration", "Undergraduate", ("Government & Nonprofit",)),
    ("Bachelor of International Relations", "Undergraduate", ("Government & Nonprofit",)),
    ("Bachelor of Exercise Science", "Undergraduate", ("Sports & Fitness",)),
    ("Bachelor of Sports Management", "Undergraduate", ("Sports & Fitness",)),
    ("Bachelor of Real Estate", "Undergraduate", ("Real Estate",)),
    ("Bachelor of Logistics", "Undergraduate", ("Operations",)),
    ("Bachelor of Project Management", "Undergraduate", ("Operations",)),
]

# --- Standalone / professional terminal degrees ------------------------------
# (name, level, [categories])
PROFESSIONAL: list[tuple[str, str, tuple[str, ...]]] = [
    ("MBA", "Masters", ("Business & Finance",)),
    ("Executive MBA", "Masters", ("Business & Finance",)),
    ("Master of Accounting", "Masters", ("Business & Finance",)),
    ("Master of Finance", "Masters", ("Business & Finance",)),
    ("Master of Marketing", "Masters", ("Business & Finance",)),
    ("Master of Business Analytics", "Masters", ("Business & Finance",)),
    ("Master of Human Resources", "Masters", ("Business & Finance",)),
    ("Master of International Business", "Masters", ("Business & Finance",)),
    ("Master of Real Estate", "Masters", ("Real Estate",)),
    ("JD", "Professional", ("Legal",)),
    ("Juris Doctor", "Professional", ("Legal",)),
    ("Juris Doctorate", "Professional", ("Legal",)),
    ("LLM", "Masters", ("Legal",)),
    ("Master of Legal Studies", "Masters", ("Legal",)),
    ("Master of Dispute Resolution", "Masters", ("Legal",)),
    ("MD", "Professional", ("Healthcare",)),
    ("DO", "Professional", ("Healthcare",)),
    ("DDS", "Professional", ("Healthcare",)),
    ("DMD", "Professional", ("Healthcare",)),
    ("PharmD", "Professional", ("Healthcare",)),
    ("DPT", "Professional", ("Healthcare",)),
    ("DNP", "Professional", ("Healthcare",)),
    ("Master of Nursing", "Masters", ("Healthcare",)),
    ("MPH", "Masters", ("Healthcare",)),
    ("Master of Health Administration", "Masters", ("Healthcare",)),
    ("Master of Physician Assistant Studies", "Masters", ("Healthcare",)),
    ("Master of Occupational Therapy", "Masters", ("Healthcare",)),
    ("MSW", "Masters", ("Social Services",)),
    ("Master of Counseling", "Masters", ("Social Services",)),
    ("Master of Marriage & Family Therapy", "Masters", ("Social Services",)),
    ("PsyD", "Professional", ("Social Services",)),
    ("Doctor of Psychology", "Professional", ("Social Services",)),
    ("Doctor of Clinical Psychology", "Professional", ("Social Services",)),
    ("MEd", "Masters", ("Education",)),
    ("Master of Teaching", "Masters", ("Education",)),
    ("EdD", "Professional", ("Education",)),
    ("Education Specialist", "Masters", ("Education",)),
    ("MFA", "Masters", ("Arts & Entertainment",)),
    ("Master of Music", "Masters", ("Arts & Entertainment",)),
    ("Master of Architecture", "Masters", ("Architecture & Construction",)),
    ("Master of Landscape Architecture", "Masters", ("Architecture & Construction",)),
    ("Master of Urban Planning", "Masters", ("Architecture & Construction",)),
    ("MEng", "Masters", ("Engineering",)),
    ("Master of Engineering Management", "Masters", ("Engineering",)),
    ("MPA", "Masters", ("Government & Nonprofit",)),
    ("MPP", "Masters", ("Government & Nonprofit",)),
    ("Master of International Affairs", "Masters", ("Government & Nonprofit",)),
    ("Master of Public Affairs", "Masters", ("Government & Nonprofit",)),
    ("MLIS", "Masters", ("Education",)),
    ("Master of Library & Information Science", "Masters", ("Education",)),
    ("MDiv", "Masters", ("Government & Nonprofit",)),
    ("Master of Theology", "Masters", ("Government & Nonprofit",)),
    ("Master of Research", "Masters", ("Science",)),
    ("Master of Philosophy", "Masters", ("Science",)),
    ("Doctor of Science", "Professional", ("Science",)),
    ("DVM", "Professional", ("Veterinary",)),
    ("Master of Veterinary Science", "Masters", ("Veterinary",)),
    ("Doctor of Public Health", "Professional", ("Healthcare",)),
    ("Doctor of Social Work", "Professional", ("Social Services",)),
    ("Master of Social Policy", "Masters", ("Government & Nonprofit",)),
]


def _build() -> list[Degree]:
    degrees: dict[str, Degree] = {}

    def add(name: str, level: str, categories: tuple[str, ...]) -> None:
        degrees[name] = Degree(name=name, level=level, categories=categories)

    for field, category in FIELDS.items():
        cats = (category,)
        add(f"MS in {field}", "Masters", cats)
        add(f"PhD in {field}", "Doctoral", cats)
        if category in MA_CATEGORIES:
            add(f"MA in {field}", "Masters", cats)
        if category in MFA_CATEGORIES:
            add(f"MFA in {field}", "Masters", cats)
        if category == "Engineering":
            add(f"MEng in {field}", "Masters", cats)
        # Undergraduate forms.
        if category in BS_CATEGORIES:
            add(f"B.S. in {field}", "Undergraduate", cats)
        if category in BA_CATEGORIES:
            add(f"B.A. in {field}", "Undergraduate", cats)

    for name, level, cats in UNDERGRAD_PROFESSIONAL:
        add(name, level, cats)

    for name, level, cats in PROFESSIONAL:
        add(name, "Doctoral" if level == "Professional" else level, cats)

    return sorted(degrees.values(), key=lambda d: d.name.lower())


DEGREES: list[Degree] = _build()
_DEGREE_NAMES: list[str] = [d.name for d in DEGREES]
_BY_NAME: dict[str, Degree] = {d.name.lower(): d for d in DEGREES}


def degree_names() -> list[str]:
    """Sorted list of degree names for the frontend typeahead/datalist."""
    return list(_DEGREE_NAMES)


def degrees_by_level() -> dict[str, list[str]]:
    """Degree names grouped by level (Undergraduate / Masters / Doctoral)."""
    grouped: dict[str, list[str]] = {lvl: [] for lvl in LEVELS}
    for d in DEGREES:
        grouped.setdefault(d.level, []).append(d.name)
    return {lvl: grouped[lvl] for lvl in LEVELS if grouped[lvl]}


def _category_for_text(text: str) -> str | None:
    """Best-effort category resolution for a free-text degree string."""
    t = (text or "").strip()
    if not t:
        return None
    d = _BY_NAME.get(t.lower())
    if d is not None:
        return d.categories[0]
    # Keyword match: any known field name appearing in the typed text.
    low = t.lower()
    for field, category in FIELDS.items():
        if field.lower() in low:
            return category
    # A few common degree-level prefixes are noise; strip and retry once.
    for prefix in ("ms in ", "ma in ", "mfa in ", "meng in ", "phd in ", "doctor of ", "master of "):
        if low.startswith(prefix):
            return _category_for_text(t[len(prefix):])
    return None


def resolve_degree(name: str) -> Degree | None:
    """Return the catalog Degree for a name, or None if unknown."""
    key = (name or "").strip()
    if not key:
        return None
    d = _BY_NAME.get(key.lower())
    if d is not None:
        return d
    # Fuzzy: case-insensitive prefix match against the sorted catalog.
    low = key.lower()
    for n, deg in _BY_NAME.items():
        if n.startswith(low):
            return deg
    return None


def map_degrees_to_categories(names: list[str]) -> set[str]:
    """Resolve a list of degree names (catalog or free-text) to a set of categories."""
    out: set[str] = set()
    for name in names or []:
        cat = _category_for_text(name)
        if cat:
            out.add(cat)
    return out
