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
* **Scriptable** – `train.py` offers a simple CLI with `--fast` and `--seed`.

---

## Quick-start

### One-shot run

```bash
bash setup.sh
```

`setup.sh` installs **PyTorch 2.3.x** from the CPU wheel index so runs stay
GPU-free and reproducible.

Run the training script with, for example:

```bash
python train.py --epochs 200 --lr 0.01
```


Add `--fast` to run a short 10‑epoch demo. The script saves `model.pkl` and
exits with status 1 when ROC-AUC is below 0.90. Use `--seed` for reproducible
results. `evaluate.py` runs a quick training to report ROC-AUC.

Add `--fast` to run a short 10-epoch demo. Use `--seed` to fix the random
split.
`train.py` trains the MLP and saves `model.pt` when ROC-AUC ≥ 0.90.
`evaluate.py` loads this file and prints the metric.


Repository layout:

```text
data/heart.csv        ← 303 × 14 (13 features + target)
setup.sh              ← fast dependency installer (≤ 45 s)


train.py              ← training script
=======
train.py              ← MLP training script

evaluate.py           ← model metrics helper

.env                  ← runtime defaults
README.md             ← you are here
TODO.md               ← roadmap tasks
NOTES.md              ← running decisions log
AGENTS.md             ← contributor & CI guidelines
.github/workflows/ci.yml ← CI pipeline
```

See [docs/overview.md](docs/overview.md) for a sketch of the MLP and
the training workflow.

### `.env` file

Stores runtime defaults such as `EPOCHS=200`. The CLI falls back to these
values when no flags are provided.

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
