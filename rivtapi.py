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
from configparser import ConfigParser
from pathlib import Path

from rivt import parse


warnings.simplefilter(action="ignore", category=FutureWarning)


docfileS = "xx"
docpathP = Path(os.getcwd())
for fileS in os.listdir(docpathP):
    # print(fileS)
    if fnmatch.fnmatch(fileS, "r????.py"):
        docfileS = fileS
        docP = Path(docpathP, docfileS)
        # print(docP)
        break
if docfileS == "xx":
    print("INFO     rivt file not found")
    exit()

# run test files if api is run as __main__
if Path(docfileS).name == "rv0101t.py":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/rv0101_Overview/rv0101t.py")
if Path(docfileS).name == "-o":
    docP = Path(
        "./tests/rivt_Example_Test_01/text/rv0101_Overview/rv0101t.py")
modnameS = __name__.split(".")[1]
# print(f"{modnameS=}")
# print(f"{docfileS=}")
# print(f"{docP=}")
# paths relative to file

docbaseS = docfileS.split(".py")[0]
pubP = docP.parent.parent               # rivt public folder path
bakP = docP.parent / ".".join((docbaseS, "bak"))
prvP = Path(pubP.parent, "private")
prfxS = docbaseS[0:3]
# config file
config = ConfigParser()
config.read(Path(prvP, "rivt.ini"))
reportS = config.get('report', 'title')
headS = config.get('md', 'head')
footS = config.get('md', 'foot')
divS = config.get("divisions", prfxS)
# output paths
reportP = Path(prvP, "docs", "report")      # report folder path
tempP = Path(prvP, "temp")
rivtP = Path("rivtapi.py").parent           # rivt package path
pypath = os.path.dirname(sys.executable)
rivtP = os.path.join(pypath, "Lib", "site-packages", "rivt")
errlogP = Path(tempP, "rivt-log.txt")
styleP = prvP
valfileS = docbaseS.replace("r", "v") + ".csv"
dataP = Path(docP.parent, "data")
# print(f"{prvP=}")

# global
utfS = """"""                         # utf-8 output string
mdS = """"""                          # github md output string
rstS = """"""                         # reST output string
rvtfileS = """"""                     # rivt input string
declareS = """"""                     # declares output string
assignS = """"""                      # assigns output string
rivtD = {}                            # rivt dictionary
folderD = {}
for item in ["docP", "dataP", "prvP", "pubP", "docpathP",
             "reportP", "dataP", "errlogP", "styleP", "tempP"]:
    folderD[item] = eval(item)
incrD = {
    "reportS": reportS,               # report title
    "titleS": "rivt Document",        # document title
    "divS": divS,                     # div title
    "sectS": "",                      # section title
    "docnumS": docbaseS[1:5],         # doc number
    "secnumI": 0,                     # section number
    "widthI": 80,                     # print width
    "equI": 1,                        # equation number
    "tableI": 1,                      # table number
    "figI": 1,                        # figure number
    "pageI": 1,                       # starting page number
    "noteL": [0],                     # footnote counter
    "footL": [1],                     # foot counter
    "unitS": "M,M",                   # units
    "descS": "2",                     # description or decimal places
    "headrS": "",                     # header string
    "footrS": "",                     # footer string
    "tocB": False,                    # table of contents
    "docstrB": False,                 # print doc strings
    "subB": False                     # sub values in equations
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

print(f"\n-------- start rivt file : [{docfileS}] ---------")

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

    hdrstS = """"""
    hdmdS = """"""
    hdutfS = """"""""

    snumI = incrD["secnumI"] + 1
    incrD["secnumI"] = snumI
    docnumS = incrD["docnumS"]
    dnumS = docnumS + "-[" + str(snumI) + "]"
    headS = dnumS + " " + hdrS
    bordrS = incrD["widthI"] * "-"

    hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
    hdmdS = "### " + headS + "\n"
    hdrstS += (
        ".. raw:: latex"
        + "   \n\n ?x?vspace{.2in} "
        + "   ?x?begin{tcolorbox} "
        + "   ?x?textbf{ " + hdrS + "}"
        + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"
        + "   ?x?end{tcolorbox}"
        + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
        + "\n\n")

    return hdutfS, hdmdS, hdrstS


def _str_set(rS, methS):
    """_summary_

    :param rS: _description_
    :type rS: _type_
    :param methS: _description_
    :type methS: _type_
    :return: _description_
    :rtype: _type_
    """

    global mdS, rstS, incrD, folderD

    rs1L = rS.split("|")

    if methS == "R":
        incrD["pageI"] = int(rs1L[1])                  # start page

    elif methS == "I":
        if rs1L[1].strip() == "default":
            incrD["subB"] = True
        else:
            incrD["subB"] = False

    elif methS == "V":
        if rs1L[1].strip() == "sub":
            incrD["subB"] = True
        else:
            incrD["subB"] = False

    elif methS == "T":
        if rs1L[1] == "code":
            folderD["codeB"] = True
        else:
            folderD["codeB"] = False

    rs1S = rs1L[0].strip()

    if rs1S.strip()[0:2] == "--":                       # skip new section
        return "\n", "\n", "\n"
    else:
        return _str_title(rs1L[0].strip())


def R(rS: str):
    """process Repo string

        : param rS: triple quoted repo string
        : type rS: str
        : return: formatted utf, md and reST strings
        : type: str
    """

    global utfS, mdS, rstS, incrD, folderD

    xmdS = xrstS = ""
    rL = rS.split("\n")
    hdutf, hmdS, hrstS = _str_set(rL[0], "R")
    doctitleS = rL[0].split("|")[0].strip()
    incrD["doctitleS"] = doctitleS
    headS = datetime.now().strftime("%Y-%m-%d | %I:%M%p") + "\n"

    utftitleS = (headS + "\n" + doctitleS + "\n")
    mdtitleS = (headS + "\n## " + doctitleS + "\n")
    rsttitleS = (
        ".. raw:: latex"
        + "   \n\n ?x?vspace{.2in} "
        + "   ?x?begin{tcolorbox} "
        + "   ?x?textbf{ " + doctitleS + "}"
        + "   ?x?end{tcolorbox}"
        + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
        + "\n\n")

    utfS += utftitleS
    mdS += mdtitleS
    rstS += rsttitleS

    print(utftitleS)

    parseC = parse.RivtParse("R", folderD, incrD, rivtD)
    xutf, xmdL, xrstL, incrD, folderD = parseC.str_parse(rL[1:], "R")
    mdS += xmdL[0]
    rstS += xrstL[0]

    utfS += utftitleS
    mdS += mdtitleS
    rstS += rsttitleS

    print(utftitleS)


def I(rS: str):
    """process Insert string

        : param rS: triple quoted insert string
        : type rS: str
        : return: formatted md string
        : rtype: str
    """

    global utfS, mdS, rstS, incrD, folderD

    xmdS = ""
    xrstS = ""
    xutfS = ""
    rL = rS.split("\n")
    hdutf, hmdS, hrstS = _str_set(rL[0], "I")
    print(hmdS)

    mdC = parse.RivtParse("I", folderD, incrD,  rivtD)
    xmdL, xrstL, incrD, folderD, localD = mdC.str_parse(rL[1:], "I")
    if hmdS != None:
        xmdS = hmdS + xmdL[0]
        xrstS = hrstS + xrstL[0]

    mdS += xmdS
    rstS += xrstS
    xmdS = ""


def V(rS: str):
    """process Value string

        :param rS: triple quoted values string
        :type rS: str: return
        :formatted md string: type: str
    """

    global utfS, mdS, rstS, incrD, folderD, rivtD

    locals().update(localD)

    xmdS = ""
    xrstS = ""
    rL = rS.split("\n")
    hmdS, hrstS = _str_set(rL[0], "V")
    print(hmdS)
    mdC = parse.RivtParse("V", folderD, incrD, rivtD)
    xmdL, xrstL, incrD, folderD, localD = mdC.str_parse(rL[1:], "V")
    # print(f"{xmdS=}", f"{rL[1:]=}")
    if hmdS != None:
        xmdS = hmdS + xmdL[0]
        xrstS = hrstS + xrstL[0]
    mdS += xmdS                      # accumulate md string
    rstS += xrstS                    # accumulate reST string
    xmdS = ""

    localD.update(locals())


def T(rS: str):
    """process Tables string

    : param rS: triple quoted insert string
    : type rS: str: return: formatted md or reST string: type: str

    """
    global utfS, mdS, rstS, incrD, folderD, rivtD

    xmdS = ""
    xrstS = ""
    rL = rS.split("\n")

    hmdS, hrstS = _str_set(rL[0], "T")
    mdC = parse.RivtParse("T", folderD, incrD, rivtD)
    xmdL, xrstL, incrD, folderD, localD = mdC.str_parse(rL[1:], "T")
    xmdS = hmdS + xmdL[0]
    xrstS = hrstS + xrstL[0]

    mdS += xmdS
    rstS += xrstS


def X(rS: str):
    """skip string - not processed

    """

    pass


def writedocs():
    pass


def _mod_tex(tfileP):
    """Modify TeX file to avoid problems with escapes:

        -  Replace marker "aaxbb " inserted by rivt with
            \\hfill because it is not handled by reST).
        - Delete inputenc package
        - Modify section title and add table of contents

    """
    startS = str(incrD["pageI"])
    doctitleS = str(incrD["doctitleS"])

    with open(tfileP, "r", encoding="md-8", errors="ignore") as f2:
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

    with open(tfileP, "w", encoding="md-8") as f2:
        f2.write(texf)

    # with open(tfileP, 'w') as texout:
    #    print(texf, file=texout)

    return


def _gen_pdf(self):
    """Write PDF file from TEX file

    """

    pdfD = {
        "xpdfP": Path(tempP, docbaseS + ".pdf"),
        "xhtmlP": Path(tempP, docbaseS + ".html"),
        "xrstP": Path(tempP, docbaseS + ".rst"),
        "xtexP": Path(tempP, docbaseS + ".tex"),
        "xauxP": Path(tempP, docbaseS + ".aux"),
        "xoutP": Path(tempP, docbaseS + ".out"),
        "xflsP": Path(tempP, docbaseS + ".fls"),
        "xtexmakP": Path(tempP, docbaseS + ".fdb_latexmk"),
    }
    # os.system('latex --version')
    os.chdir(tempP)
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
    3. execute the dictionary and write the md-8 calc and Python file
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
    texfileP = Path(tempP, docbaseS + ".tex")
    rstfileP = Path(tempP, docbaseS + ".rst")

    with open(rstfileP, "w", encoding='md-8') as f2:
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
    os.chdir(tempP)
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


def writepdf():
    """write output files

    :param formatS: comma separated output types
    :type formatS: str
    """

    global mdS, rstS, outputS, incrD, folderD

    docmdP = Path(docP.parent / "README.md")
    rstfileP = Path(docP.parent, docbaseS + ".rst")
    # eshortP = Path(*Path(rstfileP).parts[-3:])

    print(f" -------- end rivt file: [{docfileS}] --------- ")
    logging.info(f"""end rivt file: [{docfileS}]""")

    # add table of contents to summary

    tocS = ""
    secI = 0
    for iS in rivtL:
        if iS[0:5] == "rv.I(" and "--" not in iS:
            secI += 1
            jS = iS.split('"""')
            kS = jS.split("|").strip()
            tocS += str(secI) + "'" + kS
        elif i[0:4] == "rv.V" and "--" not in iS:
            secI += 1
            jS = iS.split('"""')
            kS = jS.split("|").strip()
            tocS += str(secI) + "'" + kS
        elif i[0:4] == "rv.T" and "--" not in iS:
            secI += 1
            jS = iS.split('"""')
            kS = jS.split("|").strip()
            tocS += str(secI) + "'" + kS
        else:
            pass
    incrD["tocS"] = tocS
    mdeditL = mdS.split("## ", 1)
    mdS = mdeditL[0] + tocS + mdeditL[1]

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

    if "pdf" in formatS or "html" in formatS:      # save rst file
        with open(rstfileP, "w", encoding='md-8') as f2:
            f2.write(rstS)
        logging.info(f"reST written: {rstfileP}")
        print(f"reST written: {rstfileP}")
    for i in formatL:
        if "pdf" in i:
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
    #   if "html" in I:
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
