# CardioRisk‑NN

Training a lightweight multi‑layer perceptron (MLP) to predict presence of
coronary artery disease

> **A clinical‑themed, CPU‑only PyTorch prototype that predicts coronary artery
> disease from 13 routine variables in under 60 s.**

<!-- markdownlint-disable MD013 -->
# CardioRisk-NN

Training a lightweight multi-layer perceptron (MLP) to predict coronary artery disease.

> **A clinical-themed, CPU-only PyTorch prototype that predicts coronary artery disease from 13 routine variables in under 60 s.**


[![Build & Test](https://img.shields.io/github/actions/workflow/status/example/CardioRisk-NN/ci.yml?branch=main)](https://github.com/example/CardioRisk-NN/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![PyTorch CPU](https://img.shields.io/badge/PyTorch-2.3%20CPU-lightgrey)

---

## Why this repo matters

* **Medical relevance in 30 kB** – uses the Cleveland subset of the classic UCI
  Heart-Disease data (303 patients × 13 features).
* **Speed** – trains a 13-32-16-1 MLP to ≥ 0.90 test accuracy and ROC-AUC ≈
  0.93 in ~45 s on two vCPUs.
* **Self-contained** – data file is vendored; no network needed after setup.
* **Scriptable** – a single CLI (`python train.py`) prints the metrics and
  exits with non-zero status if ROC-AUC < 0.90, so it slots into any CI gate.

---

## Quick-start


### One-shot run (installs deps on first call)

```bash
make run
```

`make run` calls `setup.sh` to install torch, pandas and scikit-learn then runs
`python train.py --epochs 200`.

```bash
# install deps on first call, then run full training
make run
```


Expected console tail:

```text
Epoch 200/200 – loss: 0.165 – val_AUC: 0.927
Test accuracy: 0.901 | ROC-AUC: 0.931
```

Repository layout:

```text
data/heart.csv        ← 303 × 14 (13 features + target)
setup.sh              ← fast dependency installer (≤ 45 s)
train.py              ← full train + evaluation
quick_test.sh         ← 10-epoch smoke test (<15 s)
requirements.txt      ← pinned deps for CI
.env                  ← runner configuration (see below)
README.md             ← you are here
TODO.md               ← roadmap tasks
NOTES.md              ← running decisions log
AGENTS.md             ← contributor & CI guidelines
.github/workflows/    ← CI pipeline (to be added)
```

Command-line options:

```bash
python train.py --epochs 200 --lr 1e-3    # default full run
python train.py --epochs 10 --fast        # smoke test
python evaluate.py                        # metric-only re-run
```

All scripts are CPU-only and keep RAM use < 100 MB.

References
UCI ML Repository – Heart Disease data set
archive.ics.uci.edu

Kaggle mirror with cleaned CSV
kaggle.com

Typical logistic‑regression baseline ROC‑AUC ≈ 0.84‑0.90
pmc.ncbi.nlm.nih.gov

---

## References

* [UCI ML Repository – Heart Disease data set](https://archive.ics.uci.edu)
* [Kaggle mirror with cleaned CSV](https://kaggle.com)
* [Typical logistic-regression baseline ROC-AUC ≈ 0.84-0.90](https://pmc.ncbi.nlm.nih.gov)

