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
]
