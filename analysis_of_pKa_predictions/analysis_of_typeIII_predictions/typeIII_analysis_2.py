#!/usr/bin/env python

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
import os
import numpy as np
import pandas as pd
from typeIII_analysis import mae, rmse, barplot_with_CI_errorbars
from typeIII_analysis import compute_bootstrap_statistics
import shutil
import seaborn as sns
from matplotlib import pyplot as plt


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


def calc_MAE_for_molecules_across_all_predictions(collection_df, directory_path, file_base_name):
    """

    :param collection_df:
    :return:
    """
    # Create list of Molecule IDs
    mol_IDs= list(set(collection_df["Molecule ID"].values)) # List of unique IDs
    mol_IDs.sort()
    print(mol_IDs)

    # List for keeping records of stats values for each molecule
    molecular_statistics = []

    # Slice the dataframe for each molecule to calculate MAE
    for mol_ID in mol_IDs:
        collection_df_mol_slice = collection_df.loc[collection_df["Molecule ID"] == mol_ID]

        # 2D array of matched calculated and experimental pKas
        data = collection_df_mol_slice[["pKa (calc)", "pKa (exp)"]].values

        # Calculate mean absolute error
        #MAE_value = mae(data)

        # Calculate MAE and RMSE and their 95% confidence intervals
        bootstrap_statistics = compute_bootstrap_statistics(samples=data, stats_funcs=[mae, rmse], percentile=0.95,
                                                                n_bootstrap_samples=10000)
        MAE = bootstrap_statistics[0][0]
        MAE_lower_CI = bootstrap_statistics[0][1][0]
        MAE_upper_CI = bootstrap_statistics[0][1][1]
        print("{} MAE: {} [{}, {}]".format(mol_ID, MAE, MAE_lower_CI, MAE_upper_CI))

        RMSE = bootstrap_statistics[1][0]
        RMSE_lower_CI = bootstrap_statistics[1][1][0]
        RMSE_upper_CI = bootstrap_statistics[1][1][1]
        print("{} RMSE: {} [{}, {}]\n".format(mol_ID, RMSE, RMSE_lower_CI, RMSE_upper_CI))

        # Record in CSV file
        molecular_statistics.append({'Molecule ID': mol_ID, 'MAE': MAE, 'MAE_lower_CI': MAE_lower_CI,
                                    'MAE_upper_CI': MAE_upper_CI, 'RMSE': RMSE, 'RMSE_lower_CI': RMSE_lower_CI,
                                     'RMSE_upper_CI': RMSE_upper_CI})



    # Convert dictionary to Dataframe to create tables/plots easily and save as CSV.
    molecular_statistics_df = pd.DataFrame(molecular_statistics)
    #molecular_statistics_df.set_index('Molecule ID', inplace=True)
    # Sort values by MAE values
    molecular_statistics_df.sort_values(by='MAE', inplace=True)
    # Create CSV
    os.makedirs(directory_path)
    file_base_path = os.path.join(directory_path, file_base_name)
    with open(file_base_path + '.csv', 'w') as f:
        molecular_statistics_df.to_csv(f)

    # Plot MAE and RMSE of each molecule across predictions as a bar plot
    barplot_with_CI_errorbars(df = molecular_statistics_df, x_label = 'Molecule ID',
                              y_label = 'MAE', y_lower_label = 'MAE_lower_CI', y_upper_label = 'MAE_upper_CI')
    plt.savefig(directory_path + "/MAE_vs_molecule_plot.pdf")

    barplot_with_CI_errorbars(df=molecular_statistics_df, x_label = 'Molecule ID',
                              y_label = 'RMSE', y_lower_label = 'RMSE_lower_CI', y_upper_label = 'RMSE_upper_CI')
    plt.savefig(directory_path + "/RMSE_vs_molecule_plot.pdf")







# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':


    # Perform the analysis using the different algorithms for matching predictions to experiment
    for algorithm in ['closest', 'hungarian']:
    #for algorithm in ['closest']:

        # Read collection file
        collection_data = read_collection_file(matching_algorithm=algorithm)

        # New directory to store molecular statistics
        output_directory_path = './analysis_outputs_{}'.format(algorithm)
        analysis_directory_name = 'MolecularStatisticsTables'

        if os.path.isdir('{}/{}'.format(output_directory_path, analysis_directory_name)):
            shutil.rmtree('{}/{}'.format(output_directory_path, analysis_directory_name))

        # Calculate MAE of each molecule across all predictions methods
        molecular_statistics_directory_path = os.path.join(output_directory_path, "MolecularStatisticsTables")
        calc_MAE_for_molecules_across_all_predictions(collection_df = collection_data,
                                                      directory_path = molecular_statistics_directory_path,
                                                      file_base_name = "molecular_error_statistics")




