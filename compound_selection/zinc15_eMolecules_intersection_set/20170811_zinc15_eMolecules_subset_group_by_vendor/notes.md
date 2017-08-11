## 2017/08/11

### Organizing Selected Compounds in Fragment-like Set by Vendor

$ cp ../20170711_zinc15_eMolecules_subset_list_search/Quote-Cart_searched_with_isoSMILES_tier1_100mg.csv .
$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_frag_final.csv .

Run organize_by_vendor.ipynb.

INPUTS
Quote-Cart_searched_with_isoSMILES_tier1_100mg.csv
df_frag_final.csv

OUTPUTS
df_frag_final_supplier.csv

### Create table with chemical structures

$ python adjust_csv_for_openeye_script.py

INPUT: df_frag_final_supplier.csv
OUTPUT: df_frag_final_supplier_oe.csv

$ python csv2xlsx.py df_frag_final_supplier_oe.csv df_frag_final_supplier_oe.xlsx

INPUT: df_frag_final_supplier_oe.csv
OUTPUT: df_frag_final_supplier_oe.xlsx
