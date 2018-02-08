#!/usr/bin/env python

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
import seaborn as sns
import collections

# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
PKA_TYPEIII_SUBMISSIONS_DIR_PATH = '../../predictions/typeIII_predictions'
EXPERIMENTAL_DATA_FILE_PATH = '../../experimental_data/pKa_experimental_values.csv'

# =============================================================================
# STATS FUNCTIONS
# =============================================================================

def r2(data):
    x, y = data.T
    slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(x, y)
    return r_value**2


def slope(data):
    x, y = data.T
    slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(x, y)
    return slope


def me(data):
    x, y = data.T
    error = np.array(x) - np.array(y)
    return error.mean()


def mae(data):
    x, y = data.T
    error = np.abs(np.array(x) - np.array(y))
    return error.mean()


def rmse(data):
    x, y = data.T
    error = np.array(x) - np.array(y)
    rmse = np.sqrt((error**2).mean())
    return rmse


def compute_bootstrap_statistics(samples, stats_funcs, percentile=0.95, n_bootstrap_samples=10000):
    """Compute bootstrap confidence interval for the given statistics functions."""
    # Handle case where only a single function is passed.
    try:
        len(stats_funcs)
    except TypeError:
        stats_funcs = [stats_funcs]

    # Compute mean statistics.
    statistics = [stats_func(samples) for stats_func in stats_funcs]

    # Generate bootstrap statistics.
    bootstrap_samples_statistics = np.zeros((len(statistics), n_bootstrap_samples))
    for bootstrap_sample_idx in range(n_bootstrap_samples):
        samples_indices = np.random.randint(low=0, high=len(samples), size=len(samples))
        for stats_func_idx, stats_func in enumerate(stats_funcs):
            bootstrap_samples_statistics[stats_func_idx][bootstrap_sample_idx] = stats_func(samples[samples_indices])

    # Compute confidence intervals.
    percentile_index = int(np.floor(n_bootstrap_samples * (1 - percentile) / 2)) - 1
    bootstrap_statistics = []
    for stats_func_idx, samples_statistics in enumerate(bootstrap_samples_statistics):
        samples_statistics.sort()
        stat_lower_percentile = samples_statistics[percentile_index]
        stat_higher_percentile = samples_statistics[-percentile_index+1]
        confidence_interval = (stat_lower_percentile, stat_higher_percentile)
        bootstrap_statistics.append([statistics[stats_func_idx], confidence_interval, samples_statistics])

    return bootstrap_statistics

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

# =============================================================================
# UTILITY CLASSES
# =============================================================================

# =============================================================================
# PKA PREDICTION CHALLENGE
# =============================================================================

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def reorganize_experimental_pKa_dataframe(dataframe):
    """Reorganize experimental data dataframe so that each row represents one pKa.
    Each row is also assigned a unique pKa ID in the form of SM##_pKa#

    Args:
        Pandas DataFrame of experimnental pKas.

    Returns:
        Pandas DataFrame
    """

    # reorganize experimental data: I want each row to represent one pKa.
    data = []

    for i, row in enumerate(dataframe.iterrows()):
        pKa1_mean = np.NaN
        pKa2_mean = np.NaN
        pKa3_mean = np.NaN

        mol_id = row[1]["Molecule ID"]
        pKa1_mean = row[1]["pKa1 mean"]
        pKa1_SEM = row[1]["pKa1 SEM"]
        pKa2_mean = row[1]["pKa2 mean"]
        pKa2_SEM = row[1]["pKa2 SEM"]
        pKa3_mean = row[1]["pKa3 mean"]
        pKa3_SEM = row[1]["pKa3 SEM"]
        assay_type = row[1]["Assay Type"]
        exp_mol_id = row[1]["Experimental Molecule ID"]
        can_iso_smiles = row[1]["canonical isomeric SMILES"]

        # all molecules have at least 1 pKa
        # Append pKa1
        data.append({
            "Molecule ID": mol_id,
            "pKa mean": pKa1_mean,
            "pKa SEM": pKa1_SEM,
            "Assay Type": assay_type,
            "Experimental Molecule ID": exp_mol_id,
            "canonical isomeric SMILES": can_iso_smiles,
            "pKa ID": mol_id + "_pKa1"
        })

        # if exists, append pKa2
        if np.isnan(pKa2_mean):
            continue
        else:
            data.append({
                "Molecule ID": mol_id,
                "pKa mean": pKa2_mean,
                "pKa SEM": pKa2_SEM,
                "Assay Type": assay_type,
                "Experimental Molecule ID": exp_mol_id,
                "canonical isomeric SMILES": can_iso_smiles,
                "pKa ID": mol_id + "_pKa2"
            })

        # if exists, append pKa3
        if np.isnan(pKa3_mean):
            continue
        else:
            data.append({
                "Molecule ID": mol_id,
                "pKa mean": pKa3_mean,
                "pKa SEM": pKa3_SEM,
                "Assay Type": assay_type,
                "Experimental Molecule ID": exp_mol_id,
                "canonical isomeric SMILES": can_iso_smiles,
                "pKa ID": mol_id + "_pKa3"
            })

    # Transform into Pandas DataFrame.
    df_exp_stacked = pd.DataFrame(data=data)
    df_exp_stacked.to_csv("../../experimental_data/pKa_experimental_values_stacked.csv", index=False)

    return df_exp_stacked


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    sns.set_style('whitegrid')
    sns.set_context('paper')

    # Read experimental data.
    with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
        # experimental_data = pd.read_json(f, orient='index')
        names = ('Molecule ID', 'pKa1 mean', 'pKa1 SEM', 'pKa2 mean', 'pKa2 SEM', 'pKa3 mean', 'pKa3 SEM',
                 'Assay Type', 'Experimental Molecule ID', 'canonical isomeric SMILES')
        experimental_data = pd.read_csv(f, names=names, skiprows=1)

    # Convert numeric values to dtype float.
    for col in experimental_data.columns[1:7]:
        experimental_data[col] = pd.to_numeric(experimental_data[col], errors='coerce')

    # Reorganize the experimental pKas into stacked form
    experimental_data = reorganize_experimental_pKa_dataframe(experimental_data)
    experimental_data.set_index("pKa ID")

    # Import user map.
    with open('../../Submissions/SAMPL6_user_map.csv', 'r') as f:
        user_map = pd.read_csv(f)


    # Configuration: statistics to compute.
    stats_funcs = collections.OrderedDict([
        ('RMSE', rmse),
        ('MAE', mae),
        ('ME', me),
        ('R2', r2),
        ('m', slope),
    ])
    ordering_functions = {
        'ME': lambda x: abs(x),
        'R2': lambda x: -x,
        'm': lambda x: abs(1 - x),
    }
    latex_header_conversions = {
        'R2': 'R$^2$',
        'RMSE': 'RMSE',
        'MAE': 'MAE',
        'ME': 'ME',
    }

    # Load submissions data.


    # Match predicted pKas to experimental pKa IDs









