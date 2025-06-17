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

2. Run `python train.py --fast --seed 0` or `python train_tf.py --fast`.
   Fast mode uses 20 epochs for the PyTorch trainer and 12 for TensorFlow.

3. Data split 80/20; early stopping triggers after `--patience` stale
   validation epochs (default 5).

4. Models saved as `model.pt` or `model_tf.h5`; scripts exit 1 if AUC < 0.90.

5. Call `evaluate_saved_model(path, seed)` with the same seed used during
   training. The test split depends on the seed so metrics match only when the
   seeds align.

6. Run `python calibrate.py` to save a reliability plot and Brier score.

7. Run `python cross_validate.py --folds 5 --backend torch` (or `tf`) for a
   quick k-fold score.

8. Run `python baseline.py --seed 0` to train a logistic-regression
   baseline and save `baseline.pkl`.

See [dataset.md](dataset.md) for the dataset columns.
