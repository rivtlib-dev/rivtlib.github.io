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

    def __init__(self, strL, folderD, incrD, outputS):
        """process rivt-string to UTF8 calc

            :param list strL: split rivt string
            :param dict folderD: folder paths
            :param dict incrD: numbers that increment
            :param dict outputS: output type
        """

        self.strL = strL
        self.folderD = folderD
        self.incrD = incrD
        self.outputS = outputS
        self.outputL = ["pdf", "html", "inter"]

    def r_parse(self):
        """process repo string

            :return string utfS: utf string
            :return string rstS: reST string
        """

        cmdL = ["project", "github", "append"]
        tagL = ["new]", "url]", "[readme]]", "[end]]"]

        utfS = """"""
        rstS = """"""
        for uS in self.strL:
            if uS[0:2] == "##":
                continue                    # remove review comments
            uS = uS[4:]                     # remove indent

            if uS[0:2] == "||":             # check commands
                usL = uS[2:].split("|")
                cmdS = usL[0].strip()
                if cmdS in cmdL:
                    rvttS = cutf.parsecmd(usL, cmdS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsecmd(usL, cmdS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

            if "_[" in uS:                  # check tags
                usL = uS.split("_[")
                tagS = usL[1].strip()
                if tagS in tagL:
                    rvttS = cutf.parsetag(usL[0], tagS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsetag(usL[0], tagS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

            return utfS, rstS, self.folderD, self.incrD

    def i_parse(self):
        """process insert string

            :return string utfS: utf string
            :return string rstS: reST string
        """

        cmdL = ["table", "text", "image1", "image2",]

        tagL = ["new]", "line]", "link]", "lit]", "foot]", "url]", "lnk]",
                "r]", "m]", "c]", "e]", "t]", "f]", "x]", "s]", "#]", "-]",
                "[r]]", "[c]]", "[lit]]", "[tex]]", "[texm]]", "[end]]"]

        utfS = """"""
        rstS = """"""
        for uS in self.strL:
            if uS[0:2] == "##":
                continue                    # remove review comments
            uS = uS[4:]                     # remove indent

            if uS[0:2] == "||":             # check commands
                usL = uS[2:].split("|")
                cmdS = usL[0].strip()
                if cmdS in cmdL:
                    rvttS = cutf.parsecmd(usL, cmdS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsecmd(usL, cmdS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

            if "_[" in uS:                  # check tags
                usL = uS.split("_[")
                tagS = usL[1].strip()
                if tagS in tagL:
                    rvttS = cutf.parsetag(usL[0], tagS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsetag(usL[0], tagS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

            return utfS, rstS, self.folderD, self.incrD

    def v_parse(self):
        """process values string

            :return string utfS: utf string
            :return string rstS: reST string
        """

        cmdL = ["table", "text", "image1", "image2",
                "value", "list", "function"]

        tagL = ["new]", "line]", "link]", "lit]", "foot]", "url]", "lnk]",
                "r]",  "m]", "c]", "e]", "t]", "f]", "x]", "s]", "#]", "-]",
                "[r]]", "[c]]", "[lit]]", "[tex]]", "[texm]]", "[end]]"]

        utfS = """"""
        rstS = """"""
        for uS in self.strL:
            if uS[0:2] == "##":
                continue    # remove review comments
            uS = uS[4:]                     # remove indent

            if uS[0:2] == "||":             # check commands
                usL = uS[2:].split("|")
                cmdS = usL[0].strip()
                if cmdS in cmdL:
                    rvttS = cutf.parsecmd(usL, cmdS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsecmd(usL, cmdS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

            if "_[" in uS:                  # check tags
                usL = uS.split("_[")
                tagS = usL[1].strip()
                if tagS in tagL:
                    rvttS = cutf.parsetag(usL[0], tagS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsetag(usL[0], tagS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

        locals().update(self.rivtD)
        return utfS, rstS, self.folderD, self.incrD

    def t_parse(self):
        """process table string

            :return string utfS: utf string
            :return string rstS: reST string
        """

        cmdL = ["table", "text", "image1", "image2",]

        tagL = ["new]", "line]", "link]", "lit]", "foot]", "url]", "lnk]",
                "r]",  "m]", "c]", "e]", "t]", "f]", "x]", "s]", "#]", "-]",
                "[r]]", "[c]]", "[lit]]", "[tex]]", "[texm]]", "[end]]"]

        utfS = """"""
        rstS = """"""
        for uS in self.strL:
            if uS[0:2] == "##":             # remove review comments
                continue
            uS = uS[4:]                     # remove indent

            if uS[0:2] == "||":             # check commands
                usL = uS[2:].split("|")
                cmdS = usL[0].strip()
                if cmdS in cmdL:
                    rvttS = cutf.parsecmd(usL, cmdS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsecmd(usL, cmdS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

            if "_[" in uS:                  # check tags
                usL = uS.split("_[")
                tagS = usL[1].strip()
                if tagS in tagL:
                    rvttS = cutf.parsetag(usL[0], tagS)
                    utfS += rvttS + "\n"
                    if self.outputS in self.outputL:
                        rvttS = crst.parsetag(usL[0], tagS)
                        rstS += rvttS + "\n"
                    continue
            rstS = uS
            utfS = uS

        locals().update(self.rivtD)
        return utfS, rstS, self.folderD, self.incrD
