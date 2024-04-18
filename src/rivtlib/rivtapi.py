#! python
'''rivt API

'''
from datetime import datetime, time
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
import __main__

from rivtlib import parse
from rivtlib import folders
from rivtlib import write_private
from rivtlib import write_public

warnings.simplefilter(action="ignore", category=FutureWarning)

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
    print(f"INFO     rivt file name is - {docS}")
    print(f"INFO     The file name must match 'rivddss-filename.py' where")
    print(f"INFO     dd and ss are two digit integers")
    sys.exit()

# files and paths
baseS = docS.split(".py")[0]
titleS = baseS.split("-")[1]
projP = docP
bakP = docP / ".".join((baseS, "bak"))
prfxS = baseS[0:7]
dataP = Path(projP, "data")
toolsP = Path(projP, "tools")

# output paths
reportP = Path(projP, "reports")
xrivtP = Path(projP, "xrivt")
tempP = Path(projP, "temp")
pypath = os.path.dirname(sys.executable)  # rivt package path
rivtpkgP = os.path.join(pypath, "Lib", "site-packages", "rivt")
errlogP = Path(tempP, "rivt-log.txt")
styleP = Path(projP, "reports", "pdf")
valfileS = baseS.replace("riv", "val") + ".csv"
readmeP = Path(projP, "README.txt")

# config file
config = ConfigParser()
config.read(Path(projP, "config.ini"))
headS = config.get('format', 'header')
footS = config.get('format', 'footer')

# global dictionaries and strings
rivtS = """"""                           # rivt input string
utfS = """"""                               # utf-8 output string
rmeS = """"""                               # readme output string
rstS = """"""                               # reST output string
declareS = """"""                           # declares output string
assignS = """"""                            # assigns output string
rivtD = {}                                  # rivt object dictionary
folderD = {}                                # folder dictionary
for item in ["rivtP", "dataP", "readmeP", "reportP",
             "dataP", "valfileS", "errlogP", "styleP", "tempP"]:
    folderD[item] = eval(item)
incrD = {
    "titleS": titleS,                           # document title
    "docnumS": prfxS,                       # doc number
    "sectS": "",                            # section title
    "secnumI": 0,                           # section number
    "widthI": 80,                           # print width
    "equI": 1,                              # equation number
    "tableI": 1,                            # table number
    "figI": 1,                              # figure number
    "pageI": 1,                             # starting page number
    "noteL": [0],                           # footnote counter
    "footL": [1],                           # foot counter
    "unitS": "M,M",                         # units
    "descS": "2",                           # description or decimal places
    "headrS": "",                           # header string
    "footrS": "",                           # footer string
    "tocB": False,                          # table of contents
    "docstrB": False,                       # print doc strings
    "subB": False                           # sub values in equations
}


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + baseS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogP,
    filemode="w")
pubshortP = Path(*Path(docP).parts[-2:])
bshortP = Path(*Path(bakP).parts[-2:])


if docP.exists():
    logging.info(f"""rivt file : [{docS}]""")
    logging.info(f"""rivt path : [{docP}]""")
    print(f"""rivt short path : [{pubshortP}]""")
else:
    logging.info(f"""rivt file path not found: {docP}""")

# write backup doc file
with open(rivtP, "r") as f2:
    rivtS = f2.read()
    rivtL = f2.readlines()
with open(bakP, "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt backup: [{bshortP}]""")
print(" ")

with open(rivtP, "r") as f1:
    rvtfileS = f1.read()
    rvtfileS += rvtfileS + """\nsys.exit()\n"""


def _str_set(rS, methS):
    """format section title and update dictionaries

    :param rS: first line of string
    :type rS: str
    :param methS: rivt method
    :type methS: str
    :return: section title
    :rtype: str
    """

    global mdS, rstS, incrD, folderD

    hdrstS = """"""
    hdmdS = """"""
    hdutfS = """"""""

    rsL = rS.split("|")
    titleS = rsL[0].strip()
    if methS == "R":
        incrD["tocS"] = rsL[1].strip()
        incrD["pageI"] = int(rsL[2])
        incrD["doctitleS"] = titleS
    elif methS == "I":
        if rsL[1].strip() == "default":
            incrD["subB"] = True
        else:
            incrD["subB"] = False
    elif methS == "V":
        if rsL[1].strip() == "sub":
            incrD["subB"] = True
        else:
            incrD["subB"] = False
    elif methS == "T":
        if rsL[1].strip() == "code":
            folderD["codeB"] = True
        else:
            folderD["codeB"] = False
    else:
        pass

    if rS.strip()[0:2] == "--":              # omit section heading
        return "\n", "\n", "\n"
    elif methS == "R":
        headS = datetime.now().strftime("%Y-%m-%d | %I:%M%p") + "\n"
        incrD["docS"] = titleS
        bordrS = incrD["widthI"] * "="
        hdutfS = (headS + "\n" + bordrS + "\n" + titleS + "\n" + bordrS + "\n")
        hdmdS = (headS + "\n## " + titleS + "\n")
        hdrstS = (
            ".. raw:: latex"
            + "   \n\n ?x?vspace{.2in} "
            + "   ?x?begin{tcolorbox} "
            + "   ?x?textbf{ " + titleS + "}"
            + "   ?x?end{tcolorbox}"
            + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
            + "\n\n")
    else:
        snumI = incrD["secnumI"] + 1
        incrD["secnumI"] = snumI
        docnumS = incrD["docnumS"]
        dnumS = docnumS + "-[" + str(snumI) + "]"
        headS = dnumS + " " + titleS
        bordrS = incrD["widthI"] * "-"

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
    """call rivt parsing classes

    :param rS: rivt string
    :type rS: str
    :param mS: rivt string method - R,I,V,T or X
    :type mS: str
    """

    global utfS, mdS, rstS, incrD, folderD, rivtD

    # section headings
    xmdS = xrstS = xutfS = ""
    rL = rS.split("\n")
    hutfS, hmdS, hrstS = _str_set(rL[0], mS)
    utfS += hutfS
    mdS += hmdS
    rstS += hrstS

    # rivt string
    parseC = parse.RivtParse(mS, folderD, incrD,  rivtD)
    xutfS, xmdS, xrstS, incrD, folderD, rivtD = parseC.str_parse(rL[1:])
    utfS += xutfS
    mdS += xmdS
    rstS += xrstS


def R(rS):
    """format Repo string

        : param rS: repo string
        : type rS: str
    """
    global utfS, mdS, rstS, incrD, folderD

    _rivt_parse(rS, "R")


def I(rS):
    """format Insert string

        : param rS: insert string
        : type rS: str
    """
    global utfS, mdS, rstS, incrD, folderD

    _rivt_parse(rS, "I")


def V(rS):
    """format Value string

        :param rS: value string
        :type rS: str
    """
    global utfS, mdS, rstS, incrD, folderD, rivtD

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


def X(rS):
    """skip string - do not format
    """

    rL = rS.split("\n")
    print("\n skip section: " + rL[0] + "\n")
    pass


def writedocs(formatS):
    """write output files

    :param formatS: comma separated output types: 'utf,md,pdf' 
    :type formatS: str
    """

    global mdS, rstS, utfS, incrD, folderD

    print(f" -------- write doc files: [{docfileS}] --------- ")
    logging.info(f"""write doc files: [{docfileS}]""")

    formatL = formatS.split(",")
    docmdS = "README.md"
    docmdP = Path(docP.parent / docmdS)
    docutfP = Path(docP.parent / docutfS)
    rstfileP = Path(docP.parent, docbaseS + ".rst")
    # eshortP = Path(*Path(rstfileP).parts[-3:])

    print("", flush=True)

    if "md" in formatL:                          # save md file
        with open(docmdP, "w", encoding='utf-8') as f1:
            f1.write(mdS)
            # with open(_rstfile, "wb") as f1:
            #   f1.write(rstcalcS.encode("md-8"))
            # f1 = open(_rstfile, "r", encoding="md-8", errors="ignore")
        print(f"markdown written: {dshortP}\README.md")
        logging.info(f"""markdown written: {dshortP}\README.md""")
    print("", flush=True)

    if "utf" in formatL:                          # save utf file
        with open(docmdP, "w", encoding='utf-8') as f1:
            f1.write(mdS)
            # with open(_rstfile, "wb") as f1:
            #   f1.write(rstcalcS.encode("md-8"))
            # f1 = open(_rstfile, "r", encoding="md-8", errors="ignore")
        print(f"markdown written: {dshortP}\README.md")
        logging.info(f"""markdown written: {dshortP}\README.md""")
    print("", flush=True)

    if "pdf" in formatL:                           # save pdf file
        with open(rstfileP, "w", encoding='md-8') as f2:
            f2.write(rstS)
        logging.info(f"reST written: {rstfileP}")
        print(f"reST written: {rstfileP}")
        logging.info(f"start PDF file process: {rstfileP}")
        print("start PDF file process: {rstfileP}")
        pdfstyleS = i.split(":")[1].strip()
        styleP = Path(prvP, pdfstyleS)
        folderD["styleP"] = styleP
        logging.info(f"PDF style file: {styleP}")
        print(f"PDF style file: {styleP}")
        pdffileP = _rest2tex(rstS)
        logging.info(f"PDF doc written: {pdffileP}")
        print(f"PDF doc written: {pdffileP}")
    sys.exit()
