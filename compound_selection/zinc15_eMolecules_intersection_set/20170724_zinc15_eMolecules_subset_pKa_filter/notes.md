## 2017/07/23

isosmiles-list-search-tier1-100mg.csv file is the starting point. It has been generated in 20170711_zinc15_eMolecules_subset_list_search/ directory by searching eMolecules and ZINC15 kinase subset intersection list in eMolecules website and picking Tier1 molecules, available at 100 mg scale.

Necessary chemical properties for both group:
1 <= titratable sites
3 <= predicted pKa <= 11
1 <= number of rings
-1 <= predicted logP <= 6
-3 <= logS (prefered if possible)

Necessary properties for fragment set:
150 <= mw <= 350
rotatable bonds <= 3

Necessary properties for drug-like set:
350 <= mw
number of titratable groups <= 4


### Filtering based on number of titratble sites and pKa range

To predict ionizable sites and pKas I will use Schrodinger's Epik tool, via [OpenMolTools](https://github.com/choderalab/openmoltools) Schrodinger and OpenEye modules.

$ source activate py35
OpenMolTools dependencies were installed through conda:
$ conda install openmoltools
openmoltools==0.8.2.dev0 installed from GitHub repo.

$ python pKa_filter.py

Started with 292 molecules.
7 molecules failed at mol2 file generation.

