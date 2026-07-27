---
title: "OSKG Pipeline — Full Session Memory"
created: 2026-07-26
session_date: 2026-07-26
model: deepseek-v4-pro
phases: 4
claims_extracted: 32
edges_created: 136
role_profiles: 9
synthesis_notes: 4
capstone: true
tags:
  - memory
  - oskg
  - pipeline
  - career-aptitude
  - anitalmid
  - methodology
  - birkman
  - knowledge-graph
---

# Anitalmid OSKG Pipeline — Session Memory

## What Was Built

The Anitalmid Project was transformed from a collection of Birkman data and
career history notes into a full **Open Source Knowledge Graph (OSKG)** — a
structured, queryable graph of 32 career aptitude claims with 136 typed edges,
modeled after the OSKG-YahWeh methodology for scholarly synthesis.

---

## Phase 1: Claims Extraction

**32 atomic claims** extracted across three categories:

| Category | Count | ID Range | Source Data |
|---|---|---|---|
| Birkman-derived | 17 | `anitalmid-birkman-1` to `anitalmid-birkman-17` | Personality profile, interest scores, strengths, needs, stress patterns |
| Career history | 9 | `anitalmid-career-1` to `anitalmid-career-9` | 7 documented roles spanning 2014-2025 |
| Role-fit synthesis | 6 | `anitalmid-fit-1` to `anitalmid-fit-6` | Cross-cutting recommendations |

Every claim follows the OSKG format: YAML frontmatter (claim_id, statement,
confidence rating very-high/high/medium/low, evidence type, source tags) +
body sections (Claim, Evidence, Confidence, Stakes, Edges, Assessment).

**136 typed edges** connecting claims:
- 46 Depends on (B logically requires A)
- 65 Supports (A provides evidence for B)
- 7 Contradicts (A and B cannot both be true)
- 18 Challenged by (A faces counter-evidence from B)

Claims are located at: `claims/claim-*.md` (flat directory, 40 files total
including architecture reference, progress tracker, and old placeholders).

## Claim ID Map (for quick reference)

### Birkman Claims
| ID | Slug | Claim |
|---|---|---|
| anitalmid-birkman-1 | claim-blue-yellow-bridge-archetype | Blue/Yellow bridge maps to IT architecture |
| anitalmid-birkman-2 | claim-technical-interest-82-percent | Technical 82% supports IT alignment |
| anitalmid-birkman-3 | claim-scientific-interest-92-percent | Scientific 92% supports analytical roles |
| anitalmid-birkman-4 | claim-literary-interest-92-technical-writing | Literary 92% maps to technical writing |
| anitalmid-birkman-5 | claim-administrative-interest-low | Admin 20% disqualifies clerical IT |
| anitalmid-birkman-6 | claim-numerical-interest-low | Numerical 17% contraindicates quantitative |
| anitalmid-birkman-7 | claim-persuasive-interest-low | Persuasive 32% contraindicates sales |
| anitalmid-birkman-8 | claim-structured-thinking-strength | Structured thinking supports systematic IT |
| anitalmid-birkman-9 | claim-investigating-troubleshooting-strength | Investigating supports security/ops |
| anitalmid-birkman-10 | claim-ambiguity-handling-strength | Ambiguity handling supports architecture |
| anitalmid-birkman-11 | claim-one-on-one-sensitivity-strength | Sensitivity supports consultative IT |
| anitalmid-birkman-12 | claim-needs-systematic-environment | Yellow Needs favor enterprise IT |
| anitalmid-birkman-13 | claim-stress-rigidity-risk | Yellow Stress is risk for high-tempo roles |
| anitalmid-birkman-14 | claim-interests-blue-innovation-planning | Blue Interests drive architecture/strategy |
| anitalmid-birkman-15 | claim-reflective-efficiency-strength | Reflective efficiency supports automation |
| anitalmid-birkman-16 | claim-social-service-low | Social Service 21% contraindicates helping roles |
| anitalmid-birkman-17 | claim-written-word-strength | Written word supports documentation |

### Career History Claims
| ID | Slug | Claim |
|---|---|---|
| anitalmid-career-1 | claim-security-operations-experience | Security ops (MFA, IR, CJIS, endpoint) |
| anitalmid-career-2 | claim-backup-dr-experience | Backup/DR (Linux + Veeam, zero data loss) |
| anitalmid-career-3 | claim-compliance-documentation-experience | Compliance docs (ISO 27001, SOC2, CJIS) |
| anitalmid-career-4 | claim-endpoint-management-experience | Endpoint management (200+ devices) |
| anitalmid-career-5 | claim-access-management-experience | IAM across 4 roles (11-year pattern) |
| anitalmid-career-6 | claim-technical-documentation-kb-experience | KB development and procedures |
| anitalmid-career-7 | claim-voip-migration-experience | VoIP migration (2014) |
| anitalmid-career-8 | claim-software-implementation-experience | Software implementation projects |
| anitalmid-career-9 | claim-remote-support-experience | Remote support (AppleCare) |

### Role-Fit Claims
| ID | Slug | Claim |
|---|---|---|
| anitalmid-fit-1 | claim-systems-administrator-primary-fit | SysAdmin is strongest primary fit |
| anitalmid-fit-2 | claim-cloud-administrator-secondary-fit | Cloud Admin is strongest progression |
| anitalmid-fit-3 | claim-security-analyst-fit | Security Analyst is strong alternative |
| anitalmid-fit-4 | claim-grc-compliance-analyst-fit | GRC Analyst is differentiated path |
| anitalmid-fit-5 | claim-documentation-engineering-fit | Documentation is competency, not career |
| anitalmid-fit-6 | claim-pure-helpdesk-contraindicated | Helpdesk careers are contraindicated |

---

## Phase 2: Role Profile Expansion

**9 IT role profiles** created at `Role Profiles/` via delegated Camufox web
research (3 parallel subagents, 54 total searches):

| Profile | Size | Birkman Colors | Dan's Strongest Fit |
|---|---|---|---|
| Windows Systems Administrator | 9.5KB | Yellow + Blue | Already performing this work |
| Cloud Administrator (Azure) | 12KB | Blue + Yellow | Blue Interests (innovation) |
| Security Analyst (SOC) | 13KB | Yellow + Blue | Investigating + security ops |
| GRC Analyst | 15KB | Yellow + Green | ISO 27001/SOC2 docs |
| Network Administrator | 13KB | Yellow + Blue | VoIP migration (dated) |
| DevOps Engineer | 14KB | Blue + Yellow + Red | Structured thinking + ambiguity |
| Database Administrator | 15KB | Yellow + Blue | Scientific interest 92% |
| IT Project Manager | 15KB | Yellow + Green | Project leadership across 4 roles |
| Systems Architect | 18KB | Blue + Yellow | Blue/Yellow bridge (strongest fit) |

Each profile includes: skills (core, specialized, soft), certifications
(entry/professional/advanced), tools (primary/secondary), salary data
(3-4 tiers), career progression (4-5 levels), 10-15 responsibilities,
aptitude signals (strong matches + development areas), adjacent roles,
day-in-the-life, and search sources.

---

## Phase 3: Structural Analysis

Four synthesis notes at `synthesis/`:

### 3.1 — Hinge Inventory
**Top 5 load-bearing claims ranked by dependency count:**

| # | Claim | Dependents | Cascade | Role |
|---|---|---|---|---|
| 1 | Blue/Yellow bridge (birkman-1) | 11 | 23 (72%) | Central hub — single point of failure |
| 2 | SysAdmin primary fit (fit-1) | 1 | — | Most supported (15 supporters) |
| 3 | Security operations (career-1) | 6 | 7 (22%) | Career-history anchor |
| 4 | Literary interest 92% (birkman-4) | 4 | 4 (12%) | Documentation engine |
| 5 | Structured thinking (birkman-8) | 4 | 10 (31%) | Execution engine |

Graph architecture: hub-and-spoke centered on birkman-1. 24 of 32 claims
connected. 8 leaf claims. Role-fit claims average 4.8 supporters each.

### 3.2 — Cascade Trees
BFS collapse traces for top 5 hinges (4-level depth limit):

- **birkman-1** (Blue/Yellow bridge): 23-claim cascade. If falsified, 72% of
  the graph collapses. Critical children at L2: birkman-13 (stress rigidity,
  challenged by fit-2), birkman-6 (numerical interest low, challenged by
  birkman-3).
- **career-1** (Security ops): 7-claim cascade. Loses 5 of fit-1's 15 supporters
  but graph survives on Birkman evidence alone.
- **birkman-4** (Literary 92%): 4-claim cascade. Documentation branch is
  structurally isolated — collapse does not affect core recommendations.
- **birkman-8** (Structured thinking): 10-claim cascade. Second-most destructive
  single failure. Execution branch collapses.
- **birkman-9** (Investigating): 9-claim cascade. Security branch weakens but
  Blue/Yellow and Technical/Scientific survive independently.

### 3.3 — Counter-Position Stress Tests
Graph integrity tested against 3 alternative career hypotheses:

| Position | Survival Rate | Verdict |
|---|---|---|
| Creative/Media career | 17% (1/6) | CONTRAINDICATED — creative aptitude belongs within IT |
| IT Management track | 17% (1/6) | Late-career only — Persuasive 32% + Admin 20% + Social 21% contradict |
| Networking specialization | 100% (6/6) | Viable secondary — underevidenced as primary (VoIP is 2014) |

### 3.4 — Convergence Analysis
Three role-fit claims meet the OSKG settled convergence standard (5+ HIGH+
supporters, zero MEDIUM+ challenges):

| Claim | Supporters | HIGH+ | Status |
|---|---|---|---|
| fit-1 — SysAdmin | 15 | 14 | ★★★ SETTLED |
| fit-2 — Cloud Admin | 7 | 6 | ★★★ SETTLED |
| fit-3 — Security Analyst | 6 | 6 | ★★★ SETTLED |
| fit-4 — GRC Analyst | 0 | 0 | △ WEAK (structurally isolated) |
| fit-5 — Documentation Eng | 0 | 0 | △ WEAK |
| fit-6 — Helpdesk contra | 1 | 1 | △ WEAK |

---

## Phase 4: Capstone Synthesis

**`Capstone - Career Aptitude Synthesis.md`** (18KB, 7 sections):

The capstone reports what the graph shows structurally — not a narrative
summary of the Birkman profile or career history.

### Primary Recommendation: Systems Administrator

"15 claims at HIGH+ confidence support Systems Administrator as the primary
fit; zero claims at MEDIUM+ confidence contradict it. Dan is already
performing mid-level systems administration under the title Information
Systems Specialist. The recommendation is formalization, not career change."

### Progression: Cloud Administrator (Azure)

"7 claims at HIGH+ confidence support Cloud Administrator as the strongest
2-4 year progression. Blue Interests (innovation, planning, future-orientation)
are served by cloud architecture work. The gap is certification (AZ-104),
not aptitude."

### Alternative: Security Analyst

"6 claims at HIGH+ confidence support Security Analyst as a strong
alternative. This represents a specialization decision to evaluate in
2-3 years. Build as secondary competency within sysadmin role."

### Action Plan

| Timeline | Actions |
|---|---|
| 0-6 months | Security+, AZ-900, resume reframe, salary check |
| 6-18 months | AZ-104, Azure lab work, PowerShell/IaC deepening |
| 18-36 months | Choose: AZ-305 (Architect) or SC-200/300 (Security) |
| 5-10 years | Systems Architect (career ceiling — Blue/Yellow bridge fully expressed) |

### Key Structural Findings

- **Single point of failure:** Blue/Yellow bridge (birkman-1) supports 72% of
  the graph. Mitigant: corroborated by 4 independent Birkman symbols.
- **Strongest convergence:** SysAdmin fit (fit-1) has 15 supporters, 14 at
  HIGH+ confidence. No other claim approaches this density.
- **Genuine tension:** Administrative interest at 20% vs. sysadmin paperwork.
  Mitigation: automation + delegation, not role change.
- **Robust against alternatives:** Both creative/media and IT management
  counter-positions show 17% survival — the recommendation survives challenge.

---

## Architecture Decisions

### Why the OSKG approach for career aptitude?

The standard mode of career advice is narrative: "Based on your profile, you
should do X." An OSKG makes the reasoning auditable. Every claim is individually
addressable. Every edge is explicit. The recommendation does not say "Dan would
be a good sysadmin" — it says "15 claims at HIGH+ confidence support this; zero
claims at MEDIUM+ confidence contradict it." The confidence is structural, not
rhetorical.

### Why flat claims directory?

Following OSKG-YahWeh: Obsidian's graph view connects files via wikilinks and
tags, not folder structure. A flat `claims/` directory with consistent tagging
enables graph view filtering without structural debt. Subfolders create
classification problems (does a claim about security AND writing go in security/
or writing/?).

### Why the edge types?

The four edge types (Supports, Contradicts, Depends on, Challenged by) are the
same as OSKG-YahWeh because they capture the universal structure of evidence-
based argumentation. A career aptitude graph has the same structural needs as a
scholarly knowledge graph: claims support or contradict each other, depend on
foundational claims, and face challenges from counter-evidence.

### Why hub-and-spoke architecture?

The graph naturally formed a hub-and-spoke structure because the Birkman profile
is a unified instrument: all personality signals derive from the same underlying
assessment. This is a feature of the domain, not a design flaw. The alternative
would be to artificially fragment the Birkman profile into independent claims,
which would misrepresent the data.

---

## Files Created (Complete Inventory)

```
The Anitalmid Project/
├── Capstone - Career Aptitude Synthesis.md    (18KB) — Culminating synthesis
├── claims/
│   ├── claims-architecture.md                 (5KB)  — OSKG methodology adapted for career aptitude
│   ├── claims-progress.md                     (4KB)  — Progress tracker with session log
│   ├── claim-blue-yellow-bridge-archetype.md  (5KB)  — birkman-1
│   ├── claim-technical-interest-82-percent.md (3KB)  — birkman-2
│   ├── ... (30 more claim files)                      birkman-3 through fit-6
│   ├── claim-written-word-strength.md         (2KB)  — birkman-17
│   └── claim-pure-helpdesk-contraindicated.md (3KB)  — fit-6
├── synthesis/
│   ├── phase1-hinge-inventory.md              (5KB)  — Top 10 load-bearing claims
│   ├── phase2-cascade-trees.md                (7KB)  — BFS collapse traces
│   ├── phase3-counter-position-stress-tests.md(6KB)  — 3 alternative hypothesis tests
│   └── phase4-convergence-analysis.md         (8KB)  — Settled vs. weak convergences
├── Role Profiles/
│   ├── Windows Systems Administrator.md       (10KB) — Existing, pre-pipeline
│   ├── Cloud Administrator (Azure).md         (12KB) — Phase 2
│   ├── Security Analyst (SOC).md              (13KB) — Phase 2
│   ├── GRC Analyst.md                         (15KB) — Phase 2
│   ├── Network Administrator.md               (13KB) — Phase 2
│   ├── DevOps Engineer.md                     (14KB) — Phase 2
│   ├── Database Administrator.md              (15KB) — Phase 2
│   ├── IT Project Manager.md                  (15KB) — Phase 2
│   └── Systems Architect.md                   (18KB) — Phase 2
└── Birkman Insights/
    └── Dan Bechtel Birkman Profile.md         (10KB) — Updated with claims+synthesis links
```

Hermes skill: `~/.hermes/skills/anitalmid-oskg-pipeline/SKILL.md`

---

## How to Continue

The pipeline is complete but the graph can be extended:

1. **Add more role profiles** — use `camufox-obsidian-research` skill for
   additional IT roles (Site Reliability Engineer, Cloud Security Engineer,
   Solutions Architect, etc.)
2. **Extract more claims** — deeper claims from existing data (e.g., individual
   strength-to-role mappings not yet extracted)
3. **Run re-analysis** — as claims or role profiles are added, re-run Phase 3
   structural analysis to see if convergences shift
4. **Add a second individual** — the OSKG architecture supports multiple
   Birkman profiles. A second person's claims would create cross-individual
   edges (e.g., "Person B's Red/Green profile supports different roles than
   Person A's Blue/Yellow")
5. **Connect to live job market** — integrate job posting APIs to validate
   salary data and skill demand against current market conditions

---

## Key Lessons

### What worked
- The OSKG-YahWeh methodology translated cleanly from biblical studies to career
  aptitude — the pipeline (claims → edges → hinge inventory → cascade trees →
  counter-position tests → convergence → capstone) is domain-agnostic
- Delegated role profile creation via parallel subagents was efficient — 8
  profiles in 5 minutes vs. ~30 minutes sequential
- The hub-and-spoke architecture is appropriate for a unified assessment
  instrument like Birkman — forcing a mesh architecture would misrepresent
  the data
- Confidence ratings with explicit rationale (very-high = quantitative score
  or measurable outcome, high = explicit statement, medium = inferred) created
  clear structural hierarchy

### What to improve
- The graph under-counts indirect support — claims that support fit-1 through
  intermediary claims don't show as direct supporters. A transitive closure
  analysis would surface more structural support
- Role profiles should be connected to claims more explicitly (currently
  the connection is through the "source_note" field and wikilinks in the
  body, not through formal typed edges)
- The counter-position tests are manually constructed — a future iteration
  could formalize them as claim-to-position edges in the graph itself
- Salary data from Camufox searches may include hallucinated URLs — all
  salary figures should be verified against primary sources (BLS, Glassdoor)
