---
title: "Frameworks Overview"
created: 2026-07-26
tags:
  - index
  - frameworks
  - anitalmid
  - psychometric
  - career-aptitude
framework_count: 6
---

# Frameworks Overview

The Anitalmid Project now integrates six psychometric frameworks for career
aptitude matching — the same data points used by Apt AI (tryapt.ai) combined
with Birkman's depth for inference.

## Framework Inventory

| # | Framework | Type | Dimensions | Evidence Strength | Anitalmid Role |
|---|---|---|---|---|---|
| 1 | **[[Dan Bechtel Birkman Profile\|Birkman Method]]** | Personality + Interests | 4 symbols + 10 interest areas + 11 strengths | High (validated instrument) | **PRIMARY** — native psychometric, source of all inferences |
| 2 | **[[Myers-Briggs MBTI]]** | Personality Type | 4 dichotomies → 16 types | Moderate (popular, debated) | Cognitive style fingerprint |
| 3 | **[[Enneagram Types]]** | Personality Type + Motivation | 9 types + wings + instincts | Low-Moderate (spiritual origins, limited validation) | Motivational depth |
| 4 | **[[DISC Behavioral Styles]]** | Behavioral Style | 4 dimensions → 12 blends | Moderate (behavioral, situational) | Workplace behavior prediction |
| 5 | **[[Big Five OCEAN]]** | Personality Traits | 5 dimensions → 30 facets | **Very High (academic gold standard)** | Scientific backbone, predictive validity |
| 6 | **[[Holland Codes RIASEC]]** | Vocational Interests | 6 types → 720+ codes | **Very High (O*NET standard)** | Career matching engine |

## Crosswalk

See **[[Birkman-to-Framework Crosswalk]]** for the complete inference mapping
from Dan's Birkman data to each framework.

## Dan's Inferred Profiles

| Framework | Result | Claim |
|---|---|---|
| **Birkman** | Blue/Yellow bridge | [[claim-blue-yellow-bridge-archetype]] |
| **MBTI** | INTJ (Architect), INTP secondary | [[claim-mbti-intj-inference]] |
| **Enneagram** | Type 5w6, Self-Preservation instinct | [[claim-enneagram-5w6-inference]] |
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

## Related

- [[Dan Bechtel Birkman Profile]] — Primary psychometric source
- [[Birkman-to-Framework Crosswalk]] — Complete inference methodology
- [[Capstone - Career Aptitude Synthesis]] — Current career recommendations
- [[Claims/claims-progress]] — Claim inventory and session log
