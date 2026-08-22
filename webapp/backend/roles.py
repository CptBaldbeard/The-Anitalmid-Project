"""Anitalmid role catalog — a field-agnostic set of career profiles.

Each RoleProfile pairs framework signals (Holland RIASEC + a typical MBTI type)
with weighted resume keyword detectors. Used by resume_matcher to score a
resume against every role and produce a ranked, graded list.
"""
from dataclasses import dataclass, field


@dataclass
class RoleProfile:
    title: str
    category: str           # career field (e.g. "Healthcare", "Engineering")
    holland_code: str       # 3-letter RIASEC code
    o_net_code: str         # O*NET-SOC code
    mbti_type: str          # typical MBTI type for this role
    salary_range: str
    experience_required: str  # "Low" (entry), "Medium", "High" (senior)

    # Weighted resume keyword detectors
    keywords_strong: list = field(default_factory=list)    # weight 3
    keywords_moderate: list = field(default_factory=list)  # weight 2
    keywords_weak: list = field(default_factory=list)      # weight 1
    contra_keywords: list = field(default_factory=list)    # penalty -2

    description: str = ""
    pivot_cost: str = ""     # "None", "Low", "Medium", "High"


ROLE_PROFILES = [
    # ─── Technology ────────────────────────────────────────────────────────
    RoleProfile(
        title="Systems Administrator",
        category="Technology",
        holland_code="RIC",
        o_net_code="15-1244.00",
        mbti_type="ISTJ",
        salary_range="$65K-$90K (mid), $90K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "systems administrator", "sysadmin", "system admin",
            "active directory", "group policy", "windows server",
            "linux administration", "server management", "infrastructure",
            "backup", "disaster recovery", "endpoint management"
        ],
        keywords_moderate=[
            "powershell", "bash", "scripting", "virtualization",
            "vmware", "hyper-v", "dns", "dhcp", "tcp/ip",
            "patch management", "monitoring", "sccm", "intune"
        ],
        keywords_weak=[
            "it support", "help desk", "troubleshooting", "ticketing",
            "documentation", "onboarding", "asset management"
        ],
        contra_keywords=["sales", "marketing", "teaching", "counseling"],
        description="Manages servers, user accounts, backups, and day-to-day IT operations.",
        pivot_cost="None",
    ),
    RoleProfile(
        title="Software Developer",
        category="Technology",
        holland_code="IRC",
        o_net_code="15-1252.00",
        mbti_type="INTP",
        salary_range="$80K-$120K (mid), $120K-$180K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "software developer", "software engineer", "programmer",
            "full stack", "front-end", "back-end", "backend", "frontend",
            "web development", "api development", "application development"
        ],
        keywords_moderate=[
            "javascript", "typescript", "python", "java", "c++", "c#", "go",
            "react", "angular", "node", "git", "agile", "scrum", "unit testing"
        ],
        keywords_weak=[
            "coding", "debugging", "object-oriented", "database",
            "rest api", "microservices", "cloud"
        ],
        contra_keywords=["help desk", "hardware repair", "cabling"],
        description="Designs, builds, and maintains software applications and services.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Security Analyst / SOC Analyst",
        category="Technology",
        holland_code="ICR",
        o_net_code="15-1212.00",
        mbti_type="ISTJ",
        salary_range="$70K-$100K (Tier 1/2), $100K-$140K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "security analyst", "soc", "security operations",
            "incident response", "siem", "threat hunting",
            "vulnerability management", "security+", "cissp",
            "endpoint protection", "mfa", "identity management"
        ],
        keywords_moderate=[
            "compliance", "iso 27001", "soc2", "hipaa", "pci dss",
            "risk assessment", "penetration testing", "forensics",
            "security monitoring", "alert triage"
        ],
        keywords_weak=[
            "firewall", "vpn", "network security", "access control",
            "audit", "logging", "incident management"
        ],
        contra_keywords=["sales engineer", "account manager"],
        description="Monitors and defends systems, responds to threats, and manages vulnerabilities.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Network Engineer",
        category="Technology",
        holland_code="RIC",
        o_net_code="15-1241.00",
        mbti_type="ISTJ",
        salary_range="$75K-$110K (mid), $110K-$150K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "network engineer", "network administrator", "networking",
            "cisco", "routing", "switching", "firewall", "vpn",
            "lan", "wan", "network infrastructure"
        ],
        keywords_moderate=[
            "tcp/ip", "bgp", "ospf", "vlan", "mpls", "sd-wan",
            "network monitoring", "load balancer", "wireless"
        ],
        keywords_weak=[
            "dns", "dhcp", "troubleshooting", "connectivity",
            "cabling", "network security"
        ],
        contra_keywords=["front-end", "graphic design"],
        description="Designs and maintains computer networks, connectivity, and network security.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Database Administrator",
        category="Technology",
        holland_code="CIR",
        o_net_code="15-1243.00",
        mbti_type="ISTJ",
        salary_range="$75K-$110K (mid), $110K-$150K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "database administrator", "dba", "database management",
            "sql server", "postgresql", "mysql", "oracle", "mongodb"
        ],
        keywords_moderate=[
            "sql", "query optimization", "backup", "replication",
            "etl", "data warehouse", "indexing", "performance tuning"
        ],
        keywords_weak=[
            "data modeling", "schema", "stored procedure", "migration"
        ],
        contra_keywords=["field service", "retail"],
        description="Manages, tunes, backs up, and secures organizational databases.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="DevOps Engineer",
        category="Technology",
        holland_code="IRC",
        o_net_code="15-1252.00",
        mbti_type="INTJ",
        salary_range="$95K-$135K (mid), $135K-$190K (senior)",
        experience_required="High",
        keywords_strong=[
            "devops", "ci/cd", "continuous integration", "continuous deployment",
            "kubernetes", "docker", "container", "terraform", "infrastructure as code"
        ],
        keywords_moderate=[
            "jenkins", "github actions", "gitlab", "ansible", "puppet",
            "aws", "azure", "gcp", "monitoring", "observability", "helm"
        ],
        keywords_weak=[
            "automation", "scripting", "linux", "cloud", "pipeline"
        ],
        contra_keywords=[],
        description="Automates software delivery and cloud infrastructure operations.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Cloud Administrator / Engineer",
        category="Technology",
        holland_code="IAR",
        o_net_code="15-1299.08",
        mbti_type="INTJ",
        salary_range="$80K-$110K (mid), $110K-$150K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "azure", "aws", "cloud", "cloud administrator", "cloud engineer",
            "entra id", "azure ad", "cloud migration", "iaas", "paas", "saas"
        ],
        keywords_moderate=[
            "terraform", "bicep", "arm template", "infrastructure as code",
            "kubernetes", "docker", "cloud security", "microsoft 365"
        ],
        keywords_weak=[
            "powershell", "scripting", "automation", "virtualization"
        ],
        contra_keywords=[],
        description="Builds and operates cloud-native infrastructure and services.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="IT Support Specialist",
        category="Technology",
        holland_code="RSC",
        o_net_code="15-1232.00",
        mbti_type="ISTJ",
        salary_range="$45K-$65K (entry-mid), $65K-$85K (senior)",
        experience_required="Low",
        keywords_strong=[
            "it support", "help desk", "desktop support", "technical support",
            "end user support", "ticketing", "troubleshooting"
        ],
        keywords_moderate=[
            "windows", "active directory", "office 365", "printer",
            "hardware", "remote support", "customer service"
        ],
        keywords_weak=[
            "onboarding", "documentation", "password reset", "imaging"
        ],
        contra_keywords=["software development", "data science"],
        description="Provides first-line technical support and troubleshooting for end users.",
        pivot_cost="None",
    ),
    RoleProfile(
        title="UX Designer",
        category="Technology",
        holland_code="ARI",
        o_net_code="15-1255.00",
        mbti_type="INFP",
        salary_range="$65K-$100K (mid), $100K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "ux design", "user experience", "ui design", "figma", "sketch",
            "adobe xd", "wireframe", "prototype", "usability", "user research"
        ],
        keywords_moderate=[
            "design thinking", "information architecture", "interaction design",
            "design system", "accessibility", "user testing", "a/b testing"
        ],
        keywords_weak=[
            "visual design", "graphic design", "adobe creative",
            "photoshop", "illustrator", "front-end", "html", "css"
        ],
        contra_keywords=[],
        description="Designs intuitive, accessible digital products and interfaces.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Data Scientist",
        category="Technology",
        holland_code="ICR",
        o_net_code="15-2051.00",
        mbti_type="INTP",
        salary_range="$90K-$130K (mid), $130K-$190K (senior)",
        experience_required="High",
        keywords_strong=[
            "data scientist", "machine learning", "data science",
            "predictive model", "python", "r", "statistical model"
        ],
        keywords_moderate=[
            "sql", "pandas", "numpy", "tensorflow", "pytorch",
            "data mining", "deep learning", "natural language"
        ],
        keywords_weak=[
            "data analysis", "visualization", "algorithm", "experimentation"
        ],
        contra_keywords=[],
        description="Extracts insight from data using statistics, ML, and programming.",
        pivot_cost="High",
    ),

    # ─── Healthcare ────────────────────────────────────────────────────────
    RoleProfile(
        title="Registered Nurse",
        category="Healthcare",
        holland_code="SIC",
        o_net_code="29-1141.00",
        mbti_type="ISFJ",
        salary_range="$65K-$90K (mid), $90K-$120K (senior)",
        experience_required="High",
        keywords_strong=[
            "registered nurse", "rn", "nursing", "patient care",
            "bedside", "clinical care", "medication administration"
        ],
        keywords_moderate=[
            "healthcare", "hospital", "clinic", "patient assessment",
            "care plan", "vitals", "charting", "emr"
        ],
        keywords_weak=[
            "compassion", "patient education", "triage", "care coordination"
        ],
        contra_keywords=["software", "coding", "accounting"],
        description="Provides and coordinates patient care in clinical settings.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Physician Assistant",
        category="Healthcare",
        holland_code="SIR",
        o_net_code="29-1071.00",
        mbti_type="ESFJ",
        salary_range="$95K-$130K (mid), $130K-$170K (senior)",
        experience_required="High",
        keywords_strong=[
            "physician assistant", "pa-c", "medical provider",
            "diagnose", "treatment plan", "clinical practice"
        ],
        keywords_moderate=[
            "healthcare", "patient examination", "prescribe",
            "primary care", "medical history", "procedures"
        ],
        keywords_weak=[
            "patient care", "health assessment", "referral"
        ],
        contra_keywords=["it support", "web design"],
        description="Practices medicine alongside physicians, diagnosing and treating patients.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Physical Therapist",
        category="Healthcare",
        holland_code="SIR",
        o_net_code="29-1123.00",
        mbti_type="ISFJ",
        salary_range="$75K-$100K (mid), $100K-$130K (senior)",
        experience_required="High",
        keywords_strong=[
            "physical therapist", "physiotherapy", "rehabilitation",
            "physical therapy", "mobility", "exercise therapy"
        ],
        keywords_moderate=[
            "patient", "recovery", "musculoskeletal", "treatment plan",
            "manual therapy", "functional movement"
        ],
        keywords_weak=[
            "injury", "wellness", "healthcare", "pain management"
        ],
        contra_keywords=["coding", "sales"],
        description="Helps patients restore movement and manage pain through exercise and therapy.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Medical Laboratory Technician",
        category="Healthcare",
        holland_code="ICR",
        o_net_code="29-2010.00",
        mbti_type="ISTJ",
        salary_range="$50K-$70K (mid), $70K-$90K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "medical laboratory", "lab technician", "clinical laboratory",
            "specimen", "diagnostic testing", "microscopy"
        ],
        keywords_moderate=[
            "hematology", "chemistry", "microbiology", "quality control",
            "phlebotomy", "sample analysis", "lab equipment"
        ],
        keywords_weak=[
            "healthcare", "accuracy", "record keeping", "protocol"
        ],
        contra_keywords=["customer service", "retail"],
        description="Performs diagnostic laboratory tests on biological samples.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Pharmacist",
        category="Healthcare",
        holland_code="ICS",
        o_net_code="29-1051.00",
        mbti_type="ISTJ",
        salary_range="$110K-$140K (mid), $140K-$170K (senior)",
        experience_required="High",
        keywords_strong=[
            "pharmacist", "pharmacy", "medication", "prescription",
            "dispensing", "drug interaction"
        ],
        keywords_moderate=[
            "pharmacology", "patient counseling", "compounding",
            "pharmaceutical", "dosage", "regulatory"
        ],
        keywords_weak=[
            "healthcare", "accuracy", "inventory", "clinical"
        ],
        contra_keywords=["software", "marketing"],
        description="Dispenses medications and advises patients and providers on drug therapy.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Radiologic Technologist",
        category="Healthcare",
        holland_code="RSI",
        o_net_code="29-2034.00",
        mbti_type="ISTJ",
        salary_range="$55K-$75K (mid), $75K-$95K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "radiologic technologist", "radiology", "x-ray",
            "medical imaging", "diagnostic imaging", "mri", "ct"
        ],
        keywords_moderate=[
            "patient positioning", "radiation safety", "imaging equipment",
            "healthcare", "anatomy"
        ],
        keywords_weak=[
            "patient care", "record keeping", "quality"
        ],
        contra_keywords=["software development", "finance"],
        description="Operates imaging equipment to capture diagnostic images of patients.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Occupational Therapist",
        category="Healthcare",
        holland_code="SIA",
        o_net_code="29-1122.00",
        mbti_type="ENFJ",
        salary_range="$75K-$100K (mid), $100K-$130K (senior)",
        experience_required="High",
        keywords_strong=[
            "occupational therapist", "occupational therapy",
            "rehabilitation", "daily living skills", "adaptive"
        ],
        keywords_moderate=[
            "patient", "therapy", "fine motor", "sensory",
            "treatment plan", "independence"
        ],
        keywords_weak=[
            "healthcare", "wellness", "compassion", "assessment"
        ],
        contra_keywords=["coding", "accounting"],
        description="Helps patients develop or regain skills for daily living and work.",
        pivot_cost="High",
    ),

    # ─── Business & Finance ────────────────────────────────────────────────
    RoleProfile(
        title="Accountant",
        category="Business & Finance",
        holland_code="CEI",
        o_net_code="13-2011.00",
        mbti_type="ISTJ",
        salary_range="$55K-$80K (mid), $80K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "accountant", "accounting", "bookkeeping", "general ledger",
            "accounts payable", "accounts receivable", "financial statements"
        ],
        keywords_moderate=[
            "gaap", "tax preparation", "audit", "reconciliation",
            "quickbooks", "excel", "payroll", "journal entries"
        ],
        keywords_weak=[
            "budgeting", "financial reporting", "invoice", "compliance"
        ],
        contra_keywords=["software development", "clinical"],
        description="Prepares and reviews financial records, tax filings, and reports.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Financial Analyst",
        category="Business & Finance",
        holland_code="ICE",
        o_net_code="13-2051.00",
        mbti_type="ISTJ",
        salary_range="$65K-$95K (mid), $95K-$140K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "financial analyst", "financial analysis", "valuation",
            "financial modeling", "budget", "forecast", "investment analysis"
        ],
        keywords_moderate=[
            "excel", "financial statements", "variance analysis",
            "capital", "portfolio", "pricing", "reporting"
        ],
        keywords_weak=[
            "data analysis", "kpi", "strategic", "risk"
        ],
        contra_keywords=["nursing", "construction"],
        description="Analyzes financial data to guide investment and business decisions.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Marketing Manager",
        category="Business & Finance",
        holland_code="EAC",
        o_net_code="11-2021.00",
        mbti_type="ENTP",
        salary_range="$75K-$110K (mid), $110K-$160K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "marketing", "campaign", "brand", "digital marketing",
            "seo", "social media", "content marketing", "advertising"
        ],
        keywords_moderate=[
            "market research", "lead generation", "email marketing",
            "google analytics", "crm", "positioning", "strategy"
        ],
        keywords_weak=[
            "communication", "creative", "public relations", "growth"
        ],
        contra_keywords=["server administration", "lab technician"],
        description="Plans and executes marketing campaigns to grow a brand and its audience.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Human Resources Specialist",
        category="Business & Finance",
        holland_code="SEC",
        o_net_code="13-1071.00",
        mbti_type="ESFJ",
        salary_range="$55K-$80K (mid), $80K-$115K (senior)",
        experience_required="Low",
        keywords_strong=[
            "human resources", "hr", "recruiting", "recruitment",
            "talent acquisition", "onboarding", "employee relations"
        ],
        keywords_moderate=[
            "benefits", "payroll", "performance management",
            "compliance", "hiring", "interviewing", "training"
        ],
        keywords_weak=[
            "communication", "people", "policy", "conflict resolution"
        ],
        contra_keywords=["programming", "mechanical"],
        description="Manages hiring, benefits, employee relations, and workplace policies.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Sales Representative",
        category="Business & Finance",
        holland_code="ECR",
        o_net_code="41-4012.00",
        mbti_type="ESTP",
        salary_range="$50K-$80K (base+commission), $80K-$150K (senior)",
        experience_required="Low",
        keywords_strong=[
            "sales", "account executive", "business development",
            "prospecting", "negotiation", "quota", "pipeline"
        ],
        keywords_moderate=[
            "crm", "cold calling", "customer relationship",
            "closing", "lead generation", "territory", "revenue"
        ],
        keywords_weak=[
            "communication", "persuasion", "relationship", "presentation"
        ],
        contra_keywords=["software development", "laboratory"],
        description="Sells products or services and builds client relationships.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Project Manager",
        category="Business & Finance",
        holland_code="ECI",
        o_net_code="13-1082.00",
        mbti_type="ENTJ",
        salary_range="$75K-$110K (mid), $110K-$150K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "project manager", "project management", "pmp",
            "stakeholder", "budget", "timeline", "deliverables", "scrum master"
        ],
        keywords_moderate=[
            "agile", "waterfall", "risk management", "scheduling",
            "resource planning", "gantt", "roadmap", "coordination"
        ],
        keywords_weak=[
            "leadership", "communication", "planning", "execution"
        ],
        contra_keywords=[],
        description="Plans and leads projects to completion on time and budget.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Business Analyst",
        category="Business & Finance",
        holland_code="IEC",
        o_net_code="13-1111.00",
        mbti_type="INTJ",
        salary_range="$65K-$95K (mid), $95K-$135K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "business analyst", "requirements", "stakeholder",
            "process improvement", "gap analysis", "use case"
        ],
        keywords_moderate=[
            "data analysis", "sql", "documentation", "workflow",
            "kpi", "reporting", "agile", "user story"
        ],
        keywords_weak=[
            "analysis", "problem solving", "facilitation", "strategy"
        ],
        contra_keywords=[],
        description="Bridges business needs and technical solutions through analysis.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Operations Manager",
        category="Business & Finance",
        holland_code="ECR",
        o_net_code="11-1021.00",
        mbti_type="ESTJ",
        salary_range="$70K-$105K (mid), $105K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "operations manager", "operations", "logistics",
            "supply chain", "process optimization", "team management"
        ],
        keywords_moderate=[
            "budgeting", "scheduling", "inventory", "vendor management",
            "efficiency", "kpi", "staffing", "quality control"
        ],
        keywords_weak=[
            "leadership", "planning", "coordination", "reporting"
        ],
        contra_keywords=["nursing", "creative writing"],
        description="Oversees daily operations, logistics, and team performance.",
        pivot_cost="Medium",
    ),

    # ─── Engineering ───────────────────────────────────────────────────────
    RoleProfile(
        title="Mechanical Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2141.00",
        mbti_type="INTJ",
        salary_range="$70K-$100K (mid), $100K-$140K (senior)",
        experience_required="High",
        keywords_strong=[
            "mechanical engineer", "mechanical engineering", "cad",
            "solidworks", "autocad", "thermal", "manufacturing design"
        ],
        keywords_moderate=[
            "finite element", "prototype", "materials", "tolerance",
            "fabrication", "design", "simulation", "gd&t"
        ],
        keywords_weak=[
            "problem solving", "technical drawing", "testing", "quality"
        ],
        contra_keywords=["nursing", "marketing"],
        description="Designs mechanical systems, components, and manufacturing processes.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Civil Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2051.00",
        mbti_type="ISTJ",
        salary_range="$70K-$100K (mid), $100K-$140K (senior)",
        experience_required="High",
        keywords_strong=[
            "civil engineer", "civil engineering", "structural",
            "infrastructure", "construction", "site development", "autocad"
        ],
        keywords_moderate=[
            "surveying", "concrete", "steel", "permitting",
            "transportation", "hydraulics", "geotechnical"
        ],
        keywords_weak=[
            "project", "design", "regulatory", "environmental"
        ],
        contra_keywords=["software", "clinical"],
        description="Designs and oversees roads, bridges, buildings, and infrastructure.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Electrical Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2071.00",
        mbti_type="INTJ",
        salary_range="$75K-$110K (mid), $110K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "electrical engineer", "electrical engineering",
            "circuit", "power systems", "pcb", "embedded", "electronics"
        ],
        keywords_moderate=[
            "hardware", "schematic", "microcontroller", "signal processing",
            "automation", "fpga", "control systems", "instrumentation"
        ],
        keywords_weak=[
            "design", "testing", "prototype", "troubleshooting"
        ],
        contra_keywords=["marketing", "counseling"],
        description="Designs electrical systems, circuits, and electronic devices.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Chemical Engineer",
        category="Engineering",
        holland_code="IRE",
        o_net_code="17-2041.00",
        mbti_type="INTJ",
        salary_range="$80K-$115K (mid), $115K-$160K (senior)",
        experience_required="High",
        keywords_strong=[
            "chemical engineer", "chemical engineering", "process engineering",
            "reactor", "distillation", "polymer", "petrochemical"
        ],
        keywords_moderate=[
            "thermodynamics", "fluid", "mass transfer", "plant",
            "scale-up", "safety", "process control", "chemistry"
        ],
        keywords_weak=[
            "optimization", "manufacturing", "design", "quality"
        ],
        contra_keywords=["it support", "sales"],
        description="Designs and optimizes chemical production processes and plants.",
        pivot_cost="High",
    ),

    # ─── Science ───────────────────────────────────────────────────────────
    RoleProfile(
        title="Chemist",
        category="Science",
        holland_code="IAR",
        o_net_code="19-2031.00",
        mbti_type="INTP",
        salary_range="$60K-$90K (mid), $90K-$130K (senior)",
        experience_required="High",
        keywords_strong=[
            "chemist", "chemistry", "laboratory", "analytical chemistry",
            "synthesis", "chromatography", "spectroscopy"
        ],
        keywords_moderate=[
            "research", "experiment", "compound", "titration",
            "quality control", "formulation", "instrumentation"
        ],
        keywords_weak=[
            "scientific method", "documentation", "data analysis", "safety"
        ],
        contra_keywords=["retail", "accounting"],
        description="Studies substances and develops new materials, compounds, and processes.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Biologist",
        category="Science",
        holland_code="IAR",
        o_net_code="19-1020.00",
        mbti_type="INTP",
        salary_range="$55K-$85K (mid), $85K-$120K (senior)",
        experience_required="High",
        keywords_strong=[
            "biologist", "biology", "research", "laboratory",
            "cell", "genetics", "molecular", "organism"
        ],
        keywords_moderate=[
            "experiment", "microscopy", "pcr", "assay", "data",
            "ecology", "microbiology", "field research"
        ],
        keywords_weak=[
            "scientific", "documentation", "analysis", "specimen"
        ],
        contra_keywords=["sales", "finance"],
        description="Studies living organisms and biological processes through research.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Environmental Scientist",
        category="Science",
        holland_code="IAR",
        o_net_code="19-2041.00",
        mbti_type="INFP",
        salary_range="$60K-$90K (mid), $90K-$125K (senior)",
        experience_required="High",
        keywords_strong=[
            "environmental scientist", "environmental science",
            "sustainability", "ecology", "conservation", "climate", "compliance"
        ],
        keywords_moderate=[
            "field sampling", "water quality", "air quality", "gis",
            "environmental impact", "regulation", "monitoring", "remediation"
        ],
        keywords_weak=[
            "research", "data analysis", "reporting", "policy"
        ],
        contra_keywords=["software development", "accounting"],
        description="Studies the environment and develops solutions for sustainability and compliance.",
        pivot_cost="High",
    ),

    # ─── Education ─────────────────────────────────────────────────────────
    RoleProfile(
        title="Teacher (K-12)",
        category="Education",
        holland_code="SAI",
        o_net_code="25-2031.00",
        mbti_type="ENFJ",
        salary_range="$45K-$65K (mid), $65K-$90K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "teacher", "teaching", "classroom", "lesson plan",
            "curriculum", "education", "student", "instruction"
        ],
        keywords_moderate=[
            "lesson", "grading", "classroom management", "pedagogy",
            "assessment", "special education", "literacy"
        ],
        keywords_weak=[
            "mentoring", "communication", "planning", "engagement"
        ],
        contra_keywords=["server administration", "surgery"],
        description="Plans and delivers instruction to students in a classroom setting.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="College Professor",
        category="Education",
        holland_code="SIA",
        o_net_code="25-1011.00",
        mbti_type="INTJ",
        salary_range="$65K-$100K (mid), $100K-$160K (senior)",
        experience_required="High",
        keywords_strong=[
            "professor", "lecturer", "faculty", "higher education",
            "university", "lecture", "research", "academic"
        ],
        keywords_moderate=[
            "teaching", "curriculum", "publication", "seminar",
            "advising", "dissertation", "grant", "peer review"
        ],
        keywords_weak=[
            "scholarship", "mentoring", "instruction", "conference"
        ],
        contra_keywords=["retail", "construction"],
        description="Teaches, researches, and mentors students at the college level.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="School Counselor",
        category="Education",
        holland_code="SAI",
        o_net_code="21-1012.00",
        mbti_type="ENFJ",
        salary_range="$50K-$75K (mid), $75K-$100K (senior)",
        experience_required="High",
        keywords_strong=[
            "school counselor", "guidance counselor", "student counseling",
            "academic advising", "career counseling", "student support"
        ],
        keywords_moderate=[
            "counseling", "education", "student", "intervention",
            "social-emotional", "college planning", "advocacy"
        ],
        keywords_weak=[
            "communication", "listening", "support", "mentoring"
        ],
        contra_keywords=["software development", "manufacturing"],
        description="Supports students' academic, social, and career development.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Librarian",
        category="Education",
        holland_code="CAI",
        o_net_code="25-4022.00",
        mbti_type="ISFJ",
        salary_range="$45K-$65K (mid), $65K-$85K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "librarian", "library", "cataloging", "archives",
            "information science", "reference", "collection"
        ],
        keywords_moderate=[
            "research", "database", "classification", "metadata",
            "outreach", "digital resources", "circulation"
        ],
        keywords_weak=[
            "organization", "customer service", "documentation", "literacy"
        ],
        contra_keywords=["construction", "surgery"],
        description="Manages information resources and helps people find what they need.",
        pivot_cost="Medium",
    ),

    # ─── Creative & Media ──────────────────────────────────────────────────
    RoleProfile(
        title="Graphic Designer",
        category="Creative & Media",
        holland_code="ARI",
        o_net_code="27-1024.00",
        mbti_type="INFP",
        salary_range="$45K-$70K (mid), $70K-$105K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "graphic designer", "graphic design", "adobe photoshop",
            "adobe illustrator", "indesign", "branding", "layout", "typography"
        ],
        keywords_moderate=[
            "logo", "print", "visual design", "illustration",
            "color theory", "creative", "adobe creative"
        ],
        keywords_weak=[
            "design", "marketing", "portfolio", "client"
        ],
        contra_keywords=["accounting", "surgery"],
        description="Creates visual designs for print, digital, and brand materials.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Writer / Author",
        category="Creative & Media",
        holland_code="AIS",
        o_net_code="27-3043.00",
        mbti_type="INFP",
        salary_range="$45K-$75K (mid), $75K-$120K+ (established)",
        experience_required="Medium",
        keywords_strong=[
            "writer", "author", "writing", "copywriting",
            "content writing", "editorial", "manuscript", "storytelling"
        ],
        keywords_moderate=[
            "editing", "proofreading", "publishing", "blog",
            "creative writing", "research", "narrative"
        ],
        keywords_weak=[
            "communication", "grammar", "style", "voice"
        ],
        contra_keywords=["surgery", "construction"],
        description="Writes content, stories, and copy across print and digital media.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Journalist / Reporter",
        category="Creative & Media",
        holland_code="ASE",
        o_net_code="27-3023.00",
        mbti_type="ENFP",
        salary_range="$45K-$75K (mid), $75K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "journalist", "reporter", "news", "reporting",
            "investigative", "article", "interview", "editorial"
        ],
        keywords_moderate=[
            "writing", "editing", "broadcast", "media", "deadline",
            "fact-checking", "story", "source"
        ],
        keywords_weak=[
            "communication", "research", "current events", "publishing"
        ],
        contra_keywords=["software development", "accounting"],
        description="Reports news and stories through research, interviews, and writing.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Public Relations Specialist",
        category="Creative & Media",
        holland_code="EAS",
        o_net_code="27-3031.00",
        mbti_type="ENFP",
        salary_range="$50K-$80K (mid), $80K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "public relations", "pr", "media relations",
            "press release", "communications", "reputation", "outreach"
        ],
        keywords_moderate=[
            "social media", "branding", "crisis communication",
            "event", "messaging", "journalism", "stakeholder"
        ],
        keywords_weak=[
            "writing", "communication", "networking", "strategy"
        ],
        contra_keywords=["lab technician", "plumbing"],
        description="Manages an organization's public image and media relationships.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Interior Designer",
        category="Creative & Media",
        holland_code="AER",
        o_net_code="27-1025.00",
        mbti_type="ENFP",
        salary_range="$50K-$75K (mid), $75K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "interior designer", "interior design", "space planning",
            "furnishings", "decor", "lighting design", "autocad", "sketchup"
        ],
        keywords_moderate=[
            "color", "materials", "layout", "client", "renovation",
            "aesthetic", "floor plan", "3d rendering"
        ],
        keywords_weak=[
            "creative", "design", "presentation", "budget"
        ],
        contra_keywords=["programming", "accounting"],
        description="Designs functional and appealing interior spaces for homes and businesses.",
        pivot_cost="Medium",
    ),

    # ─── Skilled Trades ────────────────────────────────────────────────────
    RoleProfile(
        title="Electrician",
        category="Skilled Trades",
        holland_code="RIE",
        o_net_code="47-2111.00",
        mbti_type="ISTP",
        salary_range="$50K-$75K (journey), $75K-$110K (master)",
        experience_required="Medium",
        keywords_strong=[
            "electrician", "electrical", "wiring", "circuit",
            "breaker", "conduit", "voltage", "national electrical code"
        ],
        keywords_moderate=[
            "installation", "maintenance", "troubleshooting",
            "panel", "lighting", "inspection", "safety"
        ],
        keywords_weak=[
            "repair", "blueprint", "hand tools", "residential", "commercial"
        ],
        contra_keywords=["software", "finance"],
        description="Installs, maintains, and repairs electrical systems and wiring.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Plumber",
        category="Skilled Trades",
        holland_code="RIC",
        o_net_code="47-2152.00",
        mbti_type="ISTP",
        salary_range="$50K-$75K (journey), $75K-$110K (master)",
        experience_required="Medium",
        keywords_strong=[
            "plumber", "plumbing", "pipe", "fixture", "drain",
            "water heater", "sewer", "copper", "pvc"
        ],
        keywords_moderate=[
            "installation", "repair", "maintenance", "leak",
            "backflow", "fitting", "inspection", "code"
        ],
        keywords_weak=[
            "residential", "commercial", "troubleshooting", "hand tools"
        ],
        contra_keywords=["software development", "accounting"],
        description="Installs and repairs water, gas, and drainage systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="HVAC Technician",
        category="Skilled Trades",
        holland_code="RIE",
        o_net_code="49-9021.00",
        mbti_type="ISTP",
        salary_range="$48K-$70K (mid), $70K-$100K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "hvac", "heating", "ventilation", "air conditioning",
            "refrigeration", "hvac technician", "furnace"
        ],
        keywords_moderate=[
            "installation", "maintenance", "repair", "refrigerant",
            "ductwork", "thermostat", "epa", "diagnostics"
        ],
        keywords_weak=[
            "residential", "commercial", "troubleshooting", "safety"
        ],
        contra_keywords=["software", "marketing"],
        description="Installs and services heating, ventilation, and cooling systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Welder",
        category="Skilled Trades",
        holland_code="RCE",
        o_net_code="51-4121.00",
        mbti_type="ISTP",
        salary_range="$40K-$60K (mid), $60K-$90K (specialized)",
        experience_required="Low",
        keywords_strong=[
            "welder", "welding", "mig", "tig", "arc welding",
            "fabrication", "metal", "torch"
        ],
        keywords_moderate=[
            "blueprint", "soldering", "grinding", "safety",
            "steel", "aluminum", "inspection", "fitting"
        ],
        keywords_weak=[
            "manufacturing", "construction", "hand tools", "quality"
        ],
        contra_keywords=["office", "writing"],
        description="Joins and fabricates metal components using welding techniques.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Carpenter",
        category="Skilled Trades",
        holland_code="RCE",
        o_net_code="47-2031.00",
        mbti_type="ISTP",
        salary_range="$45K-$65K (mid), $65K-$95K (senior)",
        experience_required="Low",
        keywords_strong=[
            "carpenter", "carpentry", "framing", "woodworking",
            "cabinetry", "blueprint", "finish work"
        ],
        keywords_moderate=[
            "construction", "saw", "measure", "installation",
            "drywall", "remodel", "materials", "safety"
        ],
        keywords_weak=[
            "residential", "commercial", "hand tools", "repair"
        ],
        contra_keywords=["office", "software"],
        description="Builds, installs, and repairs wooden structures and fixtures.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Automotive Technician",
        category="Skilled Trades",
        holland_code="RIC",
        o_net_code="49-3023.00",
        mbti_type="ISTP",
        salary_range="$45K-$65K (mid), $65K-$95K (master)",
        experience_required="Low",
        keywords_strong=[
            "automotive technician", "mechanic", "auto repair",
            "diagnostic", "engine", "transmission", "brake"
        ],
        keywords_moderate=[
            "vehicle", "maintenance", "obd", "suspension",
            "electrical", "troubleshooting", "inspection", "tools"
        ],
        keywords_weak=[
            "repair", "customer service", "safety", "parts"
        ],
        contra_keywords=["software development", "finance"],
        description="Diagnoses and repairs vehicles' mechanical and electrical systems.",
        pivot_cost="High",
    ),

    # ─── Social Services, Law & Public Safety ──────────────────────────────
    RoleProfile(
        title="Social Worker",
        category="Social Services",
        holland_code="SIA",
        o_net_code="21-1021.00",
        mbti_type="ENFJ",
        salary_range="$50K-$70K (mid), $70K-$95K (clinical)",
        experience_required="High",
        keywords_strong=[
            "social worker", "social work", "case management",
            "counseling", "client advocacy", "community services"
        ],
        keywords_moderate=[
            "mental health", "family", "intervention", "crisis",
            "referral", "support", "vulnerable", "assessment"
        ],
        keywords_weak=[
            "compassion", "listening", "outreach", "documentation"
        ],
        contra_keywords=["software development", "manufacturing"],
        description="Helps individuals and families navigate challenges and access services.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Clinical Psychologist",
        category="Social Services",
        holland_code="SIA",
        o_net_code="19-3033.00",
        mbti_type="INFJ",
        salary_range="$70K-$105K (mid), $105K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "psychologist", "psychology", "therapy", "counseling",
            "mental health", "clinical", "assessment", "psychotherapy"
        ],
        keywords_moderate=[
            "diagnosis", "behavioral", "cognitive", "patient",
            "treatment plan", "research", "evaluation"
        ],
        keywords_weak=[
            "empathy", "listening", "wellness", "support"
        ],
        contra_keywords=["programming", "accounting"],
        description="Assesses and treats mental, emotional, and behavioral conditions.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Lawyer",
        category="Legal",
        holland_code="EIA",
        o_net_code="23-1011.00",
        mbti_type="ENTJ",
        salary_range="$90K-$140K (mid), $140K-$220K+ (senior)",
        experience_required="High",
        keywords_strong=[
            "lawyer", "attorney", "legal", "litigation",
            "counsel", "contract", "case", "client representation"
        ],
        keywords_moderate=[
            "legal research", "brief", "negotiation", "deposition",
            "compliance", "statute", "court", "advocacy"
        ],
        keywords_weak=[
            "argumentation", "writing", "analysis", "ethics"
        ],
        contra_keywords=["surgery", "construction"],
        description="Advises and represents clients on legal matters and disputes.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Paralegal",
        category="Legal",
        holland_code="CEI",
        o_net_code="23-2011.00",
        mbti_type="ISTJ",
        salary_range="$50K-$70K (mid), $70K-$95K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "paralegal", "legal assistant", "legal research",
            "case management", "document", "litigation support"
        ],
        keywords_moderate=[
            "filing", "discovery", "contract", "court",
            "drafting", "compliance", "deadline", "correspondence"
        ],
        keywords_weak=[
            "organization", "attention to detail", "writing", "research"
        ],
        contra_keywords=["nursing", "construction"],
        description="Supports lawyers with research, documents, and case preparation.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Police Officer",
        category="Public Safety",
        holland_code="RES",
        o_net_code="33-3051.00",
        mbti_type="ESTJ",
        salary_range="$50K-$80K (mid), $80K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "police officer", "law enforcement", "patrol",
            "public safety", "emergency response", "investigation"
        ],
        keywords_moderate=[
            "arrest", "report", "community", "dispatch",
            "traffic", "surveillance", "criminal", "training"
        ],
        keywords_weak=[
            "safety", "communication", "physical fitness", "judgment"
        ],
        contra_keywords=["software development", "accounting"],
        description="Protects the public, enforces laws, and responds to emergencies.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Firefighter",
        category="Public Safety",
        holland_code="RSE",
        o_net_code="33-2011.00",
        mbti_type="ESTJ",
        salary_range="$45K-$70K (mid), $70K-$100K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "firefighter", "firefighting", "fire suppression",
            "emergency response", "ems", "rescue"
        ],
        keywords_moderate=[
            "hazmat", "first responder", "dispatch", "safety",
            "equipment", "training", "ladder", "medical"
        ],
        keywords_weak=[
            "physical fitness", "teamwork", "courage", "public service"
        ],
        contra_keywords=["office", "programming"],
        description="Responds to fires and emergencies, protecting lives and property.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="EMT / Paramedic",
        category="Public Safety",
        holland_code="SRE",
        o_net_code="29-2042.00",
        mbti_type="ESFJ",
        salary_range="$38K-$55K (EMT), $55K-$80K (paramedic)",
        experience_required="Medium",
        keywords_strong=[
            "emt", "paramedic", "emergency medical", "ambulance",
            "emergency response", "first responder", "life support"
        ],
        keywords_moderate=[
            "patient care", "cpr", "trauma", "vitals",
            "dispatch", "medical", "triage", "transport"
        ],
        keywords_weak=[
            "safety", "communication", "teamwork", "compassion"
        ],
        contra_keywords=["software", "finance"],
        description="Provides emergency medical care and transport at the scene of emergencies.",
        pivot_cost="High",
    ),

    # ─── Operations & Administrative ───────────────────────────────────────
    RoleProfile(
        title="Administrative Assistant",
        category="Operations",
        holland_code="CES",
        o_net_code="43-6014.00",
        mbti_type="ISFJ",
        salary_range="$38K-$55K (mid), $55K-$75K (senior)",
        experience_required="Low",
        keywords_strong=[
            "administrative assistant", "office manager", "clerical",
            "scheduling", "calendar", "reception", "data entry"
        ],
        keywords_moderate=[
            "customer service", "filing", "correspondence",
            "office", "organization", "record keeping", "microsoft office"
        ],
        keywords_weak=[
            "communication", "multitasking", "attention to detail", "support"
        ],
        contra_keywords=["surgery", "engineering"],
        description="Provides clerical and organizational support to teams and offices.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Customer Service Representative",
        category="Operations",
        holland_code="SEC",
        o_net_code="43-4051.00",
        mbti_type="ESFJ",
        salary_range="$35K-$50K (mid), $50K-$70K (senior)",
        experience_required="Low",
        keywords_strong=[
            "customer service", "support", "call center",
            "client service", "help desk", "troubleshooting"
        ],
        keywords_moderate=[
            "communication", "ticketing", "escalation", "resolution",
            "phone", "email support", "crm", "satisfaction"
        ],
        keywords_weak=[
            "patience", "listening", "problem solving", "multitasking"
        ],
        contra_keywords=["surgery", "laboratory"],
        description="Assists customers with inquiries, issues, and account support.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Logistics / Supply Chain Specialist",
        category="Operations",
        holland_code="ECR",
        o_net_code="13-1081.00",
        mbti_type="ISTJ",
        salary_range="$55K-$80K (mid), $80K-$115K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "logistics", "supply chain", "inventory", "warehouse",
            "distribution", "procurement", "shipping", "freight"
        ],
        keywords_moderate=[
            "scheduling", "vendor", "forecasting", "erp",
            "transportation", "fulfillment", "purchasing", "routing"
        ],
        keywords_weak=[
            "coordination", "planning", "cost", "reporting"
        ],
        contra_keywords=["nursing", "creative writing"],
        description="Coordinates the movement, storage, and procurement of goods.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="GRC Analyst / Compliance Engineer",
        category="Technology",
        holland_code="CEI",
        o_net_code="13-1041.00",
        mbti_type="ISTJ",
        salary_range="$70K-$95K (mid), $95K-$130K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "compliance", "grc", "governance", "risk management",
            "iso 27001", "soc 2", "hipaa", "pci dss", "fedramp",
            "audit", "regulatory", "policy"
        ],
        keywords_moderate=[
            "control framework", "nist", "cobit", "risk assessment",
            "gap analysis", "remediation"
        ],
        keywords_weak=[
            "documentation", "procedure", "standard operating", "security policy"
        ],
        contra_keywords=["sales", "business development"],
        description="Manages governance, risk, and regulatory compliance programs.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Systems Architect",
        category="Technology",
        holland_code="IAR",
        o_net_code="15-1299.08",
        mbti_type="INTJ",
        salary_range="$110K-$150K (mid), $150K-$200K+ (senior)",
        experience_required="High",
        keywords_strong=[
            "architect", "architecture", "systems design", "solution design",
            "enterprise architecture", "technical strategy", "roadmap"
        ],
        keywords_moderate=[
            "cloud architecture", "microservices", "system integration",
            "scalability", "high availability", "technical leadership"
        ],
        keywords_weak=[
            "design patterns", "requirements analysis", "stakeholder"
        ],
        contra_keywords=[],
        description="Designs enterprise-scale systems and technical strategy.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Technical Writer",
        category="Creative & Media",
        holland_code="AIC",
        o_net_code="27-3042.00",
        mbti_type="ISTJ",
        salary_range="$65K-$95K (mid), $90K-$130K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "technical writer", "technical writing", "documentation",
            "knowledge base", "kb articles", "user guide", "api documentation",
            "technical documentation", "style guide", "confluence", "sphinx"
        ],
        keywords_moderate=[
            "writing", "editing", "proofreading", "content creation",
            "information architecture", "content strategy", "online help"
        ],
        keywords_weak=[
            "communication", "tutorial", "how-to", "runbook", "procedure", "sop"
        ],
        contra_keywords=[],
        description="Translates technical information into clear documentation and guides.",
        pivot_cost="None",
    ),
    RoleProfile(
        title="Medical Writer",
        category="Creative & Media",
        holland_code="AIS",
        o_net_code="27-3042.00",
        mbti_type="INFP",
        salary_range="$55K-$85K (entry-mid), $85K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "medical writer", "medical writing", "scientific writing",
            "regulatory writing", "clinical research", "pharma",
            "public health", "science communicat"
        ],
        keywords_moderate=[
            "research", "scientific", "biology", "chemistry", "healthcare",
            "medical", "clinical", "peer review", "publication", "journal"
        ],
        keywords_weak=[
            "writing", "communication", "grant writing", "proposal", "patient education"
        ],
        contra_keywords=[],
        description="Communicates scientific and medical information to varied audiences.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Instructional Designer",
        category="Education",
        holland_code="SAI",
        o_net_code="25-9031.00",
        mbti_type="ENFJ",
        salary_range="$60K-$90K (corporate), $85K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "instructional design", "curriculum", "e-learning", "learning management",
            "lms", "training development", "articulate", "captivate", "addie"
        ],
        keywords_moderate=[
            "training", "onboarding", "education", "teaching",
            "learning objectives", "assessment", "course design", "pedagogy"
        ],
        keywords_weak=[
            "documentation", "knowledge base", "procedure", "user adoption", "workshop"
        ],
        contra_keywords=[],
        description="Designs effective learning experiences and training programs.",
        pivot_cost="Medium",
    ),

    # ─── Aviation ──────────────────────────────────────────────────────────
    RoleProfile(
        title="Commercial Pilot",
        category="Aviation",
        holland_code="RIE",
        o_net_code="53-2012.00",
        mbti_type="ISTP",
        salary_range="$80K-$130K (mid), $130K-$250K+ (senior)",
        experience_required="High",
        keywords_strong=[
            "pilot", "aviation", "flight", "aircraft", "cockpit",
            "instrument", "navigation", "airline", "atp", "commercial pilot"
        ],
        keywords_moderate=[
            "faa", "flight plan", "radio", "takeoff", "landing",
            "altitude", "weather", "safety", "checklist", "crew"
        ],
        keywords_weak=[
            "avionics", "communication", "procedure", "coordination"
        ],
        contra_keywords=["software development", "accounting"],
        description="Operates aircraft to transport passengers and cargo safely.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Air Traffic Controller",
        category="Aviation",
        holland_code="RCE",
        o_net_code="53-2021.00",
        mbti_type="ISTJ",
        salary_range="$70K-$110K (mid), $110K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "air traffic", "air traffic control", "atc", "radar",
            "airspace", "clearance", "flight separation"
        ],
        keywords_moderate=[
            "aviation", "aircraft", "communication", "coordination",
            "emergency", "navigation", "safety"
        ],
        keywords_weak=[
            "monitoring", "procedure", "radio", "decision"
        ],
        contra_keywords=["nursing", "creative"],
        description="Directs aircraft movement to maintain safe, orderly air traffic flow.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Aircraft Mechanic",
        category="Aviation",
        holland_code="RIE",
        o_net_code="49-3011.00",
        mbti_type="ISTP",
        salary_range="$55K-$85K (mid), $85K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "aircraft mechanic", "airframe", "powerplant", "a&p",
            "aviation maintenance", "aircraft maintenance", "avionics"
        ],
        keywords_moderate=[
            "inspection", "repair", "turbine", "hydraulic", "faa",
            "engine", "troubleshooting", "safety"
        ],
        keywords_weak=[
            "mechanical", "tools", "documentation", "maintenance"
        ],
        contra_keywords=["software", "marketing"],
        description="Inspects, maintains, and repairs aircraft to ensure airworthiness.",
        pivot_cost="High",
    ),

    # ─── Veterinary ────────────────────────────────────────────────────────
    RoleProfile(
        title="Veterinarian",
        category="Veterinary",
        holland_code="IRS",
        o_net_code="29-1131.00",
        mbti_type="ISTJ",
        salary_range="$80K-$120K (mid), $120K-$180K (senior)",
        experience_required="High",
        keywords_strong=[
            "veterinarian", "veterinary", "animal medicine", "dvm",
            "animal care", "surgery", "diagnosis", "companion animal"
        ],
        keywords_moderate=[
            "animal", "clinical", "vaccination", "treatment",
            "patient", "preventive care", "radiograph"
        ],
        keywords_weak=[
            "healthcare", "compassion", "record keeping", "client"
        ],
        contra_keywords=["software development", "finance"],
        description="Diagnoses and treats diseases and injuries in animals.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Veterinary Technician",
        category="Veterinary",
        holland_code="RIS",
        o_net_code="29-2056.00",
        mbti_type="ISFJ",
        salary_range="$35K-$50K (mid), $50K-$70K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "veterinary technician", "vet tech", "animal nursing",
            "animal care", "patient monitoring", "anesthesia"
        ],
        keywords_moderate=[
            "animal", "laboratory", "radiography", "surgery",
            "medication", "client education", "restraint"
        ],
        keywords_weak=[
            "compassion", "record keeping", "sanitation", "assist"
        ],
        contra_keywords=["programming", "accounting"],
        description="Assists veterinarians with animal care, diagnostics, and procedures.",
        pivot_cost="High",
    ),

    # ─── Agriculture & Environment ─────────────────────────────────────────
    RoleProfile(
        title="Agronomist / Crop Scientist",
        category="Agriculture & Environment",
        holland_code="IRA",
        o_net_code="19-1013.00",
        mbti_type="ISTJ",
        salary_range="$55K-$80K (mid), $80K-$115K (senior)",
        experience_required="High",
        keywords_strong=[
            "agronom", "crop science", "agronomy", "soil", "agriculture",
            "crop", "plant science", "irrigation", "fertilizer"
        ],
        keywords_moderate=[
            "research", "field", "yield", "pest", "sustainability",
            "genetic", "harvest", "cultivation"
        ],
        keywords_weak=[
            "data", "analysis", "environment", "farming"
        ],
        contra_keywords=["software development", "retail"],
        description="Studies crops and soil to improve agricultural productivity.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Forester",
        category="Agriculture & Environment",
        holland_code="IRE",
        o_net_code="19-1032.00",
        mbti_type="ISTP",
        salary_range="$50K-$75K (mid), $75K-$105K (senior)",
        experience_required="High",
        keywords_strong=[
            "forester", "forestry", "forest", "timber", "silviculture",
            "conservation", "wildlife", "ecosystem"
        ],
        keywords_moderate=[
            "field", "land management", "surveying", "reforestation",
            "habitat", "resource", "environmental"
        ],
        keywords_weak=[
            "outdoor", "data", "mapping", "planning"
        ],
        contra_keywords=["software", "accounting"],
        description="Manages forests and woodlands for conservation and sustainable use.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Conservation Scientist",
        category="Agriculture & Environment",
        holland_code="IAR",
        o_net_code="19-1031.00",
        mbti_type="INFP",
        salary_range="$55K-$80K (mid), $80K-$115K (senior)",
        experience_required="High",
        keywords_strong=[
            "conservation", "ecology", "environmental science",
            "natural resource", "wildlife", "habitat", "biodiversity"
        ],
        keywords_moderate=[
            "field", "research", "ecosystem", "restoration",
            "sustainability", "land management", "monitoring"
        ],
        keywords_weak=[
            "data", "policy", "outdoor", "reporting"
        ],
        contra_keywords=["software development", "sales"],
        description="Protects and restores natural resources and ecosystems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Landscape Architect",
        category="Agriculture & Environment",
        holland_code="AIR",
        o_net_code="17-1012.00",
        mbti_type="INFP",
        salary_range="$60K-$90K (mid), $90K-$130K (senior)",
        experience_required="High",
        keywords_strong=[
            "landscape architect", "landscape design", "site planning",
            "outdoor space", "planting design", "sustainable design"
        ],
        keywords_moderate=[
            "autocad", "sketchup", "horticulture", "environmental",
            "grading", "drainage", "parks", "urban design"
        ],
        keywords_weak=[
            "design", "creative", "client", "presentation"
        ],
        contra_keywords=["software development", "finance"],
        description="Designs outdoor spaces, parks, and sustainable landscapes.",
        pivot_cost="High",
    ),

    # ─── Architecture & Construction ───────────────────────────────────────
    RoleProfile(
        title="Architect",
        category="Architecture & Construction",
        holland_code="AIR",
        o_net_code="17-1011.00",
        mbti_type="INTJ",
        salary_range="$70K-$105K (mid), $105K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "architect", "architecture", "building design", "blueprint",
            "revit", "autocad", "construction documents"
        ],
        keywords_moderate=[
            "structural", "building code", "schematic", "design",
            "client", "site", "sustainability", "zoning"
        ],
        keywords_weak=[
            "creative", "project", "coordination", "rendering"
        ],
        contra_keywords=["nursing", "accounting"],
        description="Designs buildings and oversees their construction.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Construction Manager",
        category="Architecture & Construction",
        holland_code="ECR",
        o_net_code="11-9021.00",
        mbti_type="ESTJ",
        salary_range="$75K-$115K (mid), $115K-$170K (senior)",
        experience_required="High",
        keywords_strong=[
            "construction manager", "construction", "site management",
            "project management", "subcontractor", "scheduling", "budget"
        ],
        keywords_moderate=[
            "blueprint", "safety", "building code", "estimating",
            "procurement", "coordination", "quality control"
        ],
        keywords_weak=[
            "leadership", "planning", "compliance", "inspection"
        ],
        contra_keywords=["software development", "clinical"],
        description="Plans and oversees construction projects from start to finish.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Land Surveyor",
        category="Architecture & Construction",
        holland_code="RIC",
        o_net_code="17-1022.00",
        mbti_type="ISTJ",
        salary_range="$50K-$75K (mid), $75K-$105K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "surveyor", "surveying", "boundary", "topographic",
            "gis", "gps", "mapping", "property line"
        ],
        keywords_moderate=[
            "measurement", "elevation", "autocad", "construction",
            "legal description", "field", "data collection"
        ],
        keywords_weak=[
            "precision", "documentation", "outdoor", "analysis"
        ],
        contra_keywords=["software development", "marketing"],
        description="Measures and maps land boundaries and topography.",
        pivot_cost="High",
    ),

    # ─── Real Estate ───────────────────────────────────────────────────────
    RoleProfile(
        title="Real Estate Agent",
        category="Real Estate",
        holland_code="ECS",
        o_net_code="41-9022.00",
        mbti_type="ENFP",
        salary_range="$45K-$80K (commission), $80K-$150K+ (top)",
        experience_required="Low",
        keywords_strong=[
            "real estate", "realtor", "property", "listing",
            "home buyer", "seller", "closing", "mansion"
        ],
        keywords_moderate=[
            "sales", "negotiation", "client", "marketing",
            "open house", "mls", "contract", "referral"
        ],
        keywords_weak=[
            "communication", "networking", "customer", "market"
        ],
        contra_keywords=["nursing", "laboratory"],
        description="Helps clients buy, sell, and rent properties.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Property Manager",
        category="Real Estate",
        holland_code="ECS",
        o_net_code="11-9141.00",
        mbti_type="ESTJ",
        salary_range="$50K-$75K (mid), $75K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "property manager", "property management", "tenant",
            "leasing", "landlord", "maintenance", "rental"
        ],
        keywords_moderate=[
            "lease", "occupancy", "vendor", "budget",
            "inspection", "resident", "collection", "hud"
        ],
        keywords_weak=[
            "customer service", "coordination", "reporting", "compliance"
        ],
        contra_keywords=["software development", "surgery"],
        description="Oversees the operation and maintenance of rental properties.",
        pivot_cost="Medium",
    ),

    # ─── Sports & Fitness ──────────────────────────────────────────────────
    RoleProfile(
        title="Athletic Trainer",
        category="Sports & Fitness",
        holland_code="SIR",
        o_net_code="29-9091.00",
        mbti_type="ESFJ",
        salary_range="$45K-$65K (mid), $65K-$90K (senior)",
        experience_required="High",
        keywords_strong=[
            "athletic trainer", "athletic training", "sports medicine",
            "injury prevention", "rehabilitation", "taping"
        ],
        keywords_moderate=[
            "athlete", "first aid", "exercise", "strength",
            "conditioning", "emergency", "patient"
        ],
        keywords_weak=[
            "sports", "fitness", "wellness", "education"
        ],
        contra_keywords=["accounting", "programming"],
        description="Prevents and treats athletic injuries and supports athlete performance.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Personal Trainer",
        category="Sports & Fitness",
        holland_code="SRE",
        o_net_code="39-9031.00",
        mbti_type="ESTP",
        salary_range="$35K-$55K (mid), $55K-$90K (top)",
        experience_required="Low",
        keywords_strong=[
            "personal trainer", "fitness", "strength training",
            "exercise", "workout", "personal training", "conditioning"
        ],
        keywords_moderate=[
            "client", "nutrition", "motivation", "program",
            "cardio", "weight training", "flexibility", "goal"
        ],
        keywords_weak=[
            "wellness", "health", "coaching", "instruction"
        ],
        contra_keywords=["software development", "finance"],
        description="Coaches clients to reach their fitness and health goals.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Sports Coach",
        category="Sports & Fitness",
        holland_code="SRE",
        o_net_code="27-2022.00",
        mbti_type="ESTJ",
        salary_range="$40K-$70K (mid), $70K-$120K (collegiate/pro)",
        experience_required="Medium",
        keywords_strong=[
            "coach", "coaching", "athletics", "team", "practice",
            "game strategy", "player development"
        ],
        keywords_moderate=[
            "training", "drill", "conditioning", "recruiting",
            "competition", "sports", "motivation"
        ],
        keywords_weak=[
            "leadership", "mentoring", "instruction", "discipline"
        ],
        contra_keywords=["accounting", "nursing"],
        description="Trains and develops athletes and teams to compete effectively.",
        pivot_cost="Medium",
    ),

    # ─── Hospitality & Tourism ─────────────────────────────────────────────
    RoleProfile(
        title="Chef / Head Cook",
        category="Hospitality & Tourism",
        holland_code="AER",
        o_net_code="35-1011.00",
        mbti_type="ISTP",
        salary_range="$45K-$70K (mid), $70K-$120K (executive)",
        experience_required="Medium",
        keywords_strong=[
            "chef", "cook", "culinary", "kitchen", "menu",
            "food preparation", "cuisine", "restaurant"
        ],
        keywords_moderate=[
            "recipe", "food safety", "line cook", "sous chef",
            "inventory", "plating", "ingredient"
        ],
        keywords_weak=[
            "creative", "team", "sanitation", "quality"
        ],
        contra_keywords=["software development", "accounting"],
        description="Plans menus and prepares food in a commercial kitchen.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Hotel Manager",
        category="Hospitality & Tourism",
        holland_code="ECS",
        o_net_code="11-9081.00",
        mbti_type="ESTJ",
        salary_range="$55K-$85K (mid), $85K-$130K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "hotel", "hospitality", "guest services", "front desk",
            "lodging", "resort", "housekeeping", "operations"
        ],
        keywords_moderate=[
            "customer service", "staff", "budget", "revenue",
            "reservation", "guest", "quality", "scheduling"
        ],
        keywords_weak=[
            "management", "coordination", "communication", "problem solving"
        ],
        contra_keywords=["laboratory", "programming"],
        description="Oversees the daily operations and guest experience of a hotel.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Event Planner",
        category="Hospitality & Tourism",
        holland_code="EAS",
        o_net_code="13-1121.00",
        mbti_type="ENFP",
        salary_range="$45K-$70K (mid), $70K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "event planner", "event planning", "event coordinator",
            "conference", "wedding", "coordination", "logistics"
        ],
        keywords_moderate=[
            "vendor", "budget", "venue", "catering",
            "registration", "scheduling", "client", "marketing"
        ],
        keywords_weak=[
            "organization", "communication", "creative", "networking"
        ],
        contra_keywords=["surgery", "engineering"],
        description="Plans and coordinates events, conferences, and celebrations.",
        pivot_cost="Medium",
    ),

    # ─── Manufacturing & Production ────────────────────────────────────────
    RoleProfile(
        title="Machinist",
        category="Manufacturing & Production",
        holland_code="RIC",
        o_net_code="51-4041.00",
        mbti_type="ISTP",
        salary_range="$45K-$65K (mid), $65K-$90K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "machinist", "cnc", "milling", "lathe", "machining",
            "blueprint", "metalworking", "precision"
        ],
        keywords_moderate=[
            "tooling", "tolerance", "setup", "fabrication",
            "measurement", "calibration", "manufacturing"
        ],
        keywords_weak=[
            "inspection", "quality", "safety", "mechanical"
        ],
        contra_keywords=["software development", "marketing"],
        description="Operates and sets up machine tools to produce precision parts.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Production Supervisor",
        category="Manufacturing & Production",
        holland_code="ECR",
        o_net_code="51-1011.00",
        mbti_type="ESTJ",
        salary_range="$55K-$80K (mid), $80K-$115K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "production supervisor", "production", "manufacturing",
            "assembly line", "shop floor", "throughput", "safety"
        ],
        keywords_moderate=[
            "staff", "scheduling", "quality", "lean",
            "continuous improvement", "inventory", "kpi"
        ],
        keywords_weak=[
            "leadership", "coordination", "training", "reporting"
        ],
        contra_keywords=["nursing", "creative writing"],
        description="Supervises manufacturing operations and production teams.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Quality Control Inspector",
        category="Manufacturing & Production",
        holland_code="CIR",
        o_net_code="51-9061.00",
        mbti_type="ISTJ",
        salary_range="$40K-$60K (mid), $60K-$85K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "quality control", "qc", "quality assurance", "inspection",
            "quality inspector", "defect", "measurement"
        ],
        keywords_moderate=[
            "specification", "calibration", "sampling", "tolerance",
            "compliance", "documentation", "audit", "testing"
        ],
        keywords_weak=[
            "precision", "reporting", "standard", "safety"
        ],
        contra_keywords=["sales", "creative"],
        description="Inspects products and processes to ensure quality standards.",
        pivot_cost="Medium",
    ),

    # ─── Transportation ────────────────────────────────────────────────────
    RoleProfile(
        title="Truck Driver",
        category="Transportation",
        holland_code="REC",
        o_net_code="53-3032.00",
        mbti_type="ISTP",
        salary_range="$45K-$65K (mid), $65K-$90K (senior)",
        experience_required="Low",
        keywords_strong=[
            "truck driver", "cdl", "trucking", "freight", "hauling",
            "tractor-trailer", "semi", "logistics"
        ],
        keywords_moderate=[
            "route", "delivery", "vehicle", "safety", "dispatch",
            "inspection", "loading", "transportation"
        ],
        keywords_weak=[
            "driving", "customer service", "schedule", "compliance"
        ],
        contra_keywords=["software development", "accounting"],
        description="Transports goods over long and regional routes.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Urban Planner",
        category="Government & Nonprofit",
        holland_code="IAE",
        o_net_code="19-3051.00",
        mbti_type="INTJ",
        salary_range="$60K-$90K (mid), $90K-$130K (senior)",
        experience_required="High",
        keywords_strong=[
            "urban planner", "urban planning", "city planning",
            "zoning", "land use", "community development", "gis"
        ],
        keywords_moderate=[
            "policy", "zoning code", "transportation", "public",
            "environmental", "stakeholder", "master plan", "ordinance"
        ],
        keywords_weak=[
            "analysis", "research", "reporting", "presentation"
        ],
        contra_keywords=["nursing", "construction"],
        description="Plans land use and development for cities and regions.",
        pivot_cost="High",
    ),

    # ─── Government & Nonprofit ─────────────────────────────────────────────
    RoleProfile(
        title="Policy Analyst",
        category="Government & Nonprofit",
        holland_code="IEA",
        o_net_code="19-3099.00",
        mbti_type="INTJ",
        salary_range="$55K-$85K (mid), $85K-$125K (senior)",
        experience_required="High",
        keywords_strong=[
            "policy analyst", "policy analysis", "public policy",
            "legislative", "regulatory", "research", "advocacy"
        ],
        keywords_moderate=[
            "data", "report", "stakeholder", "government",
            "analysis", "briefing", "evaluation", "proposal"
        ],
        keywords_weak=[
            "writing", "research", "communication", "statistics"
        ],
        contra_keywords=["nursing", "construction"],
        description="Analyzes and develops public policy and regulations.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Grant Writer",
        category="Government & Nonprofit",
        holland_code="AIS",
        o_net_code="13-1131.00",
        mbti_type="INFP",
        salary_range="$45K-$70K (mid), $70K-$100K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "grant writer", "grant writing", "proposal", "fundraising",
            "grant", "foundation", "rfa", "philanthropy"
        ],
        keywords_moderate=[
            "writing", "budget", "nonprofit", "donor",
            "research", "narrative", "application", "reporting"
        ],
        keywords_weak=[
            "communication", "editing", "deadline", "persuasion"
        ],
        contra_keywords=["surgery", "engineering"],
        description="Writes proposals to secure grant funding for organizations.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Nonprofit Program Manager",
        category="Government & Nonprofit",
        holland_code="ESA",
        o_net_code="11-9199.00",
        mbti_type="ENFJ",
        salary_range="$50K-$75K (mid), $75K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "program manager", "nonprofit", "community", "outreach",
            "program", "volunteer", "mission", "advocacy"
        ],
        keywords_moderate=[
            "budget", "grant", "stakeholder", "partnership",
            "impact", "fundraising", "evaluation", "reporting"
        ],
        keywords_weak=[
            "leadership", "coordination", "communication", "planning"
        ],
        contra_keywords=["software development", "manufacturing"],
        description="Manages programs that advance a nonprofit's mission.",
        pivot_cost="Medium",
    ),

    # ─── Energy & Utilities ────────────────────────────────────────────────
    RoleProfile(
        title="Power Plant Operator",
        category="Energy & Utilities",
        holland_code="RIC",
        o_net_code="51-8013.00",
        mbti_type="ISTJ",
        salary_range="$60K-$90K (mid), $90K-$120K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "power plant", "power generation", "turbine", "boiler",
            "electrical generation", "generator", "control room"
        ],
        keywords_moderate=[
            "equipment", "monitoring", "safety", "maintenance",
            "grid", "emergency", "compliance", "operation"
        ],
        keywords_weak=[
            "mechanical", "electrical", "procedure", "inspection"
        ],
        contra_keywords=["software development", "retail"],
        description="Operates and monitors power generation equipment.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Wind Turbine Technician",
        category="Energy & Utilities",
        holland_code="RIE",
        o_net_code="49-9081.00",
        mbti_type="ISTP",
        salary_range="$50K-$75K (mid), $75K-$100K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "wind turbine", "wind energy", "turbine", "renewable energy",
            "wind farm", "blade", "gearbox", "nacelle"
        ],
        keywords_moderate=[
            "maintenance", "inspection", "hydraulic", "electrical",
            "repair", "safety", "troubleshooting", "climbing"
        ],
        keywords_weak=[
            "mechanical", "tools", "documentation", "equipment"
        ],
        contra_keywords=["office", "finance"],
        description="Installs and maintains wind turbines and renewable energy systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Solar Installer",
        category="Energy & Utilities",
        holland_code="RIC",
        o_net_code="47-2231.00",
        mbti_type="ISTP",
        salary_range="$40K-$60K (mid), $60K-$85K (senior)",
        experience_required="Low",
        keywords_strong=[
            "solar", "solar panel", "solar installation", "photovoltaic",
            "pv", "renewable energy", "solar installer"
        ],
        keywords_moderate=[
            "installation", "electrical", "roofing", "wiring",
            "inverter", "safety", "inspection", "mounting"
        ],
        keywords_weak=[
            "construction", "troubleshooting", "tools", "customer"
        ],
        contra_keywords=["software development", "accounting"],
        description="Installs and maintains solar panel systems.",
        pivot_cost="Low",
    ),

    # ─── Arts & Entertainment ──────────────────────────────────────────────
    RoleProfile(
        title="Actor",
        category="Arts & Entertainment",
        holland_code="AES",
        o_net_code="27-2011.00",
        mbti_type="ENFP",
        salary_range="$40K-$80K (variable), $80K+ (established)",
        experience_required="Medium",
        keywords_strong=[
            "actor", "acting", "performance", "theatre", "theater",
            "stage", "film", "screen", "audition"
        ],
        keywords_moderate=[
            "character", "rehearsal", "voice", "improv", "drama",
            "cast", "director", "script"
        ],
        keywords_weak=[
            "creative", "communication", "expression", "interpretation"
        ],
        contra_keywords=["accounting", "engineering"],
        description="Performs roles in theater, film, television, and other media.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Musician / Singer",
        category="Arts & Entertainment",
        holland_code="AES",
        o_net_code="27-2042.00",
        mbti_type="INFP",
        salary_range="$35K-$70K (variable), $70K+ (established)",
        experience_required="Medium",
        keywords_strong=[
            "musician", "singer", "music", "vocal", "instrument",
            "performance", "composer", "recording", "band"
        ],
        keywords_moderate=[
            "composition", "songwriting", "rehearsal", "gig",
            "concert", "studio", "arrangement", "melody"
        ],
        keywords_weak=[
            "creative", "artistic", "expression", "audition"
        ],
        contra_keywords=["accounting", "nursing"],
        description="Performs, composes, and records music.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Photographer",
        category="Arts & Entertainment",
        holland_code="ARE",
        o_net_code="27-4021.00",
        mbti_type="ISFP",
        salary_range="$35K-$65K (mid), $65K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "photographer", "photography", "photo", "camera",
            "portrait", "lighting", "photoshop", "lightroom"
        ],
        keywords_moderate=[
            "editing", "studio", "shoot", "composition",
            "digital", "client", "visual", "portfolio"
        ],
        keywords_weak=[
            "creative", "artistic", "technical", "detail"
        ],
        contra_keywords=["accounting", "surgery"],
        description="Captures and edits photographic images for clients and media.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Art Director",
        category="Arts & Entertainment",
        holland_code="AER",
        o_net_code="27-1011.00",
        mbti_type="ENFP",
        salary_range="$70K-$105K (mid), $105K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "art director", "creative director", "art direction",
            "visual", "brand", "campaign", "design team"
        ],
        keywords_moderate=[
            "design", "creative", "typography", "layout",
            "concept", "client", "photography", "advertising"
        ],
        keywords_weak=[
            "leadership", "presentation", "aesthetic", "coordination"
        ],
        contra_keywords=["accounting", "nursing"],
        description="Directs the visual style and creative output of projects.",
        pivot_cost="Medium",
    ),

    # ─── Healthcare specialties ────────────────────────────────────────────
    RoleProfile(
        title="Nurse Practitioner",
        category="Healthcare",
        holland_code="SIC",
        o_net_code="29-1171.00",
        mbti_type="INTJ",
        salary_range="$95K-$125K (mid), $125K-$160K (senior)",
        experience_required="High",
        keywords_strong=[
            "nurse practitioner", "np", "advanced practice", "diagnose",
            "prescribe", "primary care", "patient management"
        ],
        keywords_moderate=[
            "nursing", "clinical", "treatment plan", "healthcare",
            "assessment", "chronic care", "patient education"
        ],
        keywords_weak=[
            "patient", "care", "coordination", "wellness"
        ],
        contra_keywords=["software development", "sales"],
        description="Provides advanced nursing care, diagnosing and treating patients.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Dentist",
        category="Healthcare",
        holland_code="IRS",
        o_net_code="29-1021.00",
        mbti_type="ISTJ",
        salary_range="$120K-$180K (mid), $180K-$250K+ (senior)",
        experience_required="High",
        keywords_strong=[
            "dentist", "dentistry", "dental", "oral health",
            "dental care", "cavity", "orthodontic", "prosthodontic"
        ],
        keywords_moderate=[
            "patient", "clinical", "diagnosis", "restoration",
            "extraction", "hygiene", "radiography", "treatment"
        ],
        keywords_weak=[
            "healthcare", "precision", "compassion", "record"
        ],
        contra_keywords=["software", "finance"],
        description="Diagnoses and treats conditions of the teeth and mouth.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Dental Hygienist",
        category="Healthcare",
        holland_code="SRI",
        o_net_code="29-1292.00",
        mbti_type="ISFJ",
        salary_range="$60K-$85K (mid), $85K-$110K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "dental hygienist", "dental hygiene", "oral hygiene",
            "cleaning", "scaling", "periodontal", "prophylaxis"
        ],
        keywords_moderate=[
            "patient", "radiography", "preventive care",
            "education", "dental", "healthcare", "charting"
        ],
        keywords_weak=[
            "compassion", "assist", "record keeping", "sanitation"
        ],
        contra_keywords=["software development", "accounting"],
        description="Cleans teeth and educates patients on oral hygiene.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Speech-Language Pathologist",
        category="Healthcare",
        holland_code="SIA",
        o_net_code="29-1127.00",
        mbti_type="INFJ",
        salary_range="$65K-$95K (mid), $95K-$130K (senior)",
        experience_required="High",
        keywords_strong=[
            "speech-language pathologist", "speech therapy",
            "speech pathologist", "communication disorder", "swallowing"
        ],
        keywords_moderate=[
            "patient", "therapy", "language", "articulation",
            "assessment", "treatment", "pediatric", "rehabilitation"
        ],
        keywords_weak=[
            "communication", "healthcare", "education", "compassion"
        ],
        contra_keywords=["accounting", "manufacturing"],
        description="Assesses and treats speech, language, and swallowing disorders.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Dietitian / Nutritionist",
        category="Healthcare",
        holland_code="SIA",
        o_net_code="29-1031.00",
        mbti_type="INFJ",
        salary_range="$55K-$80K (mid), $80K-$110K (senior)",
        experience_required="High",
        keywords_strong=[
            "dietitian", "nutritionist", "nutrition", "dietary",
            "meal planning", "clinical nutrition", "food science"
        ],
        keywords_moderate=[
            "patient", "counseling", "wellness", "healthcare",
            "assessment", "education", "diabetes", "weight management"
        ],
        keywords_weak=[
            "health", "care", "planning", "communication"
        ],
        contra_keywords=["software development", "construction"],
        description="Assesses nutritional needs and plans diets for health and wellness.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Mental Health Counselor",
        category="Healthcare",
        holland_code="SIA",
        o_net_code="21-1014.00",
        mbti_type="INFJ",
        salary_range="$45K-$70K (mid), $70K-$100K (clinical)",
        experience_required="High",
        keywords_strong=[
            "mental health counselor", "counseling", "therapy",
            "mental health", "psychotherapy", "behavioral health", "client"
        ],
        keywords_moderate=[
            "patient", "treatment plan", "crisis", "addiction",
            "anxiety", "depression", "trauma", "assessment"
        ],
        keywords_weak=[
            "empathy", "listening", "wellness", "support"
        ],
        contra_keywords=["software development", "manufacturing"],
        description="Provides counseling and therapy for mental and emotional health.",
        pivot_cost="High",
    ),

    # ─── Engineering specialties ───────────────────────────────────────────
    RoleProfile(
        title="Aerospace Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2011.00",
        mbti_type="INTJ",
        salary_range="$85K-$125K (mid), $125K-$175K (senior)",
        experience_required="High",
        keywords_strong=[
            "aerospace engineer", "aerospace", "aircraft", "spacecraft",
            "aerodynamics", "propulsion", "avionics", "structural"
        ],
        keywords_moderate=[
            "cad", "simulation", "materials", "design",
            "testing", "flight", "engineering", "analysis"
        ],
        keywords_weak=[
            "problem solving", "technical", "documentation", "prototype"
        ],
        contra_keywords=["nursing", "retail"],
        description="Designs aircraft, spacecraft, and related systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Biomedical Engineer",
        category="Engineering",
        holland_code="IRE",
        o_net_code="17-2031.00",
        mbti_type="INTJ",
        salary_range="$70K-$105K (mid), $105K-$150K (senior)",
        experience_required="High",
        keywords_strong=[
            "biomedical engineer", "biomedical", "medical device",
            "biomechanic", "implant", "tissue engineering", "biosensor"
        ],
        keywords_moderate=[
            "engineering", "design", "clinical", "materials",
            "testing", "regulatory", "prototype", "healthcare"
        ],
        keywords_weak=[
            "research", "technical", "analysis", "documentation"
        ],
        contra_keywords=["retail", "hospitality"],
        description="Designs medical devices and systems for healthcare.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Environmental Engineer",
        category="Engineering",
        holland_code="IRE",
        o_net_code="17-2081.00",
        mbti_type="INTJ",
        salary_range="$70K-$105K (mid), $105K-$145K (senior)",
        experience_required="High",
        keywords_strong=[
            "environmental engineer", "environmental engineering",
            "wastewater", "water treatment", "pollution", "remediation"
        ],
        keywords_moderate=[
            "compliance", "environmental", "engineering", "design",
            "air quality", "sustainability", "permitting", "treatment"
        ],
        keywords_weak=[
            "analysis", "technical", "project", "reporting"
        ],
        contra_keywords=["retail", "finance"],
        description="Designs solutions for environmental protection and pollution control.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Industrial Engineer",
        category="Engineering",
        holland_code="EIR",
        o_net_code="17-2112.00",
        mbti_type="ENTJ",
        salary_range="$70K-$100K (mid), $100K-$140K (senior)",
        experience_required="High",
        keywords_strong=[
            "industrial engineer", "industrial engineering", "lean",
            "process improvement", "operations research", "efficiency"
        ],
        keywords_moderate=[
            "manufacturing", "optimization", "quality", "supply chain",
            "workflow", "ergonomic", "data", "simulation"
        ],
        keywords_weak=[
            "analysis", "design", "planning", "coordination"
        ],
        contra_keywords=["nursing", "creative writing"],
        description="Optimizes production processes, systems, and workflows.",
        pivot_cost="High",
    ),

    # ─── Business specialties ──────────────────────────────────────────────
    RoleProfile(
        title="Management Consultant",
        category="Business & Finance",
        holland_code="EIC",
        o_net_code="13-1111.00",
        mbti_type="ENTJ",
        salary_range="$85K-$130K (mid), $130K-$220K (senior)",
        experience_required="High",
        keywords_strong=[
            "consultant", "consulting", "management consulting",
            "strategy", "advisory", "client engagement", "transformation"
        ],
        keywords_moderate=[
            "analysis", "recommendation", "stakeholder", "process",
            "data", "presentation", "roadmap", "optimization"
        ],
        keywords_weak=[
            "leadership", "communication", "problem solving", "project"
        ],
        contra_keywords=["nursing", "construction"],
        description="Advises organizations on strategy, operations, and performance.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Financial Advisor",
        category="Business & Finance",
        holland_code="ECS",
        o_net_code="13-2052.00",
        mbti_type="ENTJ",
        salary_range="$65K-$100K (mid), $100K-$180K (senior)",
        experience_required="Medium",
        keywords_strong=[
            "financial advisor", "financial planning", "wealth management",
            "investment", "portfolio", "retirement planning", "client"
        ],
        keywords_moderate=[
            "finance", "insurance", "asset", "risk",
            "estate planning", "securities", "advice", "sales"
        ],
        keywords_weak=[
            "communication", "relationship", "analysis", "service"
        ],
        contra_keywords=["surgery", "construction"],
        description="Advises clients on investments, retirement, and financial goals.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Actuary",
        category="Business & Finance",
        holland_code="ICE",
        o_net_code="15-2011.00",
        mbti_type="INTJ",
        salary_range="$80K-$120K (mid), $120K-$200K (senior)",
        experience_required="High",
        keywords_strong=[
            "actuary", "actuarial", "risk assessment", "statistics",
            "probability", "insurance", "pricing", "reserve"
        ],
        keywords_moderate=[
            "mathematics", "modeling", "data", "financial",
            "forecast", "analysis", "exam", "valuation"
        ],
        keywords_weak=[
            "quantitative", "technical", "reporting", "problem solving"
        ],
        contra_keywords=["nursing", "creative"],
        description="Analyzes financial risk using statistics and mathematics.",
        pivot_cost="High",
    ),

    # ─── Science specialties ───────────────────────────────────────────────
    RoleProfile(
        title="Physicist",
        category="Science",
        holland_code="IAR",
        o_net_code="19-2012.00",
        mbti_type="INTP",
        salary_range="$80K-$125K (mid), $125K-$180K (senior)",
        experience_required="High",
        keywords_strong=[
            "physicist", "physics", "quantum", "theoretical",
            "experiment", "optics", "particle", "mathematical"
        ],
        keywords_moderate=[
            "research", "laboratory", "modeling", "simulation",
            "data", "analysis", "theory", "publication"
        ],
        keywords_weak=[
            "scientific", "computation", "documentation", "problem solving"
        ],
        contra_keywords=["retail", "marketing"],
        description="Studies the fundamental properties of matter and energy.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Geologist",
        category="Science",
        holland_code="IRA",
        o_net_code="19-2042.00",
        mbti_type="ISTP",
        salary_range="$60K-$90K (mid), $90K-$135K (senior)",
        experience_required="High",
        keywords_strong=[
            "geologist", "geology", "rock", "mineral", "geological",
            "soil", "earth", "survey", "hydrogeology"
        ],
        keywords_moderate=[
            "field", "mapping", "sampling", "gis",
            "analysis", "exploration", "data", "environmental"
        ],
        keywords_weak=[
            "research", "outdoor", "reporting", "laboratory"
        ],
        contra_keywords=["retail", "accounting"],
        description="Studies the Earth's structure, materials, and processes.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Statistician",
        category="Science",
        holland_code="ICR",
        o_net_code="15-2041.00",
        mbti_type="INTJ",
        salary_range="$75K-$110K (mid), $110K-$160K (senior)",
        experience_required="High",
        keywords_strong=[
            "statistician", "statistics", "statistical", "regression",
            "probability", "data analysis", "survey", "modeling"
        ],
        keywords_moderate=[
            "r", "python", "sas", "sampling",
            "hypothesis", "inference", "data", "experimental"
        ],
        keywords_weak=[
            "quantitative", "research", "reporting", "visualization"
        ],
        contra_keywords=["nursing", "hospitality"],
        description="Analyzes data and designs experiments to draw valid conclusions.",
        pivot_cost="High",
    ),

    # ─── Education specialties ─────────────────────────────────────────────
    RoleProfile(
        title="Special Education Teacher",
        category="Education",
        holland_code="SAI",
        o_net_code="25-2051.00",
        mbti_type="ENFJ",
        salary_range="$50K-$75K (mid), $75K-$100K (senior)",
        experience_required="High",
        keywords_strong=[
            "special education", "special ed", "iep", "individualized education",
            "learning disability", "inclusive", "accommodation", "student"
        ],
        keywords_moderate=[
            "teaching", "classroom", "curriculum", "assessment",
            "behavior", "intervention", "parent", "support"
        ],
        keywords_weak=[
            "patience", "communication", "adaptation", "advocacy"
        ],
        contra_keywords=["software development", "finance"],
        description="Teaches students with diverse learning and developmental needs.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="School Principal",
        category="Education",
        holland_code="EAS",
        o_net_code="11-9032.00",
        mbti_type="ENTJ",
        salary_range="$85K-$120K (mid), $120K-$160K (senior)",
        experience_required="High",
        keywords_strong=[
            "principal", "school administration", "school leadership",
            "education administration", "superintendent", "curriculum leadership"
        ],
        keywords_moderate=[
            "staff", "budget", "policy", "student",
            "compliance", "community", "evaluation", "instruction"
        ],
        keywords_weak=[
            "leadership", "communication", "planning", "mentoring"
        ],
        contra_keywords=["nursing", "manufacturing"],
        description="Leads and manages a school's operations, staff, and student success.",
        pivot_cost="High",
    ),

    # ─── Technology specialties ────────────────────────────────────────────
    RoleProfile(
        title="Machine Learning Engineer",
        category="Technology",
        holland_code="ICR",
        o_net_code="15-2051.00",
        mbti_type="INTJ",
        salary_range="$110K-$155K (mid), $155K-$220K+ (senior)",
        experience_required="High",
        keywords_strong=[
            "machine learning", "ml", "deep learning", "neural network",
            "ai", "artificial intelligence", "tensorflow", "pytorch"
        ],
        keywords_moderate=[
            "python", "data", "model", "training", "inference",
            "nlp", "computer vision", "feature", "deployment"
        ],
        keywords_weak=[
            "algorithm", "statistics", "coding", "optimization"
        ],
        contra_keywords=[],
        description="Builds and deploys machine learning models and AI systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Cybersecurity Engineer",
        category="Technology",
        holland_code="ICR",
        o_net_code="15-1212.00",
        mbti_type="INTJ",
        salary_range="$100K-$140K (mid), $140K-$200K (senior)",
        experience_required="High",
        keywords_strong=[
            "cybersecurity", "security engineer", "penetration testing",
            "security architecture", "threat", "vulnerability", "cryptography"
        ],
        keywords_moderate=[
            "firewall", "siem", "incident response", "identity",
            "cloud security", "network security", "compliance", "zero trust"
        ],
        keywords_weak=[
            "security", "engineering", "risk", "automation"
        ],
        contra_keywords=["sales", "retail"],
        description="Designs and implements systems to protect against cyber threats.",
        pivot_cost="Medium",
    ),
    # ─── Expansion batch (117 → 150) ─────────────────────────────────────
    RoleProfile(
        title="Materials Engineer",
        category="Engineering",
        holland_code="IRE",
        o_net_code="17-2131.00",
        mbti_type="INTJ",
        salary_range="$85K-$125K",
        experience_required="Medium",
        keywords_strong=["materials science", "metallurgy", "polymers", "composites", "ceramics", "materials engineer"],
        keywords_moderate=["nanomaterials", "failure analysis", "corrosion", "alloy", "materials testing", "semiconductor"],
        keywords_weak=["laboratory", "testing", "quality", "research", "manufacturing"],
        contra_keywords=["sales", "customer service"],
        description="Develops and tests materials for products and manufacturing.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Nuclear Engineer",
        category="Engineering",
        holland_code="ICR",
        o_net_code="17-2161.00",
        mbti_type="INTJ",
        salary_range="$100K-$140K",
        experience_required="High",
        keywords_strong=["nuclear", "reactor", "radiation", "nuclear engineering", "fission", "plasma"],
        keywords_moderate=["radioactive", "isotope", "neutron", "safety analysis", "containment", "uranium"],
        keywords_weak=["energy", "engineering", "thermal", "systems", "safety"],
        contra_keywords=["retail", "hospitality"],
        description="Designs nuclear power systems and radiation applications.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Robotics Engineer",
        category="Engineering",
        holland_code="IRC",
        o_net_code="17-2199.08",
        mbti_type="INTP",
        salary_range="$90K-$140K",
        experience_required="Medium",
        keywords_strong=["robotics", "robot", "autonomous", "mechatronics", "robotic", "computer vision"],
        keywords_moderate=["sensors", "actuators", "control systems", "embedded", "motion planning", "kinematics"],
        keywords_weak=["automation", "engineering", "programming", "hardware", "artificial intelligence"],
        contra_keywords=["retail", "customer service"],
        description="Designs robots and autonomous systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Petroleum Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2171.00",
        mbti_type="ISTJ",
        salary_range="$110K-$160K",
        experience_required="High",
        keywords_strong=["petroleum", "oil and gas", "reservoir", "drilling", "oil field", "natural gas"],
        keywords_moderate=["extraction", "well", "production", "pipeline", "refinery", "geology"],
        keywords_weak=["energy", "engineering", "field", "operations", "equipment"],
        contra_keywords=["teaching", "counseling"],
        description="Designs methods for extracting oil and gas.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Marine Engineer / Naval Architect",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2121.00",
        mbti_type="ISTJ",
        salary_range="$85K-$125K",
        experience_required="Medium",
        keywords_strong=["naval architect", "marine engineer", "ship", "vessel", "shipbuilding", "marine"],
        keywords_moderate=["hull", "propulsion", "offshore", "submarine", "naval", "boat"],
        keywords_weak=["engineering", "design", "structural", "mechanical", "systems"],
        contra_keywords=["retail", "healthcare"],
        description="Designs ships, boats, and offshore structures.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Computer Engineer",
        category="Engineering",
        holland_code="IRC",
        o_net_code="17-2061.00",
        mbti_type="INTP",
        salary_range="$85K-$130K",
        experience_required="Medium",
        keywords_strong=["computer engineer", "hardware engineer", "fpga", "microprocessor", "embedded systems", "computer architecture"],
        keywords_moderate=["circuit", "firmware", "verilog", "vlsi", "integrated circuit", "digital design"],
        keywords_weak=["hardware", "software", "engineering", "electronics", "programming"],
        contra_keywords=["retail", "sales"],
        description="Designs computer hardware and embedded systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Manufacturing Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2112.01",
        mbti_type="ISTJ",
        salary_range="$75K-$110K",
        experience_required="Medium",
        keywords_strong=["manufacturing engineer", "manufacturing", "production line", "lean manufacturing", "assembly line", "process improvement"],
        keywords_moderate=["six sigma", "kaizen", "automation", "tooling", "quality control", "cnc"],
        keywords_weak=["production", "engineering", "factory", "operations", "machining"],
        contra_keywords=["teaching", "retail"],
        description="Optimizes manufacturing processes and production systems.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Mining Engineer",
        category="Engineering",
        holland_code="RIE",
        o_net_code="17-2151.00",
        mbti_type="ISTJ",
        salary_range="$85K-$130K",
        experience_required="High",
        keywords_strong=["mining", "mine", "mineral", "excavation", "mining engineer", "ore"],
        keywords_moderate=["geology", "blasting", "extraction", "shaft", "quarry", "surface mining"],
        keywords_weak=["engineering", "field", "operations", "equipment", "safety"],
        contra_keywords=["healthcare", "retail"],
        description="Plans and oversees mining operations and mineral extraction.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Astronomer",
        category="Science",
        holland_code="IRA",
        o_net_code="19-2011.00",
        mbti_type="INTP",
        salary_range="$80K-$130K",
        experience_required="High",
        keywords_strong=["astronomy", "astronomer", "astrophysics", "telescope", "celestial", "galaxy"],
        keywords_moderate=["cosmology", "stellar", "observatory", "planetary", "spectroscopy", "dark matter"],
        keywords_weak=["physics", "research", "data analysis", "science", "modeling"],
        contra_keywords=["retail", "sales"],
        description="Studies celestial objects and the universe.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Mathematician",
        category="Science",
        holland_code="ICR",
        o_net_code="15-2021.00",
        mbti_type="INTP",
        salary_range="$80K-$130K",
        experience_required="High",
        keywords_strong=["mathematician", "mathematics", "mathematical", "theorem", "calculus", "linear algebra"],
        keywords_moderate=["proof", "numerical", "topology", "abstract algebra", "applied mathematics", "statistical"],
        keywords_weak=["analysis", "modeling", "research", "theory", "problem solving"],
        contra_keywords=["retail", "customer service"],
        description="Develops mathematical theories and applies them to real problems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Meteorologist / Atmospheric Scientist",
        category="Science",
        holland_code="ICR",
        o_net_code="19-2021.00",
        mbti_type="INTJ",
        salary_range="$70K-$110K",
        experience_required="Medium",
        keywords_strong=["meteorology", "weather", "atmospheric", "forecast", "climate", "meteorologist"],
        keywords_moderate=["storm", "precipitation", "temperature", "satellite", "climatology", "hurricane"],
        keywords_weak=["data", "modeling", "research", "science", "analysis"],
        contra_keywords=["retail", "hospitality"],
        description="Studies and forecasts weather and climate patterns.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Microbiologist",
        category="Science",
        holland_code="IRA",
        o_net_code="19-1022.00",
        mbti_type="ISTJ",
        salary_range="$70K-$110K",
        experience_required="Medium",
        keywords_strong=["microbiology", "microbe", "bacteria", "virus", "microorganism", "microbiologist"],
        keywords_moderate=["pathogen", "culture", "microscope", "antibiotic", "sterile", "fungi"],
        keywords_weak=["laboratory", "research", "biology", "testing", "science"],
        contra_keywords=["retail", "sales"],
        description="Studies microorganisms including bacteria, viruses, and fungi.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Ecologist",
        category="Science",
        holland_code="IRA",
        o_net_code="19-2041.00",
        mbti_type="INTP",
        salary_range="$60K-$95K",
        experience_required="Medium",
        keywords_strong=["ecology", "ecologist", "ecosystem", "biodiversity", "habitat", "wildlife"],
        keywords_moderate=["conservation", "field research", "species", "environmental assessment", "restoration", "wetland"],
        keywords_weak=["biology", "research", "environment", "field", "data"],
        contra_keywords=["retail", "finance"],
        description="Studies ecosystems and the relationships between organisms and their environment.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Food Scientist",
        category="Science",
        holland_code="IRC",
        o_net_code="19-1012.00",
        mbti_type="ISTJ",
        salary_range="$65K-$100K",
        experience_required="Medium",
        keywords_strong=["food science", "food scientist", "food safety", "food processing", "nutritional", "ingredient"],
        keywords_moderate=["quality control", "flavor", "preservation", "food production", "sensory", "formulation"],
        keywords_weak=["laboratory", "testing", "chemistry", "research", "manufacturing"],
        contra_keywords=["retail", "customer service"],
        description="Develops and improves food products and safety.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Pharmacologist",
        category="Science",
        holland_code="IRA",
        o_net_code="19-1042.00",
        mbti_type="INTJ",
        salary_range="$90K-$135K",
        experience_required="High",
        keywords_strong=["pharmacology", "drug", "pharmaceutical", "pharmacologist", "clinical trial", "pharmacokinetics"],
        keywords_moderate=["medication", "compound", "dose", "toxicology", "formulation", "mechanism"],
        keywords_weak=["chemistry", "biology", "research", "laboratory", "testing"],
        contra_keywords=["retail", "sales"],
        description="Studies how drugs interact with biological systems.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Biochemist",
        category="Science",
        holland_code="IRA",
        o_net_code="19-1021.00",
        mbti_type="INTJ",
        salary_range="$70K-$115K",
        experience_required="High",
        keywords_strong=["biochemistry", "biochemist", "molecular biology", "protein", "enzyme", "biochemical"],
        keywords_moderate=["dna", "rna", "genomics", "assay", "chromatography", "metabolism"],
        keywords_weak=["laboratory", "chemistry", "biology", "research", "testing"],
        contra_keywords=["retail", "sales"],
        description="Studies the chemical processes within living organisms.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Oceanographer",
        category="Science",
        holland_code="IRA",
        o_net_code="19-2099.00",
        mbti_type="INTP",
        salary_range="$70K-$115K",
        experience_required="High",
        keywords_strong=["oceanography", "ocean", "marine science", "oceanographer", "sea", "underwater"],
        keywords_moderate=["currents", "seafloor", "coastal", "hydrography", "marine biology", "salinity"],
        keywords_weak=["research", "data", "field", "environment", "science"],
        contra_keywords=["retail", "finance"],
        description="Studies the ocean's physical, chemical, and biological properties.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Entrepreneur / Founder",
        category="Business & Finance",
        holland_code="EIA",
        o_net_code="11-9199.00",
        mbti_type="ENTP",
        salary_range="Variable (equity-driven)",
        experience_required="High",
        keywords_strong=["founder", "entrepreneur", "startup", "co-founder", "launched", "bootstrapped"],
        keywords_moderate=["business", "venture", "raised funding", "product", "scale", "ownership"],
        keywords_weak=["strategy", "growth", "innovation", "leadership", "company"],
        contra_keywords=[],
        description="Starts and scales new business ventures.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Chief Executive Officer (CEO)",
        category="Business & Finance",
        holland_code="ECI",
        o_net_code="11-1011.00",
        mbti_type="ENTJ",
        salary_range="$200K+ (base plus equity)",
        experience_required="High",
        keywords_strong=["chief executive", "ceo", "president", "executive", "c-suite", "board of directors"],
        keywords_moderate=["led", "leadership", "strategy", "revenue", "growth", "stakeholders"],
        keywords_weak=["management", "operations", "vision", "company", "organization"],
        contra_keywords=[],
        description="Leads an organization's strategy, vision, and overall operations.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Venture Capitalist",
        category="Business & Finance",
        holland_code="ECI",
        o_net_code="11-9199.00",
        mbti_type="ENTJ",
        salary_range="$120K+ (plus carry)",
        experience_required="High",
        keywords_strong=["venture capital", "investor", "venture capitalist", "fund", "portfolio company", "term sheet"],
        keywords_moderate=["due diligence", "fundraising", "equity", "valuation", "startup", "exit"],
        keywords_weak=["finance", "investment", "strategy", "business", "deals"],
        contra_keywords=[],
        description="Invests in and advises early-stage companies.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Economist",
        category="Business & Finance",
        holland_code="ICE",
        o_net_code="19-3011.00",
        mbti_type="INTJ",
        salary_range="$90K-$140K",
        experience_required="High",
        keywords_strong=["economist", "economics", "econometric", "macroeconomic", "microeconomic", "economic analysis"],
        keywords_moderate=["forecast", "policy", "market research", "regression", "model", "statistical"],
        keywords_weak=["data", "research", "analysis", "finance", "policy"],
        contra_keywords=["retail", "hospitality"],
        description="Analyzes economic data and forecasts trends.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Optometrist",
        category="Healthcare",
        holland_code="IRS",
        o_net_code="29-1041.00",
        mbti_type="ISTJ",
        salary_range="$100K-$150K",
        experience_required="High",
        keywords_strong=["optometry", "optometrist", "eye exam", "vision", "contact lens", "eyeglass"],
        keywords_moderate=["ocular", "refraction", "eye care", "glaucoma", "prescription", "patient care"],
        keywords_weak=["healthcare", "clinical", "diagnosis", "patient", "medical"],
        contra_keywords=["retail", "manufacturing"],
        description="Examines eyes and prescribes corrective lenses.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Anesthesiologist",
        category="Healthcare",
        holland_code="IRS",
        o_net_code="29-1211.00",
        mbti_type="INTJ",
        salary_range="$300K+",
        experience_required="High",
        keywords_strong=["anesthesiology", "anesthesiologist", "anesthesia", "sedation", "operating room", "perioperative"],
        keywords_moderate=["pain management", "intubation", "surgery", "monitoring", "critical care", "anesthetic"],
        keywords_weak=["medicine", "physician", "patient", "clinical", "hospital"],
        contra_keywords=["retail", "hospitality"],
        description="Administers anesthesia and manages pain during surgery.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Chiropractor",
        category="Healthcare",
        holland_code="SRI",
        o_net_code="29-1011.00",
        mbti_type="ISTJ",
        salary_range="$70K-$120K",
        experience_required="High",
        keywords_strong=["chiropractic", "chiropractor", "spinal", "adjustment", "musculoskeletal", "alignment"],
        keywords_moderate=["back pain", "subluxation", "manual therapy", "posture", "rehabilitation", "wellness"],
        keywords_weak=["healthcare", "patient", "treatment", "clinical", "therapy"],
        contra_keywords=["retail", "manufacturing"],
        description="Treats musculoskeletal issues through spinal adjustment.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Judge / Magistrate",
        category="Legal",
        holland_code="ESC",
        o_net_code="23-1023.00",
        mbti_type="ISTJ",
        salary_range="$120K-$200K",
        experience_required="High",
        keywords_strong=["judge", "magistrate", "court", "ruling", "adjudicate", "judicial"],
        keywords_moderate=["legal", "case law", "hearing", "verdict", "litigation", "bench"],
        keywords_weak=["law", "justice", "legal research", "opinion", "criminal"],
        contra_keywords=["retail", "manufacturing"],
        description="Presides over legal proceedings and issues rulings.",
        pivot_cost="High",
    ),
    RoleProfile(
        title="Mediator / Arbitrator",
        category="Legal",
        holland_code="SEA",
        o_net_code="23-1022.00",
        mbti_type="ENFJ",
        salary_range="$60K-$110K",
        experience_required="Medium",
        keywords_strong=["mediation", "mediator", "arbitration", "arbitrator", "dispute resolution", "conflict resolution"],
        keywords_moderate=["negotiation", "settlement", "conciliation", "facilitation", "restorative", "agreement"],
        keywords_weak=["communication", "legal", "counseling", "negotiate", "resolution"],
        contra_keywords=[],
        description="Facilitates negotiation and resolves disputes between parties.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Ship Captain",
        category="Transportation",
        holland_code="RIE",
        o_net_code="53-5021.00",
        mbti_type="ISTJ",
        salary_range="$70K-$130K",
        experience_required="Medium",
        keywords_strong=["ship captain", "captain", "vessel", "navigation", "maritime", "seafaring"],
        keywords_moderate=["nautical", "cargo", "deck", "voyage", "pilotage", "harbor"],
        keywords_weak=["marine", "transportation", "operations", "safety", "crew"],
        contra_keywords=["retail", "healthcare"],
        description="Commands a ship and manages its crew and voyage.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Locomotive Engineer / Conductor",
        category="Transportation",
        holland_code="RCE",
        o_net_code="53-4011.00",
        mbti_type="ISTJ",
        salary_range="$60K-$95K",
        experience_required="Medium",
        keywords_strong=["locomotive", "railroad", "train", "rail", "conductor", "locomotive engineer"],
        keywords_moderate=["freight", "yard", "track", "signals", "railway", "switching"],
        keywords_weak=["transportation", "operations", "equipment", "safety", "logistics"],
        contra_keywords=["retail", "healthcare"],
        description="Operates and manages freight and passenger trains.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Emergency Management Director",
        category="Public Safety",
        holland_code="SEC",
        o_net_code="11-9161.00",
        mbti_type="ESTJ",
        salary_range="$65K-$110K",
        experience_required="Medium",
        keywords_strong=["emergency management", "disaster response", "emergency preparedness", "incident command", "disaster recovery"],
        keywords_moderate=["crisis", "contingency", "mitigation", "evacuation", "homeland security", "response planning"],
        keywords_weak=["safety", "public safety", "coordination", "operations", "planning"],
        contra_keywords=["retail", "finance"],
        description="Plans and coordinates responses to emergencies and disasters.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Executive Assistant",
        category="Operations",
        holland_code="CES",
        o_net_code="43-6011.00",
        mbti_type="ESFJ",
        salary_range="$50K-$80K",
        experience_required="Low",
        keywords_strong=["executive assistant", "calendar management", "administrative support", "scheduling", "executive support", "correspondence"],
        keywords_moderate=["travel arrangements", "meeting coordination", "office management", "stakeholder", "confidential", "expense reports"],
        keywords_weak=["organization", "communication", "multitasking", "coordination", "administrative"],
        contra_keywords=["manual labor", "construction"],
        description="Provides high-level administrative support to executives.",
        pivot_cost="Low",
    ),
    RoleProfile(
        title="Video Game Designer",
        category="Creative & Media",
        holland_code="AIR",
        o_net_code="27-1029.00",
        mbti_type="INTP",
        salary_range="$70K-$120K",
        experience_required="Medium",
        keywords_strong=["game design", "game designer", "game development", "level design", "gameplay", "video game"],
        keywords_moderate=["unity", "unreal engine", "game mechanics", "storytelling", "interactive", "animation"],
        keywords_weak=["design", "programming", "creative", "art", "software"],
        contra_keywords=["retail", "healthcare"],
        description="Designs video games and interactive experiences.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Millwright",
        category="Skilled Trades",
        holland_code="RCI",
        o_net_code="49-9044.00",
        mbti_type="ISTP",
        salary_range="$55K-$85K",
        experience_required="Medium",
        keywords_strong=["millwright", "industrial machinery", "machinery installation", "mechanical maintenance", "conveyor", "alignment"],
        keywords_moderate=["turbine", "pump", "gear", "precision", "industrial equipment", "rigging"],
        keywords_weak=["mechanical", "repair", "maintenance", "equipment", "installation"],
        contra_keywords=["healthcare", "retail"],
        description="Installs, maintains, and repairs industrial machinery.",
        pivot_cost="Medium",
    ),
    RoleProfile(
        title="Nuclear Power Reactor Operator",
        category="Energy & Utilities",
        holland_code="RCI",
        o_net_code="51-8011.00",
        mbti_type="ISTJ",
        salary_range="$90K-$130K",
        experience_required="High",
        keywords_strong=["reactor operator", "nuclear power", "nuclear reactor", "power plant", "turbine", "reactor"],
        keywords_moderate=["control room", "cooling", "radiation safety", "steam", "grid", "monitoring"],
        keywords_weak=["energy", "operations", "equipment", "safety", "maintenance"],
        contra_keywords=["retail", "healthcare"],
        description="Operates and monitors nuclear power plant reactors.",
        pivot_cost="High",
    ),
]
