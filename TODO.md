# TODO – CardioRisk‑NN initial roadmap

(Created 2025‑06‑14 from empty repo state.)

## 0. Bootstrap

- [ ] ⬜ Commit starter files (README, NOTES, TODO, AGENTS, .env, setup.sh)
- [x] ✅ Add CI workflow: black, flake8, pytest, markdown‑lint

## 1. Core functionality

- [ ] ⬜ Implement `train.py` MLP with CLI flags (epochs, lr, fast)
- [ ] ⬜ Implement `evaluate.py` to load saved model & print test metrics
- [ ] ⬜ Fail `train.py` with exit 1 if ROC‑AUC < 0.90

## 2. Testing

- [ ] ⬜ `tests/test_smoke.py` – import modules
- [ ] ⬜ `tests/test_train_fast.py` – 10‑epoch fast run under 20 s
- [ ] ⬜ `tests/test_metrics.py` – check AUC ≥ 0.85 on fixed seed

## 3. Documentation

- [ ] ⬜ Flesh out README Quick‑start once CLI stabilises
- [ ] ⬜ Add model diagram in `docs/overview.md`
- [ ] ⬜ Publish API reference via Sphinx

## 4. Stretch goals

- [ ] ⬜ TensorFlow backend (`train_tf.py`, CLI `--backend tf`)
- [ ] ⬜ Optional calibration script & reliability plot
- [ ] ⬜ Dockerfile for exact reproducibility
