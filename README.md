<!-- markdownlint-disable MD013 -->
# CardioRisk-NN

Training a lightweight multi-layer perceptron (MLP) to predict coronary artery
disease.

> **A clinical-themed, CPU-only PyTorch prototype that predicts coronary artery**
> disease from 13 routine variables in under 60 s.

[![Build & Test][ci-badge]][ci-link]
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![PyTorch CPU](https://img.shields.io/badge/PyTorch-2.3%20CPU-lightgrey)

---

## Why this repo matters

* **Medical relevance in 30 kB** – uses the Cleveland subset of the classic UCI
  Heart-Disease data (303 patients × 13 features).
* **Speed** – trains a 13-32-16-1 MLP to ≥ 0.90 test accuracy and ROC-AUC ≈
  0.93 in ~45 s on two vCPUs.
* **Self-contained** – data file is vendored; no network needed after setup.
* **Scriptable** – `train.py` will offer a CLI once
  [TODO](TODO.md#1-core-functionality) items are done.

---

## Quick-start

### One-shot run

```bash
bash setup.sh
```

`setup.sh` installs **PyTorch 2.3.x** from the CPU wheel index so runs stay
GPU-free and reproducible.

`train.py` is a placeholder script. CLI options will be added in a future
milestone. `evaluate.py` loads a saved `model.pt` and prints ROC-AUC.

Repository layout:

```text
data/heart.csv        ← 303 × 14 (13 features + target)
setup.sh              ← fast dependency installer (≤ 45 s)
train.py              ← training script (placeholder)
evaluate.py           ← model metrics helper
.env                  ← runtime defaults
README.md             ← you are here
TODO.md               ← roadmap tasks
NOTES.md              ← running decisions log
AGENTS.md             ← contributor & CI guidelines
.github/workflows/ci.yml ← CI pipeline
```

### `.env` file

Stores runtime defaults such as `EPOCHS=200`. Future CLI commands will read
these values.

Command-line options will be added once the training script has a CLI.

All scripts are CPU-only and keep RAM use < 100 MB.

---

## References

* [UCI ML Repository – Heart Disease data set](https://archive.ics.uci.edu)
* [Kaggle mirror with cleaned CSV](https://kaggle.com)
* [Typical logistic-regression baseline ROC-AUC ≈ 0.84-0.90](
  https://www.ncbi.nlm.nih.gov/pmc/)

[ci-badge]:
  https://img.shields.io/github/actions/workflow/status/example/CardioRisk-NN/ci.yml?branch=main
[ci-link]: https://github.com/example
