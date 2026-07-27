---
title: "Frameworks Overview"
created: 2026-07-26
tags:
  - index
  - frameworks
  - anitalmid
  - psychometric
  - career-aptitude
framework_count: 7
---

# Frameworks Overview

The Anitalmid Project now integrates seven frameworks for career
aptitude matching — six psychometric frameworks (the same data points used by
Apt AI/tryapt.ai combined with Birkman's depth for inference) plus Richard
Bolles' *What Color Is Your Parachute?* methodology as the practical
job-search layer.

## Framework Inventory

| # | Framework | Type | Dimensions | Evidence Strength | Anitalmid Role |
|---|---|---|---|---|---|
| 1 | **[[Dan Bechtel Birkman Profile\|Birkman Method]]** | Personality + Interests | 4 symbols + 10 interest areas + 11 strengths | High (validated instrument) | **PRIMARY** — native psychometric, source of all inferences |
| 2 | **[[Myers-Briggs MBTI]]** | Personality Type | 4 dichotomies → 16 types | Moderate (popular, debated) | Cognitive style fingerprint |
| 3 | **[[Enneagram Types]]** | Personality Type + Motivation | 9 types + wings + instincts | Low-Moderate (spiritual origins, limited validation) | Motivational depth |
| 4 | **[[DISC Behavioral Styles]]** | Behavioral Style | 4 dimensions → 12 blends | Moderate (behavioral, situational) | Workplace behavior prediction |
| 5 | **[[Big Five OCEAN]]** | Personality Traits | 5 dimensions → 30 facets | **Very High (academic gold standard)** | Scientific backbone, predictive validity |
| 6 | **[[Holland Codes RIASEC]]** | Vocational Interests | 6 types → 720+ codes | **Very High (O*NET standard)** | Career matching engine |
| 7 | **[[Parachute/What Color Is Your Parachute Framework\\|What Color Is Your Parachute?]]** ✦ NEW | Self-Inventory + Job-Hunt Methodology | 7 petals + Skills Grid + Networking | **High (50+ yrs practical application)** | Practical job-search strategy layer |

## Crosswalk

See **[[Birkman-to-Framework Crosswalk]]** for the complete inference mapping
from Dan's Birkman data to each framework.

## Dan's Inferred Profiles

| Framework | Result | Claim |
|---|---|---|
| **Birkman** | Blue/Yellow bridge | [[claim-blue-yellow-bridge-archetype]] |
| **MBTI** | INTJ (Architect), INTP secondary | [[claim-mbti-intj-inference]] |
| **Enneagram** | Type 4w5 (Individualist/Investigator) ✦ CORRECTED | [[claim-enneagram-type-4-corrected]] |
| **DISC** | High C / Medium S (CS Specialist) | [[claim-disc-cs-specialist-inference]] |
| **Big Five** | O:Very High, C:Very High, E:Low, A:Med-Low, N:Med-Low | [[claim-big-five-ocean-inference]] |
| **Holland** | IAR (Investigative-Artistic-Realistic) | [[claim-holland-code-iar-inference]] |
| **Triangulation** | All 6 frameworks converge | [[claim-framework-triangulation]] |

## Architecture

The frameworks form a layered validation structure:

```
                    ┌─────────────────────────┐
                    │  Career Recommendations  │
                    │  (Capstone Synthesis)    │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   TRIANGULATION LAYER   │
                    │   claim-triangulation-1 │
                    │   (Convergence check)   │
                    └───────────┬─────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
  ┌───────▼───────┐   ┌────────▼────────┐   ┌────────▼────────┐
  │  TYPE MODELS  │   │  TRAIT MODELS   │   │ INTEREST MODELS │
  │  MBTI + Ennea │   │  DISC + Big 5   │   │  Holland RIASEC │
  └───────┬───────┘   └────────┬────────┘   └────────┬────────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │    BIRKMAN LAYER        │
                    │    17 claims            │
                    │    (Native assessment)  │
                    └─────────────────────────┘
```

## Using These Frameworks

### For Career Matching (Phase C Pipeline)
1. User provides ANY framework data (MBTI type, Holland Code, etc.)
2. Crosswalk maps input to the six-framework profile
3. Convergence analysis identifies careers matching the full profile
4. Top 6 positions returned with confidence scores

### For Existing Claims
Each existing role-fit claim (fit-1 through fit-6) now has SECONDARY support
from five additional frameworks through the triangulation claim, increasing
structural confidence beyond the Birkman-only baseline.

## Parachute Integration (NEW — 2026-07-27)

Bolles' *What Color Is Your Parachute?* is NOT a psychometric instrument. It is
a **structured self-inventory and job-search methodology** that bridges the gap
between "knowing yourself" (psychometrics) and "finding the right work"
(execution). The Anitalmid Project uses Parachute as the **practical
application layer** on top of the six-framework psychometric foundation.

### The Seven Petals vs. Psychometric Frameworks

| Parachute Petal | Psychometric Equivalent | Dan's Data Source |
|---|---|---|
| 1. People | Birkman Colors + Holland Code + MBTI social style | Small analytical teams, I-compatible |
| 2. Working Conditions | Birkman Needs (●) + Stress (■) | Quiet, autonomous, systematic |
| 3. Skills | Birkman Strengths + Career History | D-T-P: Data-Things-People |
| 4. Purpose/Values | Enneagram core motivation + Birkman Interests (✱) | Type 4 authenticity + Blue creative drive |
| 5. Knowledge | Birkman Interest profile + Career history | IT systems, security, documentation, audio |
| 6. Salary/Level | Career area rankings + experience level | Senior IC, not management |
| 7. Geography | Lifestyle preference (inferred) | PNW, small/mid city, remote-capable |

### What Parachute Adds

1. **Methodology**: How to find the right job (networking, informational
   interviewing) — not just which job fits
2. **Skills articulation**: The D-T-P (Data-Things-People) taxonomy for
   describing transferable skills in employer-relevant language
3. **Conditional prioritization**: Which working conditions are non-negotiable
   (stress prevention) vs. flexible (nice-to-have)
4. **Profile-fit job search**: A methodology structurally aligned with Dan's
   INTJ/Blue-Yellow/Type 4w5 personality — one-on-one, written, prepared,
   systematic

See [[Parachute/What Color Is Your Parachute Framework]] and
[[Parachute/Parachute Flower Exercise - Dan Bechtel Profile]] for full
documentation. Three new OSKG claims (parachute-1, parachute-2, parachute-3)
anchor the Parachute data in the knowledge graph.

## Related

- [[Dan Bechtel Birkman Profile]] — Primary psychometric source
- [[Birkman-to-Framework Crosswalk]] — Complete inference methodology (now includes Parachute)
- [[Parachute/What Color Is Your Parachute Framework]] — Parachute framework reference
- [[Parachute/Parachute Flower Exercise - Dan Bechtel Profile]] — Dan's seven-petal profile
- [[Capstone - Career Aptitude Synthesis]] — Current career recommendations
- [[Claims/claims-progress]] — Claim inventory and session log
