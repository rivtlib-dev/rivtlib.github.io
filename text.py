#! python
'''text

'''

import os
import sys
import logging
import warnings
import fnmatch
from pathlib import Path
from collections import deque
import rivt.classes as Cls
import rivt.cmd_utf as Cutf
import rivt.cmd_rst as Crst

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
doctitleS = docbaseS.split("_")[1]
doctitleS = doctitleS.replace("-", " ")
divtitleS = resourceP.split("_", 1)[1]
divtitleS = divtitleS.replace("-", " ")

# globals
folderD = {}  # folders
for item in ["docP", "resourceP", "reportL", "siteP", "projectP"]:
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


def method_heading(hdrS, methodS, overrideB):
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
        docnumS = "[" + tagcountD["docnumS"]+"]"
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

        rgx = r"\[\d\d\]"
        nameSS = hdrS
        snumSS = ""
        cnumSS = ""
        widthI = int(_setsectD["swidthI"])
        headS = hdrS
        if re.search(rgx, hdrS):
            nameSS = _setsectD["snameS"] = hdrS[hdrS.find("]") + 2:].strip()
            snumSS = _setsectD["snumS"] = hdrS[hdrS.find(
                "[") + 1: hdrS.find("]")]
            cnumSS = str(_sectD["cnumS"])
            widthI = int(_setsectD["swidthI"])
            if _rstB:
                # draw horizontal line
                headS = (
                    ".. raw:: latex"
                    + "\n\n"
                    + "   ?x?vspace{.2in}"
                    + "   ?x?textbf{"
                    + nameSS
                    + "}"
                    + "   ?x?hfill?x?textbf{SECTION "
                    + snumSS
                    + "}\n"
                    + "   ?x?newline"
                    + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
                    + "\n\n"
                )
                uS = headS
            else:
                headS = (
                    " "
                    + nameSS
                    + (cnumSS + " " + ("[" + snumSS + "]")).rjust(
                        widthI - len(nameSS) - 1
                    )
                )
                bordrS = widthI * "_"
                uS = headS + "\n" + bordrS + "\n"

    return hdS


# set some defaults
outputS = (False, "inter")


def R(rS: str):
    """process a Repo string and evaluate output type

    R('''section label | utf;pdf;html;inter | page#

        ||text, ||table, ||project, ||append, ||github

    ''')

    :param rvrS: triple quoted repo string
    :type rvrS: str
    :return: formatted utf string
    :rtype: str
    """

    global outputS, rvtfileS, rvtS, utfS, rstS, valS, localD, folderD, incrD

    methodS = "R"
    outputL = ["pdf", "html", "inter", "utf", "both", "site", "report"]

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

    utfC = Cls.RvTextUtf()                              # section to print utf
    rvtS += method_heading(r1L, methodS, True)          # get_heading
    for i in rL[1:]:
        rS = utfC.r_utf(rL)
        utfS += rS
    print(rvtS)

    if outputS[0]:                                      # file to utf (readme)
        utfoutP = Path(docP.parent / "README.txt")
        with open(utfoutP, "wb") as f1:
            f1.write(utfS.encode("UTF-8"))
        Wrt.gen_utf(rivtL)
        logging.info("utf calc written, program complete")
        print(utfS)
        print("", flush=True)
        os.exit(1)

    if pubS == "pdf" or pubS == "both":                 # file to reST
        rcalc = init(rvS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
        Wrt.gen_rst(rivtL)
        print("exit")
        os.exit(1)

    if pubS == "pdf" or pubS == "both":                 # file to pdf
        rcalc = init(rvS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
        Wrt.gen_rst(rivtL)
        print("exit")

    if pubS == "pdf" or pubS == "both":                 # file to html
        rcalc = init(rvS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
        Wrt.gen_rst(rivtL)
        print("exit")

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
