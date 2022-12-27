"""I2utf and I2rst classes
"""

import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import logging
import time
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

logging.getLogger("numexpr").setLevel(logging.WARNING)
# tabulate.PRESERVE_WHITESPACE = True


class I2utf:
    """convert insert-string to UTF8 calc"""

    def __init__(self, strL: list, folderD, cmdD, sectD):
        """convert insert-string to UTF8 calc-string

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
        """

        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.sectD = sectD
        self.cmdD = cmdD

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

    def parseUTF(self, cmdL: list, methL: list, tagL: list):
        """parse rivt-string to UTF

        Args:
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
                continue  # remove review comment
            uS = uS[4:]  # remove indent
            if len(uS) == 0:
                if len(self.valL) > 0:  # print value table
                    hdrL = ["variable", "value", "[value]", "description"]
                    alignL = ["left", "right", "right", "left"]
                    self._vtable(self.valL, hdrL, "rst", alignL)
                    self.valL = []
                    print(uS.rstrip(" "))
                    self.calcS += " \n"
                    self.rivtD.update(locals())
                    continue
                else:
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
            if re.search(_rgx, uS):  # check for tag
                utgS = self._tags(uS, tagL)
                print(utgS.rstrip())
                self.calcS += utgS.rstrip() + "\n"
                continue
            if typeS == "values":
                self.setcmdD["saveB"] = False
                if "=" in uS and uS.strip()[-2] == "||":  # set save flag
                    uS = uS.replace("||", " ")
                    self.setcmdD["saveB"] = True
                if "=" in uS:  # just assign value
                    uL = uS.split("|")
                    self._vassign(uL)
                    continue
            if typeS == "table":
                if uS[0:2] == "||":  # check for command
                    uL = uS[2:].split("|")
                    indxI = cmdL.index(uL[0].strip())
                    methL[indxI](uL)
                    continue
                else:
                    exec(uS)  # otherwise exec Python code
                    continue
            if uS[0:2] == "||":  # check for command
                uL = uS[2:].split("|")
                indxI = cmdL.index(uL[0].strip())
                methL[indxI](uL)
                continue

            if typeS != "table":  # skip table print
                print(uS)
                self.calcS += uS.rstrip() + "\n"
            self.rivtD.update(locals())


class I2rst:
    """convert rivt-strings to reST strings

    Args:
    exportS (str): stores values that are written to file
    strL (list): calc rivt-strings
    folderD (dict): folder paths
    setcmdD (dict): command settings
    setsectD (dict): section settings
    rivtD (dict): global rivt dictionary

    """

    def __init__(
        self,
        strL: list,
        folderD: dict,
        setcmdD: dict,
        setsectD: dict,
        rivtD: dict,
        exportS: str,
    ):
        self.restS = """"""  # restructured text string
        self.exportS = exportS  # value export string
        self.strL = strL  # rivt-string list
        self.valL = []  # value blocklist
        self.folderD = folderD
        self.setsectD = setsectD
        self.setcmdD = setcmdD
        self.rivtD = rivtD

    def parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list):
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

    def i_rst(self) -> tuple:
        """parse insert-string

        Returns:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
        """

        icmdL = ["text", "table", "image"]
        imethL = [
            self._itext,
            self._itable,
            self._iimage,
        ]

        self._parseRST("insert", icmdL, imethL, itagL)

        return self.restS, self.setsectD, self.setcmdD
