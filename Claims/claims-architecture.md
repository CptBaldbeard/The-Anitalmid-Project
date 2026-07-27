---
tags:
  - type/architecture
  - anitalmid
  - methodology
created: 2026-07-26
status: implemented
related:
  - "[[Dan Bechtel Birkman Profile]]"
  - "[[Birkman Method Overview]]"
  - "[[Top_Career_Areas_to_Explore]]"
---

# Claims Architecture: Career Aptitude Knowledge Graph

## The Problem

The Anitalmid Project has rich structured data — a full Birkman personality profile,
7 career history roles, role profiles, and industry research — but no way to:

- Query "what aptitude signals point toward security roles?"
- Trace "if Dan's Administrative interest were higher, what role recommendations change?"
- See a network of how Birkman traits support or contradict specific career paths
- Identify which claims are load-bearing for the final career recommendation

## The OSKG Model

This follows the OSKG-YahWeh architecture: structured claim extraction → typed edges
→ graph querying → synthesis from structure. The approach was validated on 723 claims
across 17 scholarly books in a humanities domain. The Anitalmid Project applies the
same pipeline to career aptitude matching — a domain where:
- Claims are testable (Birkman scores, real work experience, industry data)
- Edges are inferable (traits → role fit, experience → skill alignment)
- The corpus is small (1 assessment, 7 roles, ~15 target role profiles)
- Synthesis produces actionable recommendations, not academic conclusions

## Pipeline

```
Birkman Profile + Career History + Role Profiles
  → 30+ atomic claims with typed edges
    → Hinge Inventory (which signals are most load-bearing?)
      → Cascade Trees (if a key assumption is challenged, what falls?)
        → Counter-Position Tests (what if Dan should pursue creative/media instead of IT?)
          → Capstone: "What IT career shows the strongest structural fit?"
```

## Claim File Format

### Frontmatter

```yaml
---
tags:
  - type/claim
  - topic/<primary-topic>
  - evidence/<evidence-type>
  - source/<source-type>
  - anitalmid
claim_id: "anitalmid-<category>-<num>"
statement: "<one sentence — the claim's assertion>"
confidence: "<very-high|high|medium|low>"
confidence_rationale: "<one sentence on why this rating>"
claim_type: "<birkman|career-history|role-fit|industry>"
source_note: "[[<source note>]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Tag Taxonomy

**Required:** `type/claim`, `anitalmid`

**Topic tags** (at least one):
- `topic/birkman-profile`
- `topic/personality-archetype`
- `topic/career-aptitude`
- `topic/role-fit`
- `topic/systems-administration`
- `topic/cloud-administration`
- `topic/security-operations`
- `topic/technical-writing`
- `topic/helpdesk-support`
- `topic/network-administration`
- `topic/compliance-grc`
- `topic/devops`

**Evidence tags:**
- `evidence/birkman-assessment`
- `evidence/career-history`
- `evidence/industry-research`
- `evidence/role-profile`

**Source tags:**
- `source/birkman-basics-report`
- `source/career-history-note`
- `source/role-profile`

### Claim ID Format

`anitalmid-{category}-{num}`

| Category | Source data |
|---|---|
| `birkman` | Birkman personality profile (scores, strengths, symbols) |
| `career` | Career history (real roles, responsibilities, achievements) |
| `fit` | Role-fit synthesis (cross-cutting claims about career alignment) |

### Edge Types

| Edge | Meaning |
|---|---|
| **Supports** | Claim A provides evidence that strengthens Claim B |
| **Contradicts** | Claim A and Claim B cannot both be true for the same role recommendation |
| **Depends on** | Claim B logically requires Claim A to be true |
| **Challenged by** | Claim A faces counter-evidence or caveat from another claim |

## Body Format

```markdown
# claim_id: statement

**Source:** [[source note]] — description

## The Claim

Full statement of the claim with specific data points.

## Evidence

Structured evidence — scores, responsibilities, achievements.

## Confidence

**Rating:** <very-high|high|medium|low>

**Rationale:** <One sentence on why.>

## Stakes

Why this claim matters for career aptitude matching. What role recommendations
depend on it?

## Edges

**Depends on:**
- [[claim-<slug>]] — how this claim relies on it

**Supports:**
- [[claim-<slug>]] — how this claim reinforces it

**Contradicts:**
- [[claim-<slug>]] — how these claims conflict

**Challenged by:**
- [[claim-<slug>]] — what evidence or argument threatens it

## Assessment

Evaluation of the claim's strength, caveats, and implications.
```

## Why Flat Claims Directory

Following OSKG-YahWeh: Obsidian's graph view connects files, not folders. A flat
`claims/` directory with consistent tagging lets the graph view and search handle
discovery. Subfolders create structural debt — "does a claim about security
aptitude AND technical writing go in security/ or writing/?"

## File Naming Convention

`claim-<descriptive-slug>.md`

The slug is human-readable because Obsidian's graph view displays filenames as
node labels. Examples:
- `claim-blue-yellow-bridge-archetype.md`
- `claim-security-operations-experience.md`
- `claim-systems-administrator-primary-fit.md`
