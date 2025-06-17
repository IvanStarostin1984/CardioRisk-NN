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
   (PyTorch, TensorFlow, pandas, scikit-learn). CI installs the same
   packages with `pip install -r requirements.txt` and then calls
   `bash setup.sh` for parity. Keep the version pins in
`requirements.txt` mirrored in `setup.sh` so local installs match CI.
PyTorch and TensorFlow are pinned to minor versions (`torch==2.3.*`,
`tensorflow==2.19.*`). Bump both files together so CI and local installs
stay consistent.
2. *(Optional)* build the Docker image with `docker build -t cardiorisk .`.
3. Branch off **main** – name `feat/<topic>`.
4. Keep edits to *distinct* source files where possible.
5. Update **NOTES.md** (dated bullet) and **TODO.md** (tick or add task).
6. Search for conflict markers with `git grep '<<<<<<<'` before committing.
7. Run `npx --yes markdownlint-cli '**/*.md'` and
   `npx --yes markdown-link-check README.md` before pushing. The file
   `codex.md` is excluded via `.markdownlintignore` and `.markdownlint.json`.
8. Run `black .`, `flake8 .` and `pytest -v` before pushing.
9. If you change tests, linters, or build scripts, also update **AGENTS.md**.
10. A task is *done* only when CI is **all green**.
   Docs-only commits run only the markdown jobs; code commits run the full test suite.

## 3. Coding standards

* ≤ 20 lines per function, ≤ 2 nesting levels.
* 4‑space indent, `black` line length = 88.
* Validate inputs early; raise on bad data.
* End every file with a newline; keep Markdown lines ≤ 80 chars.
* `train.py` and `train_tf.py` exit with code 1 when ROC-AUC < 0.90.
  In tests, call `train.train_model()` or `train_tf.train_model()`
  to avoid exits.
* `baseline.py` exits with code 1 when ROC-AUC < 0.84.
  Call `baseline.train_model()` in tests to avoid the exit.

## 4. Documentation style

* Use fenced code blocks with language hint.
* Surround headings/lists/code with blank lines.
* Surround headings, lists and code with blank lines.
* Keep exactly one blank line between NOTES.md entries – markdownlint (rule MD012)
  flags multiple blank lines.

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
