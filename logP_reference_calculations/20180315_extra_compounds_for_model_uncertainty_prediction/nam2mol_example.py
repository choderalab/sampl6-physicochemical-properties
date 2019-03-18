#!/usr/bin/env python
# (C) 2017 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

import sys
from openeye import oechem
from openeye import oeiupac


def Nam2Mol(itf):
    ifp = sys.stdin
    if itf.GetString("-in") != "-":
        ifp = open(itf.GetString("-in"))

    ofs = oechem.oemolostream()
    if not ofs.open(itf.GetString("-out")):
        oechem.OEThrow.Fatal("Unable to open output file: %s" % itf.GetString("-out"))

    language = oeiupac.OEGetIUPACLanguage(itf.GetString("-language"))
    charset = oeiupac.OEGetIUPACCharSet(itf.GetString("-charset"))

    mol = oechem.OEGraphMol()
    for name in ifp:
        name = name.strip()
        mol.Clear()

        # Speculatively reorder CAS permuted index names
        str = oeiupac.OEReorderIndexName(name)
        if len(str) == 0:
            str = name

        if charset == oeiupac.OECharSet_HTML:
            str = oeiupac.OEFromHTML(str)
        if charset == oeiupac.OECharSet_UTF8:
            str = oeiupac.OEFromUTF8(str)

        str = oeiupac.OELowerCaseName(str)

        if language != oeiupac.OELanguage_AMERICAN:
            str = oeiupac.OEFromLanguage(str, language)

        done = oeiupac.OEParseIUPACName(mol, str)

        if not done and itf.GetBool("-empty"):
            mol.Clear()
            done = True

        if done:
            if itf.HasString("-tag"):
                oechem.OESetSDData(mol, itf.GetString("-tag"), name)

            mol.SetTitle(name)
            oechem.OEWriteMolecule(ofs, mol)


############################################################
InterfaceData = """
# nam2mol interface file
!CATEGORY nam2mol

    !CATEGORY I/O
        !PARAMETER -in 1
          !ALIAS -i
          !TYPE string
          !REQUIRED true
          !BRIEF Input filename
          !KEYLESS 1
        !END

        !PARAMETER -out 2
          !ALIAS -o
          !TYPE string
          !DEFAULT -
          !BRIEF Output filename
          !KEYLESS 2
        !END
    !END

    !CATEGORY Lexichem Features

        !PARAMETER -language 1
           !ALIAS -lang
           !TYPE string
           !DEFAULT american
           !LEGAL_VALUE american
           !LEGAL_VALUE english
           !LEGAL_VALUE us

           !LEGAL_VALUE chinese
           !LEGAL_VALUE zh
           !LEGAL_VALUE cn

           !LEGAL_VALUE danish
           !LEGAL_VALUE dk
           !LEGAL_VALUE da

           !LEGAL_VALUE dutch
           !LEGAL_VALUE nl

           !LEGAL_VALUE french
           !LEGAL_VALUE fr

           !LEGAL_VALUE german
           !LEGAL_VALUE de

           !LEGAL_VALUE greek
           !LEGAL_VALUE el

           !LEGAL_VALUE hungarian
           !LEGAL_VALUE hu

           !LEGAL_VALUE irish
           !LEGAL_VALUE ie
           !LEGAL_VALUE ga

           !LEGAL_VALUE italian
           !LEGAL_VALUE it

           !LEGAL_VALUE japanese
           !LEGAL_VALUE jp
           !LEGAL_VALUE ja

           !LEGAL_VALUE polish
           !LEGAL_VALUE pl

           !LEGAL_VALUE portuguese
           !LEGAL_VALUE pt

           !LEGAL_VALUE romanian
           !LEGAL_VALUE ro

           !LEGAL_VALUE russian
           !LEGAL_VALUE ru

           !LEGAL_VALUE slovak
           !LEGAL_VALUE sk

           !LEGAL_VALUE spanish
           !LEGAL_VALUE es

           !LEGAL_VALUE swedish
           !LEGAL_VALUE se
           !LEGAL_VALUE sv

           !LEGAL_VALUE welsh
           !LEGAL_VALUE cy

           !REQUIRED false
           !BRIEF Language for input names.
        !END

        !PARAMETER -tag 3
           !TYPE string
           !REQUIRED false
           !BRIEF Set name as SD data with tag
        !END

        !PARAMETER -empty 4
           !TYPE bool
           !DEFAULT false
           !BRIEF Output an empty molecule for unparseable names
        !END
        !PARAMETER -charset 5
           !ALIAS -encoding
           !TYPE string
           !DEFAULT default
           !REQUIRED false
           !LEGAL_VALUE default
           !LEGAL_VALUE ascii
           !LEGAL_VALUE utf8
           !LEGAL_VALUE html
           !BRIEF Choose charset/encoding for input names.
        !END
    !END
!END
"""


def main(argv=[__name__]):
    itf = oechem.OEInterface(InterfaceData, argv)
    Nam2Mol(itf)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
