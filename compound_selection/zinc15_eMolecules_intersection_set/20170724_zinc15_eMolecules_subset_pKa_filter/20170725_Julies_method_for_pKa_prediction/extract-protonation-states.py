#!/usr/bin/env python

"""
Mine the list of clinical kinase inhibitors for pKa values near 7.

"""

import os
import sys
import csv
import math
import datetime
import commands
import numpy as np

from openeye import oechem, oequacpac, oeomega, oeiupac # Requires OpenEye toolkit

source_filename = 'clinical-kinase-inhibitors.csv'

def normalize_molecule(molecule):
    """Normalize a copy of the molecule by checking aromaticity, adding explicit hydrogens, and renaming by IUPAC name.
    Parameters
    ----------
    molecule : OEMol
        the molecule to be normalized.

    Returns
    -------
    molcopy : OEMol
        A (copied) version of the normalized molecule
    """
    molcopy = oechem.OEMol(molecule)

    # Assign aromaticity.
    oechem.OEAssignAromaticFlags(molcopy, oechem.OEAroModelOpenEye)

    # Add hydrogens.
    oechem.OEAddExplicitHydrogens(molcopy)

    # Set title to IUPAC name.
    name = oeiupac.OECreateIUPACName(molcopy)
    molcopy.SetTitle(name)

    # Check for any missing atom names, if found reassign all of them.
    if any([atom.GetName() == '' for atom in molcopy.GetAtoms()]):
        oechem.OETriposAtomNames(molcopy)

    return molcopy

def generate_conformers(molecule, max_confs=800, strictStereo=True, ewindow=15.0, rms_threshold=1.0):
    """Generate conformations for the supplied molecule
    Parameters
    ----------
    molecule : OEMol
        Molecule for which to generate conformers
    max_confs : int, optional, default=800
        Max number of conformers to generate.  If None, use default OE Value.
    strictStereo : bool, optional, default=True
        Adhere to strict specification of stereo isomer
    Returns
    -------
    molcopy : OEMol
        A multi-conformer molecule with up to max_confs conformers.

    Notes
    -----
    Roughly follows
    http://docs.eyesopen.com/toolkits/cookbook/python/modeling/am1-bcc.html
    """
    molcopy = oechem.OEMol(molecule)
    omega = oeomega.OEOmega()

    # These parameters were chosen to match http://docs.eyesopen.com/toolkits/cookbook/python/modeling/am1-bcc.html
    omega.SetMaxConfs(max_confs)
    omega.SetIncludeInput(True)
    omega.SetCanonOrder(False)

    omega.SetSampleHydrogens(True)  # Word to the wise: skipping this step can lead to significantly different charges!
    omega.SetEnergyWindow(ewindow)
    omega.SetRMSThreshold(rms_threshold)  # Word to the wise: skipping this step can lead to significantly different charges!

    omega.SetStrictStereo(strictStereo)

    omega.SetIncludeInput(False)  # don't include input
    if max_confs is not None:
        omega.SetMaxConfs(max_confs)
    omega(molcopy)  # generate conformation

    return molcopy

def smiles_to_oemol(smiles):
    """Create a OEMolBuilder from a smiles string.

    Parameters
    ----------
    smiles : str
        SMILES representation of desired molecule.
    Returns
    -------
    molecule : OEMol
        A normalized molecule with desired smiles string.

    """
    molecule = oechem.OEMol()
    if not oechem.OEParseSmiles(molecule, smiles):
        raise ValueError("The supplied SMILES '%s' could not be parsed." % smiles)

    molecule = normalize_molecule(molecule)

    return molecule

def run_epik(molecule, maxconf=99, verbose=False, outfile=None):
    """
    Enumerate the list of conformers and associated properties for each protonation and tautomeric state using epik from the Schrodinger Suite.

    Parameters
    ----------
    options
    molecule : openeye.oechem
        The molecule read from the PDB whose protomer and tautomer states are to be enumerated.
    maxconf : int, optional, default=128
        Maximum number of protomers/tautomers to generate.
    verbose : bool, optiona, default=False
        If True, outputs more information.
    outfile : file, optional, default=None
        If specified, record compiled pKas to this output file.

    """

    from schrodinger import structure # Requires Schrodinger Suite

    # Write mol2 file.
    if verbose: print "Writing input file as mol2..."
    outmol = oechem.OEMol(molecule)
    ofs = oechem.oemolostream()
    ofs.open('epik-input.mol2')
    oechem.OEWriteMolecule(ofs, outmol)
    ofs.close()
    # Use low level writer to get atom names correct.
    ofs = oechem.oemolostream()
    ofs.open('epik-input.mol2')
    for (dest_atom, src_atom) in zip(outmol.GetAtoms(), molecule.GetAtoms()):
        dest_atom.SetName(src_atom.GetName())
    oechem.OEWriteMol2File(ofs, outmol, True)
    ofs.close()

    # Write mol2 file.
    if verbose: print "Writing input file as sdf..."
    outmol = oechem.OEMol(molecule)
    ofs = oechem.oemolostream()
    ofs.open('epik-input.sdf')
    oechem.OEWriteMolecule(ofs, outmol)
    ofs.close()

    # Write pdb file.
    if verbose: print "Writing input file as pdb..."
    outmol = oechem.OEMol(molecule)
    ofs = oechem.oemolostream()
    ofs.open('epik-input.pdb')
    oechem.OEWriteMolecule(ofs, outmol)
    ofs.close()

    # Write input for epik.
    if verbose: print "Converting input file to Maestro format..."
    reader = structure.StructureReader("epik-input.mol2")
    writer = structure.StructureWriter("epik-input.mae")
    for st in reader:
        writer.append(st)
    reader.close()
    writer.close()

    # Run epik to enumerate predicted pKas.
    if verbose: print "Running Epik..."
    cmd = '%s/epik -imae epik-input.mae -omae epik-output.mae -scan -lowest_pka 1.0 -highest_pka 12.0 -WAIT' % (os.environ['SCHRODINGER'])
    output = commands.getoutput(cmd)
    if verbose: print output

    # Extract pKas from Epik output.
    cmd = 'grep conjugate epik-output.log'
    output = commands.getoutput(cmd)
    pKas = list()
    for line in output.split('\n'):
        print "> %s" % line

        # Extract information
        pKa = float(line[0:7].strip())
        type = line[9:13]
        atom_index = int(line[24:28].strip())
        notes = line[31:]

        state = dict({ 'pKa' : pKa, 'type' : type, 'atom_index' : atom_index, 'notes' : notes })
        pKas.append(state)

        print "pKa %8.3f %s atom %d type %s" % (pKa, type, atom_index, notes)

    # Store output.
    command = 'cp epik-output.log epik-output.%s.log' % molecule.GetTitle()
    commands.getoutput(command)

    # Write pKas only to file, if desired.
    if outfile:
        outfile.write('%s %d' % (molecule.GetTitle(), len(pKas)))
        for pKa in pKas:
            outfile.write(' %8.2f' % (pKa['pKa']))
        outfile.write('\n')

    return

# Read clinical kinase inhibitors.
molecules = list()
outfile = open('inhibitor-pKas.out', 'w')
with open(source_filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        name = row[0]
        smiles = row[1]

        print '%s %s' % (name, smiles)

        try:
            # Create molecule.
            molecule = smiles_to_oemol(smiles)
            molecule = generate_conformers(molecule)
            molecule.SetTitle(name)

            # Run Epik to compute pKas.
            run_epik(molecule, verbose=True, outfile=outfile)
        except Exception as e:
            print str(e)

outfile.close()

