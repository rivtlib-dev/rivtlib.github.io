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


def parsetag(lineS, tagS, folderD, incrD):
    """
    ============================ ============================================
    tag syntax                       description
    ============================ ============================================

    Values Format:                Applies only to Values rivt-string
    a = n | unit, alt | descrip   tag is =; units and description
    a <= b + c | unit, alt | n,n  tag is <=; units and decimals

    Format Line of Text:          Applies to I,V,T methods
    text _[b]                     bold
    text _[c]                     center text
    text _[i]                     italic
    text _[l]                     literal text
    text _[p]                     paragraph heading
    text _[r]                     right justify text
    text _[-]                     draw horizontal line
    text _[#]                     insert footnote, autonumber
    text _[foot]                  footnote description

    Format Element:               Applies to I,V,T methods
    label _[e]                    equation label, autonumber
    caption _[f]                  figure caption, autonumber
    sympy equation _[s]           format sympy equation
    title _[t]                    table title, autonumber
    latex equation _[x]           format LaTeX equation

    Format Link:                  Applies to I,V,T methods
    _[date]                       insert date
    _[new]                        new PDF page
    _[time]                       insert time
    reference, label _[lnk]       section, paragraph, title, caption
    address, label _[url]         http://xyz, link label

    Format Block of Text:         Applies to I,V,T method
    _[[code]]                     code text block
    _[[c]]                        center text block
    _[[end]]                      terminates block
    _[[lit]]                      literal block
    _[[r]]                        right justify text block
    _[[tex]]                      LateX block
    _[[texm]]                     LaTeX math block

    """

    tagD = {"b]": "bold", "c]": "center", "=": "equal",
            "#]": "footnumber", "foot]": "footnote", "i]": "italic",
            "l]": "literal", "-]": "line", "p]": "paragraph", "r]": "right",
            "<=": "result", "date]": "date", "new]": "page",
            "e]": "equation", "f]": "figure", "s]": "sympy", "t]": "table", "x]": "latex",
            "lnk]": "link", "lit]": "literal", "url]": "url",
            "[code]]": "codeblk", "[c]]": "centerblk", "[lit]]": "literalblk",
            "[tex]]": "latexblk", "[texm]]": "mathblk", "[r]]": "rightblk"}

    utfS = """"""
    func = globals()[tagD[tagS]]
    utfL = func(lineS, folderD, incrD)
    swidthII = incrD["swidthI"] - 1

    return utfL


def label(self, objnumI, typeS, folderD, incrD):
    """labels for equations, tables and figures

        :objnumI (int): equation, table or figure numbers
        :setsectD (dict): section dictionary
        :typeS (str): label type
        :return str: formatted label
    """

    objfillS = str(objnumI).zfill(2)
    if type(typeS) == str:
        sfillS = str(incrD["snumS"]).strip().zfill(2)
        labelS = typeS + sfillS
    else:
        cnumSS = str(incrD["cnumS"])
        labelS = typeS + cnumSS + "." + objfillS

    return labelS


def bold(lineS, folderD, incrD):
    """_summary_

    :param lineS: _description_
    :type lineS: _type_
    :param folderD: _description_
    :type folderD: _type_
    :param incrD: _description_
    :type incrD: _type_
    :return: _description_
    :rtype: _type_
    """

    return lineS, folderD, incrD


def center(lineS, folderD, incrD):
    """_summary_

    :param lineS: _description_
    :type lineS: _type_
    :param folderD: _description_
    :type folderD: _type_
    :param incrD: _description_
    :type incrD: _type_
    :return: _description_
    :rtype: _type_
    """

    lineS = lineS.center(int(incrD["widthI"]))
    tagL = tagS.strip().split("[c]_")
    uS = (tagL[0].strip()).rjust(swidthII)

    return lineS, folderD, incrD


def equal(lineS, folderD, incrD):

    return lineS, folderD, incrD


def footnumber():

    ftnumII = self.setsectD["ftqueL"][-1] + 1
    self.setsectD["ftqueL"].append(ftnumII)
    uS = tagS.replace("[x]_", "[" + str(ftnumII) + "]")


def footnote():

    tagS = tagS.strip("[foot]_").strip()
    uS = self.setsectD["ftqueL"].popleft() + tagS

    pass


def italic(lineS, folderD, incrD):
    """_summary_

    :param lineS: _description_
    :type lineS: _type_
    :param folderD: _description_
    :type folderD: _type_
    :param incrD: _description_
    :type incrD: _type_
    :return: _description_
    :rtype: _type_
    """

    return lineS, folderD, incrD


def literal(lineS, folderD, incrD):

    return lineS, folderD, incrD


def line(lineS, folderD, incrD):
    """_summary_

    :param lineS: _description_
    :type lineS: _type_
    """
    uS = int(folderD["swidthI"]) * "-"


def literal():
    pass


def new():
    uS = int(self.setsectD["swidthI"]) * "."


def paragraph():
    pass


def right():

    tagL = tagS.strip().split("[r]_")
    uS = (tagL[0].strip()).rjust(swidthII)
    pass


def sympy(lineS, folderD, incrD):

    spS = tagL[0].strip()
    spL = spS.split("=")
    spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
    # sps = sp.encode('unicode-escape').decode()
    lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

    return lineS, folderD, incrD


def url():

    tgS = tagS.strip("[link]_").strip()
    tgL = tgS.split("|")
    uS = tgL[0].strip() + " : " + tgL[1].strip()


def latex():

    tagL = tagS.strip().split("[x]_")
    txS = tagL[0].strip()
    # txS = txs.encode('unicode-escape').decode()
    ptxS = sp.parse_latex(txS)
    uS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))


def equation(lineS, folderD, incrD):

    enumI = int(self.setsectD["enumI"]) + 1
    incrD["enumI"] = enumI
    refS = label(enumI, "[ Equ: ") + " ]"
    spcI = incrD["widthI"] - len(refS) - len(tagL[0].strip())
    lineS = tagL[0].strip() + " " * spcI + refS

    return lineS, folderD, incrD


def figure(lineS, folderD, incrD):

    fnumI = int(incrD["fnumI"]) + 1
    incrD["fnumI"] = fnumI
    refS = label(fnumI, "[ Fig: ") + " ]"
    spcI = incrD["widthI"] - len(refS) - len(tagL[0].strip())
    lineS = lineS.strip() + " " * spcI + refS

    return lineS, folderD, incrD


def table():
    tagL = tagS.strip().split("[t]_")
    tnumI = int(self.setsectD["tnumI"]) + 1
    self.setsectD["tnumI"] = tnumI
    refS = self._label(tnumI, "[Table: ") + " ]"
    spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
    uS = tagL[0].strip() + " " * spcI + refS
