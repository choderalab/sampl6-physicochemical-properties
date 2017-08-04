#!/usr/bin/env python3

# This script takes a csv file for a set molecules with a SMILES column as input. OpenEye 
# functionalities are used to convert SMILES format to .mae format of Schrodinger. Schrodinger 
# Epik is used to generate protomers, tautomers and pKas.

from openmoltools import openeye as omtoe, schrodinger
import pandas as pd
import os
import numpy as np
from ast import literal_eval
from openeye.oechem import *
import pickle


##### IMPORT STARTING SET OF MOLECULES AS SMILES #####

# Import list of available molecules which were exported from eMolecules website.
df = pd.read_csv("./isosmiles-list-search-tier1-100mg.csv")
initial_number_of_molecules = df.shape[0]
print("Starting from isomeric SMILES of {} molecules.".format(initial_number_of_molecules))


# Get SMILES and eMolecules IDs as a dictionary. These are the original SMILES records of eMolecules.

print("Extracting SMILES and eMolecules ID from input file...")

eMolID_smiles_dict = {}

for i in range(initial_number_of_molecules):
# for i in range(5): # for testing
    smiles = df.loc[i,"eMolecules SMILES"]
    emol_id = df.loc[i,"eMolecules ID"]

    eMolID_smiles_dict[emol_id] = smiles

# print(eMolID_smiles_dict)

# Save "eMolecules ID: eMolecules SMILES" dictionary as a pickle file
eMolID_emol_smiles_dict = eMolID_smiles_dict 
pickle.dump(eMolID_emol_smiles_dict, open("eMolID_emol_smiles_dict.pickle", "wb"))

# Convert eMolecules SMILES to canonical isomeric SMILES
# Requires OpenEye OEChem.

for key, eMol_smiles in eMolID_smiles_dict.items():
    mol = OEGraphMol()
    OESmilesToMol(mol, eMol_smiles)
    canonical_isomeric_smiles= OEMolToSmiles(mol)
    eMolID_smiles_dict[key] = canonical_isomeric_smiles

# Save "eMolecules ID: canonical isomeric SMILES" dictionary as pickle file
eMolID_can_iso_smiles_dict = eMolID_smiles_dict
pickle.dump(eMolID_can_iso_smiles_dict, open("eMolID_can_iso_smiles_dict.pickle", "wb"))
     
print("Finished converting eMolecules SMILES to canonical isomeric SMILES.")
print("\n")


##### CONVERT SMILES TO OEMOL #####

print("Converting SMILES to OEMol...")

eMolID_oemol_dict = {} 

for key, value in eMolID_smiles_dict.items():
    # Create a OEMolBuilder from a smiles string.
    oemol_molecule = omtoe.smiles_to_oemol(smiles=value)
    eMolID_oemol_dict[key] = oemol_molecule
    
# print(oMolID_oemol_dict)

print("\n")


##### GENERATE CHARGED CONFORMERS AND SAVE AS MOL2 FILE #####

mol2_directory_path = "./mol2_files"
if not os.path.exists(mol2_directory_path):
    os.makedirs(mol2_directory_path)
    print("{} directory created.".format(mol2_directory_path))

print("Generating charged OEMol molecules...")

# Dictionary to keep track of failed molecules
failed_molecules_dict = {}

# Generate charges for an OpenEye OEMol molecule. It will return  molecule with OpenEye's recommended AM1BCC
# charge selection scheme.

for key, value in eMolID_oemol_dict.items():
    print("Generating conformer for ", key, "...")
    try:
        oe_molecule = omtoe.get_charges(value, keep_confs=1)
    except RuntimeError:
        print("Conformation generation failed for {}.".format(key))
        # Save failed molecule to failed_molecules_dict
        failed_molecules_dict[key] = value
    
    mol2_filename = mol2_directory_path + "/" + str(key) + ".mol2"
    omtoe.molecule_to_mol2(oe_molecule, tripos_mol2_filename=mol2_filename)
    print("Mol2 file {} generated.".format(mol2_filename))

print("")
print("Conformer generation for {} molecules failed.".format(len(failed_molecules_dict)))

# Remove failed molecules from oMolID_oemol_dict dictionary
for key, value in failed_molecules_dict.items():
    eMolID_oemol_dict.pop(key, None)
    
print("{} molecules removed from the list.".format(len(failed_molecules_dict)))

# Save dictionary of successful conformers as spickle file
pickle.dump(eMolID_oemol_dict, open("eMolID_oemol_dict.pickle", "wb"))
# Save dictionary of failed molecules as confromer generation as a pickle file
pickle.dump(failed_molecules_dict, open("failed_molecules_dict.pickle", "wb"))

print("\n")


##### RUN EPIK #####

print("Running Epik with sequencial pKa prediction method...")

mae_directory_path = "./mae_files"
if not os.path.exists(mae_directory_path):
    os.makedirs(mae_directory_path)
    print("{} directory created.".format(mae_directory_path))

# Sequencial pKa calculation method is used starting form pH 7.0.

for key in eMolID_oemol_dict.keys():
    print("Running Epik for molecule {} ...".format(key))
    mol2_file_path = mol2_directory_path + "/" + str(key) + ".mol2"
    mae_file_path = mae_directory_path + "/" + str(key) + ".mae"
    schrodinger.run_epik(mol2_file_path, mae_file_path, max_structures=100, ph=7.0, ph_tolerance=None,
                         tautomerize=True, extract_range=None, max_atoms=150, scan=True)

print("\n")


##### CONVERT EPIK OUTPUT (.MAE FILE) TO SDF #####

sdf_directory_path = "./sdf_files"
if not os.path.exists(sdf_directory_path):
    os.makedirs(sdf_directory_path)
    print("{} directory created.".format(sdf_directory_path))

for key in eMolID_oemol_dict.keys():
    mae_file_path = mae_directory_path + "/" + str(key) + ".mae"
    sdf_file_path = sdf_directory_path + "/" + str(key) + ".sdf"
    # Run Schrodinger's structconvert command line utility to convert mae file to sdf
    print("Converting Epik output to SDF for molecule {} ...".format(key))
    schrodinger.run_structconvert(input_file_path = mae_file_path, output_file_path = sdf_file_path)

print("\n")


##### RUN PROPLISTER TO EXTRACT PKAS #####

# Create a dictionary to store predicted pKas
predicted_pKa_dict = {}

# Iterate over molecules
for key in eMolID_oemol_dict.keys():
    mae_file_path = mae_directory_path + "/" + str(key) + ".mae"
    proplister = schrodinger.run_proplister(input_file_path=mae_file_path)

    # Iterate over properties of each molecule
    # Record predicted pKa values in a list
    pKa_list = []
    for propkey, value in proplister[0].items():
        if propkey.startswith("r_epik_pKa"):
            pKa = float(value)
            pKa_list.append(pKa)

    pKa_list = sorted(pKa_list, key=float)
    predicted_pKa_dict[key] = pKa_list
    
print("Predicted pKa dictionary: eMolecules ID : pKas")
print(predicted_pKa_dict)

print("\n")


##### ANALYZE PKA PREDICTIONS TO COUNT 3 <= PKAS <= 11 #####

# Create a pandas dataframe to store pKa information
df_pKa = pd.DataFrame(list(predicted_pKa_dict.items()), columns=["eMolecules ID", "predicted pKas"])
df_pKa["pKas in [3,11]"]=np.NaN
df_pKa["pKa count in [3,11]"]=np.NaN

for i, row in df_pKa.iterrows():
    
    # Count pKas that are within 3-11 interval
    pKa_in_interval_count = 0
    pKas_in_interval = []
    
    pKas = row["predicted pKas"]
    for pKa in pKas:    
        if (3<= pKa) and (pKa <= 11):
            pKa_in_interval_count = int(pKa_in_interval_count + 1)
            pKas_in_interval.append(pKa)
    
    df_pKa.loc[i,"pKa count in [3,11]"] = pKa_in_interval_count
    #print(pKas_in_interval)
    df_pKa.loc[i,"pKas in [3,11]"] = str(pKas_in_interval)
    

# Flag molecules with pKas that are closer than 1 log unit
df_pKa["pKas closer than 1 unit"]=False

for index, row in df_pKa.iterrows():
    # print(row["pKas in [3,11]"])
    pKas = literal_eval(row["pKas in [3,11]"])
    
    if len(pKas)> 1:
        # The difference between consecutive pKas must be >= 1. If not, we will mark True.
        for i, pKa in enumerate(pKas[0:(len(pKas)-1)]):
            pKa_difference = float(pKas[i+1]) - float(pKas[i])
            
            if pKa_difference < 1:
                df_pKa.loc[index, "pKas closer than 1 unit"]=True
            else:
                continue

# Add Canonical Isomeric SMILES to dataframe
df_pKa["canonical isomeric SMILES"] = np.NAN
for i, row in df_pKa.iterrows():
    key = row["eMolecules ID"]
    smiles = eMolID_can_iso_smiles_dict[key] 
    df_pKa.loc[i,"canonical isomeric SMILES"] = smiles

# Add original eMolecules SMILES to dataframe
eMolID_emol_smiles_dict = pickle.load(open("eMolID_emol_smiles_dict.pickle", "rb"))
df_pKa["eMolecules SMILES"] = np.NAN
for i, row in df_pKa.iterrows():
    key = row["eMolecules ID"]
    smiles = eMolID_emol_smiles_dict[key] 
    df_pKa.loc[i,"eMolecules SMILES"] = smiles
                
df_pKa.to_csv("df_pKa.csv") 
print("df_pKa.csv file generated.")

print("\n")


##### REMOVE COMPOUNDS THAT DON'T HAVE PKAS WITHIN 3-11 INTERVAL #####

df_pKa_interval = df_pKa.loc[df_pKa["pKa count in [3,11]"] >= 1.0].reset_index()

df_pKa_interval.to_csv("df_pKa_interval_3-11.csv")
print("Number of molecules with pKa in 3-11 interval: ", df_pKa_interval.shape[0])
#print(df_pKa_interval)
print("df_pKa_intercal.csv file generated.")

print("\n")


#####  REMOVE COMPOUNDS WITH PKA CLOSER THAN 1 LOG UNIT #####

df_pKa_interval_spread = df_pKa_interval.loc[df_pKa_interval["pKas closer than 1 unit"]==False].reset_index()

df_pKa_interval_spread.to_csv("df_pKa_interval_3-11_spread.csv")
print("Number of molecules with pKa in 3-11 interval and spread*: ", df_pKa_interval_spread.shape[0])
print("* pKa values of each molecule are not closer than 1 log unit.")
#print(df_pKa_interval_spread)
print("df_pKa_interval_spread.csv file generated.")

print("\n")

print("Done.")
