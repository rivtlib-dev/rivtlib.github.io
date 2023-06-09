#! python
'''rivt API

'''
import datetime
import fnmatch
import logging
import os
import shutil
import sys
import time
import warnings
from configparser import ConfigParser
from pathlib import Path

from rivt import parse


warnings.simplefilter(action="ignore", category=FutureWarning)


docfileS = "xx"
docpathP = Path(os.getcwd())
for fileS in os.listdir(docpathP):
    print(fileS)
    if fnmatch.fnmatch(fileS, "r????.py"):
        docfileS = fileS
        docP = Path(docpathP / docfileS)
        print(docP)
        break
if docfileS == "xx":
    print("INFO     rivt file not found")
    exit()

# run test files if this module is run as __main__
if Path(docfileS).name == "rv0101t.py":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/rv0101_Overview/rv0101t.py")
if Path(docfileS).name == "-o":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/rv0101_Overview/rv0101t.py")
modnameS = __name__.split(".")[1]
print(f"{modnameS=}")

print(f"{docfileS=}")
print(f"{docP=}")

# files and paths
docbaseS = docfileS.split(".py")[0]
prfxS = docbaseS[1:3]
dataP = Path(docP.parent / "data")
projP = docP.parent.parent.parent  # rivt project folder path
bakP = docP.parent / ".".join((docbaseS, "bak"))
pubcfgP = Path(docP.parent.parent / "r0000-config")

# config file
config = ConfigParser()
config.read(Path(pubcfgP, "rivt.ini"))
priP = config.get('project', 'resource')
titleS = config.get('report', 'title')
headS = config.get('utf', 'head')
footS = config.get('utf', 'foot')
# print(f"{rvconfigP=}")
# print(f"{rvtlocalP=}")

for fileS in os.listdir(priP):
    if fnmatch.fnmatch(fileS[1:5], prfxS + "-*"):
        refileP = Path(fileS)  # resource folder
        break

resourceP = Path(priP, refileP)
doctitleS = (docP.parent.name).split("-", 1)[1]
doctitleS = titleS + " [ " + doctitleS.replace("-", " ") + " ] "
divtitleS = (refileP.name).split("-", 1)[1]
divtitleS = divtitleS.replace("-", " ")
siteP = Path(priP, "website")  # site folder path
reportP = Path(priP, "report")  # report folder path
retempP = Path(priP, "r00-config")
rivtP = Path("rivtapi.py").parent  # rivt package path
pypath = os.path.dirname(sys.executable)
rivtP = os.path.join(pypath, "Lib", "site-packages", "rivt")
errlogP = Path(retempP, "rivt-log.txt")
styleP = Path   # file name added at runtime
valfileS = docbaseS.replace("r", "v") + ".csv"
saveP = Path(dataP, valfileS)


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
for item in ["docP", "dataP", "resourceP", "rvtlocalP", "resourceP", "projP",
             "reportP", "siteP", "rvconfigP", "retempP",
             "errlogP", "styleP", "saveP"]:
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
    "noteL": [0],  # footnote counter
    "footL": [1],  # foot counter
    "subvB": False,  # substitute values
    "unitS": "M,M",  # units
    "descS": "2,2",  # description or decimal places
    "saveP": "nosave",  # save values to file
    "eqlabelS": "equation",  # last used equation label
    "codeB": False,  # print code strings in doc
    "pageI": 1,  # starting page number
    "titleS": "rivtdoc",
    "headuS": headS,
    "footuS": "",
    "headrS": "",
    "footrS": ""
}

localD = {}                         # local rivt dictionary of values

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogP,
    filemode="w",
)
dshortP = Path(*Path(docP.parent).parts[-2:])
lshortP = Path(*Path(rvtlocalP).parts[-2:])
rshortP = Path(*Path(resourceP).parts[-2:])

print(f"\n-------- start rivt file : [{docfileS}] ---------")

if docP.exists():
    logging.info(f"""start rivt file : [{docfileS}]""")
    logging.info(f"""rivt short path : [{dshortP}]""")
else:
    logging.info(f"""rivt file path not found: {docP}""")
if resourceP.exists:
    logging.info(f"""resource short path: [{rshortP}]""")
else:
    logging.info(f"""resource path not found: {resourceP}""")
logging.info(f"""log folder short path: [{lshortP}]""")


with open(docP, "r") as f2:                 # write backup doc file
    rivtS = f2.read()
    rivtL = f2.readlines()
with open(bakP, "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt backup: [{dshortP}]""")
print(" ")

with open(docP, "r") as f1:
    rvtfileS = f1.read()
    rvtfileS += rvtfileS + """\nsys.exit()\n"""


def _pages(headS, footS):
    """write head or foot format line to dictionary

        :return lineS: header or footer
        :rtype: str
    """

    pageS = str(incrD["pageI"])
    if "<date>" in headS:
        headS = headS.replace("<date>",
                              datetime.date.today().strftime('%Y-%m-%d'))
    if "<datetime>" in headS:
        headS = headS.replace("<datetime>",
                              datetime.date.today().strftime('%Y-%m-%d %H:%M'))
    if "<page>" in headS:
        headS = headS.replace("<page>", pageS)

    headL = headS.split("|")
    # footL = footS.split("|")

    l1I = len(headL[0])
    l2I = len(headL[1])
    l3I = len(headL[2])
    wI = int(incrD["widthI"])
    spS = (int((wI - l1I - l3I - l2I)/2) - 2) * " "
    sepS = wI * "_" + 2*"\n"

    incrD["headuS"] = sepS + headL[0] + spS + \
        headL[1] + spS + headL[2] + "\n" + sepS
    # incrD["footS"] = lineL[0] + spS + lineL[1] + spS + lineL[2] + "\n" + sepS

    print(incrD["headuS"])


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

    snumI = incrD["secnumI"] + 1
    incrD["secnumI"] = snumI
    docnumS = "[" + incrD["docnumS"]+"]"
    dnumS = docnumS + " - " + str(snumI)
    widthI = incrD["widthI"] - 3
    headS = " " + hdrS + dnumS.rjust(widthI - len(hdrS))
    bordrS = incrD["widthI"] * "-"
    hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"

    # if snumI > 1:
    #     hdrstS = (
    #         ".. raw:: latex\n"
    #         + "\n"
    #         + "   \\clearpage \n"
    #         + "   \\pagebreak \n"
    #         + "   \\newpage \n"
    #         + "\n"
    #     )

    hdrstS += (
        ".. raw:: latex"
        + "   \n\n ?x?vspace{.2in} "
        + "   ?x?begin{tcolorbox} "
        + "   ?x?textbf{ " + hdrS + "}"
        + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"
        + "   ?x?end{tcolorbox}"
        + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
        # + "   ?x?vspace{.2in}"
        # + "   ?x?textbf{ "
        # + hdrS
        # + "}"
        # + "   ?x?hfill?x?textbf{SECTION "
        # + compnumS
        # + " }\n"
        # + "   ?x?newline"
        # + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
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
        incrD["pageI"] = int(rs1L[2])      # start page

    elif methS == "V":
        if rs1L[1].strip().casefold() == "sub".casefold():
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
        return "\n", "\n"                             # skip heading
    else:
        hdutfS, hdrstS = _str_title(rs1L[0].strip())  # get_heading
        return hdutfS, hdrstS


def R(rS: str):
    """format Repo string

        : param rS: triple quoted repo string
        : type rS: str
        : return: formatted utf string
        : type: str
    """

    global utfS, rstS, incrD, folderD, localD

    _pages(incrD["headuS"], incrD["footuS"])   # header, footer for utf pages

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = _str_set(rL[0], "R")
    print(hutfS)
    utfC = parse.RivtParse("R", folderD, incrD,  localD)
    xutfL, xrstL, incrD, folderD, localD = utfC.str_parse(rL[1:])
    if hutfS != None:
        xutfS = xutfL[1] + hutfS + xutfL[0]
        xrstS = xrstL[1] + hrstS + xrstL[0]
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string
    xutfS = ""                       # reset local string


def I(rS: str):
    """process Insert string

        : param rS: triple quoted insert string
        : type rS: str
        : return: formatted utf string
        : rtype: str
    """

    global utfS, rstS, incrD, folderD, localD

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = _str_set(rL[0], "I")
    print(hutfS)
    utfC = parse.RivtParse("I", folderD, incrD,  localD)
    xutfL, xrstL, incrD, folderD, localD = utfC.str_parse(rL[1:])
    if hutfS != None:
        xutfS = hutfS + xutfL[0]
        xrstS = hrstS + xrstL[0]
    utfS += xutfS
    rstS += xrstS
    xutfS = ""


def V(rS: str):
    """process Value string

        :param rS: triple quoted values string
        :type rS: str: return
        :formatted utf string: type: str
    """

    global utfS, rstS, incrD, folderD, localD

    locals().update(localD)

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = _str_set(rL[0], "V")
    print(hutfS)
    utfC = parse.RivtParse("V", folderD, incrD, localD)
    xutfL, xrstL, incrD, folderD, localD = utfC.str_parse(rL[1:])
    # print(f"{xutfS=}", f"{rL[1:]=}")
    if hutfS != None:
        xutfS = hutfS + xutfL[0]
        xrstS = hrstS + xrstL[0]
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string
    xutfS = ""

    localD.update(locals())


def T(rS: str):
    """process Tables string

    : param rS: triple quoted insert string
    : type rS: str: return: formatted utf or reST string: type: str

    """
    global utfS, rstS, incrD, folderD, localD

    xutfS = ""
    xrstS = ""
    rL = rS.split("\n")
    hutfS, hrstS = _str_set(rL[0], "T")
    utfC = parse.RivtParse("T", folderD, incrD, localD)
    xutfL, xrstL, incrD, folderD, localD = utfC.str_parse(rL[1:])
    if hutfS != None:
        xutfS = hutfS + xutfL[0]
        xrstS = hrstS + xrstL[0]
    utfS += xutfS                    # accumulate utf string
    rstS += xrstS                    # accumulate reST string

    xutfS = ""


def X(rS: str):
    """skip string - not processed

    """

    pass


def _mod_tex(tfileP):
    """Modify TeX file to avoid problems with escapes:

        -  Replace marker "aaxbb " inserted by rivt with
            \\hfill because it is not handled by reST).
        - Delete inputenc package
        - Modify section title and add table of contents

    """
    startS = str(incrD["pageI"])

    with open(tfileP, "r", encoding="utf-8", errors="ignore") as f2:
        texf = f2.read()

    # modify "at" command
    texf = texf.replace("""\\begin{document}""",
                        """\\renewcommand{\contentsname}{""" + doctitleS
                        + "}\n" +
                        """\\begin{document}\n""" +
                        """\\makeatletter\n""" +
                        """\\renewcommand\@dotsep{10000}""" +
                        """\\makeatother\n""")

    # add table of contents, figures and tables
    # texf = texf.replace("""\\begin{document}""",
    #                     """\\renewcommand{\contentsname}{""" + doctitleS
    #                     + "}\n" +
    #                     """\\begin{document}\n""" +
    #                     """\\makeatletter\n""" +
    #                     """\\renewcommand\@dotsep{10000}""" +
    #                     """\\makeatother\n""" +
    #                     """\\tableofcontents\n""" +
    #                     """\\listoftables\n""" +
    #                     """\\listoffigures\n""")

    texf = texf.replace("""inputenc""", """ """)
    texf = texf.replace("aaxbb ", """\\hfill""")
    texf = texf.replace("?x?", """\\""")
    texf = texf.replace(
        """fancyhead[L]{\leftmark}""",
        """fancyhead[L]{\\normalsize\\bfseries  """ + doctitleS + "}")
    texf = texf.replace("x*x*x", "[" + incrD["docnumS"] + "]")
    texf = texf.replace("""\\begin{tabular}""", "%% ")
    texf = texf.replace("""\\end{tabular}""", "%% ")
    texf = texf.replace(
        """\\begin{document}""",
        """\\begin{document}\n\\setcounter{page}{""" + startS + "}\n")

    with open(tfileP, "w", encoding="utf-8") as f2:
        f2.write(texf)

    # with open(tfileP, 'w') as texout:
    #    print(texf, file=texout)

    return


def _gen_pdf(self):
    """Write PDF file from TEX file

    """

    pdfD = {
        "xpdfP": Path(retempP, docbaseS + ".pdf"),
        "xhtmlP": Path(retempP, docbaseS + ".html"),
        "xrstP": Path(retempP, docbaseS + ".rst"),
        "xtexP": Path(retempP, docbaseS + ".tex"),
        "xauxP": Path(retempP, docbaseS + ".aux"),
        "xoutP": Path(retempP, docbaseS + ".out"),
        "xflsP": Path(retempP, docbaseS + ".fls"),
        "xtexmakP": Path(retempP, docbaseS + ".fdb_latexmk"),
    }
    # os.system('latex --version')
    os.chdir(retempP)
    texfS = str(pdfD["xtexP"])
    # pdf1 = 'latexmk -xelatex -quiet -f ' + texfS + " > latex-log.txt"
    pdf1 = 'xelatex -interaction=batchmode ' + texfS
    # print(f"{pdf1=}"")
    os.system(pdf1)
    srcS = ".".join([docbaseS, "pdf"])
    dstS = str(Path(reportP, srcS))
    shutil.copy(srcS, dstS)

    return dstS


def _rest2tex(rstfileS):
    """convert reST to tex file

    0. insert [i] data into model (see _genxmodel())
    1. read the expanded model
    2. build the operations ordered dictionary
    3. execute the dictionary and write the utf-8 calc and Python file
    4. if the pdf flag is set re-execute xmodel and write the PDF calc
    5. write variable summary to stdout

    :param pdffileS: _description_
    :type pdffileS: _type_
    """

    global folderD

    style_path = folderD["styleP"]
    # print(f"{style_path=}")
    # f2 = open(style_path)
    # f2.close

    pythoncallS = "python "
    if sys.platform == "linux":
        pythoncallS = "python3 "
    elif sys.platform == "darwin":
        pythoncallS = "python3 "

    rst2texP = Path(rivtP, "scripts", "rst2latex.py")
    # print(f"{str(rst2texP)=}")
    texfileP = Path(retempP, docbaseS + ".tex")
    rstfileP = Path(retempP, docbaseS + ".rst")

    with open(rstfileP, "w", encoding='utf-8') as f2:
        f2.write(rstS)

    tex1S = "".join(
        [
            pythoncallS,
            str(rst2texP),
            " --embed-stylesheet ",
            " --documentclass=report ",
            " --documentoptions=12pt,notitle,letterpaper ",
            " --stylesheet=",
            str(style_path) + " ",
            str(rstfileP) + " ",
            str(texfileP),
        ]
    )
    logging.info(f"tex call:{tex1S=}")
    os.chdir(retempP)
    try:
        os.system(tex1S)
        time.sleep(1)
        logging.info(f"tex file written: {texfileP=}")
        print(f"tex file written: {texfileP=}")
    except SystemExit as e:
        logging.exception('tex file not written')
        logging.error(str(e))
        sys.exit("tex file write failed")

    _mod_tex(texfileP)

    pdfS = _gen_pdf(texfileP)

    return pdfS


def writedoc(formatS):
    """write output files

    :param formatS: comma separated output types
    :type formatS: str
    """

    global utfS, rstS, outputS, incrD, folderD

    formatL = [i.strip() for i in formatS.split(",")]
    docutfP = Path(docP.parent / "README.md")
    rstfileP = Path(docP.parent, docbaseS + ".rst")
    eshortP = Path(*Path(rstfileP).parts[-3:])

    logging.info(f"""end rivt file: [{docfileS}]""")
    print(f" -------- end rivt file: [{docfileS}] --------- ")

    print("", flush=True)
    if "utf" in formatL:                          # save utf file
        with open(docutfP, "w", encoding='utf-8') as f1:
            f1.write(utfS)
            # with open(_rstfile, "wb") as f1:
            #   f1.write(rstcalcS.encode("UTF-8"))
            # f1 = open(_rstfile, "r", encoding="utf-8", errors="ignore")
        logging.info(f"""utf doc written: {dshortP}\README.txt""")
        print(f"utf doc written: {dshortP}\README.txt")
    print("", flush=True)
    if "pdf" in formatS or "html" in formatS:      # save rst file
        with open(rstfileP, "w", encoding='utf-8') as f2:
            f2.write(rstS)
        logging.info(f"reST file written: {rstfileP}")
        print(f"reST file written: {rstfileP}")
    for i in formatL:
        if "pdf" not in i:
            continue
        else:
            logging.info(f"start PDF file process: {rstfileP}")
            print("start PDF file process: {rstfileP}")
            pdfstyleS = i.split(":")[1].strip()
            styleP = Path(rvconfigP, pdfstyleS)
            folderD["styleP"] = styleP
            logging.info(f"PDF style file: {styleP}")
            print(f"PDF style file: {styleP}")
        pdffileP = _rest2tex(rstS)
        logging.info(f"PDF doc written: {pdffileP}")
        print(f"PDF doc written: {pdffileP}")
    # if "html" in formatL:
    #     pdffileP = _rest2html(rstS)
    #     logging.info(f"HTML doc written: {pdffileP}")
    sys.exit()


def writereport(fileS):
    """_summary_

    :param fileS: _description_
    :type fileS: _type_
    """

    try:
        filen1 = os.path.join(self.rpath, "reportmerge.txt")
        print(filen1)
        file1 = open(filen1, 'r')
        mergelist = file1.readlines()
        file1.close()
        mergelist2 = mergelist[:]
    except OSError:
        print('< reportmerge.txt file not found in report folder >')
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
