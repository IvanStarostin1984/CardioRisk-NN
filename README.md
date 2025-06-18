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
  Heart-Disease data (303 patients × 13 features). See [dataset overview](docs/dataset.md).
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

`setup.sh` installs **PyTorch 2.3.x** and **TensorFlow 2.x** from CPU wheels so
runs stay GPU-free and reproducible.

Run the script once before running tests:

```bash
pytest -v
```

CI first executes `pip install -r requirements.txt` and then `bash setup.sh`
so local test runs mirror the pipeline.

All helpers read `data/heart.csv` using a path relative to the module, so you
can run scripts from any directory.

Run the PyTorch training script with, for example:

```bash
python train.py --seed 0
```

The Keras variant runs similarly:

```bash
python train_tf.py --seed 0
```

The logistic-regression baseline runs as:

```bash
python baseline.py --seed 0
```

Running `baseline.py` exits with status 1 when ROC-AUC is below 0.84. Use
`baseline.train_model()` if you need the AUC without the exit:

```python
import baseline
auc = baseline.train_model(seed=0, model_path="baseline.pkl")
```

Add `--fast` for a quick demo with early stopping. Use `--patience N` (default
5, max 20 epochs in fast mode for `train.py`, 12 for `train_tf.py`) and
`--model-path` to set the output file. The trainer reloads the best validation
weights before scoring. `train.py` saves `model.pt` while `train_tf.py` defaults
to `model_tf.h5`. Both
exit with status 1 when ROC‑AUC is below 0.90.
`train_tf.py` also applies early stopping and accepts the same `--patience`
flag so longer runs stop once the loss plateaus.

`train.py` trains the MLP and saves `model.pt` when ROC‑AUC ≥ 0.90.
`evaluate.py` loads a saved `model.pt` by default via the `--model-path`
argument and prints ROC‑AUC. Call `evaluate_saved_model(path, seed)` with the
same seed used for training because the test split depends on it. The module's
`evaluate()` function (not the CLI) performs a short training run used in the
tests.
`calibrate.py` uses the same preprocessing as `train.py` to report the Brier
score and save a reliability plot image for any saved model.
`cross_validate.py` runs k-fold validation.
Use `--backend {torch,tf,baseline}` to pick a trainer,
`--seed` for reproducible splits and `--no-fast` to disable fast mode.
The script outputs the mean ROC-AUC.
`predict.py` loads a saved `model.pt` and writes predicted probabilities to a
CSV file:

```bash
python predict.py --model-path model.pt --output preds.csv --seed 0
```

### Install as a package

```bash
pip install .
```

This installs console commands like `cardiorisk-train` and `cardiorisk-evaluate`.
Run them the same way as the Python scripts:

```bash
cardiorisk-train --seed 0
cardiorisk-train-tf --seed 0
cardiorisk-evaluate --model-path model.pt
cardiorisk-calibrate --model-path model.pt
cardiorisk-cross-validate --folds 5
cardiorisk-baseline --seed 0
cardiorisk-predict --model-path model.pt --output preds.csv
```

The dataset file ships with the wheel, so `data_utils.load_data()` works
without extra paths.

Repository layout:

```text
data/heart.csv        ← 303 × 14 (13 features + target)
setup.sh              ← fast dependency installer (≤ 45 s)

train.py              ← MLP training script
train_tf.py           ← Keras training script
evaluate.py           ← model metrics helper
calibrate.py          ← reliability plot helper
cross_validate.py     ← k-fold validation helper
baseline.py          ← logistic-regression baseline
predict.py          ← save predictions to CSV

README.md             ← you are here
TODO.md               ← roadmap tasks
NOTES.md              ← running decisions log
AGENTS.md             ← contributor & CI guidelines
.github/workflows/ci.yml ← CI pipeline
```

See [docs/overview.md](docs/overview.md) for a sketch of the MLP and
the training workflow. Dataset columns are described in [docs/dataset.md](docs/dataset.md).

### `.env` file

No `.env` file is provided because the scripts run without extra
environment variables. All jobs stay CPU‑only and use under 100 MB of RAM.

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
<!-- markdown-link-check-disable -->
* [Typical logistic-regression baseline ROC-AUC ≈ 0.84-0.90](
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4885402/)
<!-- markdown-link-check-enable -->

[ci-badge]:
  https://img.shields.io/github/actions/workflow/status/IvanStarostin1984/CardioRisk-NN/ci.yml?branch=main
[ci-link]: https://github.com/IvanStarostin1984/CardioRisk-NN
