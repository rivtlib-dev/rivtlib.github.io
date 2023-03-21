#! python
'''text

'''

import os
import sys
import re
import time
import logging
import warnings
import fnmatch
from pathlib import Path
from collections import deque
from rivt import parse

docfileS = "x"
docpathP = os.getcwd()
docP = Path(docpathP)
for fileS in os.listdir(docpathP):
    if fnmatch.fnmatch(fileS, "rv????.py"):
        docfileS = fileS
        docP = Path(docP / docfileS)
        break
if docfileS == "x":
    print("INFO     rivt doc file not found")
    exit()

# run test files if this module is run directly
if Path(docfileS).name == "rv0101t.py":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/01_Division1/rv0101_Overview/r0101t.py")
if Path(docfileS).name == "-o":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/01_Division1/rv0101_Overview/r0101t.py")

# print(f"{docfileS=}")
# print(f"{docP=}")

# files and paths
docbaseS = docfileS.split(".py")[0]
dataP = Path(docP.parent / "data")
projP = docP.parent.parent.parent.parent  # rivt project folder path
bakP = docP.parent / ".".join((docbaseS, "bak"))
siteP = projP / "site"  # site folder path
reportP = projP / "report"  # report folder path
rivtcalcP = Path("rivt.rivttext.py").parent  # rivt package path
# print(f"{projP=}")
prfxS = docbaseS[2:4]
for fileS in os.listdir(projP / "resource"):
    if fnmatch.fnmatch(fileS[2:5], prfxS + "_*"):
        refileP = Path(fileS)  # resource folder path
        break
resourceP = Path(projP / "resource" / refileP)
rerootP = Path(projP / "resource")
docpdfP = Path(rerootP / resourceP / (docbaseS + ".pdf"))
doctitleS = (docP.parent.name).split("_")[1]
doctitleS = doctitleS.replace("-", " ")
divtitleS = (docP.parent.parent.name).split("_", 1)[1]
divtitleS = divtitleS.replace("-", " ")
errlogP = Path(rerootP / "error_log.txt")

# global dicts and vars

utfS = """\n"""             # utf output string
rstS = """"""               # reST output string
valS = """"""               # values string for export
rvtfileS = """"""           # rivt file
outputS = "utf"             # default output type
xflagB = 0
rstoutL = ["pdf", "html", "both"]  # reST formats
outputL = ["utf", "pdf", "html", "both", "report", "site"]

localD = {}                 # local rivt dictionary of values

folderD = {}
for item in ["docP", "dataP", "resourceP", "rerootP", "resourceP",
             "reportP", "siteP", "projP", "errlogP"]:
    folderD[item] = eval(item)

outputD = {"pdf": True, "html": True, "both": True, "site": True,
           "report": True, "inter": False, "utf": False}

incrD = {
    "docnumS": docbaseS[2:6],  # doc number
    "doctitleS": doctitleS,  # doc title
    "divtitleS": divtitleS,  # section title
    "secnumI": 0,  # section number
    "widthI": 80,  # utf printing width
    "equI": 0,  # equation number
    "tableI": 0,  # table number
    "figI": 0,  # figure number
    "ftqueL": deque([1]),  # footnote number
    "countI": 0,  # footnote counter
    "deceI": 2,  # equation decimals
    "decrI": 2,  # results decimals
    "subB": False,  # substitute values
    "saveP": "file",  # save values to file
    "codeB": False,  # insert code strings in doc
    "pdf": (True, "pdf"),  # write reST
    "html": (True, "html"),  # write reST
    "both": (True, "both"),  # write reST
    "utf": (False, "utf"),
    "inter": (False, "inter"),
    "pageI": 1  # starting page number
}

print("\nFile Paths")
print("---------- \n")
# logging
modnameS = __name__.split(".")[1]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogP,
    filemode="w",
)
# print(f"{modnameS=}")
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s" + modnameS + "   %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
warnings.filterwarnings("ignore")

dshortP = Path(*Path(docP.parent).parts[-2:])
lshortP = Path(*rerootP.parts[-2:])
rshortP = Path(*Path(resourceP).parts[-2:])
# check that calc and file directories exist
if docP.exists():
    logging.info(f"""rivt file : [{docfileS}]""")
    logging.info(f"""rivt short path : [{dshortP}]""")
else:
    logging.info(f"""rivt file path not found: {docP}""")

if resourceP.exists:
    logging.info(f"""resource short path: [{rshortP}]""")
else:
    logging.info(f"""resource path not found: {resourceP}""")
logging.info(f"""log folder short path: [{lshortP}]""")

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


def str_head(hdrS):
    """_summary_

    :param hdrS: _description_
    :type hdrS: _type_
    :return: _description_
    :rtype: _type_
    """

    global outputS

    hdrstS = """"""
    hdutfS = """"""

    if hdrS[0:2] == "--":
        return None, None

    snumI = incrD["secnumI"]+1
    incrD["secnumI"] = snumI
    docnumS = "[" + incrD["docnumS"]+"]"
    compnumS = docnumS + " - " + str(snumI)
    widthI = incrD["widthI"] - 3
    headS = " " + hdrS + compnumS.rjust(widthI - len(hdrS))
    bordrS = incrD["widthI"] * "_"
    hdutfS = bordrS + "\n\n" + headS + "\n" + bordrS + "\n"

    if outputD[outputS]:
        hdrstS = (
            ".. raw:: latex"
            + "\n\n"
            + "   ?x?vspace{.2in}"
            + "   ?x?textbf{"
            + hdrS
            + "}"
            + "   ?x?hfill?x?textbf{SECTION "
            + compnumS
            + "}\n"
            + "   ?x?newline"
            + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
            + "\n\n"
        )

    return hdutfS, hdrstS


def eval_head(rS, methS):
    """_summary_

    :param rS: _description_
    :type rS: _type_
    :param methS: _description_
    :type methS: _type_
    :return: _description_
    :rtype: _type_
    """

    global utfS, rstS, outputS, incrD, folderD

    r1L = rS.split("|")

    if methS == "R":

        if r1L[1].strip() in outputD:
            outputS = r1L[1].strip()
        else:
            outputS = "utf"

        incrD["widthI"] = int(r1L[2].split(",")[0])     # utf print width
        incrD["pageI"] = r1L[2].split(",")[1]           # starting page

    elif methS == "I":
        pass

    elif methS == "V":

        folderD["saveP"] = Path(r1L[2].strip() + ".csv")

        if r1L[1] == "data":
            folderD["data"] = dataP
        else:
            folderD["dataP"] = dataP

        if r1L[3] == "sub":
            incrD["subB"] = True
        else:
            incrD["subB"] = False

    elif methS == "T":
        if r1L[1] == "code":
            folderD["codeB"] = True
        else:
            folderD["codeB"] = False

    hdutfS, hdrstS = str_head(r1L[0].strip())   # get_heading

    return hdutfS, hdrstS


def Write():
    """_summary_
    """

    if outputS in outputL:
        if outputS == "html":
            exec(rvtfileS)
        elif outputS == "pdf":
            with open(docP, "r") as f2:
                rvtfileS = f2.read()
            logging.info(f"""write docs: """)
            print("", flush=True)

        # always write utf file if not 'inter'
        if outputS != "inter":
            docutfP = Path(docP.parent / "README.txt")
            with open(docutfP, "w") as f2:
                f2.write(utfS)
            logging.info(f"""write docs: {dshortP}\README.txt""")


def R(rS: str):
    """process a Repo string

    :param rS: triple quoted repo string
    :type rS: str
    :return: formatted utf string
    :type: str
    """

    global utfS, rstS, outputS, incrD, folderD

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = eval_head(rL[0], "R")
    utfT = parse.RivtParse(folderD, incrD, outputS, "R")
    xutfS, xrstS, folderD, incrD = utfT.str_parse(rL[1:])
    if hutfS != None:
        xutfS = hutfS + xutfS
        if outputD[outputS]:
            xrstS = hrstS + xrstS
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string

    print(xutfS)
    xutfS = ""                       # reset local string


def I(rS: str):
    """process an Insert string

    :param rS: triple quoted insert string
    :type rS: str
    :return: formatted utf string
    :rtype: str
    """

    global utfS, rstS, outputS, incrD, folderD

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = eval_head(rL[0], "I")
    utfT = parse.RivtParse(folderD, incrD, outputS, "I")
    xutfS, xrstS, folderD, incrD = utfT.str_parse(rL[1:])
    if hutfS != None:
        xutfS = hutfS + xutfS
        if outputD[outputS]:
            xrstS = hrstS + xrstS
    utfS += xutfS
    rstS += xrstS

    print(xutfS)
    xutfS = ""


def V(rS: str):
    """process a Value string

    :param rS: triple quoted values string
    :type rS: str
    :return: formatted utf string
    :type: str
    """

    global utfS, rstS, xflagB, outputS, incrD, folderD

    xutfS = """"""
    xrstS = """"""
    rL = rS.split("\n")
    hutfS, hrstS = eval_head(rL[0], "V")
    utfT = parse.RivtParse(folderD, incrD, outputS, "V")
    xutfS, xrstS, folderD, incrD = utfT.str_parse(rL[1:])
    #print(f"{xutfS=}", f"{rL[1:]=}")
    if hutfS != None:
        xutfS = hutfS + xutfS
        if outputD[outputS]:
            xrstS = hrstS + xrstS
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string

    print(xutfS)


def T(rS: str):
    """process a Tables string

    :param rS: triple quoted insert string
    :type rS: str
    :return: formatted utf or reST string
    :type: str

    """
    global utfS, rstS, xflagB, outputS, incrD, folderD

    xutfS = """"""
    rL = rS.split("\n")
    hutfS, hrstS = eval_head(rL[0], "T")
    utfT = parse.RivtParse(folderD, incrD, outputS, "T")
    xutfS, rstS, folderD, incrD = utfT.str_parse(rL[1:])
    if hutfS != None:
        utfS += hutfS + utfS
        xutfS += hutfS + xutfS                 # accumulate utf string
        if outputD[outputS]:
            rstS += hrstS + rstS               # accumulate reST string

    print(xutfS)


def X(rS: str):
    """skip string processing

    :param rvxS: triple quoted string
    :type rvxS: str
    :return: None
    """

    pass
