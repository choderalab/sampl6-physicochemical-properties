## 2018/10/01
### Linear Free Energy vs pH plots for microstates

- This analysis uses "titrato" package.
- $ source activate py36
- $ conda install typing_extensions
- `charges_per_state.csv` file is from https://github.com/choderalab/SAMPL6-Reference-pKa-Calculations/blob/reporting-updates/charges_per_state.csv

Run typeII_analysis_linear_free_energy_plots_trial.ipynb


## 2018/10/03

### Test submission - nb008-976-typeII-epik_microscopic_populations-1.csv

#### Cleaning Epik submission from Excel output defects
In VI:
vi ../typeII_predictions/nb008-976-typeII-epik_microscopic_populations-1.csv
:%s/"#/#/g
:%s/,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,/ /g

The predictions section (CSV table) is supposed to have 102 columns including the Microstate ID column. For some reason `nb008-976-typeII-epik_microscopic_populations-1.csv` submission has 92 columns instead. Therefore I couldn't parse this file. Bas prepare new submission files for Epik.

### Test all submissions for parsing Predictions section

Submissions with problems:
- aeoys-976-typeII-RobertFraczkiewicz-1.csv 
	- utf-8 error
	- To correct replace Göller with Goller

- eqvdq-976-typeII-wilcken-1.csv - problem with section names and perhaps excel errors
	- :%s/"#/#/g
	- remove <92>,<93>,<94> to get rid of UTF-8 errors
        - replace Å with A
	- replace Schrödinger with Schrodinger

- g3r25-976-typeII-wilcken-2.csv - problem with section names and perhaps excel and UTF-8 errors
        - :%s/"#/#/g
        - remove <92>,<93>,<94> to get rid of UTF-8 errors
        - replace Å with A
        - replace Schrödinger with Schrodinger


### Test parsing and plotting - 74mf6-976-typeII-Iorga-1.csv 

I learned that for reports I needed the the Images/Molecules/ directory from https://github.com/choderalab/SAMPL6-Reference-pKa-Calculations/tree/reporting-updates as an input.

$ cd /Users/isikm/lab/SAMPL6-repos/SAMPL6-Reference-pKa-Calculations/Images
$ mv Molecules.tar /Users/isikm/lab/SAMPL6-repos/sampl6-physicochemical-properties/analysis_of_pKa_predictions/analysis_of_typeII_predictions/linear_free_energy_vs_pH_plots/Images

## 2018/10/04 

After running typeII_analysis_linear_free_energy_plots_trial.ipynb an output directory called "Reports" is generated with plots and tex file for compiling a report.
Before compiling
1. copy the tex file outside of the Reports directory
2. replace the 'standalone' word in the first line of the texfile with 'article': \documentclass[9pt]{article}
3. Compile with texmaker.
 
For this analyzis I used py36 environment with titrato (commit 3539bee) installed: https://github.com/choderalab/titrato/commit/3539bee239b4856b7c7c8e0593b3c727f177929c
