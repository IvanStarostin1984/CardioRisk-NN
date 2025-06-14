import os
import sys

# Add project root to path so autodoc can import modules
sys.path.insert(0, os.path.abspath("../.."))

project = "CardioRisk-NN"
author = "Example"

extensions = ["sphinx.ext.autodoc"]

html_theme = "alabaster"

templates_path = ["_templates"]
exclude_patterns = []
