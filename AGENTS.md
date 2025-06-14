# Contributor & CI guidelines

This file summarises **how to keep the repo healthy**.

## 1. CI policy

| Rule | Why |
|------|-----|
| Every code commit **must** pass all tests and linters. | Prevents breakage |
| Docs‑only commits run markdown‑lint + link‑check. | Saves CI minutes |

The pipeline lives at `.github/workflows/ci.yml` and skips tests when
all changed files are Markdown.
It always builds the Sphinx docs with `sphinx-build`.

## 2. Workflow

1. Run `./setup.sh` once after cloning to install the Python deps
   (PyTorch, TensorFlow, pandas, scikit-learn).
2. *(Optional)* build the Docker image with `docker build -t cardiorisk .`.
3. Branch off **main** – name `feat/<topic>`.
4. Keep edits to *distinct* source files where possible.
5. Update **NOTES.md** (dated bullet) and **TODO.md** (tick or add task).
6. Run `npx markdownlint-cli '**/*.md'` before pushing.
7. If you change tests, linters, or build scripts, also update **AGENTS.md**.
8. A task is *done* only when CI is **all green**.
   Docs-only commits run only the markdown jobs; code commits run the full test suite.

## 3. Coding standards

* ≤ 20 lines per function, ≤ 2 nesting levels.
* 4‑space indent, `black` line length = 88.
* Validate inputs early; raise on bad data.
* End every file with a newline; keep Markdown lines ≤ 80 chars.

## 4. Documentation style

* Use fenced code blocks with language hint.
* Surround headings/lists/code with blank lines.
* Surround headings, lists and code with blank lines.
* Run `npx markdownlint-cli '**/*.md'` before pushing.

## 5. File roles

| File | Purpose |
|------|---------|
| `README.md` | user‑facing explainer & quick‑start |
| `TODO.md` | roadmap of work items |
| `NOTES.md` | chronological engineering log |
| `AGENTS.md` | *this* contributor guide |

| `setup.sh` | dependency installer (PyTorch & TensorFlow) |

| `.github/workflows/ci.yml` | lints & tests in CI |
| `Dockerfile` | optional container image |
