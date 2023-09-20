"""run **rivtlib** as library or script

**rivtlib** is designed to be run within an IDE but may be run from the
command line as:

    python -m rivtlib rel-path/rivtnn-filename.py

where where *nn* is an integer used for report organization and *rel-path* is
relative to the rivt project folder. If rel-path is omitted then the file is
assumed to be located in the folder where the command was invoked. See **rivt User
Manual** at https://rivt-doc.net for details.

The code base uses a last letter naming convention for signaling variable
types:

A = array
B = boolean
C = class instance
D = dictionary
F = float
I = integer
L = list
P = path
S = string
"""
__version__ = "a.b.c"
__author__ = "rhholand"

import sys
from pathlib import Path


def cmdlinehelp():
    """command line help"""

    print()
    print("Run the following command in a rivt document folder:")
    print()
    print("  python -m rivtlib rel-path/rivtnn-filename.py     ")
    print()
    print("Text output is written to stdout.                   ")
    print("Other outputs depend on rivt file settings.         ")
    print()
    print("See User Manual at https://rivt-doc.net for details            ")


if sys.version_info < (3, 8):
    sys.exit("rivtlib requires Python version 3.8 or later")

if __name__ == "__main__":
    try:
        import rivtlib.rivtapi
    except:
        cmdlinehelp()
