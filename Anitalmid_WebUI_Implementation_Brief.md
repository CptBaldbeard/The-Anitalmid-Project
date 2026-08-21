# Anitalmid Project — WebUI + Career-Mapping Engine: Implementation Brief

**Prepared for:** Dan Bechtel (Captain Baldbeard)
**Date:** 2026-08-21
**Status:** Draft for review — this is a *brief/plan*, not code.

---

## 1. Purpose

Turn the Anitalmid Project from a personal Obsidian vault + a single `resume_matcher.py` script into a **multi-user web application**:

1. A **webUI** where anyone can populate their resume, work history, education, certifications, and (optionally) psychometric self-report.
2. A **backend engine** that consumes those datapoints, cross-references them against the Anitalmid resource graph (Birkman, MBTI, Enneagram, DISC, Big Five, Holland, the OSKG claims, and the role profiles), and produces a **career map** — a ranked, evidence-tagged set of role recommendations and progression paths.

The product is the "Apt AI"-style career matcher Dan has been hand-running for himself, generalized to any user.

---

## 2. What Already Exists (do not rebuild)

The engine is ~80% designed; it just isn't a web service yet. Current assets in the vault (`/mnt/c/Users/Dan/Desktop/The Anitalmid Project/The Anitalmid Project/`):

| Component | Location | Reuse? |
|---|---|---|
| **OSKG** — 32+ typed claims (Birkman 17, career 9, fit 6) with `Depends on / Supports / Contradicts / Challenged by` edges | `claims/` | ✅ the knowledge backbone |
| **Framework triangulation** — 6 frameworks converge on Holland/RIASEC | `Frameworks/` | ✅ scoring logic |
| **`resume_matcher.py`** — PDF → top-6 role ranking (60% keyword + 40% framework + experience boost) | vault root | ✅ the reference scoring algorithm |
| **Role profiles** — 10 roles (5 IT + 5 non-IT), each with 6 framework scores + 3 keyword lists + pivot cost | `Role Profiles/` | ✅ matching targets |
| **Capstone synthesis** — settled convergences, trade-offs, fragilities | `Capstone/` | ✅ output template |
| **Birkman profile** — Dan's own test case | `Birkman Insights/` | ✅ golden dataset |

**Key design principle:** the webUI is a *new front door*; the career engine is a *refactor and productization* of the existing pipeline, not a rewrite.

---

## 3. Target Architecture

```
┌───────────────────────────── CLIENT ─────────────────────────────┐
│  Next.js / React SPA                                             │
│  • Sign-up / profile wizard (resume, jobs, certs, education)     │
│  • Optional psychometric self-report form (6 frameworks)         │
│  • Career map viewer (interactive graph) + ranked role list      │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTPS / JSON
┌──────────────────────────────▼───────────────────────────────────┐
│  API Layer — FastAPI (Python)                                    │
│  • /auth, /profile, /resume, /certifications                     │
│  • POST /analyze  →  kicks off the pipeline, returns career map  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌───────────────┐   ┌────────────────────┐   ┌────────────────────┐
│ Resume Parser │   │ Signal Extractor   │   │ Scoring / Match    │
│ (LLM + regex) │ → │ (frameworks)       │ → │ Engine             │
└───────────────┘   └────────────────────┘   └─────────┬──────────┘
                                                        │
                                    ┌───────────────────▼───────────┐
                                    │  Career Map Generator         │
                                    │  (graph: profile→signals→      │
                                    │   claims→roles→paths)         │
                                    └───────────────┬───────────────┘
                                                    ▼
                              ┌─────────────────────────────────────┐
                              │  Storage                           │
                              │  • Postgres — users, resumes,       │
                              │    scores, role results             │
                              │  • SQLite (existing) — OSKG claims  │
                              │  • Optional graph DB for maps       │
                              └─────────────────────────────────────┘
```

---

## 4. Frontend (WebUI) — recommended path

**Framework: Next.js (App Router) + TypeScript.** One codebase, SSR for SEO, easy API routes as a fallback if the Python API ever needs a thin proxy. React ecosystem maturity for the graph piece.

**Key screens:**

1. **Onboarding wizard** — stepwise input:
   - *Resume upload* (PDF/DOCX drag-drop).
   - *Structured fields*: work history (title, employer, dates, bullets), education, **certifications** (name, issuer, year, active/inactive), skills (tagged).
   - *Optional assessments*: light self-report sliders for the 6 frameworks (so users without a Birkman report still get a signal).
2. **Analysis progress** — job status polling while the backend runs.
3. **Career map viewer** — the centerpiece. Interactive graph with:
   - The user's profile node.
   - Signal nodes (Holland code, MBTI, Big Five, etc.).
   - Claim nodes (evidence-tagged, color-coded by confidence).
   - Role nodes sized by score; paths/edges showing progression.
   - A ranked list view alongside (top 6, pivot cost, salary range, "aptitude-validated vs experience-validated" flag).
4. **Export** — PDF/PNG of the map, shareable link.

**Graph rendering: React Flow** (built for node/edge graphs, handles the map interactivity) over raw D3. D3 only if fine-grained custom layouts are needed later.

**Efficient shortcut:** the resume-matcher already outputs top-6 with scores; the map is *visualization* of that output plus the claim edges. Don't over-engineer the graph — start with React Flow, a fixed force layout, and 3 node types.

---

## 5. Backend (API) — recommended path

**Framework: FastAPI (Python).** Rationale — the entire engine is already Python (`resume_matcher.py`, OSKG tooling, pymupdf). FastAPI gives async, auto OpenAPI docs, and Pydantic models that map cleanly onto the existing role-profile dataclasses. **Zero porting risk.**

**Modules (mirror the existing pipeline):**

1. **Resume Parser**
   - *Primary:* LLM structured extraction — send resume text to a model (local Ollama `magistral`, or a hosted model later) with a JSON schema prompt, forcing `{jobs[], education[], certifications[], skills[]}`.
   - *Fallback:* pymupdf text + regex/keyword heuristics (the current approach) for when no LLM is available or to keep costs at zero.
   - *Decision:* LLM-first is the **most efficient** path for messy, free-form resumes; the regex path is the free safety net. Keep both, feature-flag them.

2. **Signal Extractor**
   - Map resume keywords + form inputs to framework signals (Holland RIASEC, MBTI, Big Five) using the same keyword→signal logic in `resume_matcher.py`, upgraded to weighted rules.
   - If the user completed the self-report form, *override* keyword-inferred signals with self-report (self-report > keyword inference, matching the "assessment-verified vs inferred" confidence model already in the OSKG).

3. **Scoring / Match Engine**
   - Reuse the 60/40 keyword+frameworks scoring against the 10 role profiles.
   - Add the **OSKG edge logic** as a verification pass: role recommendations must satisfy "5+ HIGH supports, zero MEDIUM+ contradictions" (the convergence rule from the pipeline).
   - Output: ranked roles + confidence + pivot cost + evidence claims.

4. **Career Map Generator**
   - Build the graph object: profile → signals → claims → roles → paths.
   - Serialize to a JSON graph the frontend renders (nodes + edges with types, weights, confidence colors).

**Storage:** Postgres for users/resumes/results (multi-tenancy, auth). The existing **SQLite OSKG** can be embedded read-only as the shared knowledge base (claims/roles are static across users); per-user *results* go in Postgres. A graph DB (Neo4j/Arango) is **optional** and not needed for v1 — a Postgres `nodes`/`edges` table or an in-memory networkx graph suffices for the map.

---

## 6. The Career-Mapping Engine (productizing the resources)

The "resources I introduced" = the 6 psychometric frameworks + OSKG claims + role profiles + Birkman reference. The engine's job:

1. **Ingest** a user's datapoints (resume + certs + self-report).
2. **Triangulate** across frameworks → Holland code as the primary matching key (RIASEC → O*NET-style mapping, already documented in the career-matching skill).
3. **Score** against role profiles (keyword + framework fit).
4. **Validate** against the OSKG (typed edges: does a role claim get *supported* by ≥5 high-confidence claims and *contradicted* by none?).
5. **Emit** a career map + ranked list, with each recommendation tagged `experience-validated` vs `aptitude-validated` and a `pivot_cost`.

**Efficiency win:** the framework triangulation and role profiles already exist as structured data. The engine is a *thin service* over them, not new research. The single biggest new capability is **per-user instantiation** — every user gets their own claim set (generated from their inputs) that gets scored against the *shared* role profiles and framework crosswalks.

---

## 7. Tech Stack Summary

| Layer | Choice | Why (efficiency) |
|---|---|---|
| Frontend | **Next.js + TypeScript + React Flow** | one codebase, mature graph UI |
| API | **FastAPI** | Python — reuses existing engine verbatim |
| Resume parsing | **LLM structured extraction** (local Ollama now, hosted later) + pymupdf/regex fallback | highest accuracy-per-effort |
| Scoring | **existing `resume_matcher.py` logic, refactored** | no reimplementation |
| DB | **Postgres** (users/results) + **SQLite** (OSKG, embedded read-only) | relational is enough for v1 |
| Auth | JWT + OAuth (Google) | standard, low effort |
| Deployment | **Docker Compose** (already in use for Camoufox/Valemorn) | consistent with existing infra |
| Graph | **React Flow** (frontend) + in-memory/networkx (backend) | avoid a graph DB until needed |

---

## 8. Phased Plan

- **Phase 0 — Feasibility spike (1–2 days):** a FastAPI endpoint that wraps the current `resume_matcher.py`, returns its top-6 JSON. Proves the "thin service" hypothesis.
- **Phase 1 — MVP (backend core):** resume parsing + signal extraction + scoring service + Postgres schema + `/analyze` endpoint.
- **Phase 2 — MVP (frontend):** onboarding wizard + ranked results view (no graph yet).
- **Phase 3 — Career map:** React Flow graph of profile→signals→claims→roles→paths.
- **Phase 4 — Productization:** auth, multi-user, saved profiles, export/share, assessment self-report form.
- **Phase 5 — Hardening:** hosted LLM fallback, rate limiting, privacy/compliance (PII in resumes), observability.

---

## 9. Optimized Code Writing — Hermes Kanban Workflow

> This is the "how the code gets *written*, optimized, and orchestrated" layer. Hermes has a durable, SQLite-backed **Kanban board** (`hermes kanban`) purpose-built for this: tasks with dependency edges, atomic claiming, and a **Swarm** graph (parallel workers → verifier → synthesizer).

**Workflow:**

1. **`hermes kanban init`** — stand up the board for the Anitalmid WebUI workstream.
2. **Decompose with `hermes kanban decompose` / `specify`** — break the plan above into a task DAG. Suggested top-level tasks (one card each):
   - `api-scaffold` — FastAPI project + health + auth stub
   - `resume-parser` — LLM extraction + pymupdf fallback
   - `signal-extractor` — framework signal mapping
   - `scoring-engine` — refactor `resume_matcher.py` scoring into a service
   - `oskg-validation` — convergence rule (5 HIGH supports / 0 contradictions)
   - `map-generator` — JSON graph serializer
   - `db-schema` — Postgres models + migrations
   - `frontend-wizard` — onboarding form
   - `frontend-map` — React Flow career map
   - `integration` — end-to-end `/analyze`
3. **Encode dependencies with `hermes kanban link`** — e.g. `scoring-engine` depends on `signal-extractor`; `map-generator` depends on `scoring-engine` + `oskg-validation`; `frontend-map` depends on `map-generator`. This makes the build order deterministic and lets workers grab ready tasks safely.
4. **Execute via Swarm (`hermes kanban swarm`)** — for each feature, run the *parallel workers → verifier → synthesizer* graph:
   - **Workers** draft the code for independent modules in parallel (parser, signal-extractor, scoring can proceed simultaneously once `db-schema`/`api-scaffold` land).
   - **Verifier** checks each output against the task's acceptance criteria (and the project's own quality bar — see the OSKG verification checklist pattern).
   - **Synthesizer** merges verified work into the shared tree.
5. **Atomic claiming (`hermes kanban claim`)** — every task is claimed by exactly one profile/worker; no duplicate work, no merge collisions across profiles.
6. **Track with `hermes kanban stats` / `show` / `tail`** — visibility into blocked/ready/done states; `dispatch`/`daemon` for unattended execution.

**Why this is "optimized code writing":** the dependency graph *is* the parallelization plan. Independent modules (parser, extractor, scoring) get written concurrently by a swarm; dependent modules wait on their parents. The verifier stage catches integration errors *before* merge. Net effect: highest-throughput, lowest-rework code generation, with a single source of truth (the board) for what's done, blocked, or in flight.

---

## 10. Risks & Considerations

- **PII / privacy:** resumes are personal data. Encrypt at rest, provide delete-on-request, minimal retention. This matters for trust and (eventually) GDPR/CCPA.
- **Resume-parser accuracy:** LLM extraction is good but not perfect on 2-column/creative resumes — keep the fallback and surface "parsed data, please verify" in the UI.
- **Psychometric validity:** keyword-inferred signals are *directional*, never claim them as assessments. Mirror the existing confidence model (self-report/assessment = high, keyword inference = medium) — the project already treats this correctly.
- **Scope creep on the graph:** a full graph DB is overkill for v1. Start with Postgres + React Flow.
- **Camoufox research caveat:** as of this writing, Camoufox's search layer returns *hallucinated* results (the stealth scraper is failing and the LLM backfill is fabricating). **This brief was therefore authored from domain knowledge + the Anitalmid project's existing structure, not from live web research.** Before committing to any third-party service named above, verify current pricing/features directly.

---

## 11. Recommended First Action

Phase 0 spike: wrap `resume_matcher.py` in a FastAPI `/analyze` endpoint and confirm it returns the existing top-6 JSON for Dan's resume. This validates the whole "thin service over the existing engine" approach in an afternoon before any frontend or DB work begins.
