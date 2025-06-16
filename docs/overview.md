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

3. The scripts split the data 80/20 for validation. Training stops when the
   validation ROC-AUC has not improved for 5 epochs.

4. Models are saved as `model.pt` or `model_tf.h5` and the scripts exit with
   code `1` if ROC-AUC < 0.90.

5. Run `python calibrate.py` to print the Brier score and save a
   reliability plot for the saved model.

Future docs will detail the dataset and training options once implemented.
