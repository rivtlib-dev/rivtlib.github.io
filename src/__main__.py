"""rivtlib

rivtlib is generally run in an IDE. If run from the command line the command
takes one of two forms depending on whether the file is part of a report. If
part of a report the form is:

    python -m rivtlib rddnn-filename.py

where *rddnn-* and *dd* and *nn* are integers identifying the report division
and subdivision respectively. If the file is a standalone document then
resource files are assumed to be in the current folder or subfolder and the
command is:

    python -m rivtlib filename.py

In this case output files will also be in the current file folder. See the
**rivt User Manual** at https://rivt.info for details.

This code base uses a last-letter naming convention for indicating variable
types where:

A = array 
B = boolean 
C = class instance 
D = dictionary 
F = float 
I = integer 
L = list
N = file name 
P = path 
S = string

"""
__version__ = "a.b.c"
__author__ = "rhholand"

import getopt
import sys

if sys.version_info < (3, 11):
    sys.exit("rivtlib requires Python version 3.11 or later")


def cmdhelp():
    """command line help"""

    print()
    print("Run the following command in a folder with a rivt file:           ")
    print()
    print("     python -m rivtlib rddss-filename.py                  ")
    print()
    print("The command is run in the rivt file folder.                ")
    print("File name must match 'rivddss-filename.py                  ")
    print("Where dd and ss are two digit integers.                    ")
    print("Text output is written to stdout.                          ")
    print("Other outputs depend on file contents.                     ")
    print("See User Manual at https://rivt.info for details        ")
    sys.exit()


if __name__ == "__main__":
    try:
        argfileS = sys.argv[1]
        import rivtlib.api
    except:
        cmdhelp()
