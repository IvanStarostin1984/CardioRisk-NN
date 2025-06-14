#!/usr/bin/env bash
# Quick installer for CardioRisk-NN dependencies
set -e

# CPU-only PyTorch
pip install --extra-index-url https://download.pytorch.org/whl/cpu torch

# Core libraries
pip install pandas scikit-learn
