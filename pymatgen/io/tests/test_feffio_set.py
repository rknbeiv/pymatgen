#!/usr/bin/python
import unittest
import os

from pymatgen.io.feffio_set import FeffInputSet
from pymatgen.io.feffio import FeffPot
from pymatgen.io.cifio import CifParser

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        'test_files')
cif_file = 'CoO19128.cif'
central_atom = 'O'
cif_path = os.path.join(test_dir, cif_file)
r = CifParser(cif_path)
structure = r.get_structures()[0]
x = FeffInputSet("MaterialsProject")


class FeffInputSetTest(unittest.TestCase):

    header_string = """* This FEFF.inp file generated by pymatgen
TITLE comment: From cif file
TITLE Source:  CoO19128.cif
TITLE Structure Summary:  Co2 O2
TITLE Reduced formula:  CoO
TITLE space group: (P6_3mc), space number:  (186)
TITLE abc:  3.297078   3.297078   5.254213
TITLE angles: 90.000000  90.000000 120.000000
TITLE sites: 4
* 1 Co     0.333334     0.666666     0.503676
* 2 Co     0.666667     0.333333     0.003676
* 3 O     0.333334     0.666666     0.121324
* 4 O     0.666667     0.333333     0.621325"""

    def test_get_header(self):
        comment = 'From cif file'
        header = str(FeffInputSet.get_header(x, structure, 'CoO19128.cif',
                                             comment))
        self.maxDiff = 1000
        self.assertEqual(FeffInputSetTest.header_string.splitlines(),
                         header.splitlines())

    def test_getfefftags(self):
        tags = FeffInputSet.get_feff_tags(x, "XANES").to_dict
        self.assertEqual(tags['COREHOLE'], "FSR",
                         "Failed to generate PARAMETERS string")

    def test_get_feffPot(self):
        POT = str(FeffInputSet.get_feff_pot(x, structure, central_atom))
        d, dr = FeffPot.pot_dict_from_string(POT)

        self.assertEqual(d['Co'], 1, "Wrong symbols read in for FeffPot")

    def test_get_feff_atoms(self):
        ATOMS = str(FeffInputSet.get_feff_atoms(x, structure, central_atom))
        self.assertEqual(ATOMS.splitlines()[3].split()[4], central_atom,
                         "failed to create ATOMS string")

    def test_to_and_from_dict(self):
        d = x.to_dict(structure, 'XANES', 'cif', 'O', 'test')
        f = d['feff.inp']
        f2 = x.from_dict(d)
        self.assertEqual(f, f2, "FeffinputSet to and from dict do not match")

if __name__ == '__main__':
    unittest.main()
