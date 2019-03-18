## 2019/02/28 

### Checking correlation between molecular MAE and molecular descriptors

Copied `molecular_error_statistics.csv` file from  
`sampl6-physicochemical-properties/analysis_of_pKa_predictions/analysis_of_typeIII_predictions/analysis_outputs_closest/MolecularStatisticsTables` directory  
to here. 
MAE calculated in this file was based on closest matching algorithm.

1) Create new Python 3.6 environment where Jupyter notebook and OpenEye can work together
$ conda create -n sampl6_pKa_oe python=3.6
$ source activate sampl6_pKa_oe
$ conda install ipython
$ conda install jupyter
$ pip install -i https://pypi.anaconda.org/OpenEye/simple OpenEye-toolkits
$ conda install numpy
$ conda install pandas
$ conda install matplotlib
$ conda install seaborn

2) Run Jupyter notebook
check_correlation_with_descriptors.ipynb

Required input files:
- molecule_ID_and_SMILES.csv
- microstates/SMXX_microstates.csv files (copied from: /Users/isikm/lab/SAMPL6-repos/SAMPL6/physical_properties/pKa)


## 2019/03/01

Outputs:
SAMPL6_molecular_descriptors.csv
