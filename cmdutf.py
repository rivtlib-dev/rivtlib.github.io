#
import csv
import logging
import warnings
import fnmatch
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import html2text as htm
import configparser
from io import StringIO
from numpy import *
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from datetime import datetime
from TexSoup import TexSoup
from rivt import parse
from rivt.units import *
from cmd import Commands


class CmdMD(Commands):

    def __init__(self, paramL, incrD, folderD,  localD):
        """_summary_

        :param paramL: _description_
        :type paramL: _type_
        :param incrD: _description_
        :type incrD: _type_
        :param folderD: _description_
        :type folderD: _type_
        :param localD: _description_
        :type localD: _type_
        :return: _description_
        :rtype: _type_
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

        fileS = paramL[0].strip()
        if fileS[0:4] == "data":
            self.currP = folderD["docpathP"]
            self.relP = fileS
        elif fnmatch.fnmatch(fileS[0:5], "r[0-9]"):
            self.currP = Path(folderD["pubP"])
        else:
            self.currP = Path(folderD["prvP"])

    def project(self):
        """insert project information from txt

            :return lineS: utf text
            :rtype: str
        """

        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}

        tableS = ""
        plenI = 2
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} not evaluated: {plenI} parameters required")
            return

        folderP = Path(self.folderD["prvP"])
        fileP = Path(self.paramL[0].strip())
        pathP = Path(folderP, fileP)                    # file path
        extS = (pathP.suffix).strip()
        txttypeS = self.paramL[1].strip()
        with open(pathP, "r", encoding="utf-8") as f2:
            txtfileL = f2.readlines()
        j = ""
        if extS == ".txt":
            # print(f"{txttypeS=}")
            if txttypeS == "plain":
                for iS in txtfileL:
                    j += "   " + iS
                return "\n\n::\n\n" + j + "\n\n"
            elif txttypeS == "rivttags":
                xtagC = parse.RivtParseTag(
                    self.folderD, self.incrD,  self.localD)
                xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(
                    txtfileL)
                return xrstS
        else:
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
            return

    def image(self):
        """insert image(s) from files

        """
        mdS = ""
        iL = self.paramL
        if len(iL[0].split(",")) == 1:
            file1S = iL[0].strip()
            scale1S = iL[1].strip()
            imgS = "<img src=" + file1S + " width=" + \
                scale1S + "% alt=" + file1S + ">"
            mdS = imgS
        elif len(iL[0].split(",")) == 2:
            iL = iL[0].split(",")
            file1S = iL[0].strip()
            file2S = iL[1].strip()
            iL = iL[1].split(",")
            scale1S = iL[0]
            scale2S = iL[1]
            imgS = "<img src=" + file1S + " width=" + \
                scale1S + "% alt=" + file1S + "<img src=" + \
                file2S + " width=" + scale2S + "% alt=" + file2S + ">"
            mdS = imgS

        print(mdS)
        return mdS

    def table(self):
        """insert table from csv or xlsx file

            :return lineS: md table
            :rtype: str
        """

        tableS = ""
        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}
        plenI = 2
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return

        fileP = Path(self.paramL[0].strip())
        prfxP = self.folderD["docpathP"]
        if str(fileP)[0:4] == "data":
            pathP = Path(prfxP, fileP)                       # file path
        elif str(fileP)[0:4] == "data":
            pass
        else:
            pass
        maxwI = int(self.paramL[1].split(",")[0])        # max column width
        keyS = self.paramL[1].split(",")[1].strip()
        alignS = alignD[keyS]
        extS = pathP.suffix[1:]
        # print(f"{extS=}")
        if extS == "csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == "xlsx":                            # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
            return

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(
            readL,
            tablefmt="html",
            headers="firstrow",
            numalign="decimal",
            maxcolwidths=maxwI,
            stralign=alignS))

        tableS = output.getvalue()
        sys.stdout = old_stdout

        print(tableS)
        return tableS

    def text(self):
        """insert text from file

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
        with open(pathP, "r", encoding="md-8") as f1:
            txtfileS = f1.read()
        with open(pathP, "r", encoding="md-8") as f2:
            txtfileL = f2.readlines()
        j = ""
        if extS == ".txt":
            # print(f"{txttypeS=}")
            if txttypeS == "plain":
                print(txtfileS)
                return txtfileS
            elif txttypeS == "code":
                pass
            elif txttypeS == "rivttags":
                xtagC = parse.RivtParseTag(
                    self.folderD, self.incrD,  self.localD)
                xmdS, self.incrD, self.folderD, self.localD = xtagC.md_parse(
                    txtfileL)
                return xmdS
        elif extS == ".html":
            mdS = self.txthtml(txtfileL)
            print(mdS)
            return mdS
        elif extS == ".tex":
            soupS = self.txttex(txtfileS, txttypeS)
            print(soupS)
            return soupS
        elif extS == ".py":
            pass
