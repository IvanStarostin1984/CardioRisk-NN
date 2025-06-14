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
python train.py --seed 0
```

Add `--fast` for a 10‑epoch demo and `--model-path` to set the output `.pkl`
file. The script saves `model.pkl` and exits with status 1 when ROC‑AUC is below
0.90.

`train.py` trains the MLP and saves `model.pkl` when ROC‑AUC ≥ 0.90.
`evaluate.py` loads a saved `model.pt` by default via the `--model-path`
argument and prints ROC‑AUC. The module's `evaluate()` function (not the CLI)
performs a short training run used in the tests.

Repository layout:

```text
data/heart.csv        ← 303 × 14 (13 features + target)
setup.sh              ← fast dependency installer (≤ 45 s)

train.py              ← MLP training script
evaluate.py           ← model metrics helper

.env                  ← unused placeholder
README.md             ← you are here
TODO.md               ← roadmap tasks
NOTES.md              ← running decisions log
AGENTS.md             ← contributor & CI guidelines
.github/workflows/ci.yml ← CI pipeline
```

See [docs/overview.md](docs/overview.md) for a sketch of the MLP and
the training workflow.

### `.env` file

This file is currently unused and only kept as a placeholder for potential
environment variables.

All scripts are CPU-only and keep RAM use < 100 MB.


### Docker usage

An optional container builds from the repo and installs packages via
`setup.sh`.

```bash
docker build -t cardiorisk .
docker run --rm cardiorisk --fast --seed 0
```

The second command runs the demo training inside the container.

### Building the docs

Install Sphinx and run:

```bash
sphinx-build -b html docs/source docs/_build
```

The HTML pages appear in `docs/_build`.


---

## References

* [UCI ML Repository – Heart Disease data set](https://archive.ics.uci.edu)
* [Kaggle mirror with cleaned CSV](https://kaggle.com)
* [Typical logistic-regression baseline ROC-AUC ≈ 0.84-0.90](
  https://www.ncbi.nlm.nih.gov/pmc/)

[ci-badge]:
  https://img.shields.io/github/actions/workflow/status/example/CardioRisk-NN/ci.yml?branch=main
[ci-link]: https://github.com/example
