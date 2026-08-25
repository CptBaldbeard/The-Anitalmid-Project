# Contributing to The Anitalmid Project

The Anitalmid Project is a career-mapping engine: a FastAPI backend and a
vanilla-JS single-page app (see `webapp/`), plus a curated vault of role
profiles and psychometric frameworks. We build it with a **spec-driven,
pull-request-based workflow**. Never push directly to `main`.

## Workflow

1. **Spec first.** Every feature starts with a written spec, agreed between the
   author and the collaborator *before* any code. If a request arrives without
   a spec, ask for one first.
2. **Worktree + branch.** Create a `git worktree` off `main` on a new branch
   named with a Conventional Commits type — e.g. `feat/job-matching`,
   `fix/mobile-layout`, `docs/contributing`.
3. **Implement + validate.** Write the code and any tests. CI
   (`.github/workflows/ci.yml`) runs a Python compile + backend import smoke
   test and a JS syntax check on every pull request.
4. **Open a PR.** Push the branch and open a pull request into `main`. CI must
   pass. Describe *what* changed and *why*.
5. **Squash-merge.** Merge the PR with squash (keeps history linear), delete
   the branch, and remove the worktree.

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>
```

`type` is one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore`, `revert`. Subject in imperative present tense, at most
50 characters; the body explains *why*, not *what*.

## Code style

- **Python:** type hints (PEP 484); clean `ruff check` and `ruff format`.
- **Many small, focused modules** over god files (single responsibility).
- Explicit beats implicit.

## Tests

CI currently runs a compile + import smoke test (backend) and syntax checks
(frontend). Unit tests are on the roadmap — add `pytest` tests for new backend
logic as it lands, asserting invariants rather than frozen snapshots.
