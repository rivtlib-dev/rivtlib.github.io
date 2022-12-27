#!python
"""R2utf and R2rst classes
"""

import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import io
import logging
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate
from pathlib import Path
from numpy import *

logging.getLogger("numexpr").setLevel(logging.WARNING)
# tabulate.PRESERVE_WHITESPACE = True


class R2utf:
    """convert repo-string to UTF8 calc"""

    def __init__(self, strL: list, folderD: dict, tagD: dict):
        """process rivt-string to UTF8 calc-string

        The RvR2utf class converts repo-strings to calc-strings.

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
        """

        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.tagD = tagD
        self.valL = []  # value list

    def parseRutf(self, strL: list, cmdD: dict, cmdL: list, methL: list):
        """parse rivt-string to UTF

        Args:
            cmdL (list): command list
            methL (list): method list
            tagL (list): tag list
        """
        for uS in self.strL:
            if uS[0:2] == "##":
                continue  # remove review comment
            uS = uS[4:]  # remove indent
            if len(uS) == 0:
                print(" ")
                self.calcS += "\n"
                continue
            try:
                if uS[0] == "#":
                    continue  # remove comment
            except:
                print(" ")  # if uS[0] throws error
                self.calcS += "\n"
                continue

            self.utfS += uS.rstrip() + "\n"

        return self.calcS, self.setsectD

    def search(self, rutfL):
        """[summary]

        Args:
            rsL ([type]): [description]
        """
        a = 4

    def project(self, rutfL):
        b = 5

    def attach(self, rutfL):
        """[summary]

        Args:
            rsL ([type]): [description]
        """
        a = 4

    def report(self, rutfL):
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


class R2rst:
    """convert rivt-strings to reST strings

    Args:
    exportS (str): stores values that are written to file
    strL (list): calc rivt-strings
    folderD (dict): folder paths
    tagD (dict): tag dictionary


    """

    def __init__(self, strL: list, folderD: dict, tagD: dict):

        self.restS = """"""  # restructured text string
        self.strL = strL  # rivt-string list
        self.folderD = folderD
        self.tagD = tagD

    def _parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list):
        """parse rivt-string to reST

        Args:
            typeS (str): rivt-string type
            cmdL (list): command list
            methL (list): method list
            tagL (list): tag list
        """
        locals().update(self.rivtD)
        uL = []  # command arguments
        indxI = -1  # method index
        _rgx = r"\[([^\]]+)]_"  # find tags

        for uS in self.strL:
            if uS[0:2] == "##":
                continue  # remove comment
            uS = uS[4:]  # remove indent
            if len(uS) == 0:
                if len(self.valL) > 0:  # print value table
                    fltfmtS = ""
                    hdrL = ["variable", "value", "[value]", "description"]
                    alignL = ["left", "right", "right", "left"]
                    self._vtable(self.valL, hdrL, "rst", alignL, fltfmtS)
                    self.valL = []
                    self.restS += "\n\n"
                    self.rivtD.update(locals())
                    continue
                else:
                    # self.restS += "?x?vspace{7pt}"
                    self.restS += "\n"
                    continue
            try:
                if uS[0] == "#":
                    continue  # remove comment
            except:
                self.restS += "\n"
                continue
            if uS.strip() == "[literal]_":
                continue
            if re.search(_rgx, uS):  # check for tag
                utgS = self._tags(uS, tagL)
                self.restS += utgS.rstrip() + "\n"
                continue
            if typeS == "values":  # chk for values
                self.setcmdD["saveB"] = False
                if "=" in uS and uS.strip()[-2] == "||":  # value to file
                    uS = uS.replace("||", " ")
                    self.setcmdD["saveB"] = True
                if "=" in uS:  # assign value
                    uL = uS.split("|")
                    self._vassign(uL)
                    continue
            if typeS == "table":  # check for table
                if uS[0:2] == "||":
                    uL = uS[2:].split("|")
                    indxI = cmdL.index(uL[0].strip())
                    methL[indxI](uL)
                    continue
                else:
                    exec(uS)  # exec table code
                    continue
            if uS[0:2] == "||":  # check for cmd
                # print(f"{cmdL=}")
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip())
                methL[indxI](uL)
                continue  # call any cmd

            self.rivtD.update(locals())
            if typeS != "table":  # skip table prnt
                self.restS += uS.rstrip() + "\n"

    def r_rst(self) -> str:
        """parse repository string

        Returns:
             rstS (list): utf formatted calc-string (appended)
             setsectD (dict): section settings
        """

        rcmdL = ["search", "keys", "info", "text", "table", "pdf"]
        rmethL = [
            self._rsearch,
            self._rkeys,
            self._rinfo,
            self._itext,
            self._itable,
            self._rpdf,
        ]

        self._parseRST("repository", rcmdL, rmethL, rtagL)

    def search(self, rsL):
        a = 4

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
