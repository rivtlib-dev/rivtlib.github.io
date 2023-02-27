#
import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import logging
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
from numpy import *
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from IPython.display import display as _display
from IPython.display import Image as _Image
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass


def rvtags(typeS: str):

    tagL = [
        "_[new]",
        "_[line]",
        "_[link]",
        "_[lit]",
        "_[foot]",
        "_[r]",
        "_[c]",
        "_[e]",
        "_[t]",
        "_[f]",
        "_[x]",
        "_[s]"
        "_[#]",
        "_[-]",
        "_[url]",
        "_[lnk]",
        "_[[r]]",
        "_[[c]]",
        "_[[lit]]",
        "_[[tex]]",
        "_[[texm]]",
        "_[[end]]",
    ]

    tagvL = tagL.append("=")
    tagrL = ["_[[read]]", "_[[end]]"]

    tagD = {
        "R": tagrL,
        "I": tagL,
        "V": tagvL,
        "T": tagL,
    }

    return eval(str(tagD[typeS]))


def refs(self, objnumI: int, typeS: str) -> str:
    """reference label for equations, tables and figures

    Args:
        objnumI (int): equation, table or figure section number
        typeS (str): label type

    Returns:
        refS (str): reference label
    """

    objnumS = str(objnumI).zfill(2)
    cnumS = str(self.sectD["cnumS"])

    return typeS + cnumS + "." + objnumS


def e_utf(self) -> tuple:
    """parse eval-string

    Returns:
        calcS (list): utf formatted calc-string (appended)
        setsectD (dict): section settings
        setcmdD (dict): command settings
    """

    ecmdL = ["text", "table", "image"]
    emethL = [self._itext, self._itable, self._iimage]
    etagL = [
        "[page]_",
        "[line]_",
        "[link]_",
        "[literal]_",
        "[foot]_",
        "[latex]_",
        "[s]_",
        "[x]_",
        "[r]_",
        "[c]_",
        "[e]_",
        "[t]_",
        "[f]_",
        "[#]_",
    ]

    self._parseUTF("insert", icmdL, imethL, itagL)

    return self.calcS, self.setsectD, self.setcmdD


def taglist(lineS: str) -> tuple:
    """check for tags

    Parameters:
    lineS: line from rivt file

    Returns:
    (str, bool): tag or


    """

    tagL = [
        "[page]_",
        "[line]_",
        "[link]_",
        "[foot]_",
        "[n]_",
        "[s]_",
        "[x]_",
        "[r]_",
        "[c]_",
        "[e]_",
        "[t]_",
        "[f]_",
        "[#]_",
        "[math]__",
        "[literal]__",
        "[latex]__",
        "[r]__",
        "[c]__",
    ]
    try:
        tag = list(set(tagL).intersection(lineS.split()))[0]
        return (tag, True)
    except:
        return (lineS, False)


def label(self, objnumI: int, tagD: dict, typeS: str) -> str:
    """labels for equations, tables and figures

    Args:
        objnumI (int): equation, table or figure numbers
        setsectD (dict): section dictionary
        typeS (str): label type

    Returns:
        str: formatted label
    """

    objfillS = str(objnumI).zfill(2)
    if type(typeS) == str:
        sfillS = str(self.tagD["snumS"]).strip().zfill(2)
        labelS = typeS + sfillS
    else:
        cnumSS = str(self.tagD["cnumS"])
        labelS = typeS + cnumSS + "." + objfillS

    return labelS


def tags(self, lineS: str, sectD: dict) -> tuple:
    """format line with tag
    Parameters:
        lineS (str): rivt-string line with tag
        sectD (dict): section dictionary

    Return:
        uS (str): utf string
    """
    swidthII = sectD["swidthI"] - 1
    lineS = lineS.rstrip()
    tag = _taglist(lineS)
    uS = ""

    if tag == "[#]_":  # auto increment footnote mark
        ftnumII = self.setsectD["ftqueL"][-1] + 1
        self.setsectD["ftqueL"].append(ftnumII)
        uS = tagS.replace("[x]_", "[" + str(ftnumII) + "]")
    elif tag == "[foot]_":  # footnote label
        tagS = tagS.strip("[foot]_").strip()
        uS = self.setsectD["ftqueL"].popleft() + tagS
    elif tag == "[page]_":  # new page
        uS = int(self.setsectD["swidthI"]) * "."
    elif tag == "[line]_":  # horizontal line
        uS = int(self.setsectD["swidthI"]) * "-"
    elif tag == "[link]_":  # url link
        tgS = tagS.strip("[link]_").strip()
        tgL = tgS.split("|")
        uS = tgL[0].strip() + " : " + tgL[1].strip()
    elif tag == "[literal]_":  # literal text
        uS = "\n"
    elif tag == "[latex]_":  # literal text
        uS = "\n"
    elif tag == "[r]_":  # right adjust text
        tagL = tagS.strip().split("[r]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    elif tag == "[c]_":  # center text
        tagL = tagS.strip().split("[c]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    elif tag == "[f]_":  # figure caption
        tagL = tagS.strip().split("[f]_")
        fnumI = int(self.setsectD["fnumI"]) + 1
        self.setsectD["fnumI"] = fnumI
        refS = self._label(fnumI, "[ Fig: ") + " ]"
        spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
        uS = tagL[0].strip() + " " * spcI + refS
    elif tag == "[e]_":  # equation label
        tagL = tagS.strip().split("[e]_")
        enumI = int(self.setsectD["enumI"]) + 1
        self.setsectD["enumI"] = enumI
        refS = self._label(enumI, "[ Equ: ") + " ]"
        spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
        uS = tagL[0].strip() + " " * spcI + refS
    elif tag == "[t]_":  # table label
        tagL = tagS.strip().split("[t]_")
        tnumI = int(self.setsectD["tnumI"]) + 1
        self.setsectD["tnumI"] = tnumI
        refS = self._label(tnumI, "[Table: ") + " ]"
        spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
        uS = tagL[0].strip() + " " * spcI + refS
    elif tag == "[x]_":  # format tex
        tagL = tagS.strip().split("[x]_")
        txS = tagL[0].strip()
        # txS = txs.encode('unicode-escape').decode()
        ptxS = sp.parse_latex(txS)
        uS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))
    elif tag == "[s]_":  # format sympy
        tagL = tagS.strip().split("[s]_")
        spS = tagL[0].strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        # sps = sp.encode('unicode-escape').decode()
        uS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

    else:
        uS = lineS

    return uS, sectD


def _blocktags(self, lineS: str, sectD: dict) -> tuple:
    """parse block tags

    Args:
        tagS (str): rivt-string with tag
        tagL (list): list of tag parameters
        setsectD (dict): section dictionary

    Return:
        uS (str): utf string
    """

    swidthII = sectD["swidthI"] - 1

    tagS = tagS.rstrip()
    uS = ""
    try:
        tag = list(set(tagL).intersection(lineS.split()))[0]
    except:
        return lineS

    if tag == "[literal]__":  # footnote label
        tagS = tagS.strip("[foot]_").strip()
        uS = self.setsectD["ftqueL"].popleft() + tagS
    elif tag == "[math]__":  # new page
        uS = int(self.setsectD["swidthI"]) * "."
    elif tag == "[latex]__":  # horizontal line
        uS = int(self.setsectD["swidthI"]) * "-"
    elif tag == "[link]_":  # url link
        tgS = tagS.strip("[link]_").strip()
        tgL = tgS.split("|")
        uS = tgL[0].strip() + " : " + tgL[1].strip()
    elif tag == "[literal]_":  # literal text
        uS = "\n"
    elif tag == "[latex]_":  # literal text
        uS = "\n"
    elif tag == "[r]_":  # right adjust text
        tagL = tagS.strip().split("[r]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    elif tag == "[c]_":  # center text
        tagL = tagS.strip().split("[c]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    else:
        uS = lineS

    return uS, sectD


def rvcmds(typeS: str):
    """_summary_

    :param str methodS: _description_
    :return _type_: _description_
    """
    cmdL = [
        "project",
        "report",
        "github",
        "append",
        "table",
        "text",
        "image1",
        "image2",
        "values",
        "list",
        "functions"
    ]

    cmdsetD = {
        "R": [0, 1, 2, 3, 4, 5],
        "I": [4, 5, 6, 7],
        "V": [4, 5, 6, 7, 8, 9, 10, 11],
        "T": [4, 5, 6, 7]
    }

    return [cmdL[i] for i in cmdsetD[typeS]]


def vvalue(self, vL: list):
    """import values from files

    Args:
        vL (list): value command arguments
    """

    locals().update(self.rivtD)
    valL = []
    fltfmtS = ""
    if len(vL) < 5:
        vL += [""] * (5 - len(vL))  # pad command
    calpS = self.setsectD["fnumS"]
    vfileS = Path(self.folderD["cpath"] / calpS / vL[1].strip())
    with open(vfileS, "r") as csvfile:
        readL = list(csv.reader(csvfile))
    for vaL in readL[1:]:
        if len(vaL) < 5:
            vaL += [""] * (5 - len(vL))  # pad values
        varS = vaL[0].strip()
        valS = vaL[1].strip()
        unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
        descripS = vaL[4].strip()
        if not len(varS):
            valL.append(["------", "------", "------", "------"])  # totals
            continue
        val1U = val2U = array(eval(valS))
        if unit1S != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS + "*" + unit1S
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU.cast_unit(eval(unit2S))
        valL.append([varS, val1U, val2U, descripS])
    hdrL = ["variable", "value", "[value]", "description"]
    alignL = ["left", "right", "right", "left"]
    self._vtable(valL, hdrL, "rst", alignL, fltfmtS)
    self.rivtD.update(locals())

    def vdata(self, vL: list):
        """import data from files

        Args:
            vL (list): data command arguments
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        valL.append(["variable", "values"])
        vfileS = Path(self.folderD["apath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS, "r") as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]
            varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4:
                varL = str((varL[:2]).append(["..."]))
            valL.append([varS, varL])
        hdrL = ["variable", "values"]
        alignL = ["left", "right"]
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())


def vsub(self, eqL: list, eqS: str):
    """substitute numbers for variables in printed output

    Args:
        epL (list): equation and units
        epS (str): [description]
    """

    locals().update(self.rivtd)

    eformat = ""
    utfS = eqL[0].strip()
    descripS = eqL[3]
    parD = dict(eqL[1])
    varS = utfS.split("=")
    resultS = vars[0].strip() + " = " + str(eval(vars[1]))
    try:
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        # sps = sps.encode('unicode-escape').decode()
        utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
        print(utfs)
        self.calcl.append(utfs)
    except:
        print(utfs)
        self.calcl.append(utfs)
    try:
        symeq = sp.sympify(eqS.strip())  # substitute
        symat = symeq.atoms(sp.Symbol)
        for _n2 in symat:
            evlen = len((eval(_n2.__str__())).__str__())  # get var length
            new_var = str(_n2).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
        out2 = sp.pretty(symeq1, wrap_line=False)
        # print('out2a\n', out2)
        symat1 = symeq1.atoms(sp.Symbol)  # adjust character length
        for _n1 in symat1:
            orig_var = str(_n1).replace("~", "")
            orig_var = orig_var.replace("|", "_")
            try:
                expr = eval((self.odict[orig_var][1]).split("=")[1])
                if type(expr) == float:
                    form = "{:." + eformat + "f}"
                    symeval1 = form.format(eval(str(expr)))
                else:
                    symeval1 = eval(orig_var.__str__()).__str__()
            except:
                symeval1 = eval(orig_var.__str__()).__str__()
            out2 = out2.replace(_n1.__str__(), symeval1)
        # print('out2b\n', out2)
        out3 = out2  # clean up unicode
        out3.replace("*", "\\u22C5")
        # print('out3a\n', out3)
        _cnt = 0
        for _m in out3:
            if _m == "-":
                _cnt += 1
                continue
            else:
                if _cnt > 1:
                    out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                _cnt = 0
        # print('out3b \n', out3)
        self._write_text(out3, 1, 0)  # print substituted form
        self._write_text(" ", 0, 0)
    except:
        pass


def vfunc(self, vL: list):
    pass


def vtable(self, tbl, hdrL, tblfmt, alignL):
    """write value table"""

    locals().update(self.rivtD)
    sys.stdout.flush()
    old_stdout = sys.stdout
    output = StringIO()
    output.write(
        tabulate(
            tbl, tablefmt=tblfmt, headers=hdrL, showindex=False, colalign=alignL
        )
    )
    utfS = output.getvalue()
    sys.stdout = old_stdout
    sys.stdout.flush()
    print(utfS)
    self.calcS += utfS + "\n"
    self.rivtD.update(locals())


def vvalue(self, vL: list):
    """import values from files

    Args:
        vL (list): value command arguments
    """

    locals().update(self.rivtD)
    valL = []
    if len(vL) < 5:
        vL += [""] * (5 - len(vL))  # pad command
    calpS = "c" + self.setsectD["cnumS"]
    vfileS = Path(self.folderD["cpathcur"] / vL[1].strip())
    with open(vfileS, "r") as csvfile:
        readL = list(csv.reader(csvfile))
    for vaL in readL[1:]:
        if len(vaL) < 5:
            vaL += [""] * (5 - len(vL))  # pad values
        varS = vaL[0].strip()
        valS = vaL[1].strip()
        unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
        descripS = vaL[4].strip()
        if not len(varS):
            valL.append(["---------", " ", " ", " "])  # totals
            continue
        val1U = val2U = array(eval(valS))
        if unit1S != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS + "*" + unit1S
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU.cast_unit(eval(unit2S))
        valL.append([varS, val1U, val2U, descripS])
    hdrL = ["variable", "value", "[value]", "description"]
    alignL = ["left", "right", "right", "left"]
    self._vtable(valL, hdrL, "rst", alignL)
    self.rivtD.update(locals())


def vdata(self, vL: list):
    """import data from files

    Args:
        vL (list): data command arguments
    """

    locals().update(self.rivtD)
    valL = []
    if len(vL) < 5:
        vL += [""] * (5 - len(vL))  # pad command
    valL.append(["variable", "values"])
    vfileS = Path(self.folderD["cpath"] / vL[2].strip())
    vecL = eval(vL[3].strip())
    with open(vfileS, "r") as csvF:
        reader = csv.reader(csvF)
    vL = list(reader)
    for i in vL:
        varS = i[0]
        varL = array(i[1:])
        cmdS = varS + "=" + str(varL)
        exec(cmdS, globals(), locals())
        if len(varL) > 4:
            varL = str((varL[:2]).append(["..."]))
        valL.append([varS, varL])
    hdrL = ["variable", "values"]
    alignL = ["left", "right"]
    self._vtable(valL, hdrL, "rst", alignL)
    self.rivtD.update(locals())


def text_utf(self, iL: list):
    """insert text from file

    Args:
        iL (list): text command list

    || text | (file.txt) | literal; indent; html

    """

    txtP = Path(self.folderD["cpathcur"] / iL[1].strip())
    with open(txtP, "r", encoding="utf-8") as txtf1:
        uL = txtf1.readlines()
    if iL[2].strip() == "indent":
        txtS = "".join(uL)
        widthI = self.setcmdD["cwidth"]
        inS = " " * 4
        uL = textwrap.wrap(txtS, width=widthI)
        uL = [inS + S1 + "\n" for S1 in uL]
        uS = "".join(uL)
    elif iL[2].strip() == "literal":
        txtS = "  ".join(uL)
        uS = "\n" + txtS
    elif iL[2].strip() == "literalindent":
        txtS = "\n\n::\n\n"
        for iS in uL:
            txtS += "   " + iS
        uS = txtS + "\n\n"
    elif iL[2].strip() == "html":
        txtS = ""
        flg = 0
        for iS in uL:
            if "src=" in iS:
                flg = 1
                continue
            if flg == 1 and '"' in iS:
                flg = 0
                continue
            if flg == 1:
                continue
            txtS += iS
        txtS = htm.html2text(txtS)
        uS = txtS.replace("\n    \n", "")
    else:
        txtS = "".join(uL)
        uS = "\n" + txtS

    # print(str(txtP))
    # self.calcS += str(txtP) + "\n"
    print(uS)
    self.calcS += uS + "\n"


def table_utf(self, iL: list):
    """insert table from csv or xlsx file

    Args:
        ipl (list): parameter list
    """
    alignD = {"S": "", "D": "decimal",
              "C": "center", "R": "right", "L": "left"}

    if len(iL) < 4:
        iL += [""] * (4 - len(iL))  # pad parameters
    utfS = ""
    contentL = []
    sumL = []
    fileS = iL[1].strip()
    calpS = self.setsectD["fnumS"]
    tfileS = Path(self.folderD["cpathcur"] / fileS)
    extS = fileS.split(".")[1]
    if extS == "csv":
        with open(tfileS, "r") as csvfile:  # read csv file
            readL = list(csv.reader(csvfile))
    elif extS == "xlsx":
        pDF1 = pd.read_excel(tfileS, header=None)
        readL = pDF1.values.tolist()
    else:
        return
    incl_colL = list(range(len(readL[1])))
    widthI = self.setcmdD["cwidthI"]
    alignS = self.setcmdD["calignS"]
    saS = alignD[alignS]
    if iL[2].strip():
        widthL = iL[2].split(",")  # new max col width
        widthI = int(widthL[0].strip())
        alignS = widthL[1].strip()
        saS = alignD[alignS]  # new align
        self.setcmdD.update({"cwidthI": widthI})
        self.setcmdD.update({"calignS": alignS})
    totalL = [""] * len(incl_colL)
    if iL[3].strip():  # columns
        if iL[3].strip() == "[:]":
            totalL = [""] * len(incl_colL)
        else:
            incl_colL = eval(iL[3].strip())
            totalL = [""] * len(incl_colL)
    ttitleS = readL[0][0].strip() + " [t]_"
    utgS = self._tags(ttitleS, itagL)
    print(utgS.rstrip() + "\n")
    self.calcS += utgS.rstrip() + "\n\n"
    for row in readL[1:]:
        contentL.append([row[i] for i in incl_colL])
    wcontentL = []
    for rowL in contentL:  # wrap columns
        wrowL = []
        for iS in rowL:
            templist = textwrap.wrap(str(iS), int(widthI))
            templist = [i.replace("""\\n""", """\n""") for i in templist]
            wrowL.append("""\n""".join(templist))
        wcontentL.append(wrowL)
    sys.stdout.flush()
    old_stdout = sys.stdout
    output = StringIO()
    output.write(
        tabulate(
            wcontentL,
            tablefmt="rst",
            headers="firstrow",
            numalign="decimal",
            stralign=saS,
        )
    )
    utfS = output.getvalue()
    sys.stdout = old_stdout

    print(str(tfileS))
    print(utfS)
    self.calcS += str(tfileS) + "\n"
    self.calcS += utfS + "\n"


def image_utf(self, iL: list):
    """insert one or two images from file

    Args:
        iL (list): image parameters
    """
    utfS = ""
    if "," in iL[1]:  # two images
        scaleF = iL[2].split(",")
        scale1F = float(scaleF[0])
        scale2F = float(scaleF[1])
        self.setcmdD.update({"scale1F": scale1F})
        self.setcmdD.update({"scale2F": scale2F})
        fileS = iL[1].split(",")
        file1S = fileS[0].strip()
        file2S = fileS[1].strip()
        docpS = "d" + self.setsectD["cnumS"]
        img1S = str(Path(self.folderD["dpathcur"] / file1S))
        img2S = str(Path(self.folderD["dpathcur"] / file2S))
        # pshrt1S = str(Path(*Path(img1S).parts[-4:]))
        # pshrt2S = str(Path(*Path(img2S).parts[-4:]))
        for fS in [img1S, img2S]:
            utfS += "Figure path: " + fS + "\n"
            try:
                _display(_Image(fS))
            except:
                pass
        print(utfS)
        self.calcS += utfS + "\n"
    else:  # one image
        scale1F = float(iL[2])
        self.setcmdD.update({"scale1F": scale1F})
        fileS = iL[1].split(",")
        file1S = fileS[0].strip()
        docpS = "d" + self.setsectD["cnumS"]
        img1S = str(Path(self.folderD["dpathcur"] / file1S))
        utfS += "Figure path: " + img1S + "\n"
        try:
            _display(_Image(img1S))
        except:
            pass
        print(utfS)
        self.calcS += utfS + "\n"


def latex_utf(self, iL: list):
    """insert latex text from file

    Args:
        iL (list): text command list
    """

    calP = "c" + self.setsectD["cnumS"]
    txapath = Path(self.folderD["dpath0"] / iL[1].strip())
    with open(txapath, "r") as txtf1:
        uL = txtf1.readlines()
    if iL[2].strip() == "indent":
        txtS = "".join(uL)
        widthI = self.setcmdD["cwidth"]
        inS = " " * 4
        uL = textwrap.wrap(txtS, width=widthI)
        uL = [inS + S1 + "\n" for S1 in uL]
        uS = "".join(uL)
    elif iL[2].strip() == "literal":
        txtS = "  ".join(uL)
        uS = "\n" + txtS
    else:
        txtS = "".join(uL)
        uS = "\n" + txtS

    self.calcS += uS + "\n"

    print(uS)
    self.calcS += uS + "\n"


def text_rst(self, iL: list):
    """insert text from file

    Args:
        iL (list): text command list
    """
    txapath = Path(self.folderD["cpathcur"] / iL[1].strip())
    with open(txapath, "r", encoding="utf-8") as txtf1:
        rstL = txtf1.readlines()
    if iL[2].strip() == "indent":
        txtS = "".join(rstL)
        widthI = self.setcmdD["cwidth"]
        inS = " " * 4
        rstL = textwrap.wrap(txtS, width=widthI)
        rstL = [inS + S1 + "\n" for S1 in rstL]
        rstS = "".join(rstL)
    elif iL[2].strip() == "literal":
        txtS = " ".join(rstL)
        rstS = "\n\n::\n\n" + txtS + "\n\n"
    elif iL[2].strip() == "literalindent":
        txtS = "\n\n::\n\n"
        for iS in iL:
            txtS += "   " + iS
        rstS = txtS + "\n\n"
    elif iL[2].strip() == "html":
        txtS = ""
        flg = 0
        for iS in rstL:
            if "src=" in iS:
                flg = 1
                continue
            if flg == 1 and '"' in iS:
                flg = 0
                continue
            if flg == 1:
                continue
            txtS += iS
        txtS = htm.html2text(txtS)
        txtS = "   " + txtS.replace("\n    \n", "")
        rstL = txtS.split("\n")
        for num, iS in enumerate(rstL):
            rstL[num] = "   " + iS
        rstS = "\n".join(rstL[1:])
        rstS = "\n\n::\n\n" + rstS + "\n\n"
    else:
        txtS = "".join(rstL)
        rstS = "\n" + txtS

    self.restS += rstS + "\n"


def table_rst(self, iL: list):
    """insert table from csv or xlsx file

    Args:
        ipl (list): parameter list
    """
    alignD = {"S": "", "D": "decimal",
              "C": "center", "R": "right", "L": "left"}

    if len(iL) < 4:
        iL += [""] * (4 - len(iL))  # pad parameters
    utfS = ""
    contentL = []
    sumL = []
    fileS = iL[1].strip()
    calpS = self.setsectD["fnumS"]
    tfileS = Path(self.folderD["cpathcur"] / fileS)
    extS = fileS.split(".")[1]
    if extS == "csv":
        with open(tfileS, "r") as csvfile:  # read csv file
            readL = list(csv.reader(csvfile))
    elif extS == "xlsx":
        tDF1 = pd.read_excel(tfileS, header=None)
        readL = tDF1.values.tolist()
    else:
        return
    incl_colL = list(range(len(readL[1])))
    widthI = self.setcmdD["cwidthI"]
    alignS = self.setcmdD["calignS"]
    saS = alignD[alignS]
    if iL[2].strip():
        widthL = iL[2].split(",")  # new max col width
        widthI = int(widthL[0].strip())
        alignS = widthL[1].strip()
        self.setcmdD.update({"cwidthI": widthI})
        self.setcmdD.update({"calignS": alignS})
        saS = alignD[alignS]  # new align
    totalL = [""] * len(incl_colL)
    if iL[3].strip():  # columns
        if iL[3].strip() == "[:]":
            totalL = [""] * len(incl_colL)
        else:
            incl_colL = eval(iL[3].strip())
            totalL = [""] * len(incl_colL)
    ttitleS = readL[0][0].strip() + " [t]_"
    utgS = self._tags(ttitleS, itagL)
    self.restS += utgS.rstrip() + "\n\n"
    for row in readL[1:]:
        contentL.append([row[i] for i in incl_colL])
    sys.stdout.flush()
    old_stdout = sys.stdout
    output = StringIO()
    output.write(
        tabulate(
            contentL,
            tablefmt="latex",
            headers="firstrow",
            numalign="decimal",
            stralign=saS,
        )
    )
    rstS = output.getvalue()
    sys.stdout = old_stdout

    # print(rstS)
    cS = 0
    self.restS += ".. raw:: latex" + "\n\n"
    for i in rstS.split("\n"):
        counter = i.count("&")
        if counter > 0:
            cS = "{" + alignS * (counter + 1) + "}"
            continue
    # self.restS += "  \\vspace{-.1in}"
    self.restS += "  \\begin{tabulary}{1.0\\textwidth}" + cS + "\n"
    inrstS = ""
    for i in rstS.split("\n"):
        inrstS += "  " + i + "\n"
    self.restS += inrstS
    self.restS += "  \\end{tabulary}\n"
    self.restS += "  \\vspace{.15in}\n"


def image_rst(self, iL: list):
    """insert one or two images from file

    Args:
        il (list): image parameters
    """
    rstS = ""
    fileS = iL[1].split(",")
    file1S = fileS[0].strip()
    fileS = iL[1].split(",")
    file1S = fileS[0].strip()
    img1S = str(Path(self.folderD["dpathcur"] / file1S).as_posix())
    scaleF = iL[2].split(",")
    scale1S = str(int(scaleF[0])) + "%"
    self.setcmdD.update({"scale1F": scale1S})
    if "," in iL[1]:  # two images
        scale2S = str(int(scaleF[1])) + "%"
        self.setcmdD.update({"scale2F": scale2S})
        file2S = fileS[1].strip()
        img2S = str(Path(self.folderD["dpathcur"] / file2S).as_posix())
        pic1S = "|pic" + str(self.setsectD["counter"] + 1) + "|"
        pic2S = "|pic" + str(self.setsectD["counter"] + 2) + "|"
        self.setsectD["counter"] = self.setsectD["counter"] + 3
        rstS += (
            pic1S
            + "  ____  "
            + pic2S
            + "\n\n"
            + ".. "
            + pic1S
            + " image:: "
            + img1S
            + "\n"
            + "   :width: "
            + scale1S
            + "\n\n"
            + ".. "
            + pic2S
            + " image:: "
            + img2S
            + "\n"
            + "   :width: "
            + scale2S
            + "\n"
        )
    else:  # one image
        rstS += (
            ".. image:: "
            + img1S
            + "\n"
            + "   :width: "
            + scale1S
            + "\n"
            + "   :align: left \n"
        )

    self.restS += rstS + "\n"
    time.sleep(1)


def project(self, rL):
    """insert tables or text from csv, xlsx or txt file

    Args:
        rL (list): parameter list

    Files are read from /docs/docfolder
    The command is identical to itable except file is read from docs/info.

    """
    alignD = {"S": "", "D": "decimal",
              "C": "center", "R": "right", "L": "left"}

    if len(rL) < 4:
        rL += [""] * (4 - len(rL))  # pad parameters
    rstS = ""
    contentL = []
    sumL = []
    fileS = rL[1].strip()
    tfileS = Path(self.folderD["dpath0"] / fileS)
    extS = fileS.split(".")[1]
    if extS == "csv":
        with open(tfileS, "r") as csvfile:  # read csv file
            readL = list(csv.reader(csvfile))
    elif extS == "xlsx":
        xDF = pd.read_excel(tfileS, header=None)
        readL = xDF.values.tolist()
    else:
        return
    incl_colL = list(range(len(readL[0])))
    widthI = self.setcmdD["cwidthI"]
    alignS = self.setcmdD["calignS"]
    saS = alignD[alignS]
    if rL[2].strip():
        widthL = rL[2].split(",")  # new max col width
        widthI = int(widthL[0].strip())
        alignS = widthL[1].strip()
        saS = alignD[alignS]  # new alignment
        self.setcmdD.update({"cwidthI": widthI})
        self.setcmdD.update({"calignS": alignS})
    totalL = [""] * len(incl_colL)
    if rL[3].strip():  # columns
        if rL[3].strip() == "[:]":
            totalL = [""] * len(incl_colL)
        else:
            incl_colL = eval(rL[3].strip())
            totalL = [""] * len(incl_colL)
    ttitleS = readL[0][0].strip() + " [t]_"
    rstgS = self._tags(ttitleS, rtagL)
    self.restS += rstgS.rstrip() + "\n\n"
    for row in readL[1:]:
        contentL.append([row[i] for i in incl_colL])
    wcontentL = []
    for rowL in contentL:
        wrowL = []
        for iS in rowL:
            templist = textwrap.wrap(str(iS), int(widthI))
            templist = [i.replace("""\\n""", """\n""") for i in templist]
            wrowL.append("""\n""".join(templist))
        wcontentL.append(wrowL)
    sys.stdout.flush()
    old_stdout = sys.stdout
    output = StringIO()
    output.write(
        tabulate(
            wcontentL,
            tablefmt="rst",
            headers="firstrow",
            numalign="decimal",
            stralign=saS,
        )
    )
    rstS = output.getvalue()
    sys.stdout = old_stdout

    self.restS += rstS + "\n"


def attach(self, rsL):
    b = 5


def report(self, rL):
    """skip info command for utf calcs

    Command is executed only for docs in order to
    separate protected information for shareable calcs.

    Args:
        rL (list): parameter list
    """

    """       
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
    return """
    pass
