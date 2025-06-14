# Contributor & CI guidelines

This file summarises **how to keep the repo healthy**.

## 1. CI policy

| Rule | Why |
|------|-----|
| Each code commit must pass tests and linters. | Prevents breakage |
| Docs-only commits run the markdown lint job. | Saves CI minutes |

## 2. Workflow

1. Run `./setup.sh` once after cloning to install the Python deps.
2. Branch off **main** – name `feat/<topic>`.
3. Keep edits to *distinct* source files where possible.
4. Update **NOTES.md** (dated bullet) and **TODO.md** (tick or add task).
5. If you change tests, linters, or build scripts, also update **AGENTS.md**.
6. A task is *done* only when CI is **all green**.

## 3. Coding standards

* ≤ 20 lines per function, ≤ 2 nesting levels.
* 4‑space indent, `black` line length = 88.
* Validate inputs early; raise on bad data.
* End every file with a newline; keep Markdown lines ≤ 80 chars.

## 4. Documentation style

* Use fenced code blocks with language hint.
* Surround headings, lists and code with blank lines.
* Run `npx markdownlint-cli '**/*.md'` before pushing.

## 5. File roles

| File | Purpose |
|------|---------|
| `README.md` | user‑facing explainer & quick‑start |
| `TODO.md` | roadmap of work items |
| `NOTES.md` | chronological engineering log |
| `AGENTS.md` | *this* contributor guide |
| `.env` | runtime variables for the sandbox |
| `setup.sh` | dependency installer |
