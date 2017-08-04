##### IMPORT STARTING SET OF MOLECULES AS SMILES #####

# Convert molecules in SDF file to canonical isomeric smiles
ifs = oemolistream()
ofs = oemolostream()

ifs.SetFormat(OEFormat_SDF) # MDL SD File
ofs.SetFormat(OEFormat_SMI) # Canonical Isomeric Smiles

input_file_name = "eMol_similarity_set_2017_07.sdf"
output_file_name = input_file_name.split(".")[0] + "_CanIsoSMILES.smi"
print("Output file: ", output_file_name)

i=0 # To count molecules

if ifs.open(input_file_name):
    if ofs.open(output_file_name):
        for mol in ifs.GetOEGraphMols():
            OEWriteMolecule(ofs, mol)
            # print("Molecule ",i)
            i=i+1
    else:
        OEThrow.Fatal("Unable to create output file.")
else:
    OEThrow.Fatal("Unable to open input file.")

print("Done creating canonical isomeric SMILES for molecules in SDF file.")
