#!/usr/bin/env python3
#############################################################################
# Copyright (C) 2014-2016 OpenEye Scientific Software, Inc.
#############################################################################
# Converting CSV or SDF files into EXCEL
#############################################################################

import sys
import os
import xlsxwriter
from openeye.oechem import *
from openeye.oedepict import *


def main(argv=[__name__]):

    itf = OEInterface(InterfaceData)
    OEConfigure2DMolDisplayOptions(itf, OE2DMolDisplaySetup_AromaticStyle)

    if not OEParseCommandLine(itf, argv):
        return 1

    iname = itf.GetString("-in")
    oname = itf.GetString("-out")

    # check input/output files

    ifs = oemolistream()
    if not ifs.open(iname):
        OEThrow.Fatal("Cannot open input file!")

    if ifs.GetFormat() != OEFormat_CSV and ifs.GetFormat() != OEFormat_SDF:
        OEThrow.Fatal("Input must be CSV or SDF file!")

    ext = OEGetFileExtension(oname)
    if ext != "xlsx":
        OEThrow.Fatal("Output must be XLSX format.")

    # import molecules

    mollist = []
    for mol in ifs.GetOEGraphMols():
        mollist.append(OEGraphMol(mol))

    # setup depiction options

    width, height = 350, 350
    opts = OE2DMolDisplayOptions(width, height, OEScale_AutoScale)
    OESetup2DMolDisplayOptions(opts, itf)
    opts.SetTitleLocation(OETitleLocation_Hidden)

    # collect data tags

    tags = CollectDataTags(mollist)

    # generate XLSX file

    WriteXLSXFile(oname, mollist, iname, tags, opts)

    return 0


def CollectDataTags(mollist):

    tags = []
    for mol in mollist:
        for dp in OEGetSDDataIter(mol):
            if not dp.GetTag() in tags:
                tags.append(dp.GetTag())

    return tags


def WriteXLSXFile(oname, mollist, iname, tags, opts):

    # create an Excel file and add formating

    workbook = xlsxwriter.Workbook(oname)
    worksheet = workbook.add_worksheet()

    headfont, headformat = AddHeadFormat(workbook)
    datafont, dataformat_even, dataformat_odd = AddDataFormats(workbook)

    # estimate width of columns

    maxwidths = []
    maxwidths.append(opts.GetWidth() * 0.15)

    for tag in tags:
        maxwidth = OEEstimateTextWidth(tag, headfont) * 1.5
        for mol in mollist:
            if OEHasSDData(mol, tag):
                maxwidth = max(maxwidth, OEEstimateTextWidth(OEGetSDData(mol, tag), datafont))
        maxwidths.append(maxwidth * 0.12)

    # generate header

    row, col = 0, 0
    worksheet.set_row(row, None, headformat)
    worksheet.merge_range('A1:D1', iname)

    row, col = 1, 0
    worksheet.set_row(row, None, headformat)
    worksheet.set_column(col, col, maxwidths[col])
    worksheet.write(row, col, "Molecule")

    for tag in tags:
        col += 1
        worksheet.set_column(col, col, maxwidths[col])
        worksheet.write(row, col, tag)

    # generate rows

    tmpfnames = []

    for mol in mollist:
        row += 1

        if row % 2 == 0:
            dataformat = dataformat_even
        else:
            dataformat = dataformat_odd

        worksheet.set_row(row, opts.GetHeight() * 0.50, dataformat)

        col = 0
        fname = "tmp%d.png" % row
        WriteImageToFile(fname, mol, opts)
        worksheet.insert_image(row, col, fname)
        tmpfnames.append(fname)

        for tag in tags:
            col += 1
            value = "N/A"
            if OEHasSDData(mol, tag):
                value = OEGetSDData(mol, tag)
            worksheet.write(row, col, value)

    workbook.close()

    # remove temporary image files

    for fname in tmpfnames:
        os.remove(fname)


def WriteImageToFile(fname, mol, opts):

    OEPrepareDepiction(mol)
    disp = OE2DMolDisplay(mol, opts)
    OERenderMolecule(fname, disp, False)


def AddHeadFormat(workbook):

    font = OEFont(OEFontFamily_Default, OEFontStyle_Bold, 18,
                  OEAlignment_Center, OEBlack)
    format = workbook.add_format({'bold': True, 'align': 'center',
                                 'valign': 'vcenter', 'size': 18})
    format.set_bg_color('#F4F4F4')
    format.set_border_color('#DDDDDD')
    format.set_border()

    return font, format


def AddDataFormats(workbook):

    font = OEFont(OEFontFamily_Default, OEFontStyle_Default, 12,
                  OEAlignment_Center, OEBlack)

    format_even = workbook.add_format({'bold': False, 'align': 'center',
                                      'valign': 'vcenter', 'size': 12})
    format_even.set_shrink()
    format_even.set_bg_color('#FFFFF4')
    format_even.set_border_color('#DDDDDD')
    format_even.set_border()

    format_odd = workbook.add_format({'bold': False, 'align': 'center',
                                     'valign': 'vcenter', 'size': 12})
    format_odd.set_shrink()
    format_odd.set_bg_color('#FFF4FF')
    format_odd.set_border_color('#DDDDDD')
    format_odd.set_border()

    return font, format_even, format_odd


InterfaceData = '''
!CATEGORY "input/output options"

    !PARAMETER -in
      !ALIAS -i
      !TYPE string
      !REQUIRED true
      !KEYLESS 1
      !VISIBILITY simple
      !BRIEF Input filename(s)
    !END

    !PARAMETER -out
      !ALIAS -o
      !TYPE string
      !REQUIRED true
      !KEYLESS 2
      !VISIBILITY simple
      !BRIEF Output XLSX filename (extension .xlsx)
    !END

!END
'''

if __name__ == "__main__":
        sys.exit(main(sys.argv))
