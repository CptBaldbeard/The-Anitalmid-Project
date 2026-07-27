# The Anitalmid Project

An open-source knowledge base for career aptitude analysis, built as an [Obsidian](https://obsidian.md) vault. Maps Birkman personality assessment data to IT role profiles, career history, and structured claims — enabling evidence-based career path discovery.

## What This Is

The Anitalmid Project models career aptitude as an **Open Source Knowledge Graph (OSKG)**. Every claim is an atomic, falsifiable assertion about career fit, with typed edges (supports, contradicts, depends on, challenged by) forming a queryable web of evidence.

### Pipeline

```
Birkman Profile + Career History + Role Profiles
  → 32+ atomic claims with typed edges
    → Hinge Inventory (which signals are most load-bearing?)
      → Cascade Trees (if a key assumption is challenged, what falls?)
        → Counter-Position Tests (what if they should pursue X instead of IT?)
          → Capstone: "What IT career shows the strongest structural fit?"
```

## Vault Structure

```
├── Birkman Insights/          # Personality profile + methodology
├── Birkman Colors/            # Red/Green/Yellow/Blue behavioral styles
├── Birkman Symbols/           # Diamond/Circle/Square/Asterisk meanings
├── Birkman Interests/         # Interest profile reference
├── Birkman Career Exploration/ # Top career area recommendations
├── Career History/            # 7 past roles with achievements
├── Role Profiles/             # 9 IT role targets (SysAdmin, Cloud, Sec, etc.)
├── Claims/                    # 32+ OSKG claims with typed edges
├── synthesis/                 # Capstone synthesis outputs
├── Projects/                  # Project-related notes
└── Reflections/               # Personal reflections
```

## Key Findings

The strongest structural fit is **Systems Administrator**, with 6 claims at HIGH+ confidence and zero at MEDIUM+ contradiction. **Cloud Administrator (Azure)** is the strongest progression path.

| Role | Fit Strength | Key Evidence |
|------|-------------|--------------|
| Systems Administrator | Primary | Blue/Yellow bridge archetype, 11-year IAM pattern, endpoint management at scale |
| Cloud Administrator (Azure) | Secondary | Structured thinking, ambiguity handling, reflective efficiency |
| Security Analyst (SOC) | Alternative | Security operations experience, investigating strength |
| GRC Analyst | Specialization | Compliance documentation (ISO 27001, SOC2, CJIS), low persuasive interest |
| DevOps Engineer | Emerging | Automation aptitude, backup/DR experience |

## Confidence Rating Guide

| Rating | Criteria |
|--------|----------|
| **very-high** | Quantitative Birkman score OR specific achievement with measurable outcome |
| **high** | Explicit strength statement OR documented achievement without metrics |
| **medium** | Inferred from converging signals without direct measurement |
| **low** | Speculative |

## How to Use This Vault

1. Install [Obsidian](https://obsidian.md)
2. Clone this repo
3. Open the folder as an Obsidian vault
4. Navigate via the graph view or `[[wikilinks]]`
5. Start with `Birkman Insights/Dan Bechtel Birkman Profile.md` for the full profile
6. Explore `Claims/claims-architecture.md` for the OSKG structure
7. Read `synthesis/` for capstone analysis

## Edge Types

Claims connect through four typed relationships:

| Edge | Meaning |
|------|---------|
| **Depends on** | B logically requires A |
| **Supports** | A provides evidence for B |
| **Contradicts** | A and B cannot both be true |
| **Challenged by** | A faces counter-evidence |

## Tags

All content uses a structured tag taxonomy for Dataview queries:
- `type/claim` — OSKG claim files
- `topic/birkman-profile`, `topic/career-aptitude`, `topic/role-fit`
- `evidence/birkman-assessment`, `evidence/career-history`
- `source/birkman-basics-report`, `source/career-history-note`

## License

This knowledge base is available under the [MIT License](LICENSE). The Birkman assessment data within is personal and included for methodological transparency — the framework and methodology are the reusable parts.

---

*Built with Obsidian. Methodology inspired by OSKG-YahWeh.*
