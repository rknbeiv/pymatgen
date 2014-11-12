# coding: utf-8

from __future__ import unicode_literals

"""
Created on Nov 14, 2012
"""


__author__ = "Anubhav Jain"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Anubhav Jain"
__email__ = "ajain@lbl.gov"
__date__ = "Nov 14, 2012"

import unittest
import os

from pymatgen.util.testing import PymatgenTest
from pymatgen.util.io_utils import micro_pyawk

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        'test_files')


class FuncTest(PymatgenTest):

    def test_micro_pyawk(self):
        filename = os.path.join(test_dir, "OUTCAR")
        data = []
        def f(x, y):
            data.append(y.group(1).strip())
        micro_pyawk(filename, [["POTCAR:(.*)", lambda x: x, f]])
        print data

if __name__ == "__main__":
    unittest.main()
