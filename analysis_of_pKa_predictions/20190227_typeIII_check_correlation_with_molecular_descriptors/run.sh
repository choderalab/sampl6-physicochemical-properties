#!/bin/bash
  
# Activate environment
source activate sampl6_pKa

# Update requirements
conda list --export > requirements.txt
