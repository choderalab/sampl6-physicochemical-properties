## 2017/12/17

# Updating Microstates Lists

Goals for v1_4_2:
1. Adding missing microstate(SM21_micro020) identified by Epik prediction
2. adding a canonical SMILES column
2. lists of suggested physical microstate pairs (microstates pairs that interconvert by one deprotonation event) 

## Correction to microstate lists
SM21_micro020 microstate was deprecated by mistake. We caught it via  Epik prediction.
I removed the "deprecated" remark for this microstate in v1_4_2 cumulative correction files.

## Adding canonical SMILES column

Run update_microstate_lists_files.ipynb
Output directory: microstate_lists_with_canonical_SMILES/

## List of physical microstate pairs

Run enumerate_microstate_pairs.ipynb  
Output directory: microstate_pairs/

