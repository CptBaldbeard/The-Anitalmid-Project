---
tags:
  - type/synthesis
  - anitalmid
  - phase3
  - hinge-inventory
created: 2026-07-26
related:
  - "[[phase2-cascade-trees]]"
  - "[[phase3-counter-position-stress-tests]]"
  - "[[phase4-convergence-analysis]]"
scale:
  claims: 32
  edges: 136
  hinges_identified: 10
---

# Phase 3.1: Hinge Inventory — Load-Bearing Claims

> **Generated:** 2026-07-26 | **Total claims analyzed:** 32 | **Claims acting as dependencies:** 24

A claim is *load-bearing* if many other claims list it as a dependency in their
`Depends on` section. This inventory identifies the structural hinges of the
career aptitude knowledge graph: the claims whose truth-status has the widest
downstream consequences for career recommendations.

---

## Top 10 Hinge Claims

| Rank | Claim ID | Statement | Deps | Sup | Type | Topic |
|------|----------|-----------|------|-----|------|-------|
| 1 | `birkman-1` | Blue/Yellow bridge archetype maps to IT architecture and systems roles | 11 | 0 | birkman | personality-archetype |
| 2 | `fit-1` | Systems Administrator is the strongest primary career fit | 1 | 15 | role-fit | systems-administration |
| 3 | `career-1` | Security operations experience (MFA, monitoring, IR, CJIS, endpoint) | 6 | 2 | career-history | security-operations |
| 4 | `birkman-4` | Literary interest at 92% maps to technical writing | 4 | 3 | birkman | technical-writing |
| 5 | `birkman-8` | Structured thinking strength supports systematic IT roles | 4 | 5 | birkman | career-aptitude |
| 6 | `career-3` | Compliance documentation experience (ISO 27001, SOC2, CJIS) | 2 | 6 | career-history | compliance-grc |
| 7 | `birkman-3` | Scientific interest at 92% supports analytical IT roles | 3 | 3 | birkman | career-aptitude |
| 8 | `fit-2` | Cloud Administrator is the strongest next-step progression | 0 | 7 | role-fit | cloud-administration |
| 9 | `birkman-9` | Investigating strength supports security and operations roles | 3 | 3 | birkman | security-operations |
| 10 | `fit-3` | Security Analyst is a strong alternative career path | 0 | 6 | role-fit | security-operations |

## Top 10: What Depends on Them

**1. Blue/Yellow Bridge (birkman-1)** — 11 dependents + 23-claim cascade radius

The foundational claim. The Blue/Yellow bridge is the cognitive architecture
that explains WHY every other aptitude signal points the way it does. Dependents
cluster in: personality-archetype, career-aptitude, and role-fit. If this claim
is falsified — if Dan's profile is actually Red/Green or purely Blue — nearly
every role recommendation shifts. **This is the graph's single point of failure.**

**2. Systems Administrator Primary Fit (fit-1)** — 15 supporters, 1 dependent

The most heavily SUPPORTED claim in the graph — 15 claims from both Birkman and
career history provide direct evidence. Only 1 claim depends on it (Cloud Admin
fit-2), but the supporter count is the highest of any claim by a wide margin.
This is the recommendation the graph was built to produce.

**3. Security Operations Experience (career-1)** — 6 dependents

The career-history anchor. 5 other career-history claims and the Systems
Administrator fit claim depend on this for their evidence base. The ISS role at
City of Moscow is the substrate for most of the experience-based competency
claims.

**4. Literary Interest 92% (birkman-4)** — 4 dependents

The documentation engine. Claims about compliance writing, KB development, GRC
fit, and documentation engineering all depend on Literary interest as their
Birkman foundation.

**5. Structured Thinking (birkman-8)** — 4 dependents + 1 challenger

The execution engine. The reflective efficiency claim, security operations
experience, software implementation experience, and the SysAdmin fit claim all
depend on structured thinking. The lone challenger is the Administrative interest
claim — which argues that structured thinking should not be confused with
administrative aptitude.

---

## Edge Statistics

| Metric | Count |
|---|---|
| Total typed edges | 136 |
| Depends on | 46 |
| Supports | 65 |
| Contradicts | 7 |
| Challenged by | 18 |

- **24 of 32 claims** act as dependency or support targets (connected)
- **8 claims** are leaf nodes (no inbound edges)
- Birkman claims average 1.9 dependents each — they form the foundation
- Role-fit claims average 4.8 supporters each — they synthesize from the foundation
- Career-history claims average 1.3 dependents and 1.3 supporters — they bridge the layers

---

## Fragility Map

The graph has one clear single point of failure: **birkman-1 (Blue/Yellow bridge)**.
With 11 direct dependents and a 23-claim cascade radius, falsifying this claim
would collapse the majority of the graph. The next strongest hinge (career-1)
has only 6 dependents — a steep drop.

The graph's architecture is *hub-and-spoke*: one central hub (birkman-1) supports
a web of Birkman and career-history claims, which in turn support role-fit
recommendations. This is efficient for a 32-claim graph but creates fragility —
the hub claim must be extremely well-evidenced. Fortunately, birkman-1 is rated
**very-high confidence** with four-symbol corroboration from the Birkman
assessment.
