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
from TexSoup import TexSoup
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

    def __init__(self, paramL, incrD, folderD,  localD):
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

        modnameS = __name__.split(".")[1]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
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
        """3 insert an image from file

        Args:
            il (list): image parameters
        """
        rstS = ""
        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        iL = self.paramL
        scale1S = iL[2]
        file1S = iL[1].strip()
        if iL[0].strip() == "resource":
            img1S = str(Path(self.folderD["resourceP"], file1S))
        else:
            img1S = str(Path(self.folderD["resourceP"], file1S))
        img1S = img1S.replace("\\", "/")
        rstS = ("\n.. image:: "
                + img1S + "\n"
                + "   :scale: "
                + scale1S + "%" + "\n"
                + "   :align: center"
                + "\n\n"
                )

        return rstS

    def image2(self):
        """4 insert two images from file

            :return rstS: image string
            :rtype: str

        """
        rstS = ""
        plenI = 5
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return

        iL = self.paramL
        scale1S = iL[2]
        scale2S = iL[4]
        file1S = iL[1].strip()
        file2S = iL[3].strip()
        if iL[0].strip() == "resource":
            img1S = str(Path(self.folderD["resourceP"], file1S))
            img2S = str(Path(self.folderD["resourceP"], file2S))
        else:
            img1S = str(Path(self.folderD["resourceP"], file1S))
            img2S = str(Path(self.folderD["resourceP"], file2S))
        img1S = img1S.replace("\\", "/")
        img2S = img2S.replace("\\", "/")
        rstS = ("|L| . |R|"
                + "\n\n"
                + ".. |L| image:: "
                + img1S + "\n"
                + "   :width: "
                + scale1S + "%"
                + "\n\n"
                + ".. |R| image:: "
                + img2S + "\n"
                + "   :width: "
                + scale2S + "%"
                + "\n\n"
                )

        return rstS

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

        fileP = Path(self.folderD["rvconfigP"], "data", self.paramL[1].strip())
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
                txtfile = f.readlines()
                txtfile = "\n".join(txtfile)
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

    def table(self):
        """8 insert table from csv or xlsx file

        Args:
            ipl (list): parameter list
        """
        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}

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
        align2S = self.paramL[2].split(",")[1].strip()
        colS = self.paramL[3].strip()                    # rows read
        extS = (pathP.suffix).strip()                    # file suffix
        if extS == ".csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                            # read xls file
            pdfO = pd.read_excel(pathP, header=None)
            readL = pdfO.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} command not evaluated: {extS} files not processed")
            return
        sys.stdout.flush()
        old_stdout = sys.stdout

        output = StringIO()
        output.write(tabulate(readL, tablefmt="rst", maxcolwidths=maxwI,
                              headers="firstrow", numalign="decimal"))
        rstS = output.getvalue()
        sys.stdout = old_stdout

        # restS = ".. raw:: latex" + "\n\n"       # align cells
        # # for i in rstS.split("\n"):
        # #     counter = i.count("&")
        # #     if counter > 0:
        # #         cS = "{|" + (align2S + "|") * (counter + 1) + "}"
        # #         cS = "{" + align2S * (counter + 1) + "}"
        # #         continue
        # restS += "  \\vspace{.15in}" + "\n"
        # inrstS = ""
        # for i in rstS.split("\n"):
        #     inrstS += "  " + i + "\n\n"
        # restS = restS + inrstS
        # restS += "  \\vspace{.15in}\n"

        restS = "\n" + rstS + "\n"
        return restS

    def text(self):
        """9 insert text from file

        || text | folder | file | type | shade

        """

        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated:  \
                                    {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])

        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        txttypeS = self.paramL[2].strip()
        extS = pathP.suffix

        with open(pathP, "r", encoding="utf-8") as f:
            txtfileS = f.read()
        with open(pathP, "r", encoding="utf-8") as f:
            txtfileL = f.readlines()

        j = ""
        if extS == ".txt":
            # print(f"{txttypeS=}")
            if txttypeS == "literal":
                for iS in txtfileL:
                    j += "   " + iS
                return "\n\n::\n\n" + j + "\n\n"
            elif txttypeS == "literalindent":
                txtS = "\n\n::\n\n"
                for iS in txtfileL:
                    j += "   " + iS
                return txtS + j + "\n\n"
            elif txttypeS == "sympy":
                for iS in txtfileL:
                    try:
                        spL = i.split("=")
                        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
                        # sps = sp.encode('unicode-escape').decode()
                        lineS = sp.pretty(sp.sympify(
                            spS, _clash2, evaluate=False))
                        j += lineS
                    except:
                        lineS = sp.pretty(sp.sympify(
                            spS, _clash2, evaluate=False))
                        j += lineS
            elif txttypeS == "itag":
                utfI = parse.RivtParse(folderD, incrD,
                                       txtfileS, "itag", localD)
                xutfS, xrstS, folderD, incrD, localD = utfI.str_parse(
                    txtfileS)
                return xutfS, xrstS
            else:
                pass
        elif extS == ".html":
            txtS = ".. raw:: html" + "\n\n"
            for iS in txtfileL:
                j += "   " + iS
            return txtS + j + "\n\n"
        elif extS == ".tex":
            txtS = ".. raw:: latex" + "\n\n"
            for iS in txtfileL:
                j += "   " + iS
            return txtS + j + "\n\n"

    def vtable(self, tbL, hdrL, tblfmt, alignL):
        """write value table"""

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbL, headers=hdrL, tablefmt=tblfmt,
                showindex=False, colalign=alignL
            )
        )
        rstS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return rstS

        # self.calcS += utfS + "\n"
        # self.rivtD.update(locals())

    def values(self):
        """10 import values from files

        """

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
                valL.append(["_ _", "_ _", "_ _", "Total"])  # totals
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

        rstS = self.vtable(valL, hdrL, "rst", alignL)

        # print(utfS + "\n")
        return rstS
