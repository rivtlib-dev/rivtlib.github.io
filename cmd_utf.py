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


class CmdUTF:

    def __init__():

        pass

    def parse_cmd(lineS, cmdS, strL):
        """
        =============================================================== ============
            command syntax / snippet prefix and description                 methods
        =============================================================== ============

        || append | file_name | ./docfolder; default / resize;default          R
        || github | repo_name; none | readme; noneparam                        R
        || project | file_name | /docsfolder; default                          R
        || list | file_name  | [:];[x:y]                                       V
        || functions | file_name | docs; nodocs                                V
        || values | file_name | [:];[x:y]                                      V
        || image1 | file_name  | .50                                         I,V,T
        || image2 | file_name  | .40 | file_name  | .40                      I,V,T
        || table | file_name |  [:] | 60 r;l;c                               I,V,T
        || text | file_name | shade; noshade                                 I,V,T

        """

    def append(self, rsL):
        b = 5

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

    def values(self, vL: list):
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

    def vlist(self, vL: list):
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

    def image(self, iL: list):
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

    def text(self, iL: list):
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
