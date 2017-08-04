## 2016/06/27

http://zinc15.docking.org/subclasses/kinase/substances/subsets/now+anodyne/
number of molecules: 10883

Downloaded as: kinase-now+anodyne.csv

Filters used:
- anodyne: subtances matching no reactivity filters including PAINs
- now: immediate delivery, includes in-stock and agent 

This set doesn't have any "Bioactive and Drugs" filters, such as:
- Fda: FDA approved drugs, per Drugbank
- In Cells: Substances reported or infered active in cells
- In Man: Substances that have been in man
- In Trial: Compunds that have been investigated, including drugs
- In Vitro: Substance reported or infered active at 10 uM or better in direct binding assays 
- In Vivo: Substances tested in animals including man
- World: Approved drugs in major juridications, including FDA, i.e. Drugbank approved
 
## 2017/06/28 

I will convert Zinc records to Isomeric Canonical SMILES with OpenEye. 

"OEMolToSmiles for the best, most consistent treatment. Also, note that if you are STARTING 
with a SMILES in either dataset, then you want to go SMILES -> OEMol -> SMILES, if that's not 
obvious." - David Mobley

I also downloaded free version of eMolecules library in .smi format:
eMolecules_version_2017-06-01.smi 

Original eMolecules SMILES wasn't canonical isomeric SMILES. For comparison to ZINC Kinase subset, 
I converted eMolecules SMILES to canonical isomeric smiles with convert_eMolecules_database_to_canonical_smiles.py
script: 

$ python convert_eMolecules_database_to_canonical_smiles.py 

INPUT: eMolecules_version_2017-06-01.smi
OUTPUT: eMolecules_version_2017-06-01_CanIsoSMILES.smi  

These files are not included in repository because they are too large.  
