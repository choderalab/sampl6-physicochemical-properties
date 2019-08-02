## 2019/03/02

### Microstate analysis of Type I predictions for  4-aminoquinazoline series 

Using closest algorithm, predicted pKa values were matched to experimental pKa values. 
For type I predictions participants have also reported Microstate ID pairs of each of their predicted pKa values.
Based on NMR experiments of SM07, assuming similar scaffolds will keep the same protonation order, I prepared a table of experimental microstate pairs:

experimental_microstates.csv

Copied `typeI_submission_collection.csv` from `/sampl6-physicochemical-properties/analysis_of_pKa_predictions/analysis_of_typeI_predictions/analysis_outputs_closest`

$ source activate sampl6_pKa_oe  

run analyze_microstate_pairs.ipynb  


## 2019/03/24

### Develop matching by microstate ID algorithm

In a Juptter notebook I will develop `microstate_matching` and `add_pKa_IDs_to_matching_predictions_microstate_based_matching` algorithms for matching experimental and predicted typeI  microscopic pKas. This analysis can only be used for 4-aminoquinazoline series.

$ source activate sampl6_pKa
