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
 
Additionally we would like molecules to have cover logP space evenly, but I 
will make that selection last.


 
