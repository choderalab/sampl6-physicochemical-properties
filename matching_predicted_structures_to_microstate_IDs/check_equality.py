# Bas Rustenburg's script for checking if two structures are the same microstate.
# 2017/12/18
#
# Rationelle: if MCSS can map all atoms of two structures (target and pattern), it has to be the exact same graph.
# Here the MCSS checks atomic number, but ignores electronic structure (bond order/charges).
# If the entire target, and the entire pattern have the same amount if atoms as the match, it means it found the full 
# map between them.


from openeye import oechem
import logging as logger

def are_equal_microstates(mol1: oechem.OEMol, mol2: oechem.OEMol):
    """ Check if two supplied OE(Graph)Mol objects have the same molecular microstate present.
    
    If all atoms and bonds are matched in MCSS returns True. Ignores charges and bond order
    to deal with chirality and geometry differences as well as resonance structures
    (which we won't consider as different).
    
    Returns
    -------
    bool    
    """
    # Copy input
    pattern = oechem.OEMol(mol1) 
    target = oechem.OEMol(mol2)
    
    # Atoms are equal if they have same atomic number (so explicit Hydrogens are needed as well for a match)
    atomexpr = oechem.OEExprOpts_AtomicNumber
     # single or double bonds are considered identical (resonance,chirality fix)
    bondexpr = oechem.OEExprOpts_EqSingleDouble
    # create maximum common substructure object
    mcss = oechem.OEMCSSearch(pattern, atomexpr, bondexpr, oechem.OEMCSType_Exhaustive)
    
    # set scoring function
    mcss.SetMCSFunc(oechem.OEMCSMaxAtomsCompleteCycles())
    # ignore matches smaller than 6 atoms
    mcss.SetMinAtoms(6)
    unique = True


    # loop over matches
    count = 0
    match = oechem.OEMol()
    for i, match in enumerate(mcss.Match(target, unique)):
        count = i + 1
        logger.debug("Match %d:" % (count))
    
        logger.debug( "Num atoms in match %d" % match.NumAtoms())
        logger.debug( "Num atoms in mol1 %d" % pattern.NumAtoms())
        logger.debug( "Num atoms in mol2 %d" % target.NumAtoms())


    # check if there is only single match
    if (count > 1):
        logger.warning("Warning! There are multiple matches.")
    elif count == 0:
        logger.debug("No match")
        
    m_num = match.NumAtoms()
    p_num = pattern.NumAtoms()
    t_num = target.NumAtoms()
        
        
    return m_num == p_num == t_num



# Testing
def add_h(mol: oechem.OEMol):
    """Add explicit hydrogens for test cases"""
    for atom in mol.GetAtoms():
        oechem.OEAddExplicitHydrogens(mol, atom)

# electrons shifted for benzene
mol1 = oechem.OEMol()
oechem.OESmilesToMol(mol1, "C1=C[CH-]=CC=[CH+]1")
add_h(mol1)

# regular benzene
mol2 = oechem.OEMol()
oechem.OESmilesToMol(mol2, "c1ccccc1")
add_h(mol2)

# protonated benzene
mol3 = oechem.OEMol()
oechem.OESmilesToMol(mol3, "C1=C[CH2-]=CC=[C+]1")
add_h(mol3)

if not are_equal_microstates(mol1, mol2):
    raise RuntimeError("These should be resonance structures")

if not are_equal_microstates(mol2, mol1):
    raise RuntimeError("Order should not matter.")

if are_equal_microstates(mol1, mol3):
    raise RuntimeError("These should not be equal states.")

if are_equal_microstates(mol2, mol3):
    raise RuntimeError("These should not be equal states either.")
