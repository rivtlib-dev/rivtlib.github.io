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


class CmdRST:
    """convert rivt-strings to reST strings

    Args:
    exportS (str): stores values that are written to file
    strL (list): calc rivt-strings
    folderD (dict): folder paths
    tagD (dict): tag dictionary


    """

    def __init__(self, paramL, folderD, incrD):
        """
        ======================================================== ============
            command syntax / snippet prefix and description        methods
        ======================================================== ============

        || append | file_name | ./docfolder; default / resize;default   R
        || github | repo_name; none | readme; noneparam                 R
        || project | file_name | /docsfolder; default                   R

        || list | file_name  | [:];[x:y]                                V
        || functions | file_name | docs; nodocs                         V
        || values | file_name | [:];[x:y]                               V

        || image1 | file_name  | .50                                  I,V,T
        || image2 | file_name  | .40 | file_name  | .40               I,V,T
        || table | file_name |  [:] | 60 r;l;c                        I,V,T
        || text | file_name | shade; noshade                          I,V,T

        """

        self.folderD = folderD
        self.incrD = incrD
        self.widthII = incrD["widthI"] - 1
        self.rL = paramL

    def cmd_parse(self, cmdS):
        """_summary_
        """

        return eval("self." + cmdS + "()")

    def r_rst(self, typeS: str, cmdL: list, methL: list, tagL: list):
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
            uS = uS[4:]  # remove indent
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

    def i_rst(self) -> tuple:
        """parse insert-string

        Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings

        convert rivt-strings to reST strings

        Args:
        :param exportS (str): stores values that are written to file
        :param strL (list): calc rivt-strings
        folderD (dict): folder paths
        setcmdD (dict): command settings
        setsectD (dict): section settings
        rivtD (dict): global rivt dictionary

        """

        icmdL = ["text", "table", "image"]
        imethL = [
            self._itext,
            self._itable,
            self._iimage,
        ]

        self._parseRST("insert", icmdL, imethL, itagL)
        return self.restS, self.setsectD, self.setcmdD

    def v_rst(self) -> tuple:
        """parse value-string and set method

        Return:
        calcS (list): utf formatted calc-string (appended)
        setsectD (dict): section settings
        setcmdD (dict): command settings
        rivtD (list): calculation results
        exportS (list): value strings for export
        """

        locals().update(self.rivtD)
        vcmdL = ["config", "value", "data", "func", "text", "table", "image"]
        vmethL = [
            self._vconfig,
            self._vvalue,
            self._vdata,
            self._vfunc,
            self._itext,
            self._itable,
            self._iimage,
        ]

    def t_rst(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation values
        """

        tcmdL = ["text", "table", "image"]
        tmethL = [self._itext, self._itable, self._iimage]

        self._parseUTF("table", tcmdL, tmethL, ttagL)

        return self.calcS, self.setsectD, self.setcmdD, self.rivtD


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
