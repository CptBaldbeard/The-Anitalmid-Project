"""College-major → career-category mapping for the "enter your interests & major" mode.

Each major maps to one of the role-catalog categories (see roles.py). The signals
mode boosts every role in the matching category, so a major acts as a coarse
field-level signal while MBTI + Holland (interests) supply the finer granularity.
"""

# Ordered list of majors for the frontend dropdown (display name → canonical).
MAJORS: dict[str, str] = {
    # Technology
    "Computer Science": "Technology",
    "Software Engineering": "Technology",
    "Information Technology": "Technology",
    "Cybersecurity": "Technology",
    "Data Science": "Technology",
    "Information Systems": "Technology",
    "Computer Engineering": "Technology",
    "Web Development": "Technology",
    "Game Design / Development": "Technology",
    # Engineering
    "Mechanical Engineering": "Engineering",
    "Electrical Engineering": "Engineering",
    "Civil Engineering": "Engineering",
    "Chemical Engineering": "Engineering",
    "Aerospace Engineering": "Engineering",
    "Biomedical Engineering": "Engineering",
    "Industrial Engineering": "Engineering",
    "Materials Science & Engineering": "Engineering",
    # Healthcare
    "Nursing": "Healthcare",
    "Pre-Med / Medicine": "Healthcare",
    "Pharmacy": "Healthcare",
    "Physical Therapy": "Healthcare",
    "Physician Assistant Studies": "Healthcare",
    "Public Health": "Healthcare",
    "Health Administration": "Healthcare",
    "Medical Laboratory Science": "Healthcare",
    "Dental Hygiene": "Healthcare",
    "Radiologic Technology": "Healthcare",
    "Kinesiology / Exercise Science": "Healthcare",
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
    # Science
    "Biology": "Science",
    "Chemistry": "Science",
    "Physics": "Science",
    "Biochemistry": "Science",
    "Mathematics": "Science",
    "Statistics": "Science",
    "Environmental Science": "Science",
    "Geology / Earth Science": "Science",
    "Astronomy / Astrophysics": "Science",
    "Neuroscience": "Science",
    "Microbiology": "Science",
    # Creative & Media
    "Graphic Design": "Creative & Media",
    "Journalism": "Creative & Media",
    "Communications": "Creative & Media",
    "Digital Media": "Creative & Media",
    "Film / Video Production": "Creative & Media",
    "Photography": "Creative & Media",
    "Advertising": "Creative & Media",
    "Public Relations": "Creative & Media",
    "Animation": "Creative & Media",
    # Education
    "Education": "Education",
    "Early Childhood Education": "Education",
    "Special Education": "Education",
    "Secondary Education": "Education",
    # Skilled Trades (vocational)
    "Construction Management": "Architecture & Construction",
    "Welding Technology": "Skilled Trades",
    "Electrical Technology": "Skilled Trades",
    "HVAC Technology": "Skilled Trades",
    "Automotive Technology": "Skilled Trades",
    "Culinary Arts": "Hospitality & Tourism",
    # Legal
    "Pre-Law / Legal Studies": "Legal",
    "Paralegal Studies": "Legal",
    # Public Safety
    "Criminal Justice": "Public Safety",
    "Criminology": "Public Safety",
    "Fire Science": "Public Safety",
    "Emergency Management": "Public Safety",
    # Operations
    "Operations Management": "Operations",
    "Logistics Management": "Operations",
    "Project Management": "Operations",
    # Agriculture & Environment
    "Agriculture / Agribusiness": "Agriculture & Environment",
    "Forestry": "Agriculture & Environment",
    "Horticulture": "Agriculture & Environment",
    "Animal Science": "Agriculture & Environment",
    # Government & Nonprofit
    "Political Science": "Government & Nonprofit",
    "Public Administration": "Government & Nonprofit",
    "International Relations": "Government & Nonprofit",
    "Public Policy": "Government & Nonprofit",
    "Nonprofit Management": "Government & Nonprofit",
    # Energy & Utilities
    "Energy Management": "Energy & Utilities",
    "Renewable Energy": "Energy & Utilities",
    "Petroleum Engineering": "Energy & Utilities",
    # Arts & Entertainment
    "Fine Arts": "Arts & Entertainment",
    "Music": "Arts & Entertainment",
    "Theater / Drama": "Arts & Entertainment",
    "Dance": "Arts & Entertainment",
    "Art History": "Arts & Entertainment",
    "Creative Writing": "Arts & Entertainment",
    # Aviation
    "Aviation / Piloting": "Aviation",
    "Aviation Management": "Aviation",
    "Air Traffic Control": "Aviation",
    # Architecture & Construction
    "Architecture": "Architecture & Construction",
    "Interior Design": "Architecture & Construction",
    "Landscape Architecture": "Architecture & Construction",
    "Urban Planning": "Architecture & Construction",
    # Sports & Fitness
    "Sports Management": "Sports & Fitness",
    "Athletic Training": "Sports & Fitness",
    "Recreation Management": "Sports & Fitness",
    # Hospitality & Tourism
    "Hospitality Management": "Hospitality & Tourism",
    "Tourism Management": "Hospitality & Tourism",
    "Event Management": "Hospitality & Tourism",
    # Manufacturing & Production
    "Manufacturing Engineering": "Manufacturing & Production",
    "Industrial Technology": "Manufacturing & Production",
    # Transportation
    "Transportation Management": "Transportation",
    # Social Services
    "Social Work": "Social Services",
    "Counseling": "Social Services",
    "Psychology": "Social Services",
    "Sociology": "Social Services",
    "Human Services": "Social Services",
    # Veterinary
    "Veterinary Medicine": "Veterinary",
    "Pre-Veterinary / Animal Science": "Veterinary",
    # Real Estate
    "Real Estate": "Real Estate",
}


def resolve_major(name: str) -> str | None:
    """Return the role category for a major name, or None if unknown."""
    if not name:
        return None
    key = name.strip()
    if key in MAJORS:
        return MAJORS[key]
    # Fuzzy fallback: case-insensitive exact / prefix match.
    lower = key.lower()
    for known, cat in MAJORS.items():
        if known.lower() == lower or known.lower().startswith(lower):
            return cat
    return None


def major_names() -> list[str]:
    """Sorted list of major names for the UI dropdown."""
    return sorted(MAJORS.keys())
