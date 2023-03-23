#
import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import logging
import warnings
import time
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
from io import StringIO
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

from io import StringIO  # Python 3

from rivt.units import *


class CmdUTF:

    def __init__(self, paramL, incrD, folderD, localD):
        """
        ======================================================== ============
            command syntax / snippet prefix and description        methods
        ======================================================== ============

        || append | folder | file_name                               R
        || github | folder | repo_name                               R
        || project | folder | file_name | max width,align            R

        || list | folder | file_name                                 V
        || functions | folder | file_name | code; nocode             V
        || values | folder | file_name | [:];[x:y]                   V

        || image1 | folder | file_name  | size                       I,V,T
        || image2 | folder | file_name  | size | file_name  | size   I,V,T
        || table | folder | file_name | max width, align | rows      I,V,T
        || text | folder | file_name | shade; noshade                I,V,T

        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.widthII = incrD["widthI"] - 1
        self.paramL = paramL
        self.errlogP = folderD["errlogP"]

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(name)-8s %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def cmd_parse(self, cmdS):
        """_summary_
        """
        self.cmdS = cmdS
        return eval("self." + cmdS+"()")

    def append(self):
        pass

    def github(self):
        pass

    def image(self):
        """insert image from file

        """
        utfS = ""
        iL = self.rL
        scale1F = float(iL[1])
        self.incrD.update({"scale1F": scale1F})
        file1S = iL[0].strip()
        img1S = str(Path(self.folderD["defaultP"] / file1S))
        # pshrt1S = str(Path(*Path(img1S).parts[-3:]))
        # pshrt2S = str(Path(*Path(img2S).parts[-3:]))
        for fS in [img1S]:
            utfS += "Figure path: " + fS + "\n"
            try:
                _display(_Image(fS))
            except:
                pass

        return utfS

    def image2(self):
        """insert two images from file side by side

            :param iL (list): image parameters
        """

        utfS = ""
        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        iL = self.paramL
        scale1F = float(iL[1])
        scale2F = float(iL[3])
        self.incrD.update({"scale1F": scale1F})
        self.incrD.update({"scale2F": scale2F})
        file1S = iL[0].strip()
        file2S = iL[2].strip()
        img1S = str(Path(self.folderD["resourceP"] / file1S))
        img2S = str(Path(self.folderD["resourceP"] / file2S))
        pshrt1S = str(Path(*Path(img1S).parts[-3:]))
        pshrt2S = str(Path(*Path(img2S).parts[-3:]))
        temp_out = StringIO()
        sys.stdout = temp_out
        for fS in [pshrt1S, pshrt2S]:
            utfS += "Figure path: " + fS + "\n"
            try:
                _display(_Image(fS))
            except:
                pass

        sys.stdout = sys.__stdout__
        return utfS

    from io import StringIO  # Python 3

    def project(self):
        """insert project information from csv, xlsx or txt file

            :return lineS: utf table
            :rtype: str
        """

        alignD = {"S": "", "D": "decimal",
                  "C": "center", "R": "right", "L": "left"}
        tableS = ""
        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "resource":
            folderP = Path(self.folderD["resourceP"])
        else:
            folderP = Path(self.folderD["resourceP"])

        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)                   # file path
        maxwI = int(self.paramL[2].split(",")[0])       # max column width
        alignS = alignD[self.paramL[2].split(",")[1].strip()]
        extS = pathP.suffix

        if extS == ".csv":                              # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                           # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        elif extS == ".txt":                            # read txt file
            with open(pathP, "r") as f:
                txtfile = f.read()
            return txtfile
        else:
            logging.info(
                f"||{self.cmdS} not evaluated: [{extS}] file not processed")
            return

        wcontentL = []                                  # wrap columns
        for rowL in readL:
            wrowL = []
            for iS in rowL:
                templist = textwrap.wrap(str(iS), int(maxwI))
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
                stralign=alignS,
            )
        )
        tableS = output.getvalue()
        sys.stdout = old_stdout

        logging.info(f"{self.cmdS} evaluated")
        return tableS

    def table(self):
        """insert table from csv or xlsx file

            :return lineS: utf table
            :rtype: str
        """

        alignD = {"S": "", "D": "decimal",
                  "C": "center", "R": "right", "L": "left"}
        tableS = ""
        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)                    # file path
        maxwI = int(self.paramL[2].split(",")[0])        # max column width
        alignS = alignD[self.paramL[2].split(",")[1].strip()]
        colS = self.paramL[3].strip()                    # rows read
        extS = (pathP.suffix).strip()                    # file suffix
        if extS == ".csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                            # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} command not evaluated: {extS} files not processed")
            return

        incl_colL = list(range(len(readL[1])))
        if colS == "[:]":
            colL = [] * len(incl_colL)
        else:
            incl_colL = eval(colS)
            colL = eval(colS)
        for row in readL[1:]:                           # select columns
            colL.append([row[i] for i in incl_colL])
        wcontentL = []
        for rowL in colL:                               # wrap columns
            wrowL = []
            for iS in rowL:
                templist = textwrap.wrap(str(iS), int(maxwI))
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
                stralign=alignS,
            )
        )
        tableS = output.getvalue()
        sys.stdout = old_stdout

        return tableS

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

    def vfunc(self, vL: list):
        pass

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

    def values(self):
        """import values from files

        """

        locals().update(self.localD)

        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        plenI = 2                       # number of parameters
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        valL = []
        fltfmtS = ""
        with open(pathP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vL = len(vaL)
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

        utfS = self.vtable(valL, hdrL, "rst", alignL)
        locals().update(self.localD)
        self.localD.update(locals())

        print(utfS + "\n")
        return utfS

    def vtable(self, tbl, hdrL, tblfmt, alignL):
        """write value table"""

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbl, headers=hdrL, tablefmt=tblfmt,
                showindex=False, colalign=alignL
            )
        )
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return utfS

        # self.calcS += utfS + "\n"
        # self.rivtD.update(locals())
