## 2017/08/08

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
