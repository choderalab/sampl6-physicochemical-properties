## 2017//07/11

# Checking availability of intersection molecules
 
Checking how much of ZINC15 Kinase - eMolecules intersection (1205) molecules can be found in eMolecules,
by using list search of eMolecules website.

## 1. Searching by Canonical Isomeric SMILES
I uploaded zinc15-kinase-now-anodyne-found-in-eMolecules.smi to eMolecules website for this search. 
It contained canonical isomeric smiles of intersection molecyle set. I had 1085 items in resultes page. 
Most compounds were labeled "compound not available". This is exported as:

Quote-Cart_searched_with_canIsoSMILES.csv


## 2. Searching by Isomeric SMILES (orijinal eMolecules SMILES)
I searched eMolecules with zinc15-kinase-now-anodyne-found-in-eMolecules-isosmiles.smi list. It has original
SMILES strings of eMolecules for intersection molecules. It returned a list of 1108 compounds. Most compounds 
were labeled "compound not available".

Quote-Cart_searched_with_isoSMILES.csv 

Hyperlink for this search:
https://ordersc.emolecules.com/cgi-bin/rene/visitor.cgi?h=a6e969652896dd91c97a2586a56fde1983afe460082e301b

To narrow down by suppliers I picked all Tier 1 (2 week) suppliers except Chembridge (dried film) and MolMall Sarl (only had 3 compounds).
Exported as:
Quote-Cart_searched_with_isoSMILES_tier1_100mg.csv

I also manually copied tables with prices to a spreadsheat as this was not available in exported tables:
isosmiles-list-search-tier1-100mg.xlsx

## 2017/07/24
I will create a csv table from isosmiles-list-search-tier1-100mg.xlsx, removing compound structures. Most of the compounds are 
less than 200$/100 mg range. I should prioritize those compounds after filtering by necessary chemical property.
isosmiles-list-search-tier1-100mg.csv

Necessary chemical properties for both group:
1 <= titratable sites
3 <= predicted pKa <= 11
1 <= number of rings
3 <= predicted pKa <= 11
-1 <= predicted logP <= 6
-3 <= logS (prefered if possible)

Necessary properties for fragment set:
150 <= mw <= 350
rotatable bonds <= 3

Necessary properties for drug-like set:
350 <= mw 
number of titratable groups <= 4



