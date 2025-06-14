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

1. Install dependencies with `bash setup.sh`.

2. Run `python train.py --fast --seed 0` for a quick demo.

3. The script saves `model.pkl` and exits with code `1` if ROC-AUC < 0.90.

Future docs will detail the dataset and training options once implemented.
