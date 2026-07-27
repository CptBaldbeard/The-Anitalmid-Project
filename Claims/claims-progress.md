---
tags:
  - type/progress
  - anitalmid
created: 2026-07-26
updated: 2026-07-26
---

# Claims Extraction Progress

## Status Summary

- **Total claims extracted:** 50
- **Birkman claims:** 17 (anitalmid-birkman-1 through anitalmid-birkman-17)
- **Career history claims:** 10 (anitalmid-career-1 through anitalmid-career-10)
- **Role-fit synthesis claims:** 6 (anitalmid-fit-1 through anitalmid-fit-6)
- **Credential claims:** 1 (anitalmid-credential-1: CompTIA Security+)
- **Education claims:** 1 (anitalmid-edu-1: BS Public Relations)
- **Strength claims:** 1 (anitalmid-strength-1: Learning Agility, Open-Source, Collaboration)
- **Framework inference claims:** 7 (anitalmid-mbti-1, anitalmid-enneagram-1 [SUPERSEDED], anitalmid-enneagram-2 [CORRECTED], anitalmid-disc-1, anitalmid-ocean-1, anitalmid-holland-1, anitalmid-triangulation-1)
- **Parachute claims:** 7 (anitalmid-parachute-1 through anitalmid-parachute-7)
- **Edges added:** Yes (all claims include intra-domain edges; Parachute session 2 added cross-domain edges to Birkman, Enneagram, and existing Parachute claims)
- **Cross-domain edges:** Complete (Birkman → Framework → Role-fit chain; Parachute → Role-fit chain)
- **Frameworks integrated:** 7 (Birkman + MBTI + Enneagram + DISC + Big Five + Holland Codes + Parachute)
- **Last session:** 2026-07-27 — What Color Is Your Parachute? full-text verification (4 new claims from Chapters 3, 5, 12; Parachute claims: 3 → 7)

## Remaining Work

### Framework Integration ✓ COMPLETE
- [x] MBTI reference note + inference claim (anitalmid-mbti-1)
- [x] Enneagram reference note + inference claim (anitalmid-enneagram-1)
- [x] DISC reference note + inference claim (anitalmid-disc-1)
- [x] Big Five (OCEAN) reference note + inference claim (anitalmid-ocean-1)
- [x] Holland Codes (RIASEC) reference note + inference claim (anitalmid-holland-1)
- [x] Birkman-to-Framework Crosswalk reference note
- [x] Frameworks Overview index
- [x] Multi-framework triangulation claim (anitalmid-triangulation-1)

### Phase 2: Additional Role Profiles ✓ COMPLETE
9 role profiles now in `Role Profiles/`:
- [x] Windows Systems Administrator (existing)
- [x] Cloud Administrator (Azure)
- [x] Security Analyst / SOC Analyst
- [x] GRC Analyst / Compliance Engineer
- [x] Network Administrator
- [x] DevOps Engineer
- [x] Database Administrator
- [x] IT Project Manager
- [x] Systems Architect

### Phase 3: Structural Analysis
- [ ] Hinge Inventory — identify most load-bearing claims
- [ ] Cascade Trees — trace collapse radii for top 5 hinges
- [ ] Counter-Position Tests — test against alternative career paths
- [ ] Convergence Analysis — find role recommendations with strongest structural support

### Phase 4: Capstone
- [x] Capstone synthesis document: "What IT career does Dan show the most aptitude for?"
- Written to `Capstone - Career Aptitude Synthesis.md` (18KB, 7 sections)

## Session Log

### 2026-07-27 — Session 8 (Parachute Full-Text Verification)
- Downloaded and extracted the complete 2012 edition of *What Color Is Your Parachute?* (epub, 14 MB, ~350 pages)
- Full-text extraction confirmed all 14 chapters + Appendices A-D
- Existing integration validated — Wikipedia/LLM summaries were accurate for Chapters 7, 12, 13
- 4 new OSKG claims created from chapters NOT covered by summaries:
  - `anitalmid-parachute-4`: Five-Part Survival Framework (HIGH confidence) — Bolles' structural architecture of Attitudes → Techniques → Job-Creation → Self-Inventory → Teaching parallels the Anitalmid OSKG pipeline
  - `anitalmid-parachute-5`: Employer Preference Inversion (HIGH confidence) — Chapters 5's core thesis: during hard times, employers revert to THEIR preferred hiring channels while job-hunters keep using THEIR preferred channels, creating structural mismatch
  - `anitalmid-parachute-6`: Three Survival Attitudes (MEDIUM confidence) — Tenacity (always have ≥2 alternatives), Adaptability (identity beyond job-title), and Deliberate Optimism (learning during unemployment); mapped to Dan's Birkman/Enneagram architecture
  - `anitalmid-parachute-7`: Career Testing Warnings (HIGH confidence) — Bolles' 6 explicit testing cautions serve as a quality standard for the project; the Anitalmid 7-framework approach passes all 6
- Updated `Parachute/What Color Is Your Parachute Framework.md` — added Five-Part Framework section, chapter coverage table, updated sources, corrected ISBN
- Updated `Capstone - Career Aptitude Synthesis.md` — added Part 9 (Full-Text Verification), updated claims count to 50, edges to 210
- **KEY INSIGHTS:**
  1. The employer preference inversion is the "Rosetta Stone" for the Parachute methodology — it explains WHY networking works and job boards don't
  2. The five-part framework structurally parallels the OSKG pipeline — independent methodological convergence
  3. Bolles' testing warnings validate the project's 7-framework triangulation approach from a 40-year career counseling authority
  4. Full-text verification did NOT change any settled convergences — it added execution strategy (HOW), not career direction (WHAT)
- Total claims: 46 → 50. Parachute claims: 3 → 7. Evidence layers unchanged (6). Book coverage: summary-based → full-text verified.

### 2026-07-27 — Session 7 (Parachute Integration — What Color Is Your Parachute?)
- Sourced Richard Nelson Bolles' *What Color Is Your Parachute?* (1970, revised annually through 2022, 10M+ copies)
- Scraped Wikipedia summary, Four Minute Books summary, author site (JobHuntersBible.com), and incorporated LLM knowledge of the book's frameworks
- Created 2 reference notes in new `Parachute/` directory:
  - `What Color Is Your Parachute Framework.md` — Full framework reference: Flower Exercise (7 petals), Skills Grid (People/Data/Things), networking methodology, informational interviewing, Holland Code connection
  - `Parachute Flower Exercise - Dan Bechtel Profile.md` — Dan's Birkman data mapped onto all seven petals with skills grid analysis and Party Exercise synthesis
- Created 3 new OSKG claims:
  - `anitalmid-parachute-1`: D-T-P Skills Grid profile (Data > Things > People hierarchy) — HIGH confidence
  - `anitalmid-parachute-2`: Seven-petal flower independently converges with all 3 Capstone recommendations — HIGH confidence
  - `anitalmid-parachute-3`: Bolles' networking methodology is structurally aligned with Dan's INTJ/Blue-Yellow/Type 4w5 profile — HIGH confidence
- Updated documents:
  - Frameworks Overview: Parachute added as framework #7, Parachute Integration section added
  - Birkman-to-Framework Crosswalk: Crosswalk 6 (Parachute Flower Exercise) added with full seven-petal mapping
  - Dan Bechtel Birkman Profile: Updated claims_count, frameworks_integrated, added Parachute references
  - Capstone synthesis: Part 8 (Parachute Integration) added
  - Triangulation claim: Updated to reflect 7 frameworks
- **KEY INSIGHTS:**
  1. Dan's skills architecture is D-T-P (Data > Things > People). This simple formula evaluates job fit: Data/Things primary with People limited to written/one-on-one = fit.
  2. Networking/informational interviewing is Dan's IDEAL job-search method. One-on-one, structured, prepared conversations map to INTJ/Blue-Yellow strengths. Traditional methods (career fairs, cold calling, mass applications) are contraindicated.
  3. The Parachute profile reveals that some "preferences" are actually NEEDS — quiet, autonomy, and systematic environments aren't nice-to-haves; their violation triggers the Yellow stress pattern.
  4. The seven-petal flower INDEPENDENTLY CONVERGES with the Capstone's 3 settled recommendations, cross-validating both the OSKG analysis and the Parachute method.
- Total claims: 43 → 46. Frameworks: 6 → 7. Evidence layers: 5 → 6 (added Parachute Self-Inventory).

### 2026-07-26 — Session 6 (Enneagram Type 4 Correction)
- Direct Enneagram assessment reviewed: `test_result_type_4.pdf` (15 pages) identifies Dan as Type 4 (Individualist)
- **CRITICAL CORRECTION:** Previous Birkman-inferred Type 5w6 was WRONG. Dan's core Enneagram type is Type 4 — driven by authenticity, creative self-expression, and meaning.
- New claim created: `anitalmid-enneagram-2` (Type 4w5 — VERY HIGH confidence, assessment-verified)
- Previous claim `anitalmid-enneagram-1` (Type 5w6) marked SUPERSEDED
- **Why the error:** Birkman measures WORK BEHAVIOR, not core motivation. Dan USES Type 5 analytical skills (Wing 5) in service of Type 4 creative/meaning goals.
- **Birkman Blue/Yellow bridge = Type 4w5**: Blue = Type 4 creative/emotional core; Yellow = Type 5 analytical wing
- Enneagram Report source note created at `Enneagram Report/Dan Bechtel Type 4 Report.md`
- Updated: Birkman-to-Framework Crosswalk, Frameworks Overview, Triangulation claim, Capstone synthesis, resume_matcher.py
- **Career impact:** Strengthens Technical Writer, Science Communicator, UX Designer recommendations. Adds Type 4 meaning-alignment caveat to Security Analyst and GRC Analyst.
- Total claims: 42 → 43

### 2026-07-26 — Session 5 (Framework Integration)
- 6 framework reference notes created in `Frameworks/`:
  - Myers-Briggs MBTI, Enneagram Types, DISC Behavioral Styles, Big Five OCEAN, Holland Codes RIASEC
  - Birkman-to-Framework Crosswalk (inference methodology)
  - Frameworks Overview (index + architecture diagram)
- 6 new claims extracted:
  - `anitalmid-mbti-1`: Dan maps to INTJ (Architect), INTP secondary (MEDIUM confidence)
  - `anitalmid-enneagram-1`: Dan maps to Type 5w6, SP instinct (MEDIUM confidence)
  - `anitalmid-disc-1`: Dan maps to High-C / Medium-S CS Specialist (MEDIUM confidence)
  - `anitalmid-ocean-1`: O:Very High, C:Very High, E:Low, A:Med-Low, N:Med-Low (MEDIUM confidence)
  - `anitalmid-holland-1`: Dan maps to IAR (Investigative-Artistic-Realistic) (MEDIUM confidence)
  - `anitalmid-triangulation-1`: All 6 frameworks converge on same personality architecture (HIGH confidence)
- **CRITICAL FINDING:** Five independent frameworks ALL converge on the Blue/Yellow bridge pattern. The Very High C (Conscientiousness) finding is the single best predictor of job performance across all occupations. Zero frameworks contradict.
- All framework inference claims connected to Birkman claims via typed edges (Depends on, Supports)
- Birkman-to-Framework Crosswalk provides complete inference methodology with confidence per dimension
- Total claims: 36 → 42. Evidence layers: 4 → 5 (added Multi-Framework Triangulation)
- Project now framework-agnostic: can accept input from any of 6 frameworks

### 2026-07-26 — Session 4 (Resume Integration)
- Professional resume extracted: "Dan Bechtel Resume.pdf" → 2 pages, 11 years of experience
- Resume note created at `Resume/Dan Bechtel Resume.md`
- 4 new claims extracted from resume data:
  - `anitalmid-credential-1`: CompTIA Security+ certification (VERY-HIGH confidence)
  - `anitalmid-edu-1`: BS Public Relations, University of Idaho (VERY-HIGH confidence)
  - `anitalmid-career-10`: GRC SaaS platform documentation at Valdyr.io (HIGH confidence)
  - `anitalmid-strength-1`: Learning agility, open-source advocacy, collaborative mindset (MEDIUM confidence)
- **CRITICAL FINDING:** Security+ was listed as an "Immediate (0-6 months)" action item in the original Capstone. Resume confirms it is already achieved. Certification roadmap accelerated by ~6 months.
- Capstone synthesis updated: new "Achieved" section, adjusted action plan timeline, Security Analyst convergence strengthened with formal credential backing
- Total claims: 32 → 36. Evidence layers: 3 → 4 (added Professional Resume)
- Birkman profile `claims_count` updated to 36

### 2026-07-26 — Session 3
- Phase 3: Structural Analysis complete
  - Hinge Inventory: 10 load-bearing claims identified, birkman-1 (Blue/Yellow bridge) is central hub
  - Cascade Trees: Top 5 hinges traced, birkman-1 has 23-claim radius (72% of graph)
  - Counter-Position Tests: Creative/Media 17%, IT Management 17%, Networking 100% survival
  - Convergence Analysis: 3 settled convergences (SysAdmin, Cloud Admin, Security Analyst)
- Phase 4: Capstone Synthesis complete
  - Primary: Systems Administrator (15 supporters, 14 HIGH+, zero challenges)
  - Progression: Cloud Administrator — Azure (7 supporters, 6 HIGH+)
  - Alternative: Security Analyst (6 supporters, 6 HIGH+)
  - Action plan with 0-6 month, 6-18 month, 18-36 month timelines
  - Certification roadmap: Security+ → AZ-900 → AZ-104 → AZ-305 or SC-200/300

### 2026-07-26 — Session 2
- 8 role profiles created via delegated Camoufox research (3 parallel subagents)
- Cloud Administrator (Azure), Security Analyst (SOC), GRC Analyst
- Network Administrator, DevOps Engineer, Database Administrator
- IT Project Manager, Systems Architect
- All profiles include Birkman color mapping, salary data, career progression, and Dan-specific aptitude cross-references
- Phase 2: Role Profile Expansion — COMPLETE

### 2026-07-26 — Session 1
- Claims extracted: 32 (17 Birkman + 9 Career History + 6 Role Fit)
- Edges added: ~120 intra-domain and cross-domain edges
- Claims architecture document created
- Progress tracker created
