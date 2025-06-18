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
   validation epochs (default 5) and the best weights are restored.

4. Models saved as `model.pt` or `model_tf.h5`; `train.py` and `train_tf.py`
   exit with code 1 if AUC < 0.90. `baseline.py` exits with code 1 if AUC
   < 0.84.

5. Call `evaluate_saved_model(path, seed)` with the same seed used during
   training. The helper prints ROC-AUC and F1 score. The test split depends on
   the seed so metrics match only when the seeds align.

6. Run `python cross_validate.py --folds 5 --backend torch` (or `tf` or
   `baseline`) for k-fold evaluation. Splits come from
   `sklearn.model_selection.KFold` and can be reproduced with `--seed 0`
   (default). Fast mode is on by default; add `--no-fast` for the full
   200 epochs. Set `--patience N` to control early stopping (default 5).

7. Run `python calibrate.py` to save a reliability plot and Brier score.
   The script uses the same preprocessing as `train.py` so the mean and
   standard deviation come from the training split.

8. Run `python baseline.py --seed 0` to train a logistic-regression baseline
   and save `baseline.pkl`. In tests, call `baseline.train_model()` directly
   to read the AUC without triggering a SystemExit:

   ```python
   import baseline
   auc = baseline.train_model(seed=0, model_path="baseline.pkl")
   ```

See [dataset.md](dataset.md) for the dataset columns.
