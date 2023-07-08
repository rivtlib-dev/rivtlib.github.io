#
import csv
import logging
import warnings
import os
import re
import subprocess
import sys
import tempfile
import textwrap

from io import StringIO
from pathlib import Path
from io import StringIO
from pathlib import Path

import sympy as sp
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex as parsx
from tabulate import tabulate
from rivt import parse
from rivt.units import *
from rivt.tag_parse import Tags


class TagsMD(Tags):
    """convert rivt tags to md

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

    def __init__(self, lineS, incrD, folderD, tagsD, localD):
        """convert rivt tags to md or reST

        """

        self.lineS = lineS
        self.tagsD = tagsD
        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.widthI = incrD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

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

    def bold(self):
        """bold text _[b]

        :return lineS: bold line
        :rtype: str
        """
        print(self.lineS)
        return self.lineS

    def italic(self):
        """italicize text _[i]

        :return lineS: centered line
        :rtype: str
        """
        print(self.lineS)
        return self.lineS

    def center(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = self.lineS.center(int(self.widthI))
        print(lineS)
        return lineS

    def boldcenter(self):
        """center text _[bc]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.center(int(self.widthI))

        print(lineS)

    def bolditalic(self):
        """center text _[bc]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.center(int(self.widthI))

        print(lineS)
        return lineS

    def right(self):
        """right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """

        lineS = self.lineS.rjust(int(self.widthI))

        return lineS

    def label(self, labelS, numS):
        """format labels for equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """
        secS = str(self.incrD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS
        # store for equation table
        self.incrD["eqlabelS"] = self.lineS + " [" + numS.zfill(2) + "]"
        return labelS

    def description(self):
        """footnote description _[d]

        :return lineS: footnote
        :rtype: str
        """
        ftnumI = self.incrD["noteL"].pop(0)
        lineS = "[" + str(ftnumI) + "] " + self.lineS
        print(lineS)
        return lineS

    def equation(self):
        """md equation label _[e]

        :return lineS: md equation label
        :rtype: str
        """

        enumI = int(self.incrD["equI"]) + 1
        fillS = str(enumI).zfill(2)
        wI = self.incrD["widthI"]
        refS = self.label("E", fillS)
        spcI = len("Equ. " + fillS + " - " + self.lineS.strip())
        lineS = "Equ. " + fillS + " - " + self.lineS.strip() \
            + refS.rjust(wI-spcI)
        self.incrD["equI"] = enumI

        print(lineS)
        return lineS

    def figure(self):
        """md figure caption _[f]

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.incrD["figI"])
        sectnumI = self.incrD["secnumI"]
        fillS = str(fnumI).zfill(2)
        sectnumS = "[" + str(sectnumI) + "]"
        lineS = sectnumS + " Fig. " + fillS + " - " + self.lineS
        self.incrD["figI"] = fnumI + 1

        print(lineS + "\n")
        return lineS + "\n"

    def foot(self):
        """footnote number _[#]


        """
        ftnumI = self.incrD["footL"].pop(0)
        self.incrD["noteL"].append(ftnumI + 1)
        self.incrD["footL"].append(ftnumI + 1)
        lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")
        print(lineS)
        return lineS

    def latex(self):
        """format latex

        :return lineS: formatted latex
        :rtype: str
        """
        txS = self.lineS
        # txS = txs.encode('unicode-escape').decode()
        ptxS = sp.parse_latex(txS)
        lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))

        print(lineS)
        return lineS

    def plain(self):
        """format plain literal text _[p]

        :param lineS: _description_
        :type lineS: _type_
        """
        print(self.lineS)
        return self.lineS

    def sympy(self):
        """format line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """

        spS = self.lineS.strip()
        # try:
        #     spL = spS.split("=")
        #     spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        #     # sps = sp.encode('unicode-escape').decode()
        # except:
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

        print(lineS)
        return lineS

    def table(self):
        """format table title  _[t]

        :return lineS: md table title
        :rtype: str
        """
        sectnumI = self.incrD["secnumI"]
        tnumI = int(self.incrD["tableI"])
        fillS = str(tnumI).zfill(2)
        sectnumS = "[" + str(sectnumI) + "]"
        lineS = sectnumS + " Table " + fillS + " - " + self.lineS
        self.incrD["tableI"] = tnumI + 1

        print(lineS)
        return lineS

    def link(self):
        """format url or internal link _[link]

        :return: _description_
        :rtype: _type_
        """
        lineL = self.lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]
        print(lineS)
        return lineS

    def page(self):
        """insert new page header _[page]

        :return lineS: page header
        :rtype: str
        """
        pagenoS = str(self.incrD["pageI"])
        rvtS = self.incrD["headuS"].replace("p##", pagenoS)
        self.incrD["pageI"] = int(pagenoS)+1
        lineS = "\n"+"_" * self.incrD["widthI"] + "\n" + rvtS +\
                "\n"+"_" * self.incrD["widthI"] + "\n"
        return "\n" + rvtS

    def underline(self):
        """underline _[u]

        :return lineS: underline
        :rtype: str
        """
        return self.lineS

    def centerblk(self):
        """

        """
        lineS = ""
        for i in self.lineS:
            lineS += i.center(int(self.widthI))

        return lineS

    def latexblk(self):
        pass

    def mathblk(self):
        pass

    def codeblk(self):
        pass

    def rightblk(self):
        pass

    def shadeblk(self):
        """ start shade block _[[s]]

        :param lineS: _description_
        :type lineS: _type_
        """
        pass

    def quitblock(self):
        """ quit shade block _[[q]]

        :param lineS: _description_
        :type lineS: _type_
        """
        pass

    def tagblk(self):
        pass
