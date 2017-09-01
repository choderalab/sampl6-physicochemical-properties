# 2017/08/08

### Eliminating compounds with reported experimental logP values

I checked the following sources to make sure measured logP values of these compounds are not reported:
1. DrugBank
2. Chemspider
3. Pubchem
4. NCI CACTUS database

#### 1. DrugBank
##### 1.1. Fragment-like group
I manually queried DrugBank using eMolecules SMILES strings of 25 compounds in fragment-like set. 
My search criteria was looking up compounds with similarity criteria of minimum 0.8. If records 
of compounds that matched this criteria showed up, I inspected them to make sure they don't have 
exactly the same structure as my query compound.

Only 1 compound matched a record exactly in DrugBank: geninstein(eMolecules ID: 532754). Its logP 
values wasn't recorded in DrugBank but I was able to find it by searching the internet with geninstein
name. I recorded it in `drugbank_reported_experimental_logP.csv ` file.


##### 1.2. Drug-like group
DrugBank was manually queried with canonical isomeric SMILES for 10 compounds in drug-like set. I used
similarity based search with minimum similarity score 0.8.

Only 2 compounds had experimental logP reported: Gefitinib(eMolecules ID: 876432), Celecoxib (eMolecules ID:901601).
I recorded them in `drugbank_reported_experimental_logP.csv ` file. 

I also modified `../20170727_zinc15_eMolecules_subset_logP_mw_filter/drug-like-compound-selection.ipynb` to 
skip these molecules.


#### 2. ChemSpider
##### 2.1. Fragment-like group

$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_frag_final.csv .
$ cp df_frag_final.csv df_frag_final_chemspider_logP.csv

- I created a Chemspider column in `df_frag_final_chemspider_logP.csv` to save found logPs or record 'None'
if no experimental logP was found in Chemspider. I manually queried by Chemspider website searching by canonical
isomeric SMILES. Experimental logP values (if exists), were under `Properties/Experimental Physico-chemical 
Properties/Experimental LogP`. I recorded these values under Chemspider columb in `df_frag_final_chemspider_logP.csv`.

- Then to create a list of compounds to skip,  run `frag_set_chemspider_reported_experimental_logP.ipynb`. But it is necessary to increment the pickle file name round # before each run. Outputs:
fragments_with_exp_logP_round1.pickle
fragments_with_exp_logP_round2.pickle
fragments_with_exp_logP_round3.pickle
fragments_with_exp_logP_round4.pickle

- Add the path to new pickle file to `../20170727_zinc15_eMolecules_subset_logP_mw_filter/fragment-like-compound-selection.ipynb` and rerun that notebook.  

- I run 4 rounds of this until I get a molecule free of experimental logPs.

##### 2.2. Drug-like group
$ cp ../20170727_zinc15_eMolecules_subset_logP_mw_filter/df_drug_final.csv .
$ cp df_drug_final.csv df_drug_final_chemspider_logP.csv

- Chemspider column in `df_drug_final_chemspider_logP.csv` is used to save found logPs or record 'None'
if no experimental logP was found in Chemspider. I manually queried by Chemspider website searching by canonical
isomeric SMILES. Experimental logP values (if exists), were under `Properties/Experimental Physico-chemical
Properties/Experimental LogP`. 

- Then to create a list of compounds to skip,  run `drug_set_chemspider_reported_experimental_logP.ipynb`. But it is necessary to increment the pickle file name round # before each run. Outputs:
drugs_with_exp_logP_round1.pickle

- Add the path to new pickle file to `../20170727_zinc15_eMolecules_subset_logP_mw_filter/drug-like-compound-selection.ipynb` and rerun that notebook.


## 2017/09/11

#### 3. NCI CACTUS Open Database Compounds

##### 3.1 NCI Open Database August 2006
I downloaded NCI Open Database August 2006 release `ncidb_August2006.sdf ` to ./ncidb directory, because this version 
included experimental logP values. This directory is not included in the repository due to size. It can be downloaded 
from https://cactus.nci.nih.gov/download/nci/.

$ cd ncidb
$ python convert.py ncidb_August2006.sdf  ncidb_August2006.csv
This creates ./ncidb/ncidb_August2006.csv file. 

Run frag_set_ncidb_reported_experimental_logP.ipnb.
Only one of the selected compounds of fragment-like set matched a record in NCIDB (eMolecules ID: 719540). But it doesn't have any experimental logP. So I don't have to replace any of these compounds.

##### 3.1 NCI Open Database 2.2

$ cp df_frag_final.csv df_frag_final_ncidb_logP.csv

I queried https://cactus.nci.nih.gov/ncidb2.2/ with canonical isomeric SMILES of fragment-like compounds and recorded the experimental logP results in `ncidb` column of `df_frag_final_ncidb_logP.csv`. There wasn't any matching molecules with experimental logP records.


#### 4. PubChem

$ cp df_frag_final.csv df_frag_final_pubchem_logP.csv

Using Chemical Identifier Resolver of NCI CACTUS (https://cactus.nci.nih.gov/chemical/structure), I converted canonical isomeric SMILES of the compounds in my fragment-like list to InChIKeys. With InChIKeys I queried PubChem(https://pubchem.ncbi.nlm.nih.gov/) to make sure no experimental logP values were reported for these compounds. InChIKeys and logP results were recorded in `InChIKey` and `pubchem` columns of `df_frag_final_pubchem_logP.csv`, respectively. There wasn't any matching molecules with experimental logP records.


