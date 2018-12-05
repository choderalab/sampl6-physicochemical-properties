#!/bin/bash

# Activate environment
source activate sampl6_pKa

# Update requirements
conda list --export > requirements.txt

# Run first step of analysis and create collection file
python typeIII_analysis.py


