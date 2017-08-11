# This script coverts NCI Open Database from sdf to csv file.

from openeye import oechem, oedepict, oemolprop


input_db_path = "./ncidb/ncidb_August2006.sdf"
output_db_path = "./ncidb/ncidb_August2006.csv"

ifs = oechem.oemolistream()
ofs = oechem.oemolostream()

ifs.SetFormat(oechem.OEFormat_SDF)
ofs.SetFormat(oechem.OEFormat_CSV)

if ifs.open(input_db_path):
    if ofs.open("output_db_path"):
        for mol in ifs.GetOEGraphMols():
            oechem.OEWriteMolecule(ofs, mol)
    else:
        oechem.OEThrow.Fatal("Unable to create output.")
else:
    oechem.OEThrow.Fatal("Unable to open input sdf file.")
    
print("SDF file converted to CSV: ", output_db_path)
print ("Done.")


