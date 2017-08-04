# Converting eMolecules database to canonical isomeric SMILES
# Free version of eMolecules database of 2017-06-01 was downloaded as eMoleucules_version_2017-06-01.smi.
#
# Usage: python convert_eMolecules_database_to_canonical_smiles.py
#

from openeye.oechem import *

ifs = oemolistream()
ofs = oemolostream()

ifs.SetFormat(OEFormat_SMI)
ofs.SetFormat(OEFormat_SMI) # Canonical Isomeric Smiles

input_file_name = "eMolecules_version_2017-06-01.smi"
output_file_name = input_file_name.split(".")[0] + "_CanIsoSMILES.smi"
print("Output file: ", output_file_name)

i=0 # To count molecules

if ifs.open(input_file_name):
    if ofs.open(output_file_name):
        for mol in ifs.GetOEGraphMols():
            OEWriteMolecule(ofs, mol)
            print("Molecule ",i)
            i=i+1
    else:
        OEThrow.Fatal("Unable to create output file.")
else:
    OEThrow.Fatal("Unable to open input file.")

print("Done.")
