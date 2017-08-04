## 2017/08/04

### Which aromatic ring scaffolds are seen in FDA approved kinase inhibitors?

#### Step 1. FDA-approved kinase inhibitors list
http://www.brimr.org/PKI/PKIs.htm
From the Blue Ridge Institute for Medical Research in Horse Shoe, North Carolina USA
FDA-approved protein kinase inhibitors compiled by Robert Roskoski Jr.

FDA_approved_PKIs.xls

Using the names of the inhibotors form this list, I constructed CSV file with names and SMILES,
by searching in DrugBank Version 5.0.

USFDA_approved_PKIs_SMILES.csv

#### Step 2. BemisBurcko fragmentation and looking at frequent rings

I will used OpenEye's OEMedChem OEGetBemisMurcko function:
fragments a molecule into ring, linker, framework and functional group components as in [Bemis-1996] .

kinase_inhibitor_fragmentation_for_rings.ipynb

INPUT: USFDA_approved_PKIs_SMILES.csv  

OUTPUTS:
all_rings.png
frequent_rings.png

Upon inspection of ring fragments, I decided to include the following in SAMPL6 fragment set:
pyridine
piperazine
quinazoline
quinoline
pyrimidine
indazole
pyrazole
imidazole

Structures of these are summarized in frequent_ring_fragments_in_PKIs.png


