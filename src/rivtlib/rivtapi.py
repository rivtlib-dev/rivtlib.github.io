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
from pathlib import Path
from configparser import ConfigParser
from pathlib import Path

from rivtlib import parse
from rivtlib import folders
from rivtlib import write_private
from rivtlib import write_public

warnings.simplefilter(action="ignore", category=FutureWarning)

if __name__ != "__main__":
    argfileS = Path(sys.argv[0]).name
    print(f"{argfileS=}")
rivtpathP = Path(os.getcwd())
if fnmatch.fnmatch(argfileS, "rivt??-*.py"):
    rivtfileS = argfileS
    rivtP = Path(rivtpathP, rivtfileS)
    print(f"{rivtfileS=}")
    print(f"{rivtP=}")
else:
    print("INFO     rivt file not found")
    print("INFO     file name must match 'rivtnn-filename.py'")
    print("INFO     where nn is a two digit integer")
    exit()

# modnameS = __name__.split(".")[1]
# print(f"{modnameS=}")

# relative paths
rivtbaseS = rivtfileS.split(".py")[0]
projP = rivtP.parent.parent                   # rivt project path
bakP = rivtP.parent / ".".join((rivtbaseS, "bak"))
prvP = Path(projP, "private")
prfxS = rivtbaseS[0:6]
# output paths
reportP = Path(prvP, "docs", "report")      # report folder path
tempP = Path(prvP, "temp")
rivtP = Path("rivtapi.py").parent           # rivt package path
pypath = os.path.dirname(sys.executable)
rivtP = os.path.join(pypath, "Lib", "site-packages", "rivt")
errlogP = Path(tempP, "rivt-log.txt")
styleP = prvP
valfileS = rivtbaseS.replace("rivt", "val") + ".csv"

# config file
config = ConfigParser()
config.read(Path(prvP, "rivt.ini"))
reportS = config.get('report', 'title')
headS = config.get('md', 'head')
footS = config.get('md', 'foot')
divS = config.get("divisions", prfxS)

# print(f"{prvP=}")
# global
utfS = """"""                               # utf-8 output string
mdS = """"""                                # github md output string
rstS = """"""                               # reST output string
rvtfileS = """"""                           # rivt input string
declareS = """"""                           # declares output string
assignS = """"""                            # assigns output string
rivtD = {}                                  # rivt dictionary
folderD = {}
for item in ["docP", "dataP", "prvP", "pubP", "docpathP", "reportP",
             "dataP", "valfileS", "errlogP", "styleP", "tempP"]:
    folderD[item] = eval(item)
incrD = {
    "modnameS": modnameS,
    "reportS": reportS,                     # report title
    "docS": "rivt Document",                # document title
    "divS": divS,                           # div title
    "sectS": "",                            # section title
    "docnumS": docbaseS[1:5],               # doc number
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
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogP,
    filemode="w")
dshortP = Path(*Path(docP.parent).parts[-2:])
pubshortP = Path(*Path(pubP).parts[-2:])
prvshortP = Path(*Path(prvP).parts[-2:])

if docP.exists():
    logging.info(f"""rivt file : [{docfileS}]""")
    logging.info(f"""rivt public path : [{pubP}]""")
    print(f"""rivt public short path : [{pubshortP}]""")
else:
    logging.info(f"""rivt file path not found: {docP}""")
if prvP.exists:
    logging.info(f"""private path: [{prvP}]""")
    print(f"""rivt private short path : [{prvshortP}]""")
else:
    logging.info(f"""private path not found: {prvP}""")

logging.info(f"""log folder short path: [{prvshortP}]""")
# write backup doc file
with open(docP, "r") as f2:
    rivtS = f2.read()
    rivtL = f2.readlines()
with open(bakP, "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt backup: [{dshortP}]""")
print(" ")

with open(docP, "r") as f1:
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
