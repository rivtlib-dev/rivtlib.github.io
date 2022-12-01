# type:ignore
"""
***rivtcalc** may be run interactively from an editor or IDE and from the
command line. In an IDE an API function or cell (designated by # %%) can be run
at a time. The command line invocation that operates on the whole file is made
from the folder containing the file:

    python -m rivtcalc cddss_calcfile.py (-term)

The calc number ddss is used for document and report organization, where dd is
a two digit division number and ss is a two digit subdivision number. Calcs are
output as UTF text calcs or PDF docs. UTF calcs are printed to the terminal
when interactive cell is run. If file output is specified, the calc or doc
files are written to the calc folder.

The following convention for variable names has been used: the last letter of
each variable name indicates the type.

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
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

__version__ = "0.8.1-beta.1"
__author__ = "rholland@structurelabs.com"
_calcfileS = "empty"

if sys.version_info < (3, 7):
    sys.exit("rivtCalc requires Python version 3.7 or later")


def _cmdlinehelp():
    """command line help"""
    print()
    print("Run rivt at the command line within the calc folder as:")
    print("     python -m rivt ")
    print("The program will find and run the file rvddnn_calcfilename.py")
    print()
    print()
    print("The logs and output specified in the calc is written to the") 
    print("calc, pdf or html folder.")
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
    except Exception as exception:
        # Output unexpected Exceptions.
        print("exception-----------------------------------------")
        print(exception)
