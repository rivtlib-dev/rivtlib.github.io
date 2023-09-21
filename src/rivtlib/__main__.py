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
import getopt

if sys.version_info < (3, 8):
    sys.exit("rivtlib requires Python version 3.8 or later")


def main(argv):
    """process command line arguments"""

    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is ', inputfile)
    print('Output file is ', outputfile)


def cmdlinehelp():
    """command line help"""

    print()
    print("Run the following command in a rivt file folder:           ")
    print()
    print("     python -m rivtlib rivtnn-filename.py                  ")
    print()
    print("The command is run in the rivt file folder.                ")
    print("Text output is written to stdout.                          ")
    print("Other file outputs depend on file contents.                ")
    print("See User Manual at https://rivt-doc.net for details        ")
    sys.exit()


if __name__ == "__main__":
    try:
        fileS = sys.argv[1]
        import rivtlib.rivtapi
    except:
        cmdlinehelp()
