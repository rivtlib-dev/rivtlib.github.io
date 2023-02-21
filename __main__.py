"""check if run as script or interactively and adjust initialization

*rivt* may be run interactively from an IDE or from the command line. In an IDE
the API calls can be grouped by the standard cell designation #%% and run
interactively. If run from the the command line within the rivt document folder,
**rivt** will process the entire file:

    python -m rivt

The program will find and execute the file *rvddnn_file.py*, where dd is the
two digit division number and nn the subdivision number. Docs are output as UTF
text, PDF and HTML files. See https://rivtDocs.net for the **rivtDocs** user
manual.

Within the code base the following convention for typing variable names has
been used, where the last letter of each variable name indicates the type.

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
utfS = """"""  # rivtText string
calcfileP = ""  # calc file name


def cmdlinehelp():
    """command line help"""

    print()
    print("Run rivt at the command line in the rivt document folder:   ")
    print()
    print("                 python -m rivt                             ")
    print()
    print("If rivt file is not found, check that it has the form:      ")
    print("rvddnn_some_name.py - where dd and nn are two digit integers")
    print()
    print("The output files are written to:                ")
    print("        dcoument folder:  README.txt            ")
    print("        report folder:    rddnn_file.pdf        ")
    print("        website folder:   rddnn_file.html       ")
    print()
    print("User manual is at: https://rivtDocs.net         ")


if sys.version_info < (3, 8):
    sys.exit("rivtCalc requires Python version 3.8 or later")

if __name__ == "__main__":
    print("""
    rivt is running from commmand line
    """)
    try:
        # get calc file name
        for fileS in os.listdir("."):
            if fnmatch.fnmatch(fileS, "c[0-9][0-9][0-9][0-9]_*.py"):
                for fileS in os.listdir("."):
                    if fnmatch.fnmatch(fileS, "c[0-9][0-9][0-9][0-9]_*.py"):
                        calcfileP = Path(os.getcwd(), fileS)
                calcnameS = os.path.basename(calcfileP)  # calc file
                calcbaseS = calcnameS.split(".py")[0]  # calc file basename
                calcfolderP = calcfileP.parent  # calc file basename
            print("MAIN  current folder: ", calcfolderP)
            print("MAIN  rivt file name: ", calcbaseS)
            importlib.import_module(calcbaseS)
    except ImportError as error:
        print("error------------ rivt file not found ----------------------")
        print(" ")
        cmdlinehelp()
        # test files and paths
        cwdP = Path(os.getcwd())
        print("current working directory:", cwdP)
        calcfileS = "rv0101_test.py"
        calcbaseS = "rv0101_test"
        P = Path(cwdP / "rivt_test")
        calcfileP = P / "text" / "rv0101_test" / calcfileS
        calcnameS = os.path.basename(calcfileP)  # calc file
        calcbaseS = str(calcnameS.split(".py")[0])  # calc file basename
        sys.exit()
