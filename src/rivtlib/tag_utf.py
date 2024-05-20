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
from rivtlib import parse
from rivtlib.units import *
from rivtlib.tag_parse import Tags


class TagsUTF(Tags):
    """convert rivt tags to md

    :param paramL: _description_
    :type paramL: _type_
    :param labelD: _description_
    :type labelD: _type_
    :param folderD: _description_
    :type folderD: _type_
    :param localD: _description_
    :type localD: _type_
    :return: _description_
    :rtype: _type_
    """

    def __init__(self, lineS, labelD, folderD, tagsD, localD):
        """convert rivt tags to md or reST

        """

        self.lineS = lineS
        self.tagsD = tagsD
        self.localD = localD
        self.folderD = folderD
        self.labelD = labelD
        self.lineS = lineS
        self.widthI = labelD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

        modnameS = self.labelD["modnameS"]
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

    def center(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = self.lineS.center(int(self.widthI))
        print(lineS)
        return lineS

    def italic(self):
        """italicize text _[i]

        :return lineS: centered line
        :rtype: str
        """
        print(self.lineS)
        return self.lineS

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

    def bolditaliccenter(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.rjust(int(self.widthI))

        print(lineS)
        return lineS

    def italiccenter(self):
        """center text _[c]

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
        secS = str(self.labelD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS
        # store for equation table
        self.labelD["eqlabelS"] = self.lineS + " [" + numS.zfill(2) + "]"
        return labelS

    def description(self):
        """footnote description _[d]

        :return lineS: footnote
        :rtype: str
        """
        ftnumI = self.labelD["noteL"].pop(0)
        lineS = "[" + str(ftnumI) + "] " + self.lineS
        print(lineS)
        return lineS

    def equation(self):
        """md equation label _[e]

        :return lineS: md equation label
        :rtype: str
        """

        enumI = int(self.labelD["equI"]) + 1
        fillS = str(enumI).zfill(2)
        wI = self.labelD["widthI"]
        refS = self.label("E", fillS)
        spcI = len("Equ. " + fillS + " - " + self.lineS.strip())
        lineS = "Equ. " + fillS + " - " + self.lineS.strip() \
            + refS.rjust(wI-spcI)
        self.labelD["equI"] = enumI

        print(lineS)
        return lineS

    def figure(self):
        """md figure caption _[f]

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.labelD["figI"])
        self.labelD["figI"] = fnumI + 1
        lineS = "Fig. " + str(fnumI) + " - " + self.lineS

        print(lineS + "\n")
        return lineS + "\n"

    def foot(self):
        """footnote number _[#]


        """
        ftnumI = self.labelD["footL"].pop(0)
        self.labelD["noteL"].append(ftnumI + 1)
        self.labelD["footL"].append(ftnumI + 1)
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
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        lineS = "Table " + str(tnumI) + " - " + self.lineS
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
        pagenoS = str(self.labelD["pageI"])
        rvtS = self.labelD["headuS"].replace("p##", pagenoS)
        self.labelD["pageI"] = int(pagenoS)+1
        lineS = "\n"+"_" * self.labelD["widthI"] + "\n" + rvtS +\
                "\n"+"_" * self.labelD["widthI"] + "\n"
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
