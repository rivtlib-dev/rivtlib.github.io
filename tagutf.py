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
from datetime import datetime
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass


class TagsUTF:

    def __init__(self, lineS, folderD, incrD):
        """format tags to utf

        ============================ ============================================
        tag syntax                      description (one tag per line)
        ============================ ============================================

        Values Only Formats: 
        a = n | unit, alt | descrip   assign tag =; units and description
        a := b + c | unit, alt | n,n  result tag :=; units and decimals

        Format Line: 
        text _[c]                     center line
        _[date]                       date insert
        text _[e]                     equation label, autonumber
        text _[f]                     figure caption, autonumber
        text <#>                      footnote, autonumber
        text _[foot]                  footnote description 
        _[-]                          horizontal divider insert
        <reference, label>            internal link, section etc
        latex equation _[x]           LaTeX equation format
        text _[r]                     right justify line
        text _[s]                     sympy equation
        <sympy text>                  sympy inline (no commas)
        _[page]                       new page (PDF)
        _[time]                       time (insert)
        title _[t]                    table title, autonumber
        <http: address, label>        url reference, http:\\xyz


        Format Block:
        _[[c]]                        center text block
        _[[o]]                        code text block
        _[[e]]                        end of block
        _[[l]]                        literal block
        _[[r]]                        right justify text block
        _[[x]]                        LateX block
        _[[m]]                        LaTeX math block

        """

        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.swidthII = incrD["widthI"] - 1
        self.errlogP = folderD["errlogP"]

        self.tagD = {"c]": "center",  "#]": "footnumber", "foot]": "footnote",
                     "-]": "line", "r]": "right",  "date]": "date",
                     "page]": "page", "e]": "equation", "f]": "figure", "sym]": "sympy",
                     "t]": "table", "x]": "latex", "lnk]": "link", "url]": "url",
                     "[o]]": "codeblk", "[c]]": "centerblk", "[x]]": "latexblk",
                     "[m]]": "mathblk", "[r]]": "rightblk",
                     "=": "assign", ":=": "result"}

        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        # print(f"{modnameS=}")
        logconsole = logging.StreamHandler()
        logconsole.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(levelname)-8s" + modnameS + "   %(message)s")
        logconsole.setFormatter(formatter)
        logging.getLogger("").addHandler(logconsole)
        warnings.filterwarnings("ignore")

    def tag_parse(self, tagS):
        """_summary_
        """
        print(f"*****{self.tagD[tagS]=}")
        return eval("self." + self.tagD[tagS] + "()")

    def label(self, objI, text):
        """format labels for equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """

        objfillS = str(objI).zfill(2)
        if type(text) == int:
            sfillS = str(self.incrD["snumI"]).strip().zfill(2)
            labelS = text + sfillS
        else:
            dnumSS = str(self.incrD["docnumS"])
            labelS = text + dnumSS + "." + objfillS

        return labelS

    def center(self):
        """center text in document width

        :return lineS: centered line
        :rtype: str
        """

        lineS = lineS.center(int(self.incrD["widthI"]))

        return lineS

    def date(self):
        """insert date

        :return lineS: date string
        :rtype: str
        """

        lineS = datetime.today().strftime('%Y-%m-%d')

        return lineS

    def equation(self):
        """formats equation label to utf

        :return lineS: reST equation label
        :rtype: str
        """

        enumI = int(self.incrD["enumI"]) + 1
        self.incrD["enumI"] = enumI
        refS = self.label(enumI, "[ Equ: ") + " ]"
        spcI = self.incrD["widthI"] - len(refS) - len(self.lineS)
        utfS = self.lineS + " " * spcI + refS

        return utfS

    def figure(self):
        """formats figure caption to reST

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.incrD["fignumI"]) + 1
        self.incrD["fignumI"] = fnumI
        refS = self.label(fnumI, " Fig. [ ") + " ]"
        spcI = self.incrD["widthI"] - len(refS) - len(self.lineS)
        utfS = self.lineS + " " * spcI + refS

        return utfS

    def footnumber(self):
        """increment footnote number
        """

        ftnumI = self.incrD["ftqueL"][-1] + 1
        self.incrD["ftqueL"].append(ftnumI)
        lineS = self.lineS.replace("[#]", "[" + str(ftnumI) + "]")

        return lineS

    def footnote(self):
        """insert footnote

        :return lineS: footnote
        :rtype: str
        """

        lineS = ".. [*] " + self.lineS

        return lineS

    def line(lineS, folderD, incrD):
        """_summary_

        :param lineS: _description_
        :type lineS: _type_
        """
        lineS = int(folderD["widthI"]) * "_"

        return lineS

    def latex(self):
        """format line of sympy

        :return lineS: formatted latex
        :rtype: str
        """
        txS = self.lineS
        # txS = txs.encode('unicode-escape').decode()
        ptxS = sp.parse_latex(txS)
        lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))

        return lineS

    def link(self):
        pass

    def page(self):
        """insert page break line

        :return lineS: page break line
        :rtype: str
        """

        lineS = int((self.incrD["widthI"])/3) * " - "

        return lineS

    def right(self):
        """right justify text

        :return lineS: right justified text
        :rtype: str
        """

        lineS = lineS.rjust(int(self.incrD["widthI"]))

        return lineS

    def sympy(self):
        """format line of sympy

        :return lineS: formatted sympy
        :rtype: str
        """

        spS = self.lineS
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        # sps = sp.encode('unicode-escape').decode()
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

        return lineS

    def table(self):
        """format table title to utf

        :return lineS: utf table title
        :rtype: str
        """

        enumI = int(self.incrD["tnumI"]) + 1
        self.incrD["tnumI"] = enumI
        refS = self.label(enumI, "[ Equ: ") + " ]"
        spcI = self.incrD["widthI"] - len(refS) - len(self.lineS)
        utfS = self.lineS + " " * spcI + refS

        return utfS

    def time(self):
        """insert date and time

        :return lineS: centered line
        :rtype: str
        """

        lineS = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        return lineS

    def url(self):
        pass

    def codeblk(self):
        pass

    def centerblk(self):
        pass

    def endblk(self):
        pass

    def latexblk(self):
        pass

    def mathblk(self):
        pass

    def rightblk(self):
        pass

    def assign(self):
        pass

    def result(self):
        pass
