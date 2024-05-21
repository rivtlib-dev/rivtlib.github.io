#! python
"""rivt API

The rivt API exposes 6 functions:

import rivtlib.rivtapi as rv

rv.R(rS) - (Run) Execute shell scripts 
rv.I(rS) - (Insert) Insert static text, math, images and tables
rv.V(rS) - (Values) Evaluate values and equations 
rv.T(rS) - (Tools) Execute Python functions and scripts 
rv.X(rS) - (eXclude) Skip string processing 
rv.W(rS) - (Write) Write formatted document 

where rS is a triple quoted Python string.

Note on code notation:

Variable types are indicated by the last letter of the variable name
S = string
D = dictionary
F = float
I = integer
P = path
C = class instance

"""

import __main__
import fnmatch
import logging
import os
import shutil
import sys
import time
import warnings
import IPython
from pathlib import Path
from configparser import ConfigParser
from pathlib import Path
from datetime import datetime, time

from rivtlib import parse
from rivtlib import folders

warnings.simplefilter(action="ignore", category=FutureWarning)

# get rivt file path
docP = Path(os.getcwd())
if __name__ == "rivtlib.rivtapi":
    argfileS = Path(__main__.__file__)
    docS = argfileS.name
    print(f"{argfileS=}")
if fnmatch.fnmatch(docS, "riv????-*.py"):
    rivtP = Path(docP, docS)
    print(f"{docS=}")
    print(f"{docP=}")
else:
    print(f"INFO     rivt file is - {docS}")
    print(f"INFO     The name must match 'rivddss-filename.py' where")
    print(f"INFO     dd and ss are two digit integers")
    sys.exit()


def _sections(rS):
    """format section titles and update dictionaries




    :param rS: first line of string
    :type rS: str
    :param apiS: api function
    :type methS: str
    :return: section title
    :rtype: str
    """

    global rivtS, rstS, labelD, folderD

    hdrstS = """"""
    hdreadS = """"""
    hdutfS = """"""""

    rsL = rS.split("|")              # function string as list
    titleS = rsL[0].strip()          #
    labelD["tocS"] = rsL[1].strip()  # set redaction
    labelD["pageI"] = int(rsL[2])    # set background color
    if rS.strip()[0:2] == "--":         # omit section heading
        return "\n", "\n", "\n"

    headS = datetime.now().strftime("%Y-%m-%d | %I:%M%p") + "\n"
    labelD["docS"] = titleS
    bordrS = labelD["widthI"] * "="
    hdutfS = (headS + "\n" + bordrS + "\n" + titleS + "\n" + bordrS + "\n")
    hdmdS = (headS + "\n## " + titleS + "\n")

    snumI = labelD["secnumI"] + 1
    labelD["secnumI"] = snumI
    docnumS = labelD["docnumS"]
    dnumS = docnumS + "-[" + str(snumI) + "]"
    headS = dnumS + " " + titleS
    bordrS = labelD["widthI"] * "-"

    hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
    hdmdS = "### " + headS + "\n"
    hdrstS += (
        ".. raw:: latex"
        + "   \n\n ?x?vspace{.2in} "
        + "   ?x?begin{tcolorbox} "
        + "   ?x?textbf{ " + titleS + "}"
        + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"
        + "   ?x?end{tcolorbox}"
        + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
        + "\n\n")

    print(hdutfS)
    return hdutfS, hdmdS, hdrstS


def _rivt_parse(rS, mS):
    """call parse.RivtParse on API function strings

    :param rS: rivt string
    :type rS: str
    :param mS: rivt string method - R,I,V,T or X
    :type mS: str
    """

    global readS, xreadS, rstS, labelD, folderD, rivtD

    # section headings
    xmdS = xrstS = xutfS = ""
    rL = rS.split("\n")
    hutfS, hmdS, hrstS = _sections(rL[0], mS)
    utfS += hutfS
    mdS += hmdS
    rstS += hrstS

    # rivt string
    parseC = parse.RivtParse(mS, folderD, labelD,  rivtD)
    xutfS, xrstS, labelD, folderD, rivtD = parseC.str_parse(rL[1:])
    utfS += xutfS
    rstS += xrstS


def R(rS):
    """process Run string

        : param rS: repo string
        : type rS: str
    """
    global utfS, rstS, labelD, folderD

    _rivt_parse(rS, "R")


def I(rS):
    """format Insert string

        : param rS: insert string
        : type rS: str
    """
    global utfS, rstS, labelD, folderD

    _rivt_parse(rS, "I")


def V(rS):
    """format Value string

        :param rS: value string
        :type rS: str
    """
    global utfS, rstS, labelD, folderD, rivtD

    locals().update(rivtD)
    _rivt_parse(rS, "V")
    rivtD.update(locals())


def T(rS):
    """process Tools string

        : param rS: tool string
        : type rS: str
    """

    locals().update(rivtD)
    _rivt_parse(rS, "T")
    rivtD.update(locals())


def W(rS):
    """write output files

    :param formatS: comma separated output types: 'utf,md,pdf' 
    :type formatS: str
    """
    pass


def X(rS):
    """skip string - do not format
    """

    rL = rS.split("\n")
    print("\n skip section: " + rL[0] + "\n")
    pass
