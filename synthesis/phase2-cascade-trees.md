---
tags:
  - type/synthesis
  - anitalmid
  - phase3
  - cascade-trees
created: 2026-07-26
related:
  - "[[phase1-hinge-inventory]]"
  - "[[phase3-counter-position-stress-tests]]"
  - "[[phase4-convergence-analysis]]"
---

# Phase 3.2: Cascade Trees — Collapse Radii

> **Generated:** 2026-07-26 | **Method:** BFS from top 5 hinges, 4-level depth limit

For each of the top 5 load-bearing claims, this analysis traces the full
collapse radius using breadth-first search: "If this claim is falsified, what
other claims lose their dependency foundation?"

---

## Hinge #1: Blue/Yellow Bridge Archetype (birkman-1)

**Confidence:** very-high | **Direct dependents:** 11
**Cascade radius:** 23 claims (72% of the graph)

```
birkman-1 (Blue/Yellow bridge)
├─ L1 (11 claims)
│  ├─ birkman-10 (Ambiguity handling)
│  ├─ fit-2 (Cloud Admin fit)
│  ├─ birkman-14 (Blue Interests)
│  ├─ birkman-9 (Investigating strength)
│  ├─ birkman-4 (Literary interest)
│  ├─ birkman-12 (Yellow Needs)
│  ├─ birkman-8 (Structured thinking) ──→ L2
│  ├─ birkman-3 (Scientific interest)
│  ├─ birkman-2 (Technical interest)
│  ├─ birkman-13 (Stress rigidity) ──→ L2
│  └─ birkman-6 (Numerical interest low)
│
├─ L2 (9 claims)
│  ├─ fit-3 (Security Analyst fit)
│  ├─ career-1 (Security operations experience) ──→ L3
│  ├─ career-3 (Compliance documentation)
│  ├─ fit-4 (GRC Analyst fit)
│  ├─ fit-5 (Documentation Engineering fit)
│  ├─ career-6 (KB development)
│  ├─ fit-1 (SysAdmin fit) ──→ L3
│  ├─ birkman-15 (Reflective efficiency)
│  └─ career-8 (Software implementation)
│
└─ L3 (3 claims)
   ├─ career-5 (IAM experience)
   ├─ career-2 (Backup/DR experience)
   └─ career-4 (Endpoint management)
```

**Critical children** (deep cascaded + actively challenged):
- `birkman-13` (Stress rigidity) at L2 — challenged by birkman-1 itself (circular)
  and fit-2. The stress pattern is both load-bearing AND contested.
- `birkman-6` (Numerical interest low) at L2 — challenged by birkman-3. The
  Scientific/Numerical distinction is fragile.

**Collapse assessment:** If the Blue/Yellow bridge is falsified, **23 of 32
claims (72%)** lose their dependency foundation. The graph effectively collapses.
This is the single point of failure. Mitigant: birkman-1 is the most heavily
corroborated claim in the graph (4 independent Birkman symbols).

---

## Hinge #2: Security Operations Experience (career-1)

**Confidence:** very-high | **Direct dependents:** 6
**Cascade radius:** 7 claims (22% of the graph)

```
career-1 (Security operations experience)
├─ L1 (6 claims)
│  ├─ career-5 (IAM experience)
│  ├─ career-2 (Backup/DR experience)
│  ├─ career-4 (Endpoint management)
│  ├─ fit-4 (GRC Analyst fit)
│  ├─ fit-3 (Security Analyst fit)
│  └─ fit-1 (SysAdmin fit) ──→ L2
│
└─ L2 (1 claim)
   └─ fit-2 (Cloud Admin fit)
```

**Collapse assessment:** If the ISS role experience is invalidated — if Dan's
security operations responsibilities are overstated or the role scope is narrower
than claimed — 7 claims fall. This would not collapse the entire graph
(Birkman-derived claims survive) but would severely weaken the experience-based
recommendations. The SysAdmin fit claim (fit-1) would lose 5 of its 15 supporters.

---

## Hinge #3: Literary Interest 92% (birkman-4)

**Confidence:** very-high | **Direct dependents:** 4
**Cascade radius:** 4 claims (12% of the graph)

```
birkman-4 (Literary interest 92%)
├─ career-3 (Compliance documentation)
├─ fit-5 (Documentation Engineering fit)
├─ fit-4 (GRC Analyst fit)
└─ career-6 (KB development)
```

**Collapse assessment:** Falsifying Literary interest would collapse the
documentation/GRC branch of the graph — 4 claims. The core SysAdmin/Cloud/Security
recommendations survive intact. This branch is isolated — it does not support
the primary role recommendations. Losing it narrows career options but doesn't
change the primary recommendation.

---

## Hinge #4: Structured Thinking (birkman-8)

**Confidence:** very-high | **Direct dependents:** 4
**Cascade radius:** 10 claims (31% of the graph)

```
birkman-8 (Structured thinking)
├─ L1 (4 claims)
│  ├─ birkman-15 (Reflective efficiency)
│  ├─ career-1 (Security operations) ──→ L2
│  ├─ career-8 (Software implementation)
│  └─ fit-1 (SysAdmin fit) ──→ L2
│
└─ L2 (6 claims)
   ├─ career-5 (IAM experience)
   ├─ career-2 (Backup/DR experience)
   ├─ career-4 (Endpoint management)
   ├─ fit-4 (GRC Analyst fit)
   ├─ fit-3 (Security Analyst fit)
   └─ fit-2 (Cloud Admin fit)
```

**Challenged by:** birkman-5 (Administrative interest low) — the claim that
structured thinking ≠ administrative aptitude.

**Collapse assessment:** Structured thinking is the execution engine. Falsifying
it collapses 10 claims including the SysAdmin, Cloud Admin, and Security Analyst
fit recommendations. This is the second-most destructive single-point failure
after the Blue/Yellow bridge. Mitigant: Strength #8 is an explicit Birkman
statement with three career-history corroborations.

---

## Hinge #5: Investigating Strength (birkman-9)

**Confidence:** very-high | **Direct dependents:** 3
**Cascade radius:** 9 claims (28% of the graph)

```
birkman-9 (Investigating/troubleshooting strength)
├─ L1 (3 claims)
│  ├─ birkman-10 (Ambiguity handling)
│  ├─ fit-3 (Security Analyst fit)
│  └─ career-1 (Security operations) ──→ L2
│
├─ L2 (5 claims)
│  ├─ career-5 (IAM experience)
│  ├─ career-2 (Backup/DR experience)
│  ├─ career-4 (Endpoint management)
│  ├─ fit-4 (GRC Analyst fit)
│  └─ fit-1 (SysAdmin fit) ──→ L3
│
└─ L3 (1 claim)
   └─ fit-2 (Cloud Admin fit)
```

**Challenged by:** fit-5 (Documentation Engineering) — which argues that
investigation drive may be under-served in pure writing roles.

**Collapse assessment:** Investigating strength is the problem-solving engine.
Falsifying it collapses 9 claims — significant but not catastrophic. The
Blue/Yellow bridge and Technical/Scientific interests survive independently.

---

## Summary: Fragility Architecture

| Hinge | Cascade | % of Graph | Critical Children | Single Point of Failure? |
|---|---|---|---|---|
| birkman-1 (Blue/Yellow bridge) | 23 | 72% | birkman-13, birkman-6 | **YES** — graph collapses |
| birkman-8 (Structured thinking) | 10 | 31% | None deep | Partial — execution branch collapses |
| birkman-9 (Investigating) | 9 | 28% | None deep | Partial — security branch weakens |
| career-1 (Security ops) | 7 | 22% | None deep | Partial — experience branch weakens |
| birkman-4 (Literary 92%) | 4 | 12% | None | No — documentation branch isolated |

The graph has a **hub-and-spoke architecture** centered on birkman-1. This is
the weakest point structurally but the strongest point evidentially. The
recommendation for Phase 4: the Capstone must explicitly address the dependency
on the Blue/Yellow bridge and quantify what confidence the corroborating
evidence provides.
