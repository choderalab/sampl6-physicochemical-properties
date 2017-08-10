## 2017/07/31

johnslist.emol.2017_07.sdf file is the list of molecules generated by Paul Czodrowski and Marcel, by searching eMolecules dtatabase for high similarity molecules with the kinase intersection list I provided.


### Preliminary filtering on eMolecules similarity set

Filters out repeating entries, molecules without prices and molecules with lower availability than 100 mg. 
run initial_availability_filter.ipynb

INPUTS:
eMol_similarity_set_2017_07.sdf

OUTPUTS:
df_eMol_sim_price_tier1_100mg.csv # All entries that satify criteria
df_eMol_sim_unique_molecules_smiles.smi # Unique molecular structures that satify criteria 
df_eMol_sim_unique_molecules.csv


### eMolecules similarity set pKa filtering

johnslist.emol.2017_07.sdf file is the list of molecules generated by Paul Czodrowski and Marcel, by searching eMolecules dtatabase for high similarity molecules with the kinase intersection list I provided. 

$ cp johnslist.emol.2017_07.sdf eMol_similarity_set_2017_07.sdf
$ source activate py35
$ python pKa_filter.py

INPUTS:
df_eMol_sim_unique_molecules_smiles.smi 

OUTPUTS:
df_pKa.csv                                   
df_pKa_interval_3-11.csv                     
df_pKa_interval_3-11_spread.csv              
eMolSKU_can_iso_smiles_dict.pickle           
eMolSKU_oemol_dict.pickle                    
failed_molecules_dict.pickle             
eMol_similarity_set_2017_07_CanIsoSMILES.smi 

