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
   (PyTorch, TensorFlow, pandas, scikit-learn). Run it before `pytest`
   or the tests will fail. CI installs the same packages with
   `pip install -r requirements.txt` and then calls `bash setup.sh` for
   parity. Keep the version pins in `requirements.txt` mirrored in
   `setup.sh` so local installs match CI. PyTorch and TensorFlow are
   pinned to minor versions (`torch==2.3.*`, `tensorflow==2.19.*`). Bump
   both files together so CI and local installs stay consistent.
2. Install the dev tools with `pip install black flake8 pytest sphinx`
   after running `setup.sh`. This keeps your local checks consistent
   with CI.
3. *(Optional)* build the Docker image with `docker build -t cardiorisk .`.
4. Branch off **main** – name `feat/<topic>`.
5. Keep edits to *distinct* source files where possible.
6. Update **NOTES.md** (dated bullet) and **TODO.md** (tick or add task).
7. Search for conflict markers with:
   git grep -n '<<<<<<<\|=======\|>>>>>>>'
   before committing. Leftover markers often cause markdownlint errors (e.g. MD032).
8. Run `git diff --check` to catch trailing whitespace before committing.

9. Run `npx --yes markdownlint-cli '**/*.md'` and
   `npx --yes markdown-link-check README.md` before pushing. The file
   `codex.md` is excluded via `.markdownlintignore` and `.markdownlint.json`.
10. Run `black --check .` before pushing.
   If it reports issues, run `black .` to format.
   Then re-run `black --check .`, `flake8 .` and `pytest -v`.
11. If you change tests, linters, or build scripts, also update **AGENTS.md**.
12. A task is *done* only when CI is **all green**.
    Docs-only commits run only the markdown jobs;
    code commits run the full test suite.
13. If you fork or rename the repo, update the CI badge links in `README.md`.
14. Bump the version in `pyproject.toml` whenever packaging or console scripts change.

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
* Import heavy packages used only for type hints inside `if TYPE_CHECKING:`
  blocks. This avoids flake8 F821 and keeps runtime imports light. Run
  `flake8 .` after updating such hints.

## 4. Documentation style

* Use fenced code blocks with language hint.
* Surround headings/lists/code with blank lines.
* Surround headings, lists and code with blank lines.
* Keep exactly one blank line between NOTES.md entries.
  The linter allows up to two blank lines (`MD012` maximum=2)
  so the final entry can end with a blank line.
* Avoid trailing spaces—markdownlint (rule MD009) fails if a line ends with spaces.
  Run `npx markdownlint-cli '**/*.md'` to check.
* Break long NOTES.md bullets across multiple lines with two-space indentation
  so each line stays ≤ 80 characters.
* Follow every list with a blank line—even after the last item—so
  markdownlint rule MD032 passes.

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
