## 2019/03/15

### Convert PDF Table 1 to Excel 

With Adobe Acrobat I converted Table 1 of "pH-Metric log P. 4. Comparison of Partition Coefficients Determined by
HPLC and Potentiometric Methods to Literature Values" Journal of Pharmaceutical Science Vol. 83, No. 9, September 1994
paper to Excel spreadsheet.

Manual editing was necessary to correct superscripts, scrambled numbers and table shape.

Filename: extra_molecules_with_pHmetric_logP.xlsx


## 2019/03/18

### Convert to CSV

Converted to csv, replaced non-UTF ± with +-.
Removed lines that reported anion and cation logPs.

Filename: extra_molecules_with_pHmetric_logP_only_neutral.csv


### Convert to SMILES

I will use `nam2mol_example.py` script from OpenEye to convert chemical names to SMILES.
Created  a file with just name column as input.
I had to do some manual corrections to names. I found alternative names for compounds using Pubchem.

1. replace "(+-)-Propranolol" (racemic) with "Propranolol"
2. replace "Phenobarbitone" with "Phenobarbital"
3. replace "4-lodophenol" with "4-Iodophenol"
4. replace "Butobarbitone" with "5-butyl-5-ethyl-1,3-diazinane-2,4,6-trione"
5. replace "Amylobarbitone" with "Amobarbital"
6. replace "Pentobarbitone" with "Pentobarbital"
7. replace "Quinalbarbitone" with "Secobarbital"
File name: extra_molecule_names.csv

$ source activate py36
$ python nam2mol_example.py -in extra_molecule_names.csv -out extra_molecule_names_and_SMILES.csv -language english


### Convert to canonical SMILES and combine with logP data

Run convert_SMILES_to_can_SMILES.ipynb

Output file: extra_molecules_with_pHmetric_logP_only_neutral_with_canonical_SMILES.csv


### Create XLSX file with molecular depictions

$ cp extra_molecules_with_pHmetric_logP_only_neutral_with_canonical_SMILES.csv extra_molecules_csvxlsx_input.csv

Manually rearrange columns for csv2xlsx.py script:
Canonical SMILES, Canonical SMILES, Compound ..., Canonical SMILES

$ python csv2xlsx.py  extra_molecules_csvxlsx_input.csv extra_molecules_with_pHmetric_logP_only_neutral_with_canonical_SMILES_and_2Ddepiction.xlsx

