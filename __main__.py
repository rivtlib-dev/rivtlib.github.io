"""intialize if run as script

*rivt* may be run interactively from an IDE or from the command line. In an IDE
the API calls can be grouped by the standard cell designation #%% and run
interactively. As e command line within the rivt document folder, **rivt** will
process the entire file:

    python -m rivt

The program execute the file *rvddnn_file.py* in the folder, where dd is the
two digit division number and nn the subdivision number. Docs are output as md
text, PDF and HTML files. See https://rivtDocs.net for the **rivtDocs** user
manual.

This code base uses a last letter convention for variable name types:

A = array
B = boolean
I = integer
L = list
F = float
P = path
S = string
D = dictionary
C = class instance
"""

import os
import sys
import importlib
import fnmatch
from pathlib import Path

__version__ = "0.9.1-beta.1"
__author__ = "rholland@structurelabs.com"


def cmdlinehelp():
    """command line help"""

    print()
    print("Run command in rivt document folder ")
    print()
    print("                 python -m rivt                             ")
    print()
    print("file is rddnn.py - where dd and nn are two digit integers.  ")
    print()
    print("Output files are written to:      ")
    print("    current document folder:  README.txt       ")
    print("    report folder:            rvddnn_file.pdf  ")
    print("    site folder:              rvdnn_file.html  ")
    print()
    print("User manual is at: https://rivtDocs.net        ")


if sys.version_info < (3, 8):
    sys.exit("rivtCalc requires Python version 3.8 or later")

if __name__ == "__main__":
    try:
        import rivt.rivtapi
    except:
        cmdlinehelp()
