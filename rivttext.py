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
    if fnmatch.fnmatch(fileS, "r????.py"):
        docfileS = fileS
        docP = Path(docP / docfileS)
        break
if docfileS == "x":
    print("INFO     rivt doc file not found")
    exit()

# run test files if this module is run as __main__
if Path(docfileS).name == "rv0101t.py":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/01_Division1/rv0101_Overview/rv0101t.py")
if Path(docfileS).name == "-o":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/01_Division1/rv0101_Overview/rv0101t.py")

# print(f"{docfileS=}")
# print(f"{docP=}")

# files and paths
docbaseS = docfileS.split(".py")[0]
dataP = Path(docP.parent / "data")
projP = docP.parent.parent.parent  # rivt project folder path
bakP = docP.parent / ".".join((docbaseS, "bak"))
rivtcalcP = Path("rivt.rivttext.py").parent  # rivt package path
prfxS = docbaseS[1:3]
configP = Path(docP.parent.parent / "rv0000")
for fileS in os.listdir(projP / "resource"):
    if fnmatch.fnmatch(fileS[2:5], prfxS + "-*"):
        refileP = Path(fileS)  # resource folder path
        break
resourceP = Path(projP / "resource" / refileP)
rerootP = Path(projP / "resource")
doctitleS = (docP.parent.name).split("-", 1)[1]
doctitleS = doctitleS.replace("-", " ")
divtitleS = (resourceP.name).split("-", 1)[1]
divtitleS = divtitleS.replace("-", " ")
errlogP = Path(rerootP / "error_log.txt")
siteP = projP / "site"  # site folder path
docpdfS = docbaseS + ".pdf"
dochtmlS = docbaseS + ".html"
reportP = Path(projP / "report" / docpdfS)  # report folder path
siteP = Path(projP / "site" / dochtmlS)  # site folder path

# global dicts and vars
utfS = """\n"""                     # utf output string
rstS = """\n"""                     # reST output string
valS = """"""                       # values string for export
rvtfileS = """"""                   # rivt input file
outputS = "utf"                     # default output type
xflagB = 0
rstoutL = ["pdf", "html", "both"]   # reST formats
outputL = ["utf", "pdf", "html", "both", "report", "site"]

folderD = {}
for item in ["docP", "dataP", "resourceP", "rerootP", "resourceP",
             "reportP", "siteP", "projP", "errlogP", "configP"]:
    folderD[item] = eval(item)

incrD = {
    "docnumS": docbaseS[1:5],  # doc number
    "doctitleS": doctitleS,  # doc title
    "divtitleS": divtitleS,  # section title
    "secnumI": 0,  # section number
    "widthI": 80,  # utf printing width
    "equI": 0,  # equation number
    "tableI": 0,  # table number
    "figI": 0,  # figure number
    "ftqueL": deque([1]),  # footnote number
    "countI": 0,  # footnote counter
    "subB": False,  # substitute values
    "unitS": "M,M",  # units
    "descS": "2,2",  # description or decimal places
    "saveP": "nosave",  # save values to file
    "eqlabelS": "equation",  # last used equation label
    "codeB": False,  # print code strings in doc
    "pageI": 1,  # starting page number
    "headuS": "",
    "footuS": "",
    "headrS": "",
    "footrS": ""\
}

outputD = {"pdf": True, "html": True, "both": True, "site": True,
           "report": True, "inter": False, "utf": False}

localD = {}                         # local rivt dictionary of values

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


def _str_title(hdrS):
    """_summary_

    :param hdrS: _description_
    :type hdrS: _type_
    :return: _description_
    :rtype: _type_
    """

    global outputS

    hdrstS = """"""
    hdutfS = """"""

    snumI = incrD["secnumI"]+1
    incrD["secnumI"] = snumI
    docnumS = "[" + incrD["docnumS"]+"]"
    compnumS = docnumS + " - " + str(snumI)
    widthI = incrD["widthI"] - 3
    headS = " " + hdrS + compnumS.rjust(widthI - len(hdrS))
    bordrS = incrD["widthI"] * "-"
    hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"

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


def _str_set(rS, methS):
    """_summary_

    :param rS: _description_
    :type rS: _type_
    :param methS: _description_
    :type methS: _type_
    :return: _description_
    :rtype: _type_
    """

    global utfS, rstS, outputS, incrD, folderD

    rs1L = rS.split("|")

    if methS == "R":
        incrD["widthI"] = int(rs1L[1])     # utf print width
        incrD["pageI"] = int(rs1L[2])      # initial page number

    elif methS == "V":
        if rs1L[1].strip().casefold() != "save".casefold():
            tempfileS = docbaseS.replace("r", "v") + ".csv"
            incrD["saveP"] = Path(folderD["dataP"], tempfileS)
        else:
            incrD["saveP"] = None
        if rs1L[2].strip().casefold() == "sub".casefold():
            incrD["subB"] = True
        else:
            incrD["subB"] = False

    elif methS == "T":
        if rs1L[1] == "code":
            folderD["codeB"] = True
        else:
            folderD["codeB"] = False

    rs1S = rs1L[0].strip()

    if rs1S.strip()[0:2] == "--":
        return "\n", "\n"                            # skip heading
    else:
        hdutfS, hdrstS = _str_title(rs1L[0].strip())  # get_heading
        return hdutfS, hdrstS


def _report(fileS):
    """_summary_

    :param fileS: _description_
    :type fileS: _type_
    """

    f1 = open(_cfull, "r")
    utfcalcL = f1.readlines()
    f1.close()
    print("INFO calc file read: " + str(_cfull))

    indx = 0  # skip D() in calc list - avoid recursion
    for iS in enumerate(utfcalcL):
        if "rv.D" in iS[1]:
            indx = int(iS[0])
            break
    rstcalcL = utfcalcL = utfcalcL[0:indx] + utfcalcL[indx + 1:]
    cmdS = "".join(utfcalcL)

    exprtfile = Path(_cpathcur / ".".join([_cnameS, "csv"]))
    str1 = """header string\n"""  # write values file
    str1 = str1 + exportS
    with open(exprtfile, "w") as expF:
        expF.write(str1)
    print("INFO  values file written to calc folder", flush=True)

    if doctypeS == "utf8":
        gen_utf8(cmdS, stylefileS, calctitleS)

    pdfD = {
        "cpdfP": Path(_dpath0 / ".".join([_cnameS, "pdf"])),
        "chtml": Path(_dpath0 / ".".join([_cnameS, "html"])),
        "trst": Path(_dpath0 / ".".join([_cnameS, "rst"])),
        "ttex1": Path(_dpath0 / ".".join([_cnameS, "tex"])),
        "auxfile": Path(_dpath0 / ".".join([_cnameS, ".aux"])),
        "outfile": Path(_dpath0 / ".".join([_cnameS, ".out"])),
        "texmak2": Path(_dpath0 / ".".join([_cnameS, ".fls"])),
        "texmak3": Path(_dpath0 / ".".join([_cnameS, ".fdb_latexmk"])),
    }
    os.chdir(_dpath0)
    tmpS = os.getcwd()
    if tmpS == str(_dpath0):
        for f in fileL:
            try:
                os.remove(f)
            except:
                pass
        time.sleep(1)
    print("INFO: temporary Tex files deleted \n", flush=True)
    gen_rst(cmdS, doctypeS, stylefileS, calctitleS, startpageS)

    if stylefileS == "default":
        stylefileS = "pdf_style.sty"
    else:
        stylefileS == stylefileS.strip()
    style_path = Path(_dpath0 / stylefileS)
    print("INFO: style sheet " + str(style_path))
    pythoncallS = "python "
    if sys.platform == "linux":
        pythoncallS = "python3 "
    elif sys.platform == "darwin":
        pythoncallS = "python3 "

    rst2xeP = Path(rivpath / "scripts" / "rst2xetex.py")
    texfileP = pdfD["ttex1"]
    tex1S = "".join(
        [
            pythoncallS,
            str(rst2xeP),
            " --embed-stylesheet ",
            " --documentclass=report ",
            " --documentoptions=12pt,notitle,letterpaper ",
            " --stylesheet=",
            str(style_path) + " ",
            str(_rstfile) + " ",
            str(texfileP),
        ]
    )

    os.chdir(_dpath0)
    os.system(tex1S)
    print("INFO: tex file written " + str(texfileP))

    # fix escape sequences
    fnumS = _setsectD["fnumS"]
    with open(texfileP, "r", encoding="utf-8", errors="ignore") as texin:
        texf = texin.read()
    texf = texf.replace("?x?", """\\""")
    texf = texf.replace(
        """fancyhead[L]{\leftmark}""",
        """fancyhead[L]{\\normalsize  """ + calctitleS + "}",
    )
    texf = texf.replace("x*x*x", fnumS)
    texf = texf.replace("""\\begin{tabular}""", "%% ")
    texf = texf.replace("""\\end{tabular}""", "%% ")
    texf = texf.replace(
        """\\begin{document}""",
        """\\begin{document}\n\\setcounter{page}{""" + startpageS + "}\n",
    )

    # texf = texf.replace(
    #     """\\begin{document}""",
    #     """\\renewcommand{\contentsname}{"""
    #     + self.calctitle
    #     + "}\n"
    #     + """\\begin{document}"""
    #     + "\n"
    #     + """\\makeatletter"""
    #     + """\\renewcommand\@dotsep{10000}"""
    #     + """\\makeatother"""
    #     + """\\tableofcontents"""
    #     + """\\listoftables"""
    #     + """\\listoffigures"""
    # )

    time.sleep(1)
    with open(texfileP, "w", encoding="utf-8") as texout:
        texout.write(texf)
    print("INFO: tex file updated")

    if doctypeS == "pdf":
        gen_pdf(texfileP)

    os._exit(1)

    rstcalcS = """"""
    exec(cmdS, globals(), locals())
    docdir = os.getcwd()
    with open(_rstfile, "wb") as f1:
        f1.write(rstcalcS.encode("UTF-8"))
    print("INFO: rst calc written ", docdir, flush=True)

    f1 = open(_rstfile, "r", encoding="utf-8", errors="ignore")
    rstcalcL = f1.readlines()
    f1.close()
    print("INFO: rst file read: " + str(_rstfile))

    if doctypeS == "tex" or doctypeS == "pdf":
        gen_tex(doctypeS, stylefileS, calctitleS, startpageS)
    elif doctypeS == "html":
        gen_html()
    else:
        print("INFO: doc type not recognized")

    os._exit(1)

    try:
        filen1 = os.path.join(self.rpath, "reportmerge.txt")
        print(filen1)
        file1 = open(filen1, 'r')
        mergelist = file1.readlines()
        file1.close()
        mergelist2 = mergelist[:]
    except OSError:
        print('< reportmerge.txt file not found in reprt folder >')
        return
    calnum1 = self.pdffile[0:5]
    file2 = open(filen1, 'w')
    newstr1 = 'c | ' + self.pdffile + ' | ' + self.calctitle
    for itm1 in mergelist:
        if calnum1 in itm1:
            indx1 = mergelist2.index(itm1)
            mergelist2[indx1] = newstr1
            for j1 in mergelist2:
                file2.write(j1)
            file2.close()
            return
    mergelist2.append("\n" + newstr1)
    for j1 in mergelist2:
        file2.write(j1)
    file2.close()
    return


def _site(fileS):
    pass


def write(formatS):
    """write output files

    :param formatS: output type string, comma separated
    :type formatS: str
    """

    global utfS, rstS, outputS, incrD, folderD

    formatL = formatS.split(",")

    for i in formatL:
        if "utf" in i.strip():
            docP = Path(docP.parent / "README.txt")
            with open(docP, "w") as f2:
                f2.write(utfS)
            print("", flush=True)
            logging.info(f"""utf doc written: {dshortP}\README.txt""")
        if "pdf" in i.strip():
            pdffileS = report(rstS)
            docP = folderD["reportP"]
            with open(docP, "w") as f2:
                f2.write(pdffileS)
            print("", flush=True)
            logging.info(f"""pdf doc written: {docpdfS}""")
        if "site" in i.strip():
            htmlfileS = site(rstS)
            docP = folderD["siteP"]
            with open(docP, "w") as f2:
                f2.write(htmlfileS)
            print("", flush=True)
            logging.info(f"""html doc written: {dochtmlS}""")


def R(rS: str):
    """process Repo string

    :param rS: triple quoted repo string
    :type rS: str
    :return: formatted utf string
    :type: str
    """

    global utfS, rstS, incrD, folderD, localD

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = _str_set(rL[0], "R")
    utfC = parse.RivtParse(folderD, incrD, "R", localD)
    xutfL, xrstL, folderD, incrD, localD = utfC.str_parse(rL[1:])
    if hutfS != None:
        xutfS = xutfL[1] + hutfS + xutfL[0]
        xrstS = xrstL[1] + hrstS + xrstL[0]
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string
    print(utfS)
    xutfS = ""                       # reset local string


def I(rS: str):
    """process Insert string

    :param rS: triple quoted insert string
    :type rS: str
    :return: formatted utf string
    :rtype: str
    """

    global utfS, rstS, incrD, folderD, localD

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = str_set(rL[0], "I")
    print(hutfS)
    utfC = parse.RivtParse(folderD, incrD, "I", localD)
    xutfL, xrstL, folderD, incrD, localD = utfC.str_parse(rL[1:])
    if hutfS != None:
        xutfS = hutfS + xutfL[0]
        xrstS = hrstS + xrstL[0]
    utfS += xutfS
    rstS += xrstS

    xutfS = ""


def V(rS: str):
    """process Value string

    :param rS: triple quoted values string
    :type rS: str
    :return: formatted utf string
    :type: str
    """

    global utfS, rstS, incrD, folderD, localD

    xutfS = """"""
    xrstS = """"""
    rL = rS.split("\n")
    hutfS, hrstS = str_set(rL[0], "V")
    utfC = parse.RivtParse(folderD, incrD, "V", localD)
    xutfL, xrstL, folderD, incrD, localD = utfC.str_parse(rL[1:])
    # print(f"{xutfS=}", f"{rL[1:]=}")
    if hutfS != None:
        xutfS = hutfS + xutfL[0]
        xrstS = hrstS + xrstL[0]
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string

    xutfS = ""


def T(rS: str):
    """process Tables string

    :param rS: triple quoted insert string
    :type rS: str
    :return: formatted utf or reST string
    :type: str

    """
    global utfS, rstS, incrD, folderD, localD

    xutfS = """"""
    rL = rS.split("\n")
    hutfS, hrstS = str_set(rL[0], "T")
    utfC = parse.RivtParse(folderD, incrD, outputS, "T", localD)
    xutfL, rstL, folderD, incrD, localD = utfC.str_parse(rL[1:])
    if hutfS != None:
        xutfS = hutfS + xutfL[0]
        xrstS = hrstS + xrstL[0]
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string

    xutfS = ""


def X(rS: str):
    """skip string processing

    :param rvxS: triple quoted string
    :type rvxS: str
    :return: None
    """

    pass
