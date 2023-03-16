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
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from datetime import datetime
from IPython.display import display as _display
from IPython.display import Image as _Image
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass


class TagsRST():

    def __init__(self, lineS, folderD, incrD):
        """format tags to reST

        ============================ ============================================
        tag syntax                      description (one tag per line)
        ============================ ============================================

        Values Only Formats: 
        a = n | unit, alt | descrip   assign tag =; units and description
        a := b + c | unit, alt | n,n  result tag :=; units and decimals

        Format Line: 
        text _[b]                     bold line
        text _[c]                     center line
        _[date]                       date insert
        text _[e]                     equation label, autonumber
        text _[f]                     figure caption, autonumber
        text <#>                      footnote, autonumber
        text _[n]                     footnote description 
        _[-]                          horizontal divider insert
        text _[i]                     italicize line
        <reference, label>            internal link, section etc
        latex equation _[x]           LaTeX equation format
        text _[r]                     right justify line
        text _[s]                     sympy equation
        <sympy text>                  sympy inline (no commas)
        _[p]                          new page (PDF)
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

        self.tagD = {"b]": "bold", "c]": "center", "d]": "date", "i]": "italic",
                     "e]": "equation", "f]": "figure", "#]": "footnumber",
                     "foot]": "footnote", "-]": "line", "x]": "latex", "lnk]": "link",
                     "p]": "page", "r]": "right", "s]": "sympy", "t]": "table",
                     "url]": "url", "[o]]": "codeblk", "[c]]": "centerblk",
                     "[x]]": "latexblk", "[m]]": "mathblk", "[r]]": "rightblk",
                     "=": "assign", ":=": "result"}

    def tag_parse(self, tagS):
        """_summary_
        """

        return eval("self." + self.tagD[tagS] + "()")

    def label(self, objI, text):
        """reST labels equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """

        objfillS = str(objI).zfill(2)
        if type(text) == int:
            sfillS = str(self.incrD["snumI"]).strip().zfill(2)
            labelS = sfillS
        else:
            dnumSS = str(self.incrD["docnumS"])
            labelS = dnumSS + "." + objfillS

        return labelS

    def bold(self):
        """reST formats line to bold

        :return lineS: bold line of text
        :rtype: str
        """

        lineS = "**"+lineS+"**"

        return lineS

    def center(self):
        """reST formats text to center of document width

        :return lineS: centered line
        :rtype: str
        """

        lineS = "?x?begin{center} " + self.lineS + "?x?end{center}"

        return lineS

    def date(self):
        """insert reST date and time

        :return lineS: date reST string
        :rtype: str
        """

        lineS = datetime.today().strftime('%Y-%m-%d')

        return lineS

    def equation(self):
        """format equation label

        :return lineS: equation label
        :rtype: str
        """

        enumI = int(self.incrD["enumI"]) + 1
        self.incrD["enumI"] = enumI
        refS = self.label(enumI, "[ Equ: ") + " ]"
        lineS = "**" + self.lineS + "**" + " ?x?hfill " + refS

        return lineS

    def figure(self):
        """format figure caption

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.incrD["fnumI"]) + 1
        self.incrD["fnumI"] = fnumI
        refS = self.label(fnumI, "[ Fig: ") + " ]"
        lineS = "**" + self.lineS + "**" + " ?x?hfill " + refS

        return lineS

    def footnumber(self):
        """increment footnote number
        """

        ftnumI = self.incrD["ftqueL"][-1] + 1
        self.incrD["ftqueL"].append(ftnumI)

    def footnote(self):
        """insert footnote

        :return lineS: footnote
        :rtype: str
        """

        lineS = ".. [*] " + self.lineS

        return lineS

    def italic(self):
        """italicizes line

        :return lineS: italicized line
        :rtype: str
        """

        lineS = "*"+lineS+"*"

        return lineS

    def line(self):
        """_summary_

        :param lineS: _description_
        :type lineS: _type_
        """

        lineS = int(self.incrD["swidthI"]) * "-"

        return lineS

    def latex(self):
        """format line of latex

        :return lineS: reST formatted latex
        :rtype: str
        """

        lineS = ".. raw:: math\n\n   " + self.lineS + "\n"

        return lineS

    def link(self):
        pass

    def page(self):
        """insert page break line

        :return lineS: page break line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n ?x?newpage \n"

        return lineS

    def right(self):
        """right justify text

        :return lineS: right justified text
        :rtype: str
        """

        lineS = "?x?hfill " + lineS

        return lineS

    def sympy(self):
        """reST format line of sympy

        :return lineS: formatted sympy
        :rtype: str
        """

        spS = self.lineS
        txS = sp.latex(S(spS))
        lineS = ".. raw:: math\n\n   " + txS + "\n"

        return lineS

    def table(self):
        """format table title to reST

        :return lineS: figure label
        :rtype: str
        """

        tnumI = int(self.incrD["tnumI"]) + 1
        self.incrD["tnumI"] = tnumI
        refS = self.label(tnumI, "[Table: ") + "]"
        lineS = "**" + refS + "**" + " ?x?hfill  " + refS

        return lineS

    def time(self):
        """insert reST date and time 

        :return lineS: date and time reST string
        :rtype: str
        """

        lineS = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        return lineS

    def url(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """

        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

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
