# Mehtap Isik, Dec. 2017
#
# Based on Bas Rustenburg's check_equality.py script for checking if two structures are the same microstate.
# (2017/12/18)
#
# Rationelle: if MCSS can map all atoms of two structures (target and pattern), it has to be the exact same graph.
# Here the MCSS checks atomic number, but ignores electronic structure (bond order/charges).
# If the entire target, and the entire pattern have the same amount of atoms as the match, it means it found the full
# map between them.


from openeye import oechem

def get_labeled_mol(smiles, label='heavy'):
    """
    returns an OEMol with heavy atoms labeled with a specific indice
    """
    mol = oechem.OEMol()
    if not oechem.OESmilesToMol(mol, smiles):
        print("Couldn't parse smiles (%s) returning None" % smiles)
        return None
    
    for idx, a in enumerate(mol.GetAtomIter(oechem.OEIsHeavy())):
        a.SetData('heavy', idx+1)
    
    return mol

def add_h(mol: oechem.OEMol):
    """Add explicit hydrogens to a molecule"""
    for atom in mol.GetAtoms():
        oechem.OEAddExplicitHydrogens(mol, atom)

def match_subset(pattern: oechem.OEMol, target:oechem.OEMol):
    """Check if target is a subset of pattern."""
    # Atoms are equal if they have same atomic number (so explicit Hydrogens are needed as well for a match)
    atomexpr = oechem.OEExprOpts_AtomicNumber
     # single or double bonds are considered identical (resonance,chirality fix)
    bondexpr = oechem.OEExprOpts_EqSingleDouble
    ss = oechem.OESubSearch(pattern, atomexpr, bondexpr )
    oechem.OEPrepareSearch(target, ss)

    return ss.SingleMatch(target)

def match_microstates(mol1, mol2):
    """If both states are contained in each other, they're the same."""
    return match_subset(mol1, mol2) and match_subset(mol2, mol1)

# Examples that shouldn't match
benzene = "C1=CC=CC=C1"
toluene = "CC1=CC=CC=C1"

SM21_micro001_canIsoSmiles = "c1cc(cc(c1)Br)Nc2[nH]cc(/c(=[NH+]/c3cccc(c3)Br)/n2)F"
SM21_micro002_canIsoSmiles = "c1cc(cc(c1)Br)[NH2+]c2ncc(c(n2)Nc3cccc(c3)Br)F"

# Example pairs that should match
SM21_micro001_canIsoSmiles = "c1cc(cc(c1)Br)Nc2[nH]cc(/c(=[NH+]/c3cccc(c3)Br)/n2)F"
SM21_micro001_canSmiles = "c1cc(cc(c1)Br)Nc2[nH]cc(c(=[NH+]c3cccc(c3)Br)n2)F"


# Testing match between pKa microstates

mol1 = get_labeled_mol(SM21_micro001_canIsoSmiles )
mol2 = get_labeled_mol(SM21_micro002_canIsoSmiles)

add_h(mol1) # It is necessary to use explicit hydrogens.
add_h(mol2)

print(match_microstates(mol1, mol2)) # Prints true if two structures are related to the same pKa microstate.



