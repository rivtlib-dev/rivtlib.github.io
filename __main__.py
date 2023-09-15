"""run as library or script

*rivtlib* is designed to be run from within an IDE but may be run from the
command line:

    python -m rivtlib rivt-filename.py

where *rivt-filename.py* is in the execution folder. See https://rivt-doc.net
for further details.

This code base uses a last letter naming convention for indicating variable
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

import sys
from pathlib import Path

__version__ = "0.8.1-beta.1"
__author__ = "rholland@structurelabs.com"


def cmdlinehelp():
    """command line help"""

    print()
    print("Run the following command in a rivt document folder:")
    print()
    print("       python -m rivtlib rivt-filename.py           ")
    print()
    print("Text output is written to stdout.                   ")
    print("Other outputs depend on rivt file settings.         ")
    print()
    print("See User Manual at: https://rivt-doc.net            ")


if sys.version_info < (3, 8):
    sys.exit("rivtlib requires Python version 3.8 or later")

if __name__ == "__main__":
    try:
        import rivtlib.rivtapi
    except:
        cmdlinehelp()
