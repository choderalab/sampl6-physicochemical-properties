## 2017/08/07

To depict 2D molecular structures in a table format I used csv2xlsx.py script from OpenEye. For it to work first column must contain SMILES strings and the dataframe must be saved without index. To adjust my dataframe accordingly I created adjust_csv_for_openeye_script.py.
$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_drug_final.csv ./
$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_frag_final.csv ./
$ source activate py35
$ python adjust_csv_for_openeye_script.py

INPUT: df_frag_final.csv
OUTPUT: df_frag_final_oe.csv 

$ python csv2xlsx.py df_frag_final_oe.csv df_frag_final_oe.xlsx

INPUT: df_frag_final_oe.csv
OUTPUT: df_frag_final_oe.xlsx
