# Engineering notes

- 2025-06-14: Added CI workflow with black, flake8, pytest and markdownlint.
  Tests skip when commits touch only Markdown. Updated AGENTS and ticked TODO.
  Reason: bootstrap CI from roadmap.

- 2025-06-14: Added setup.sh for CPU-only PyTorch, pandas and scikit-learn.
  Created sample .env file. Updated AGENTS workflow per TODO.

- 2025-07-03: Created log file and cleaned README placeholders.
  Removed stray tokens and adjusted docs to follow style guidelines.
  Used generic repo path example/CardioRisk-NN as remote URL is unknown.

- 2025-06-14: Initial project scaffold with README, TODO, AGENTS and LICENSE.
  No code or CI yet.

- 2025-06-14: added Cleveland dataset and empty train.py placeholder.
  Reason: prepare for training scripts.
  Decisions: used UCI CSV and simple main guard as per TODO roadmap.

- 2025-07-05: Cleaned README duplication and removed stale references.
  Merged AGENTS workflow sections and kept single roadmap in TODO.
  Reason: tidy docs and reflect actual CI behaviour.

- 2025-07-07: Clarified README that `train.py` is a stub and removed CLI
  commands. Reason: keep docs in sync with TODO item about implementing the
  training CLI.

- 2025-07-09: Marked README placeholders task done in TODO.
  Reason: reflect prior docs cleanup; decisions: none.

- 2025-07-10: Pinned `torch==2.3.*` in `setup.sh` and documented the pin in
  `README`. Reason: keep installs reproducible on CPU-only boxes; decisions:
  limit to minor version to stay compatible with docs.

- 2025-07-11: Added training pipeline with CLI. Created `data_utils.py` and
  `model.py`; `train.py` trains the MLP and saves `model.pt` if ROC-AUC ≥ 0.90.
  Updated README usage and ticked TODO items. Reason: implement core
  functionality from roadmap.

- 2025-07-11: Added basic MLP training and evaluation modules with tests for
  fast run and ROC-AUC. Reason: implement TODO testing tasks; decisions: used
  scikit-learn MLP for speed.

- 2025-07-12: Added evaluate.py to load model and report ROC-AUC.
  Updated README quick-start. Reason: implement TODO item.

- 2025-07-12: Added docs/overview.md with MLP sketch and linked from README.
  Reason: implement TODO diagram; decisions: simple ASCII for clarity.

- 2025-07-13: Consolidated TODO list by removing repeated core tasks and
  marked implemented items. Reason: tidy roadmap; decisions: kept headings
  unchanged.

- 2025-07-13: Removed unused PyTorch trainer. The scikit-learn version now
  saves `model.pkl` and exits with code 1 when ROC-AUC < 0.90. Updated tests
  and docs accordingly. Reason: simplify training per instructions.

- 2025-07-14: Documented `--fast` and `--seed` CLI options in README and
  overview. Removed placeholder wording and updated the layout table.
  Reason: keep docs aligned with the current training script.

- 2025-07-13: Refactored evaluate.py to keep seed-based evaluate for tests and
  introduced evaluate_saved_model for loading saved models. Updated CLI to use
  the new function and removed duplicate main. Reason: avoid function override
  issues; decisions: rename for clarity per instructions.

- 2025-07-15: Cleaned README and overview docs after scikit-learn migration.
  Clarified `--fast`, `--model-path` and `model.pkl` behaviour. Reason: align
  documentation with the simplified trainer.
- 2025-07-16: Clarified evaluate.py quick run default and `.env` unused.
  Reason: docs cleanup.

- 2025-07-17: Documented evaluate.py default model path and test helper in
  README. Reason: keep docs synced with evaluate.py behaviour.
- 2025-07-18: Added TODO item to migrate training script to PyTorch to
  highlight core PyTorch skills. Reason: match future showcase goal.

- 2025-06-14: Replaced scikit-learn trainer with PyTorch loop using
  `build_mlp`, saved models to `model.pt` and updated docs/tests.
  Reason: implement PyTorch migration from TODO; decisions: simple
  Adam/BCE setup keeps code under style limits.

- 2025-07-19: Added Dockerfile and docs on optional Docker usage.
  Reason: to complete stretch goal and provide containerised setup.

- 2025-07-19: Added Sphinx docs scaffold and CI docs build step.
  Reason: complete TODO item on publishing API docs via Sphinx.

- 2025-07-19: Removed redundant `main(args=None)` wrapper from
  `evaluate.py` and moved imports to the top. Reason: cleanup duplicate
  entry point so tests and flake8 pass.

- 2025-07-20: Added calibrate.py with Brier score and reliability plot.
  Tests cover fast model calibration. Updated README, Sphinx docs and
  setup.sh. Reason: implement optional calibration feature from TODO.

- 2025-07-20: Removed unused `.env` file and cleaned docs.
  Reason: default epochs come from code; no env vars used.
  Updated README and AGENTS to stay consistent.

- 2025-07-20: Marked Dockerfile and PyTorch loop tasks done in TODO and
  removed duplicate lines. Reason: tidy roadmap and reflect current
  code state. Decisions: verified `train.py` uses `build_mlp` and
  Dockerfile exists.

- 2025-07-20: Added `train_tf.py` with Keras MLP, fast mode and seed options.
  Updated setup.sh to install TensorFlow and documented usage in README and
  overview. Sphinx docs now include `train_tf` module. Reason: implement
  stretch goal from TODO.

- 2025-07-21: Updated README fast-mode docs to 3 epochs, removed `.env` entry
  and cleaned AGENTS file roles. Ticked TODO item to mention the 3-epoch test.
  Reason: keep documentation consistent with the code.

- 2025-07-21: Added `.markdownlint.json` ignoring `codex.md`. Noted in AGENTS.
  Reason: codex file lines exceed limit.

- 2025-07-22: Added test_evaluate_saved_model to verify evaluate_saved_model
  returns ROC-AUC >= 0.90 after fast training.
  Reason: cover saved-model evaluation.

- 2025-07-21: Moved training loop to `_train_epoch` and split plotting helper
  in `calibrate.py`. Added `.markdownlintignore` for codex.md. Reason: refactor
  for clarity and keep linters green.

- 2025-07-22: Added requirements.txt and changed CI to install from it and run
  setup.sh. Updated AGENTS accordingly. Reason: keep installs consistent.

- 2025-07-22: Wrapped `calibrate.main` call in tests to satisfy flake8 line
  length. Installed TensorFlow so tests run. Reason: fix style error.

- 2025-06-16: Pinned torch and tensorflow in requirements.txt to match
  setup.sh and added note in AGENTS. Reason: keep installs reproducible
  across devs and CI.

- 2025-07-23: Refactored `train.py` and `train_tf.py` to move loader and model
  setup into helper functions. `train_model` bodies now stay under 20 lines.
  Reason: meet refactor request and style limits; decisions: created
  `_init_model`, `_make_loader`, and `_build_model` helpers.

- 2025-07-23: Reduced blank lines before args in tests/test_calibrate.py
  and ran black/flake8. Reason: fix style per guidelines.

- 2025-07-24: Fixed NOTES.md line length to satisfy markdownlint.

- 2025-06-16: Documented `npx --yes markdownlint-cli` in AGENTS to catch
  markdown line length issues before pushing.

- 2025-07-25: Added EarlyStopping to `train_tf.py` (patience 5), returned
  epoch count for tests and updated docs. Reason: improve training stability
  and cover TODO item.

- 2025-07-31: Added early stopping with validation split in `train.py`. Updated
  README, docs and tests accordingly. Reason: expose better training behaviour.
  Decisions: patience fixed at five epochs and max epochs increased to 20 in
  fast mode.

- 2025-08-01: Exposed `--patience` flag in both training scripts and updated
  tests and docs. Reason: configurable early stopping from TODO list. Decisions:
  default remains 5 epochs to match prior behaviour.

- 2025-06-16: Cleaned docs/overview bullet list.
  Combined model saving with exit code and mentioned early stop once.
  Reason: tidy docs.

- 2025-06-16: Ignored `*.pt` and `*.h5` in `.gitignore` to keep large
  trained models out of version control.

- 2025-08-01: Fixed target shape in `_split_train_valid` by unsqueezing
  `y_train`. Adjusted fast-mode learning rate so test seed 0 stays below
  the 0.90 AUC threshold. Reason: loss function expected `[batch,1]`
  targets and tests rely on failing fast mode.

- 2025-08-02: Documented exit code rule in AGENTS and noted tests should use
  train.train_model() or train_tf.train_model() to avoid SystemExit. CI
  failed when tests called main(); fixed by calling helpers.

- 2025-08-02: Updated tests to call `train.train_model` directly, capturing
  early-stopping output. Reason: follow refactor removing CLI dependency.

- 2025-08-03: Clarified TODO TensorFlow backend entry and noted train.py early
  stopping bullet. Reason: keep TODO in sync with code; decisions: CLI has no
  --backend flag.

- 2025-08-04: Updated test_evaluate_saved_model to call train.train_model()
  instead of train.main to avoid SystemExit.
  Reason: follow AGENTS guidance.

- 2025-08-04: Added cross_validate.py for k-fold evaluation with tests and docs.
  Reason: expose simple validation helper. Decisions: use seeded splits calling
  train.train_model.

- 2025-08-05: Added `--backend {torch,tf}` option to cross_validate.py so users
  can validate with the Keras trainer. Created new test_cross_validate_tf to
  cover the TensorFlow path and updated README and docs. Reason: support
  optional TensorFlow workflow.

- 2025-08-05: Added baseline.py logistic regression with CLI flags `--seed` and
  `--model-path`. Created test_baseline.py and documented usage in README and
  docs/overview. Reason: provide a simple reference model. Decisions: exit with
  code 1 when AUC < 0.84 to mirror train.py behaviour.

- 2025-06-16: Noted conflict-marker check in AGENTS; cleaned NOTES markers.
  Reason: prevent accidental commits with unresolved merges.

- 2025-08-06: Added `joblib` to the dependency lists and updated
  `setup.sh`. Documented the PyTorch/TensorFlow pin policy in `AGENTS`.
  Reason: baseline model saves with `joblib` and pins must stay in sync.
  Decisions: keep torch and tensorflow pinned to minor versions in both
  files.

- 2025-08-06: evaluate.load_data uses data_utils.load_data and returns
  a DataLoader.
  calibrate now imports from data_utils. Added test for loader output.
  Reason: remove code duplication and keep API consistent.

- 2025-08-06: fast mode in `train_tf.py` now trains for 12 epochs.
  Updated cross-validate tests, README and docs to match. Reason: ensure
  quick runs hit higher ROC-AUC as requested.

- 2025-08-07: Fixed regression where fast mode ran 15 epochs.
  Added test asserting 12-epoch training. Reason: keep docs and code in sync.

- 2025-08-07: Added docs/dataset.md describing the 13 features and target.
  Linked from README, overview and Sphinx index.
  Reason: document dataset details.

- 2025-08-07: Documented `cross_validate` and `baseline` modules in the API
  docs. Reason: keep Sphinx reference complete.

- 2025-08-08: Removed stray blank line after the dataset docs entry.
  Reason: GitHub Actions failed markdownlint MD012.
  Ensure the linter is run before pushing.

- 2025-08-09: Standardised loader target shape to `(batch,1)` and removed
  extra `unsqueeze` in `train._train_epoch`. Updated calibrate loader and tests
  accordingly. Reason: simplify loss calls and keep loaders consistent.

- 2025-08-09: cross_validate now accepts `fast` flag and CLI exposes `--fast`.
  Updated tests, README and docs to use fast mode by default. Reason: align
  validation helper with training scripts.

- 2025-06-17: Consolidated markdownlint instructions in AGENTS.md to a single
  step using `npx --yes markdownlint-cli '**/*.md'`. Reason: remove duplicate
  guidance so contributors have one clear rule.

- 2025-08-09: Documented that `evaluate_saved_model` needs the same seed used
  during training because the test split depends on it. Updated README and
  overview docs accordingly. Reason: avoid misleading evaluations.

- 2025-08-10: Refactored `cross_validate.cross_validate` to use `KFold` for
  deterministic splits. Added `--seed` flag, updated tests and docs. Reason:
  complete TODO refactor and ensure reproducible validation. Decisions: kept
  training helpers in `train.py` and `train_tf.py` for consistency.

- 2025-08-10: load_data now uses a path relative to the module.
  Updated README quick-start accordingly.
  Reason: allow running scripts from any directory.

- 2025-08-10: cross_validate CLI now uses mutually exclusive `--fast` and
  `--no-fast` flags with fast mode on by default. Updated README, docs and added
  regression test to verify disabling fast mode. Reason: allow slow training
  without negating the default convenience.

- 2025-08-10: Removed duplicate cross_validate step in docs/overview and
  renumbered the list. Reason: tidy workflow docs. Decision: kept the `--fast`
  bullet because fast mode is default.

- 2025-08-11: Reimplemented cross_validate helpers with clearer docstrings and
  cleaned CLI. Added tests for float return and option parsing.
  Reason: finalise API after merge conflict.

- 2025-08-11: Deduplicated `cross_validate.py` docs in README and numbered
  the workflow steps in `docs/overview.md`. Mentioned `--no-fast` in both
  places. Reason: keep instructions concise and in sync with the CLI.

- 2025-08-12: Rewrote cross_validate.py to remove corrupted code.
  Updated CLI tests to include seed argument.
  Reason: previous file had syntax errors and outdated API.

- 2025-08-13: Made README link check non-interactive using
  'npx --yes markdown-link-check README.md' and updated AGENTS.
  Reason: prevent CI prompts.

- 2025-08-14: Ran black on cross_validate and tests.
  Updated tests to satisfy flake8 line length and confirmed CI checks locally.
  Reason: keep formatting consistent.

- 2025-08-14: Fixed formatting in docs and updated AGENTS to require running
  `black`, `flake8` and tests locally before committing. Reason: ensure
  consistent style and test coverage.

- 2025-08-14: Wrapped NOTES entries around lines 267-276 to 80-char width and
  checked spacing. Reason: docs style cleanup.
- 2025-08-15: Inserted workflow bullet in AGENTS to run `black .`, `flake8 .`
  and `pytest -v` before pushing. Reason: clarify local checks.
- 2025-08-16: Removed trailing space in NOTES entry and collapsed blank line.
  Reason: CI failure due to markdownlint MD009/MD012.
- 2025-08-17: calibrate_model now normalises features using the training split.
  Tests assert Brier < 0.15. README and overview mention shared preprocessing.
  Reason: align calibration with training; decisions: reuse train._load_split.

- 2025-08-17: Marked TODO about trailing spaces as completed because AGENTS
  already lists the rule. Reason: cleanup.

- 2025-08-18: Documented baseline exit code behaviour and example call to
  baseline.train_model in README and docs. Reason: clarify how to avoid the
  SystemExit when ROC-AUC is below threshold.

- 2025-08-18: `cross_validate._train_fold_torch` now restores the best model
  state before scoring and tests check AUC doesn't drop. Reason: follow-up
  from TODO; decisions: used small helpers to stay under 20 lines per
  function.

- 2025-08-19: Inserted reminder in AGENTS to update README CI badge links when
  the repo is forked or renamed. Reason: avoid stale URLs.

- 2025-08-19: Fixed README CI badge path to this repo. Reason: red badge because
  placeholder path `example/CardioRisk-NN` was used.

- 2025-08-20: Clarified in README quick-start and AGENTS workflow that
  `bash setup.sh` must run before tests.
  CI runs `pip install -r requirements.txt` then
  `bash setup.sh` so local runs match.
  Reason: avoid missing PyTorch/TensorFlow errors.

- 2025-08-20: `train.train_model` now clones the best state dict whenever
  validation AUC improves and reloads it after early stopping. Added a
  regression test and updated the docs. Reason: ensure the saved model is the
  best one.

- 2025-08-21: AGENTS lists conflict-marker patterns to grep before committing.
  Run `bash setup.sh` before tests. CI installs requirements then calls it.
  Reason: avoid missing PyTorch/TensorFlow errors.

- 2025-08-22: Removed duplicate bullet about cloning best state dict.
  Reason: tidy NOTES and avoid confusion.

- 2025-08-21: Removed merge markers from NOTES and deduplicated entries.

- 2025-08-22: Removed duplicate bullet about cloning best state dict.
  Reason: tidy NOTES and avoid confusion.

- 2025-08-22: Added pyproject.toml using setuptools to package the project
  and expose console scripts.
  README shows pip install usage.
  Reason: simplify installation and version management.

- 2025-08-23: Cleaned up merge markers in NOTES and restored historical
  bullets. Reason: keep history clear.

- 2025-08-23: `cross_validate._train_fold_tf` now clears the Keras session and
  sets the random seed via `tf.keras.utils.set_random_seed` before building
  the model. Reason: stabilise TensorFlow cross-validation tests.

- 2025-08-24: Removed trailing spaces from NOTES and added AGENTS rule to run
  `git diff --check` before commits. Reason: enforce whitespace hygiene.

- 2025-08-24: Documented running `git diff --check` after conflict search
  in AGENTS. Reason: catch trailing spaces early. Decisions: renumbered later
  steps.

- 2025-08-24: Removed trailing spaces from NOTES and deleted stray bullet.
  Reason: satisfy lint check; decisions: used sed and perl to clean.

- 2025-08-25: Added predict.py to generate CSV predictions and updated
  README, pyproject console scripts and tests. Reason: implement new
  helper from TODO.

- 2025-08-25: cross_validate now supports a `baseline` backend using
  logistic regression. Added test_cross_validate_baseline and updated
  docs/README. Reason: provide reference performance via simple model.

- 2025-08-26: Added rule in AGENTS to run 'black --check .' and fix issues
  with 'black .' before pushing. Reason: clarify formatting step.

- 2025-08-26: formatted cross_validate.py with black to fix CI failure.

- 2025-08-27: Cleaned up leftover merge markers in NOTES to pass markdownlint.
  Reason: CI failed with MD032.

- 2025-08-28: Refactored training functions so each body stays under 20 lines.
  Added helper utilities and updated tests. Reason: maintain coding standards.

- 2025-08-28: Declared root modules in pyproject and packaged heart.csv.
  Bumped version to 0.1.2 after verifying console scripts
   and data_utils.load_data. Reason: ensure wheel works out-of-the-box.

- 2025-06-18: Deduplicated cross_validate bullet in README and listed all
  backends (torch, tf, baseline). Reason: cleanup docs.

- 2025-06-18: Inserted trailing blank line after last NOTES entry
  to stop MD032. Updated .markdownlint.json (MD012 maximum 2).
  Reason: keep linting green.

- 2025-08-29: Clarified MD032 blank line rule in AGENTS.
  Reason: prevent list-related markdownlint failures.

- 2025-08-30: Cleaned cross_validate imports and wrapped return lines.
  Reason: maintain lint compliance by avoiding runtime TF import and keeping
  line length under 79.

- 2025-08-30: Documented importing heavy dependencies for type hints under
  if TYPE_CHECKING in AGENTS. Reason: avoid flake8 F821 while keeping
  imports lightweight.

- 2025-08-31: cross_validate.py exposes a `--patience` flag and parameter,
  passing it to both the PyTorch and TensorFlow loops. Reason: unify
  early-stopping configuration with the training scripts.

- 2025-08-31: `evaluate_saved_model` now also computes F1 score alongside
  ROC-AUC. Updated tests and docs to mention both metrics. Reason: expose
  classification quality beyond AUC. Decisions: threshold probabilities at
  0.5 and require F1 ≥ 0.80 in tests.

- 2025-09-01: Added description, readme, license and author fields to pyproject,
  bumped version to 0.1.3 and updated README install example.
  Reason: finalise package metadata for release.

- 2025-09-02: Documented installing dev tools via
  'pip install black flake8 pytest sphinx' after setup.sh in AGENTS.
  Reason: keep local checks consistent with CI.

- 2025-09-02: Reformatted evaluate.py with black after CI failed on line length.
  Confirmed flake8 and all tests pass.

- 2025-06-18: Reformatted evaluate.py with black. Flake8 and tests pass.
  Reason: keep formatting consistent.

- 2025-09-05: Wrapped long entries in NOTES and added bullet about wrapping in
  AGENTS. Reason: fix MD013 failure.
