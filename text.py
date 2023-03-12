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

print(f"sys.argv=")
try:
    docfileS = Path(sys.argv[1]).name
except:
    docfileS = Path(sys.argv[0]).name
if Path(docfileS).name == "r0101t.py":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/01_Division1/rv0101_Overview/r0101t.py")
elif Path(docfileS).name == "-o":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/01_Division1/rv0101_Overview/r0101t.py")
else:
    docP = Path(os.getcwd(), docfileS)

if ".py" not in docfileS:
    import __main__
    docfileS = __main__.__file__
    # print(dir(__main__))


# files and paths
docbaseS = docfileS.split(".py")[0]
dataP = Path(os.getcwd(), "data")
projP = docP.parent.parent.parent.parent  # rivt project folder path
bakP = docP.parent / ".".join((docbaseS, "bak"))
siteP = projP / "site"  # site folder path
reportP = projP / "report"  # report folder path
rivtcalcP = Path("rivt.text.py").parent  # rivt package path
# print(f"{docfileS=}")
# print(f"{docP=}")
# print(f"{projP=}")

prfxS = docbaseS[1:3]
for fileS in os.listdir(projP / "resource"):
    if fnmatch.fnmatch(fileS, prfxS + "_*"):
        resourceP = Path(fileS)  # resource folder path
resourceL = (resourceP, "default")
docpdfP = Path(str(resourceP / docbaseS) + ".pdf")
doctitleS = (docP.parent.name).split("_")[1]
doctitleS = doctitleS.replace("-", " ")
divtitleS = (docP.parent.parent.name).split("_", 1)[1]
divtitleS = divtitleS.replace("-", " ")

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
for item in ["docP", "dataP", "resourceP", "reportP", "siteP", "projP"]:
    folderD[item] = eval(item)

outputD = {"pdf": True, "html": True, "both": True, "site": True,
           "report": True, "inter": False, "utf": False}

incrD = {
    "docnumS": docbaseS[1:5],  # doc number
    "doctitleS": doctitleS,  # doc title
    "divtitleS": divtitleS,  # section title
    "secnumI": 0,  # section number
    "widthI": 80,  # utf printing width
    "equI": 0,  # equation number
    "tableI": 0,  # table number
    "fignumI": 0,  # figure number
    "ftqueL": deque([1]),  # footnote number
    "countI": 0,  # footnote counter
    "deceI": 2,  # equation decimals
    "decrI": 2,  # results decimals
    "subB": False,  # substitute values
    "saveB": False,  # save values to file
    "pdf": (True, "pdf"),  # read file, write reST
    "html": (True, "html"),
    "both": (True, "both"),
    "utf": (True, "utf"),
    "inter": (False, "inter"),
    "pageI": 1  # starting page
}


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=Path(projP / "resource" / "error_log.txt"),
    filemode="w",
)
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
warnings.filterwarnings("ignore")
dshortP = Path(*Path(docP.parent).parts[-2:])
rshortP = Path(*Path(resourceP).parts[-2:])
# check that calc and file directories exist
if docP.exists():
    logging.info(f"""rivt file path : {docP}""")
else:
    logging.info(f"""rivt file path not found: {docP}""")

if resourceP.exists:
    logging.info(f"""resource path: {resourceP}""")
else:
    logging.info(f"""resource path not found: {resourceP}""")
logging.info(f"""text folder short path: {dshortP}""")
logging.info(f"""log folder short path: {rshortP.parent}""")

# write backup doc file
with open(docP, "r") as f2:
    rivtS = f2.read()
    rivtL = f2.readlines()
with open(bakP, "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt file backup written: {rshortP / bakP}""")
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

    if hdrS[0:2] == "--":
        hdS = "\n"
    else:
        hdS = hdrS
        snumI = incrD["secnumI"]+1
        incrD["secnumI"] = snumI
        docnumS = "[" + incrD["docnumS"]+"]"
        compnumS = docnumS + " - " + str(snumI)
        widthI = incrD["widthI"] - 3
        headS = " " + hdS + compnumS.rjust(widthI - len(hdrS))
        bordrS = incrD["widthI"] * "_"
        hdS = "\n" + bordrS + "\n\n" + headS + "\n" + bordrS + "\n"

    if outputD[outputS]:
        hdS = (
            ".. raw:: latex"
            + "\n\n"
            + "   ?x?vspace{.2in}"
            + "   ?x?textbf{"
            + hdS
            + "}"
            + "   ?x?hfill?x?textbf{SECTION "
            + compnumS
            + "}\n"
            + "   ?x?newline"
            + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
            + "\n\n"
        )
    return hdS


def eval_str(rS, methS):
    """_summary_

    :param rS: _description_
    :type rS: _type_
    :param methS: _description_
    :type methS: _type_
    :return: _description_
    :rtype: _type_
    """

    global utfS, rstS, outputS, incrD, folderD

    rvtS = """"""
    rL = rS.split("\n")
    r1L = rL[0].split("|")
    if r1L[1].strip() != "default":                     # resource folder
        folderD[resourceP.parent] = r1L[1]

    if methS == "R":
        incrD["widthI"] = int(r1L[3].split(",")[0])     # utf print width
        incrD["pageI"] = r1L[3].split(",")[1]           # starting page
        if r1L[2].strip() in outputD:
            outputS = r1L[2].strip()
        else:
            outputS = "utf"
    elif methS == "I":
        incrD["widthI"] = int(r1L[3].split(",")[0])     # utf print width
        incrD["pageI"] = r1L[3].split(",")[1]           # starting page
        if r1L[2].strip() in outputD:
            outputS = rL[2].strip()
        else:
            outputS = "utf"
    elif methS == "V":
        incrD["widthI"] = int(r1L[3].split(",")[0])     # utf print width
        incrD["pageI"] = r1L[3].split(",")[1]           # starting page
        if rL[2].strip() in outputD:
            outputS = rL[2].strip()
        else:
            outputS = "utf"
    elif methS == "T":
        incrD["widthI"] = int(r1L[3].split(",")[0])     # utf print width
        incrD["pageI"] = r1L[3].split(",")[1]           # starting page
        if rL[2].strip() in outputD:
            outputS = rL[2].strip()
        else:
            outputS = "utf"
    else:
        pass

    hS = str_head(r1L[0].strip())                       # get_heading
    utfT = parse.RivtParse(folderD, incrD, outputS, methS)
    rS = utfT.str_parse(rL[1:],)
    rvtS = hS + rS[0]
    utfS += rvtS
    rstS += rS[1]

    return rvtS, utfS, rstS


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

        # always write utf file
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

    global utfS, rstS, xflagB, outputS

    rvtS, utfS, rstS = eval_str(rS, "R")

    print(rvtS)


def I(rS: str):
    """process an Insert string

    :param rS: triple quoted insert string
    :type rS: str
    :return: formatted utf string
    :rtype: str
    """

    eval_str(rS, "I")


def V(rS: str):
    """process a Value string

    :param rS: triple quoted values string
    :type rS: str
    :return: formatted utf string
    :type: str
    """

    eval_str(rS, "V")


def T(rS: str):
    """process a Tables string

    :param rS: triple quoted insert string
    :type rS: str
    :return: formatted utf or reST string
    :type: str

    """

    eval_str(rS, "T")


def X(rS: str):
    """skip string processing

    :param rvxS: triple quoted string
    :type rvxS: str
    :return: None
    """

    pass
