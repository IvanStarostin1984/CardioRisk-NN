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

2. Run `python train.py --fast --seed 0` for a PyTorch demo or
   `python train_tf.py --fast --seed 0` for the Keras version.

3. The scripts save `model.pt` or `model_tf.h5` and exit with code `1` if
   ROC-AUC < 0.90.

4. Run `python calibrate.py` to print the Brier score and save a
   reliability plot for the saved model.

Future docs will detail the dataset and training options once implemented.
