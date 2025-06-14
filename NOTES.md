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
