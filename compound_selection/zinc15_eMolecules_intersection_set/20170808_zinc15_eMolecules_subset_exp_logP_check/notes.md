# 2017/08/08

### Eliminating compounds with reported experimental logP values

I checked the following sources to make sure measured logP values of these compounds are not reported:
1. DrugBank
2. Chemspider
3. Pubchem
4. NCI CACTUS database

#### 1. DrugBank
I manually queried DrugBank using eMolecules SMILES strings of 25 compounds in fragment-like set. 
My search criteria was looking up compounds with similarity criteria of minimum 0.8. If records 
of compounds that matched this criteria showed up, I inspected them to make sure they don't have 
exactly the same structure as my query compound.

Only 1 compound matched a record exactly in DrugBank: geninstein(eMolecules ID: 532754). Its logP 
values wasn't recorded in DrugBank but I was able to find it by searching the internet with geninstein
name.

#### 2. ChemSpider

$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_frag_final.csv .
$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_drug_final.csv .
$ cp df_frag_final.csv df_frag_final_chemspider_logP.csv

- I created a Chemspider column in `df_frag_final_chemspider_logP.csv` to save found logPs or record 'None'
if no experimental logP was found in Chemspider. I manually queried by Chemspider website searching by canonical
isomeric SMILES. Experimental logP values (if exists), were under `Properties/Experimental Physico-chemical 
Properties/Experimental LogP`. I recorded these values under Chemspider columb in `df_frag_final_chemspider_logP.csv`.

- Then to create a list of compounds to skip, I run frag_set_reported_experimental_logP.ipnb. But it is necessary to
increment the pickle file name round#:
fragments_with_exp_logP_round1.pickle
fragments_with_exp_logP_round2.pickle
fragments_with_exp_logP_round3.pickle
fragments_with_exp_logP_round4.pickle

- Add the path to new pickle file to ../20170727_zinc15_eMolecules_subset_logP_mw_filter/logP_and_mw_filter.ipynb  

- I run 4 rounds of this until I get a molecule free of experimental logPs.

