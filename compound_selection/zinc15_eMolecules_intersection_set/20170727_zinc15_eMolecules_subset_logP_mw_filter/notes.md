## 2017/07/27

After filtering for required pKa properties, I ended up with 180 molecules. 
Criteria for candidate molecules is having a logP in the following interval:
-1 <= predicted logP <= 6

$ source activate py35
$ python logP_filter.py

Input files:
df_pKa_interval_3-11_spread.csv

Output files:
df_XlogP_interval.csv 
 
Run `logP_and_mw_filter.ipynb` for fragment and drug-like compound selection. All necessary
criteria are implemented in this notebook.

Additionally we would like molecules to have cover logP space evenly, but I 
will make that selection last.


## 2017/08/25

One of the compounds was not available in 2 weeks timeframe, so I will pick another
compound instead of this compound:

SMILES = O=C(Nc1ccccc1)c1n[nH]c2ccccc12
N-phenyl-1H-indazole-3-carboxamide

## 2017/08/31

`logP_and_mw_filter.ipynb` is replaced with following 3 notebooks that separate selection of
fragment-like and drug-like compounds. 

Run the notebooks in following order:
1. Run `XlogP_and_mw_filter.ipynb`              
2. Run `fragment-like-compound-selection.ipynb`
3. Run `drug-like-compound-selection.ipynb`     
 
