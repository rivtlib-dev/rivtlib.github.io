#
import os
import sys
import csv
import textwrap
import logging
import warnings
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
import configparser
from io import StringIO
from numpy import *
from IPython.display import display as _display
from IPython.display import Image as _Image
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from IPython.display import display as _display
from IPython.display import Image as _Image
from datetime import datetime
from TexSoup import TexSoup
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass

from rivt import parse
from rivt.units import *
from rivt import tagutf


class CmdUTF:
    """translate rivt-strings to utf strings

    param:exportS (str): stores values that are written to file
    strL (list): calc rivt-strings
    folderD (dict): folder paths
    tagD (dict): tag dictionary

    """

    def __init__(self, paramL, incrD, folderD, localD):
        """
        ======================================================== ============
                        command syntax                              methods
        ======================================================== ============

        1- || append | folder | file_name                               R
        2- || functions | folder | file_name | code; nocode             V
        3- || image | folder | file_name  | size                       I,V,T
        4- || image2 | folder | file_name  | size | file_name  | size   I,V,T
        5- || list | folder | file_name                                 V
        6- || pages | folder | file_name | file_name | page             R
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
        """1 _summary_
        """
        pass

    def func(self):
        """2 _summary_
        """
        pass

    def image(self):
        """3 insert image from file

        """

        utfS = ""
        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        iL = self.paramL
        file1S = iL[1].strip()
        imgL = file1S.split(",")
        if iL[0].strip() == "resource":
            imgP = Path(self.folderD["resourceP"])
        elif iL[0].strip() == "data":
            imgP = Path(self.folderD["data"])
        else:
            imgP = Path(self.folderD["resourceP"])
        temp_out = StringIO()
        sys.stdout = temp_out
        for i in imgL:
            imgS = Path(imgP, i)
            shrt1S = str(Path(*Path(imgS).parts[-3:]))
            utfS += "Figure path: " + shrt1S + "\n"
            try:
                _display(_Image(imgS))
            except:
                pass
        sys.stdout = sys.__stdout__

        return utfS

    def pages(self):
        """write head or foot format line to dictionary

            :return lineS: header or footer
            :rtype: str
        """

        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command skipped: {plenI} parameters required"
            )
            return

        iL = self.paramL
        iD = self.folderD["styleP"]
        if iL[0].strip() == "config":
            iniP = Path(self.folderD["rvconfigP"], self.paramL[1].strip())
            styP = Path(self.folderD["rvconfigP"], self.paramL[2].strip())
        elif iL[0].strip() == "data":
            iniP = Path(self.folderD["dataP"], self.paramL[1].strip())
            styD = Path(self.folderD["dataP"], self.paramL[2].strip())
        elif iL[0].strip() == "resource":
            iniP = Path(self.folderD["resourceP"], self.paramL[1].strip())
            styP = Path(self.folderD["resourceP"], self.paramL[2].strip())
        else:
            iniP = Path(self.folderD["dataP"], self.paramL[1].strip())
            styP = Path(self.folderD["resourceP"], self.paramL[2].strip())

        self.folderD["styleP"] = styP
        configC = configparser.ConfigParser()
        configC.read(iniP)
        headS = configC["utf-page"]["head1"]

        lineL = headS.split()

        if "<date>" in headS:
            headS = headS.replace("<date>",
                                  datetime.today().strftime('%Y-%m-%d'))
        if "<datetime>" in headS:
            headS = headS.replace("<datetime>",
                                  datetime.today().strftime('%Y-%m-%d %H:%M'))
        if "<page>" in headS:
            headS = headS.replace("<page>", "p##")

        self.incrD["pageI"] = int(self.paramL[3])
        lineL = headS.split("|")
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

        return self.folderD["styleP"]

    def project(self):
        """7 insert project information from csv, xlsx or syk

            :return lineS: utf table
            :rtype: str
        """

        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}

        tableS = ""
        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} not evaluated: {plenI} parameters required")
            return

        if self.paramL[0].strip() == "resource":
            folderP = Path(self.folderD["resourceP"])
        else:
            folderP = Path(self.folderD["resourceP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)                    # file path
        maxwI = int(self.paramL[2].split(",")[0])        # max column width
        alignS = alignD[self.paramL[2].split(",")[1].strip()]
        colS = self.paramL[3].strip()                    # rows read
        extS = (pathP.suffix).strip()
        if extS == ".csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                            # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
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

        # print(tableS)
        return tableS

    def table(self):
        """8 insert table from csv or xlsx file

            :return lineS: utf table
            :rtype: str
        """

        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}

        tableS = ""
        plenI = 4
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} not evaluated: {plenI} parameters required")
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
        extS = (pathP.suffix).strip()
        if extS == ".csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == ".xlsx":                            # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
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

        print(tableS)
        return tableS

    def txthtml(self, txtfileL):
        """9a _summary_

        :return: _description_
        :rtype: _type_
        """
        txtS = ""
        flg = 0
        for iS in txtfileL:
            if "src=" in iS:
                flg = 1
                continue
            if flg == 1 and '"' in iS:
                flg = 0
                continue
            if flg == 1:
                continue
            txtS += " "*4 + iS
            txtS = htm.html2text(txtS)
            utfS = txtS.replace("\n    \n", "")

            return utfS

    def txttex(self, txtfileS, txttypeS):
        """9b _summary_

        :return: _description_
        :rtype: _type_
        """

        soup = TexSoup(txtfileS)
        soupL = list(soup.text)
        soupS = "".join(soupL)
        soup1L = []
        soupS = soupS.replace("\\\\", "\n")
        soupL = soupS.split("\n")
        for s in soupL:
            sL = s.split("&")
            sL = s.split(">")
            try:
                soup1L.append(sL[0].ljust(10) + sL[1])
            except:
                soup1L.append(s)
        soupS = [s.replace("\\", " ") for s in soup1L]
        soupS = "\n".join(soup1L)

        return soupS

    def text(self):
        """9 insert text from file

        || text | folder | file | type 

        :param lineS: string block

        """
        plenI = 3
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
        with open(pathP, "r", encoding="utf-8") as f1:
            txtfileS = f1.read()
        with open(pathP, "r", encoding="utf-8") as f2:
            txtfileL = f2.readlines()
        j = ""
        if extS == ".txt":
            # print(f"{txttypeS=}")
            if txttypeS == "plain":
                print(txtfileS)
                return txtfileS
            elif txttypeS == "code":
                pass
            elif txttypeS == "tags":
                xtagC = parse.RivtParseTag(
                    self.folderD, self.incrD,  self.localD)
                xutfS, self.incrD, self.folderD, self.localD = xtagC.utf_parse(
                    txtfileL)
                return xutfS
        elif extS == ".html":
            utfS = self.txthtml(txtfileL)
            print(utfS)
            return utfS
        elif extS == ".tex":
            soupS = self.txttex(txtfileS, txttypeS)
            print(soupS)
            return soupS
        elif extS == ".py":
            pass

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
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return utfS

        # self.calcS += utfS + "\n"
        # self.rivtD.update(locals())

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
                vaL += [" "] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["-", "-", "-", "Total"])  # totals
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

        self.localD.update(locals())

        print(utfS + "\n")
        return utfS

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
