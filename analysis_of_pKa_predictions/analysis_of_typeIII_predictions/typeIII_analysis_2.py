#!/usr/bin/env python

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
import os
import numpy as np
import pandas as pd
from typeIII_analysis import mae
from typeIII_analysis import compute_bootstrap_statistics


# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
PKA_TYPEIII_CLOSEST_COLLECTION_PATH = './analysis_outputs_closest/typeIII_submission_collection.csv'
PKA_TYPEIII_HUNGARIAN_COLLECTION_PATH = './analysis_outputs_hungarian/typeIII_submission_collection.csv'

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def read_collection_file(matching_algorithm):
    """
    Function to read SAMPL6 collection CSV file that was created by pKaTypeIIISubmissionCollection.
    :param matching_algorithm: 'closest' or 'hungarian'
    :return: Pandas DataFrame
    """
    # Select collection file path
    if algorithm == 'closest':
        collection_file_path = PKA_TYPEIII_CLOSEST_COLLECTION_PATH
    elif algorithm == 'hungarian':
        collection_file_path = PKA_TYPEIII_HUNGARIAN_COLLECTION_PATH
    else:
        raise Exception("Correct matching algorithm not specified. Should be 'closest' or 'hungarian', or both.")

    # Check if submission collection file already exists.
    if os.path.isfile(collection_file_path):
        print("Analysis will be done using the existing collection file: {}".format(collection_file_path))

        collection_df = pd.read_csv(collection_file_path, index_col=0)
        print("\n SubmissionCollection: \n")
        print(collection_df)
    else:
        raise Exception("Collection file doesn't exist: {}".format(collection_file_path))

    return collection_df


def calc_MAE_for_molecules_across_all_predictions(collection_df):
    """

    :param collection_df:
    :return:
    """
    # Create list of Molecule IDs
    mol_IDs= list(set(collection_df["Molecule ID"].values)) # List of unique IDs
    mol_IDs.sort()
    print(mol_IDs)

    # Slice the dataframe for each molecule to calculate MAE
    for mol_ID in mol_IDs:
        collection_df_mol_slice = collection_df.loc[collection_df["Molecule ID"] == mol_ID]
        print("Molecule ID: {}\n".format(mol_ID))
        #print(collection_df_mol_slice.head(), "\n")

        # 2D array of matched calculated and experimental pKas
        data = collection_df_mol_slice[["pKa (calc)", "pKa (exp)"]].values

        # Calculate mean absolute error
        #MAE_value = mae(data)

        # Calculate MAE and 95% confidence intervals
        MAE_bootstrap_statistics = compute_bootstrap_statistics(samples=data, stats_funcs=[mae], percentile=0.95, n_bootstrap_samples=1000)
        MAE = MAE_bootstrap_statistics[0][0]
        MAE_lower_CI = MAE_bootstrap_statistics[0][1][0]
        MAE_upper_CI = MAE_bootstrap_statistics[0][1][0]
        print("MAE: {} [{}, {}]\n".format(MAE, MAE_lower_CI, MAE_upper_CI))





# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    # Perform the analysis using the different algorithms for matching predictions to experiment
    #for algorithm in ['closest', 'hungarian']:
    for algorithm in ['closest']:

        # Read collection file
        collection_data = read_collection_file(matching_algorithm=algorithm)

        # Calculate MAE of each molecule across all predictions methods
        calc_MAE_for_molecules_across_all_predictions(collection_df = collection_data)




