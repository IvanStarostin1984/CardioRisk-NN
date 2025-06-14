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
- [x] `tests/test_train_fast.py` – 10-epoch fast run under 20 s
- [x] `tests/test_metrics.py` – check AUC ≥ 0.85 on fixed seed

## 3. Documentation

- [x] Flesh out README Quick-start once CLI stabilises
- [x] Add model diagram in `docs/overview.md`
- [x] Document CLI usage in `docs/overview.md` once the training script has a CLI
- [x] Publish API reference via Sphinx
- [x] Fix README placeholders and remove stray tokens
- [x] Align README with current `train.py` stub
- [x] Refresh README/doc overview after scikit-learn migration
- [x] Clarify in README that `evaluate.py` loads `model.pt` by default and that
  `evaluate()` runs the short training used in tests

## 4. Stretch goals

- [x] TensorFlow backend (`train_tf.py`, CLI `--backend tf`)
- [ ] Optional calibration script & reliability plot
- [x] Dockerfile for exact reproducibility
- [x] Switch `train.py` to a PyTorch loop using `build_mlp`
