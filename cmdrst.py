#
import os
import sys
import csv
import time
import textwrap
import logging
import warnings
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
from rivt import parse
from rivt.units import *


class CmdRST:
    """translate rivt-strings to reST strings

    param:exportS (str): stores values that are written to file
    strL (list): calc rivt-strings
    folderD (dict): folder paths
    tagD (dict): tag dictionary

    """

    def __init__(self, paramL, folderD, incrD, localD):
        """
        ======================================================== ============
                        command syntax                              methods
        ======================================================== ============

        1- || append | folder | file_name                               R
        2- || functions | folder | file_name | code; nocode             V
        3- || image1 | folder | file_name  | size                       I,V,T
        4- || image2 | folder | file_name  | size | file_name  | size   I,V,T
        5- || list | folder | file_name                                 V
        6- || pages | folder | file_name | head;foot                    R
        7- || project | folder | file_name | max width | align          R
        8- || table | folder | file_name | max width | rows             I,V,T
        9- || text | folder | file_name | text type |shade; noshade     I,V,T
        10-|| values | folder | file_name | [:];[x:y]                   V

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
        """1 append pdf files
        """
        pass

    def func(self):
        """2 import functions
        """
        pass

    def image(self):
        """3 insert one or two images from file

        Args:
            il (list): image parameters
        """
        rstS = ""
        iL = self.rL
        scale1F = float(iL[1])
        self.incrD.update({"scale1F": scale1F})
        file1S = iL[0].strip()
        img1S = str(Path(self.folderD["defaultP"] / file1S))
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

    def image2(self):
        """4 insert one or two images from file

        Args:
            il (list): image parameters
        """
        rstS = ""
        plenI = 5
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        iL = self.paramL
        scale1F = float(iL[2])
        scale2F = float(iL[4])
        self.incrD.update({"scale1F": scale1F})
        self.incrD.update({"scale2F": scale2F})
        file1S = iL[1].strip()
        file2S = iL[3].strip()
        if iL[0].strip() == "resource":
            img1S = str(Path(self.folderD["resourceP"] / file1S))
            img2S = str(Path(self.folderD["resourceP"] / file2S))
        else:
            img1S = str(Path(self.folderD["resourceP"] / file1S))
            img2S = str(Path(self.folderD["resourceP"] / file2S))
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

        self.restS += rstS + "\n"
        time.sleep(1)

    def list(self):
        """5 import data from files


            :return lineS: utf table
            :rtype: str
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
        self.vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

        return

    def pages(self):
        """6 write head or foot format line to dictionary

            :return lineS: header or footer
            :rtype: str
        """

        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated:  \
                                    {plenI} parameters required")
            return

        fileP = Path(self.folderD["configP"], "data", self.paramL[1].strip())
        with open(fileP, "r") as f2:
            pageL = f2.readlines()

        lineL = ["-", "-", "-"]
        for i in range(3):
            if "<date>" in pageL[i]:
                lineL[i] = datetime.today().strftime('%Y-%m-%d')
            elif "<datetime>" in pageL[i]:
                lineL[i] = datetime.today().strftime('%Y-%m-%d %H:%M')
            elif "<page>" in pageL[i]:
                lineL[i] = "page"
            else:
                lineL[i] = pageL[i].strip()

        l1I = len(lineL[0])
        l2I = len(lineL[1])
        l3I = len(lineL[2])
        wI = int(self.incrD["widthI"])
        spS = (int((wI - l1I - l3I - l2I)/2) - 2) * " "
        sepS = wI * "_" + 2*"\n"

        if self.paramL[2].strip() == "head":
            self.incrD["headS"] = lineL[0] + spS + \
                lineL[1] + spS + lineL[2] + "\n" + sepS
        if self.paramL[2].strip() == "foot":
            self.incrD["footS"] = lineL[0] + spS + \
                lineL[1] + spS + lineL[2] + "\n" + sepS

        return "None"

    def project(self):
        """7 insert project information from csv, xlsx or txt file

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
        print(tableS)
        return tableS

    def table(self, iL: list):
        """8 insert table from csv or xlsx file

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

    def text(self):
        """9 insert text from file

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

    def values(self):
        """10 import values from files

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
