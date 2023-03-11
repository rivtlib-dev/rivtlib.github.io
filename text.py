#! python
'''text

'''

import os
import sys
import re
import logging
import warnings
import fnmatch
from pathlib import Path
from collections import deque
import rivt.parse as par
import rivt.cmd_utf as cutf
import rivt.cmd_rst as crst

print(f"sys.argv=")
try:
    docfileS = sys.argv[1]
except:
    docfileS = sys.argv[0]
if Path(docfileS).name == "r0101t.py":
    docP = Path("./tests/rivt_test01/text/rv0101_test01/r0101t.py")
elif Path(docfileS).name == "-o":
    docP = Path("./tests/rivt_test01/text/rv0101_test01/r0101t.py")
elif ".py" not in docfileS:
    import __main__
    docfileS = __main__.__file__
    # print(dir(__main__))

# files and paths
docbaseS = docfileS.split(".py")[0]
docP = Path(os.getcwd(), docfileS)
dataP = Path(os.getcwd(), "data")
projectP = docP.parent.parent.parent  # rivt project folder path
bakP = docP.parent / ".".join((docbaseS, "bak"))
siteP = projectP / "site"  # site folder path
reportP = projectP / "report"  # report folder path
rivtcalcP = Path("rivt.text.py").parent  # rivt package path

prfxS = docbaseS[0:3]
for fileS in os.listdir(projectP / "resource"):
    if fnmatch.fnmatch(fileS, prfxS + "_*"):
        resourceP = Path(fileS)  # resource folder path
resourceL = (resourceP, "default")
docpdfP = resourceP / docbaseS + ".pdf"
doctitleS = docbaseS.split("_")[1]
doctitleS = doctitleS.replace("-", " ")
divtitleS = resourceP.split("_", 1)[1]
divtitleS = divtitleS.replace("-", " ")

# global dicts and vars
folderD = {}
for item in ["docP", "dataP", "resourceP", "reportL", "siteP", "projectP"]:
    folderD[item] = eval(item)

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
    "inter": (False, "inter")
}
rvtS = """"""  # rivtText method string
rvtfileS = """"""  # full rivt file input
utfS = """"""  # utf output string
rstS = """"""  # reST output string
valS = """"""  # values string for export
localD = {}  # local dictionary

# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=resourceP.parent / "error_log.txt",
    filemode="w",
)
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
warnings.filterwarnings("ignore")
dshortP = Path(*Path(docP).parts[-2:])
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

# set defaults
outputS = (False, "inter")
outputL = ["pdf", "html", "inter", "utf", "both", "site", "report"]


def str_head(hdrS, methodS, overrideB):
    """set method heading

    Args:
        :param hdrS: first line of method
        :type hdrS: str
    """

    global outputS, rvtfileS, rvtS, utfS, rstS, valS, localD, folderD, incrD

    if hdrS[0:2] == "--":
        utfhS = "\n"
    elif hdrS[0:1] == "-":
        headS = hdrS[1:]
        utfhS = "\n" + headS + "\n"
    else:
        snumI = incrD["secnumI"]+1
        incrD["secnumI"] = snumI
        docnumS = "[" + incrD["docnumS"]+"]"
        methodS = incrD["methodtitleS"]
        compnumS = docnumS + " - " + str(snumI)
        widthI = incrD["secwidthI"] - 3
        headS = " " + methodS + compnumS.rjust(widthI - len(methodS))
        bordrS = incrD["secwidthI"] * "_"
        hdS = "\n" + bordrS + "\n\n" + headS + "\n" + bordrS + "\n"

    if not overrideB:
        if outputS[0]:
            hdS = (
                ".. raw:: latex"
                + "\n\n"
                + "   ?x?vspace{.2in}"
                + "   ?x?textbf{"
                + methodS
                + "}"
                + "   ?x?hfill?x?textbf{SECTION "
                + compnumS
                + "}\n"
                + "   ?x?newline"
                + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
                + "\n\n"
            )

    return hdS


def eval_str(rS, funcS):

    global outputS, rvtfileS, rvtS, utfS, rstS, valS, localD, folderD, incrD

    rL = rS.split()
    r1L = [i.strip() for i in rL[0].split("|")]         # first line parameters

    if r1L[1] != "default":                             # resource folders
        folderD[resourceL][1] = r1L[1]
    if incrD[r1L[2]] in outputL:
        outputS = incrD[r1L[2]]
    else:
        outputS = (False, "utf")

    incrD["widthI"] = int(r1L[3].split(",")[0])         # utf print width
    pageS = r1L[3].split(",")[1]                        # starting page

    rvtS += str_head(r1L, funcS, True)                 # get_heading
    utfM = par.RivtParse(rL[1:], folderD, incrD, outputS, funcS)
    rS = utfM.str_parse()
    rvtS += rS
    print(rvtS)


def R(rS: str):
    """process a Repo string and set output type

    :param rS: triple quoted repo string
    :type rS: str
    :return: formatted utf string
    :type: str
    """

    global outputS, rvtfileS, rvtS, utfS, rstS, valS, localD, folderD, incrD

    eval_str(rS, "R")                               # evaluate rivt string

    if outputS("utf"):                              # write utf file (readme)
        docutfP = Path(docP.parent / "README.txt")
        with open(docP, "r") as f2:
            rivtL = f2.readlines()
            rivtS = rivtL[1:].join()
            exec(rivtS)
        logging.info("utf calc written, program complete")
        os.exit(1)

    if outputS == "pdf" or outputS == "HTML" or outputS == "both":  # reST file
        with open(docP, "r") as f2:
            rivtL = f2.readlines()
            rivtS = rivtL[1:].join()
            exec(rivtS)
        logging.info(outputS, " utf calc written")
        print("", flush=True)


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
