import sys
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
from rivt import cmd_rst as crst
from rivt import cmd_utf as cutf

logging.getLogger("numexpr").setLevel(logging.WARNING)
# tabulate.PRESERVE_WHITESPACE = True


class RivtParse:
    """process rivt-string"""

    def __init__(self, folderD, incrD,  outputS, methS):
        """process rivt-string to UTF8 calc

            :param dict folderD: folder paths
            :param dict incrD: numbers that increment
            :param dict outputS: output type
            :param dict outputS: output type
        """

        self.folderD = folderD  # folder paths
        self.incrD = incrD      # incrementing formats
        self.outputS = outputS  # output type
        self.outputL = ["pdf", "html", "both"]  # reST formats

        # valid commands and tags
        if methS == "R":
            self.cmdL = ["project", "github", "append"]
            self.tagL = ["new]", "url]"]
            self.blockL = ["[readme]]"]
        elif methS == "I":
            self.cmdL = ["table", "text", "image1", "image2"]
            self.tagL = ["new]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        elif methS == "V":
            self.cmdL = ["table", "text", "image1", "image2",
                         "value", "list", "function", "=", ":="]
            self.tagL = ["new]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        elif methS == "T":
            self.cmdL = ["table", "text", "image1", "image2"]
            self.tagL = ["new]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        else:
            pass

    def str_parse(self, strL):
        """parse insert string

            :param list strL: split rivt string
            :return utfS: utf formatted string
            :return rstS: reST formatted string
            :return incrD: increment references
            :return folderD: folder paths
            :rtype utfS: string
            :rtype rstS: string
            :rtype folderD: dictionary
            :rtype incrD: dictionary
        """

        utfS = """"""
        rstS = """"""
        blockB = False
        for uS in strL:
            if uS[0:2] == "##":
                continue                    # remove review comments
            uS = uS[4:]                     # remove indent

            if blockB:                      # block accumulator
                lineS += uS
            if blockB and uS.strip() == "[end]]":
                rvttS = cutf.parsetag(lineS, tagS, self.strL)
                utfS += rvttS + "\n"
                if self.outputS in self.outputL:
                    rvttS = crst.parsetag(lineS, tagS, self.strL)
                    rstS += rvttS + "\n"
                blockB = False
            elif uS[0:2] == "||":            # find commands
                usL = uS[2:].split("|")
                paramL = usL[1:]
                cmdS = usL[0].strip()
                if cmdS in self.cmdL:
                    rvttS = cutf.parsecmd(paramL, cmdS, self.strL)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsecmd(paramL, cmdS, self.strL)
                        rstS += rvttS + "\n"
                    continue
            elif "_[" in uS:                 # find tags
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS in self.tagL:
                    rvttS = cutf.parsetag(lineS, tagS,
                                          self.folderD, self.incrD)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsetag(lineS, tagS,
                                              self.folderD, self.incrD)
                        rstS += rvttS + "\n"
                if tagS[0] == "[":
                    blockB = True
                continue
            else:
                rstS = uS
                utfS = uS

            return utfS, rstS, self.folderD, self.incrD
