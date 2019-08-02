## 2018/01/25

### To calculate mean and SEM of pKa values
$ python calc_pKa_value_statistics.py


## 2018/01/26

### Renaming experimental methods with Molecule ID prefixes
$ mkdir experiment_reports_with_experimental_molecule_ID
$ mkdir experiment_reports_with_molecule_ID
$ cp -rf experiment_reports experiment_reports_with_experimental_molecule_ID 

run rename_experimental_reports_with_molecule_IDs.ipynb

Output directory: experiment_reports_with_molecule_ID/

Copy to main SAMPL6 repo:
$ cp experiment_reports_with_molecule_ID/*.pdf /Users/isikm/lab/SAMPL6-repos/SAMPL6/physical_properties/pKa/experimental_data/experiment_reports

### Organize pKa results of replicate experiments
run organize_pKa_results_of_replicate_experiments.ipynb

$ cp pKa_results_of_replicate_experiments.csv /Users/isikm/lab/SAMPL6-repos/SAMPL6/physical_properties/pKa/experimental_data


### To calculate mean and SEM of pKa values
$ python calc_pKa_value_statistics.py
Output: pKa_experimental_values.csv
$ cp pKa_experimental_values.csv /Users/isikm/lab/SAMPL6-repos/SAMPL6/physical_properties/pKa/experimental_data
$ cp calc_pKa_value_statistics.py /Users/isikm/lab/SAMPL6-repos/SAMPL6/physical_properties/pKa/experimental_data


## 2018/03/25

### Experimental microstate pair table

`experimental_microstates.csv` copied from sampl6-physicochemical-properties/analysis_of_pKa_predictions/20190302_typeI_4aminoquinazoline_series.  
