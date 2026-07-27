---
title: "Camufox → Camoufox Full Rename"
created: 2026-07-26
source: "Hermes Agent — systematic project rename"
tags:
  - memory
  - rename
  - camufox
  - camoufox
  - infrastructure
  - skills
  - vault
  - github
---

# Camufox → Camoufox Full Rename

**Date:** 2026-07-26
**Agent:** Hermes (deepseek-v4-pro)
**Scope:** The Anitalmid Project vault, GitHub mirror, Hermes skills, Crew-Camoufox infrastructure

## What Changed

Every reference to "Camufox" across the entire Anitalmid ecosystem was corrected
to "Camoufox" (adding the missing 'o' — the correct spelling of the Camoufox
browser automation library that powers the web search pipeline).

## Files Changed

### Vault (15 files)
- Birkman Insights/Birkman Method Overview.md — 7 replacements
- Birkman Insights/Dan Bechtel Birkman Profile.md — 1 replacement
- Capstone - Career Aptitude Synthesis.md — 2 replacements
- Claims/claim-systems-administrator-primary-fit.md — 1 replacement
- Claims/claims-progress.md — 1 replacement
- Memories/2026-07-26 - OSKG Pipeline Full Session.md — 2 replacements
- Role Profiles/Cloud Administrator (Azure).md — 7 replacements
- Role Profiles/Database Administrator.md — 2 replacements
- Role Profiles/DevOps Engineer.md — 2 replacements
- Role Profiles/GRC Analyst.md — 7 replacements
- Role Profiles/IT Project Manager.md — 3 replacements
- Role Profiles/Network Administrator.md — 2 replacements
- Role Profiles/Security Analyst (SOC).md — 7 replacements
- Role Profiles/Systems Architect.md — 3 replacements
- Role Profiles/Windows Systems Administrator.md — 2 replacements

### GitHub Mirror (15 files — identical changes, synced via rsync)

### Skills (3 renamed, 3 patched)
- **Created:** camoufox-web-search (replaces camufox-web-search)
- **Created:** camoufox-obsidian-research (replaces camufox-obsidian-research, includes updated template)
- **Deleted:** camufox-web-search, camufox-obsidian-research
- **Patched:** anitalmid-vault-builder (9 replacements: tags, body refs, cross-skill links)
- **Patched:** anitalmid-oskg-pipeline (3 replacements: cross-skill links, Phase 2 reference)

### Infrastructure
- Directory: `/home/dbadmin/crew-camufox/` → `/home/dbadmin/crew-camoufox/`
- Systemd service: `crew-camufox.service` → `crew-camoufox.service`
- 18 source files updated with new paths
- 8 venv files fixed (shebangs, editable install metadata, pyvenv.cfg)

## Verification

- Zero "Camufox" or "camufox" remaining in vault, GitHub mirror, or skills
- Crew-Camoufox service running, health check passing: `{"status": "ok"}`
- All role profile `source` fields updated to `"Camoufox Web Search + Industry Research"`
- GitHub commit `d5493ff` pushed to main

## Skill Created

A reusable skill `anitalmid-rename-refactor` was created to document this
workflow for future systematic renames across the project.

## Related

- Skill: `anitalmid-rename-refactor` — repeatable rename/refactor workflow
- Skill: `camoufox-web-search` — web search via Camoufox API
- Skill: `camoufox-obsidian-research` — career role research pipeline
