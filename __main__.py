# type:ignore
""" 
*rivt* may be run interactively from an IDE or from the command line. In
IDE's one or more API calls can be grouped by the standard cell designation #%%
and run interactively.

If run from the the command line within the calc folder, **rivt** processes the
entire file:

    python -m rivt

In this case the program finds the calc file *rvddnn_calcfile.py*, where where
dd is the two digit division number and nn is the two digit subdivision number.
Calcs are output as UTF text, PDF and HTML files. See https://rivt.info for the
**rivtcalc** manual.

The following convention for typing variable names has been used, where the
last letter of each variable name indicates the type.

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
from pathlib import Path

__version__ = "0.9.1-beta.1"
__author__ = "rholland@structurelabs.com"
utfS = """"""  # rivtText string
cfileP = ""  # calc file name

if sys.version_info < (3, 8):
    sys.exit("rivtCalc requires Python version 3.8 or later")


def cmdlinehelp():
    """command line help"""
    print()
    print("Run rivt at the command line in the calc folder: ")
    print()
    print("                 python -m rivt                         ")
    print()
    print("The program will find and run the file cddnn_calcfile.py")
    print()
    print("The output files specified in the calc are written to:  ")
    print("          calc folder:      README.txt                  ")
    print("          report folder:    cddnn_calcfile.pdf          ")
    print("          site folder:      index.html                  ")
    print()
    print("The rivtCalc user manual is at: https://rivtDocs.net    ")
    sys.exit()


if __name__ == "__main__":
    try:
        # get calc file name
        for fileP in os.listdir("."):
            if fnmatch.fnmatch(file, "c[0-9][0-9][0-9][0-9]_*.py"):
                cfileP = fileP
        cwdP = os.getcwd()  # get calc folder
        cfullP = Path(cfileP)  # calc file full path
        cbaseP = cfileP.split(".py")[0]  # calc file basename
        print("MAIN  current folder: ", cwdP)
        print("MAIN  calc name: ", cfileP)
        importlib.import_module(cbaseP)
    except ImportError as error:
        print("error---------------------------------------------")
        print(error)
        cmndlinehelp()
    except Exception as exception:
        # Output unexpected Exceptions.
        print("exception-----------------------------------------")
        print(exception)
        cmndlinehelp()
