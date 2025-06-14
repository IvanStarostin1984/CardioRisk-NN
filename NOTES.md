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
