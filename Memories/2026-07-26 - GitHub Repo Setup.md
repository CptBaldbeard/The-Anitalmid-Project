---
tags:
  - type/session-log
  - topic/github-setup
  - topic/ssh-configuration
  - anitalmid
created: 2026-07-26
session_date: 2026-07-26
---

# 2026-07-26 — GitHub Repo Setup & Initial Push

## Summary

Created the local GitHub mirror for The Anitalmid Project and completed the
initial push to GitHub. Established the three-path architecture (Obsidian vault
→ local Git mirror → GitHub remote) and configured SSH authentication.

## Paths Established

| Purpose | Path |
|---------|------|
| Active Obsidian vault (source of truth) | `C:\Users\Dan\Desktop\The Anitalmid Project\The Anitalmid Project\` |
| Local GitHub mirror (git repo) | `C:\Users\Dan\Desktop\The Anitalmid Project\GitHub Repo\` |
| GitHub remote | `https://github.com/CptBaldbeard/The-Anitalmid-Project` |
| SSH remote | `git@github.com:CptBaldbeard/The-Anitalmid-Project.git` |

## What Was Done

### Repo Initialization
- Created local git repo at `GitHub Repo/` with full vault contents (rsync from vault)
- Added `.gitignore` excluding `workspace.json`, `.trash/`, `.DS_Store`, OS junk
- Wrote `README.md` with project overview, OSKG pipeline, role fit summary
- Added `LICENSE` (MIT) and `.gitkeep` files for empty directories
- Initial commit: 82 files, 5,565 lines

### SSH Key Setup
- Generated ED25519 key pair at `~/.ssh/id_ed25519` (dan@bechtel.dev)
- Added public key to GitHub account (CptBaldbeard)
- Added `github.com` to `known_hosts`
- Switched remote from HTTPS to SSH

### Sync Workflow
- Synced vault changes to mirror including:
  - `Capstone - Career Aptitude Synthesis.md`
  - Four phase analysis files (`synthesis/phase1-4-*.md`)
  - `Memories/2026-07-26 - OSKG Pipeline Full Session.md`
  - Updated Birkman Profile and claims progress
- Committed and pushed to GitHub: 8 files changed, 1,394 insertions

### Final State
- 85 tracked files on GitHub
- 4 commits (3 local + 1 initial upload)
- SSH authentication working (`Hi CptBaldbeard!`)

## Hermes Agent Artifacts

### Skills Created
- `anitalmid-github-sync` — workflow for syncing vault changes to GitHub (rsync → commit → push)

### Memory Saved
- GitHub repo URL and local mirror path for future sessions

## Git Log (after push)

```
4431eac synthesis: add capstone analysis, phase reports, session memory, updated claims progress
4035362 Add .gitkeep to preserve empty directories
94ac2ad Initial commit: The Anitalmid Project — OSKG career aptitude knowledge base
39046eb Add files via upload
```

## .gitignore Rules

Excludes from tracking:
- `.obsidian/workspace.json`, `workspace-mobile.json`, `hotkeys.json` (personal state)
- `.obsidian/cache` (plugin caches)
- `.trash/` (deleted files)
- `.DS_Store`, `Thumbs.db`, `desktop.ini` (OS junk)
- `*.tmp`, `*.bak`, `*.swp`, `*~` (editor temp)
- `__pycache__/`, `*.pyc`, `*.pyo` (Python cache)

Tracks (shared configuration):
- `.obsidian/app.json`, `appearance.json`, `core-plugins.json`, `graph.json`

## Sync Command Reference

```bash
rsync -av --delete \
  --exclude='.obsidian/workspace.json' \
  --exclude='.obsidian/workspace-mobile.json' \
  --exclude='.obsidian/cache' \
  --exclude='.trash/' \
  --exclude='.DS_Store' \
  --exclude='.git/' \
  --exclude='.gitignore' \
  --exclude='README.md' \
  --exclude='LICENSE' \
  "/mnt/c/Users/Dan/Desktop/The Anitalmid Project/The Anitalmid Project/" \
  "/mnt/c/Users/Dan/Desktop/The Anitalmid Project/GitHub Repo/"
```
