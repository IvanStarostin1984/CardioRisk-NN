# Project overview

This document sketches the simple multi-layer perceptron (MLP) and the basic
training workflow.

## Network architecture

```text
13 features → [Linear 13→32] → ReLU
            → [Linear 32→16] → ReLU
            → [Linear 16→1 ] → Sigmoid
```

The model predicts the probability of coronary artery disease from 13 numeric
inputs.

## Workflow steps

1. Install dependencies with `bash setup.sh` then `pip install -e .`.

2. Run `cardiorisk-train --fast --seed 0` or `cardiorisk-train-tf --fast`.

3. Data split 80/20; early stopping triggers after `--patience` stale
   validation epochs (default 5).

4. Models saved as `model.pt` or `model_tf.h5`; scripts exit 1 if AUC < 0.90.

5. Run `cardiorisk-calibrate` to save a reliability plot and Brier score.

6. Run `cardiorisk-cross-validate --folds 5` for a quick k-fold score.

Future docs will detail the dataset and training options once implemented.
