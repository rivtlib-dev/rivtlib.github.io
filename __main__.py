# type:ignore
""" 

**rivt** may be run interactively from an IDE or from the command line. In
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
_calcfileS = "empty"    # primary processed rivtText string

if sys.version_info < (3, 8):
    sys.exit("rivtCalc requires Python version 3.8 or later")


def cmdlinehelp():
    """command line help"""
    print()
    print("Run rivt at the command line within the calc folder as:")
    print("     python -m rivt ")
    print("The program will find and run the file rvddnn_calcfilename.py")
    print()
    print("The logs and output specified in the calc are written to the") 
    print("calc (.txt), pdf (.pdf) or html (.html) folder.")
    print()
    print("The rivtCalc user manual is at: https://rivt.info.")
    sys.exit()


if __name__ == "__main__":
    try:
        _calcfileS = sys.argv[1]  # calc file argument
        _cwdS = os.getcwd()  # get calc folder
        _cfull = Path(_calcfileS)  # calc file full path
        _cfileS = Path(_cfull).name  # calc file name
        _cbaseS = _cfileS.split(".py")[0]  # calc file basename
        print("MAIN  current folder: ", _cwdS)
        print("MAIN  calc name: ", _cfileS)
        importlib.import_module(_cbaseS)
    except ImportError as error:
        print("error---------------------------------------------")
        print(error)
        cmndlinehelp()
    except Exception as exception:
        # Output unexpected Exceptions.
        print("exception-----------------------------------------")
        print(exception)
        cmndlinehelp()
