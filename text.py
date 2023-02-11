#! python
'''text

'''

import os
import sys
import logging
import warnings
from pathlib import Path
from collections import deque
import rivt.classes as clsM
import rivt.tags as tagM
import rivt.commands as cmdM
import rivt.write as wrtM

try:
    docfileS = sys.argv[1]
except:
    docfileS = sys.argv[0]
if Path(docfileS).name == "rvtext.py":
    docfileS = "./rivt_test01/text/rv0101_div/r0101_test.py"
elif Path(docfileS).name == "-o":
    docfileS = "./rivt_test01/text/rv0101_div/r0101_test.py"
elif ".py" not in docfileS:
    import __main__
    docfileS = __main__.__file__
    # print(dir(__main__))

# files and paths
docfileP = Path(docfileS)
cwdP = Path(os.getcwd())
docbaseS = docfileP.name  # file basename
docfolderP = Path(os.path.dirname(docfileP))
docP = docfolderP.parent  # calc folder path

rivtprojectP = docfolderP.parent.parent  # rivt project folder path
docbakP = docfolderP / ".".join((docbaseS, "bak"))
descripS = docbaseS.split("_")[1]
docconfigP = docP / "rv0000"  # doc config

resourceS = "r" + str(docbaseS[1:3])
resourceP = rivtprojectP / "resource"  # binary folder path
resourcefolderP = resourceP / resourceS  # a binary source folder
resourceconfigP = resourceP / "r00"  # log and report config folder

siteP = rivtprojectP / "site"  # site folder path
reportP = rivtprojectP / "reports"  # report folder path
rivtcalcP = Path("rivt.rvtext.py").parent  # rivt package path
# initialize strings
utfS = """"""  # utf accumulating string
rstS = """"""  # reST accumulating string
valuexS = """"""  # export values accumulating string
# initialize dicts
rivtvalD = {}  # all persistent computed values
foldersD = {}  # folders
# folder names
for item in ["docfileP", "docconfigP", "binfolderP", "binconfigP", "reportP", "siteP"]:
    foldersD[item] = eval(item)
# tag settings
tagcountD = {
    "divnumS": docbaseS[1:3],  # division number
    "subnumS": docbaseS[3:5],  # subdivision number
    "docnumS": docbaseS[1:5],  # doc number
    "doctitleS": "rivt Document",  # doc title
    "methodtitleS": "rivt section",  # section title
    "secnumI": 0,  # section number
    "secwidthI": 80,  # utf section width
    "equI": 0,  # equation number
    "tableI": 0,  # table number
    "fignumI": 0,  # figure number
    "ftqueL": deque([1]),  # footnote number
    "countI": 0,  # footnote counter
    "decvI": 2,  # decimals for variables
    "decrI": 2,  # decimals for results
    "subsvalsB": False,  # substitute values
    "savevalsB": False  # save values to file
}
# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=resourceconfigP / "error_log.txt",
    filemode="w",
)
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
warnings.filterwarnings("ignore")
dshortP = Path(*Path(docfolderP).parts[-2:])
bshortP = Path(*Path(resourcefolderP).parts[-2:])
lshortP = Path(*Path(resourceconfigP).parts[-2:])
# check that calc and file directories exist
if docfileP.exists():
    logging.info(f"""rivt file path : {docfileP}""")
else:
    logging.info(f"""rivt file path not found: {docfileP}""")

if resourcefolderP.exists:
    logging.info(f"""resource path: {resourcefolderP}""")
else:
    logging.info(f"""resource path not found: {resourcefolderP}""")
logging.info(f"""text folder short path: {dshortP}""")
logging.info(f"""log forlder short path: {lshortP}""")

# backup doc file
with open(docfileP, "r") as f2:
    rivtS = f2.read()
    rivtL = f2.readlines()
with open(docbakP, "w") as f3:
    f3.write(rivtS)
logging.info("""rivt file read and backed up to text folder""")
print(" ")
# set some defaults
restL = ["pdf", "html", "both"]
pubS = "inter"
methodS = "R"


def method_heading(sectS, methodS):
    """method heading settings

    Args:
        hdrS (str): first line of method
    """

    global utfS, rstS, pubS, tagcountD, restL

    if sectS[0:2] == "--":
        utfhS = "\n"
    elif sectS[0:1] == "-":
        headS = sectS[1:]
        utfhS = "\n" + headS + "\n"
    else:
        snumI = tagcountD["secnumI"]+1
        tagcountD["secnumI"] = snumI
        docnumS = "[" + tagcountD["docnumS"]+"]"
        methodS = tagcountD["methodtitleS"]
        compnumS = docnumS + " - " + str(snumI)
        widthI = tagcountD["secwidthI"] - 3
        headS = " " + methodS + compnumS.rjust(widthI - len(methodS))
        bordrS = tagcountD["secwidthI"] * "_"
        utfhS = "\n" + bordrS + "\n\n" + headS + "\n" + bordrS + "\n"
        utfS += utfhS
        print(utfhS)

    if pubS in restL:
        rsthS = (
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
        rstS += rsthS


def R(rvrS: str):
    """process a Repo string and determine output type

    R('''section label | utf;pdf;html;inter | page#

        ||text, ||table, ||project, ||append, ||github 

    ''')

    :param rvrS: triple quoted repo string
    :type rvrS: str
    :return: formatted utf string
    :rtype: str
    """

    global utfS, rstS, valuexS, rivtvalD, foldersD, tagcountD, pubS, restL

    rvr1L = [i.strip() for i in rvrS[0].split("|")]    # first line parameters
    sectS = rvr1L[0].strip()
    pubS = rvr1L[1].strip()
    pageS = rvr1L[2].strip()
    methodS = "R"
    cmdL = cmdM.rvcmds("R")                 # returns list of valid commands
    tagL = tagM.rvtags("R")                 # returns list of valid tags
    rvrL = rvrS.split("\n")                 # list of rivt string lines

    hS = method_heading(sectS, methodS)     # get_heading

    utfC = clsM.RvTextUtf()
    for i in rvrL[1:]:
        rS = utfC.rparseutf(i)
        utfS += rS
    print(utfS)

    if pubS != "inter":
        utfoutP = Path(calcfileP / "README.txt")
        with open(utfoutP, "wb") as f1:
            f1.write(utfS.encode("UTF-8"))
        wrtM.gen_utf(rivtL)
        logging.info("utf calc written, program complete")
        print(utfS)
        print("", flush=True)
        os.exit(1)

    if pubS == "pdf" or pubS == "both":
        rcalc = init(rvS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
        wrtM.gen_rst(rivtL)
        print("exit")
        os.exit(1)

    if pubS == "site" or pubS == "both":
        rcalc = init(rvS)
        rcalcS, setsectD = rcalc.r_rst()
        wrtM.gen_rst(rivtL)
        rstcalcS += rcalcS
        os.exit(1)

    return rS


def I(rviS: str):
    """process an Insert string

    I('''section label | file folder; default

        ||text, ||table, ||image1, ||image2
    ''')

    :param rviS: triple quoted insert string
    :type rviS: str
    :return: formatted utf string
    :rtype: str
    """

    global utfS, rstS, valuexS, rivtvalD, foldersD, tagcountD, pubS, restL

    rvi1L = [i.strip() for i in rviS[0].split("|")]    # first line parameters
    sectS = rvi1L[0].strip()
    methodS = "I"
    cmdL = cmdM.rvcmds("R")                 # returns list of valid commands
    tagL = tagM.rvtags("R")                 # returns list of valid tags
    rviL = rviS.split("\n")                 # list of rivt string lines

    hS = method_heading(sectS, methodS)     # get_heading

    utfC = clsM.RvTextUtf()
    for i in rviL[1:]:
        iS = utfC.iparseutf(i)
        utfS += iS
    print(utfS)

    return iS


def V(rvvS: str):
    """processes a Value string

    V('''section label | file folder; default | sub; nosub | save; nosave

        Value string commands.
        ||text, ||table, ||image1, ||image2, || values, || list, || functions
    ''')

    :param rvvS: triple quoted values string
    :type rvvS: str
    :return: formatted utf string
    :rtype: str
    """

    global utfS, rstS, valuexS, rivtvalD, foldersD, tagcountD, pubS, restL

    rvv1L = [i.strip() for i in rviS[0].split("|")]    # first line parameters
    sectS = rvv1L[0].strip()
    methodS = "V"
    cmdL = cmdM.rvcmds("R")                 # returns list of valid commands
    tagL = tagM.rvtags("R")                 # returns list of valid tags
    rvvL = rvvS.split("\n")                 # list of rivt string lines

    hS = method_heading(sectS, methodS)     # get_heading

    utfC = clsM.RvTextUtf()
    for i in rvvL[1:]:
        vS = utfC.vparseutf(i)
        utfS += vS
    print(utfS)

    return vS


def T(rvtS: str):
    """processes a Tables string

    T('''section label | file folder; default
        Table string commands
        ||text, ||table, ||image1, ||image2,
    ''')

    :param rvtS: triple quoted insert string
    :type rvtS: str
    :return: formatted utf or reST string
    :rtype: str

    """
    global utfS, rstS, rivtvalD, foldersD, tagL, cmdL, typeS, genrstB
    cmdL = cmdM.rvcmds("T")  # returns list of valid commands
    rvL = rvtS.split("\n")  # line list of rivt string
    tC = tM._T2utf()

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += tC.t_utf(cmdL)
        print(utfS)


def X(rvxS: str):
    """processes an Exclude string

    X('''

    An exclude string can be any triple quoted string. It is used for review
    and debugging. To skip a rivt string processing, change the R,I,V,T to X.
    ''')

    :param rvxS: triple quoted string
    :type rvxS: str
    :return: None
    """

    pass
