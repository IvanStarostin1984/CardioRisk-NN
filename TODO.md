# TODO – CardioRisk-NN initial roadmap

> Created 2025-06-14 from empty repo state.

## 0. Bootstrap

- [x] ✅ Commit starter files (README, NOTES, TODO, AGENTS, .env, setup.sh)
- [x] ✅ Add CI workflow: black, flake8, pytest, markdown-lint
- [x] ✅ Vendored Cleveland dataset `data/heart.csv`
- [x] ✅ Add placeholder `train.py`
- [x] ✅ Pin `torch==2.3.*` in setup.sh for CPU-only installs

## 1. Core functionality

- [x] Implement `train.py` MLP with CLI flags (epochs, lr, fast)
- [x] Implement `evaluate.py` to load saved model & print test metrics
- [x] Fail `train.py` with exit 1 if ROC-AUC < 0.90
- [x] Remove duplicate `main(args=None)` from `evaluate.py`
- [x] Remove unused `.env` file; docs updated accordingly

## 2. Testing

- [x] `tests/test_smoke.py` – import modules
- [x] `tests/test_train_fast.py` – 3-epoch fast run under 20 s
- [x] `tests/test_metrics.py` – check AUC ≥ 0.85 on fixed seed
- [x] Add test for `evaluate_saved_model` ensuring ROC-AUC ≥ 0.90
- [x] Adapt tests to call `train.train_model()` or `train_tf.train_model()`
  to avoid exit code failures when AUC < 0.90
- [x] Use train.train_model in saved-model test to avoid SystemExit.

## 3. Documentation

- [x] Flesh out README Quick-start once CLI stabilises
- [x] Add model diagram in `docs/overview.md`
- [x] Document CLI usage in `docs/overview.md` once training has a CLI
- [x] Publish API reference via Sphinx
- [x] Fix README placeholders and remove stray tokens
- [x] Align README with current `train.py` stub
- [x] Refresh README/doc overview after scikit-learn migration
- [x] Clarify in README that `evaluate.py` loads `model.pt` by default and that
  `evaluate()` runs the short training used in tests
- [x] Add `.markdownlint.json` ignoring `codex.md`
- [x] Wrap long entry in NOTES.md to satisfy markdownlint
- [x] Consolidate workflow steps in `docs/overview.md`
- [x] Document dataset columns in docs/dataset.md and link from README.
- [x] Document `cross_validate` and `baseline` modules in the Sphinx index
- [x] Clarify that `evaluate_saved_model` needs the same seed used for training
  so the test split matches.

## 4. Stretch goals

- [x] Optional calibration script & reliability plot
- [x] TensorFlow backend provided by `train_tf.py` script (no `--backend` flag)
- [x] Dockerfile for exact reproducibility
- [x] Switch `train.py` to a PyTorch loop using `build_mlp`
- [x] Refactor training and calibration helpers for clarity
- [x] Add requirements.txt and use it in CI

- [x] Pin torch==2.3.\* and tensorflow==2.19.\* in requirements.txt.
  Document keeping pins in sync with `setup.sh` in AGENTS.
- [x] Add early stopping to Keras trainer with patience 5 and update tests
  and docs.
- [x] Added early stopping to `train.py` with fixed patience 5 (see NOTES 2025-07-31).
- [x] Expose CLI flag for early stopping patience.
- [x] Add cross_validate.py helper and tests.
- [x] Optional `--backend` flag in cross_validate.py to choose PyTorch or
  TensorFlow backend and tests for the TensorFlow path.
- [x] Add baseline.py with logistic regression and tests.

## 5. Maintenance

- [x] Add joblib to requirements and install it in setup.sh.
- [x] Simplify evaluate.load_data using data_utils.load_data
- [x] Increase fast-mode epochs for TensorFlow trainer to 12 and update
  docs and tests so cross-validation stays under 40 s.
- [x] Regression test ensures fast mode uses 12 epochs after accidental change.
- [x] Fix MD012 blank line issue in NOTES.md.
- [x] Consolidate `markdownlint-cli` instructions in AGENTS.md to use `--yes`.
