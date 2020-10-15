## 2020/08/05

### Microstate pair matching analysis between Type I predictions with Hungarian match and experimental data (NMR) 

Using the Hungarian algorithm, predicted pKa values were matched to experimental pKa values. 
For type I predictions participants have also reported Microstate ID pairs of each of their predicted pKa values.
Based on NMR experiments of SM07, assuming similar scaffolds will keep the same protonation order, I prepared a table of experimental microstate pairs:

experimental_microstates.csv

Copied `typeI_submission_collection.csv` from `/sampl6-physicochemical-properties/analysis_of_pKa_predictions/analysis_of_typeI_predictions_8mol/analysis_outputs_hungarian`

$ source activate sampl6_pKa  

run analyze_microstate_pairs.ipynb  

