#
import csv
import logging
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings
from io import StringIO
from pathlib import Path

import html2text as htm
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex as parsx
from tabulate import tabulate

try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass
from rivt.units import *


class Tagsmd:

    def __init__(self, lineS, incrD, folderD,  localD):
        """format tags to md
            ============================ ======================================
            tags                                   description 
            ============================ ======================================

            I,V,T line formats:               place at end of a line
            ---- can be combined 
            1 text _[b]                       bold 
            2 text _[c]                       center
            3 text _[i]                       italicize
            4 text _[r]                       right justify
            ---------
            5 text _[u]                       underline   
            6 text _[m]                       LaTeX math
            7 text _[s]                       sympy math
            8 text _[e]                       equation label, autonumber
            9 text _[f]                       figure caption, autonumber
            10 text _[t]                      table title, autonumber
            11 text _[#]                      footnote, autonumber
            12 text _[d]                      footnote description 
            13 _[line]                        horizontal line
            14 _[page]                        new page
            15 address, label _[link]         url or internal reference

            I,V,T block formats:             end block with quit 
            ---- can be combined 
            16 _[[p]]                        plain  
            17 _[[s]]                        shade 
            -------
            18 _[[l]]                        LateX
            19 _[[h]]                        HTML 
            20 _[[q]]                        quit

            V calculation formats: 
            21 a := n | unit, alt | descrip    declare = ; units, description
            22 a := b + c | unit, alt | n,n    assign := ; units, decimals

        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.widthI = incrD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

        self.tagsD = {"b]": "bold", "i]": "italic", "c]": "center", "r]": "right",
                      "d]": "description", "e]": "equation", "f]": "figure",
                      "#]": "foot", "l]": "latex", "s]": "sympy", "t]": "table",
                      "u]": "underline", ":=": "declare",  "=": "assign",
                      "link]": "link", "line]": "line", "page]": "page",
                      "[c]]": "centerblk", "[e]]": "endblk", "[l]]": "latexblk",
                      "[m]]": "mathblk", "[o]]": "codeblk", "[p]]": "plainblk",
                      "[q]]": "quitblk", "[s]]": "shadeblk"}

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

    def tag_parse(self, tagS):
        """_summary_
        """
        if tagS in self.tagsD:
            return eval("self." + self.tagsD[tagS] + "()")

        if "b" in tagS and "c" in tagS:
            return self.boldcenter()
        if "b" in tagS and "r" in tagS:
            return self.boldright()
        if "i" in tagS and "c" in tagS:
            return self.italiccenter()
        if "i" in tagS and "r" in tagS:
            return self.italicright()

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

    def right(self):
        """right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """

        lineS = self.lineS.rjust(int(self.widthI))

        return lineS

    def boldcenter(self):
        """center text _[bc]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.center(int(self.widthI))

        print(lineS)
        return lineS

    def boldright(self):
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

    def italicright(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = self.lineS.rjust(int(self.widthI))
        print(lineS)
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
        """4 footnote description _[d]

        :return lineS: footnote
        :rtype: str
        """
        ftnumI = self.incrD["noteL"].pop(0)
        lineS = "[" + str(ftnumI) + "] " + self.lineS
        print(lineS)
        return lineS

    def equation(self):
        """3 md equation label _[e]

        :return lineS: md equation label
        :rtype: str
        """

        enumI = int(self.incrD["equI"]) + 1
        fillS = str(enumI).zfill(2)
        wI = self.incrD["widthI"]
        refS = self.label("E", fillS)
        spcI = len("Fig. " + fillS + " - " + self.lineS.strip())
        lineS = "Equ. " + fillS + " - " + self.lineS.strip() \
            + refS.rjust(wI-spcI)
        self.incrD["equI"] = enumI
        print(lineS)
        return lineS

    def figure(self):
        """5 figure caption _[f]

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.incrD["figI"])
        fillS = str(fnumI).zfill(2)
        wI = self.incrD["widthI"]
        refS = self.label("F", fillS)
        spcI = len("Table " + fillS + " - " + self.lineS.strip())
        lineS = "Fig. " + fillS + " - " + self.lineS.strip() \
            + refS.rjust(wI-spcI)
        self.incrD["figI"] = fnumI + 1
        print(lineS)
        return lineS

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
        tnumI = int(self.incrD["tableI"])
        fillS = str(tnumI).zfill(2)
        wI = self.incrD["widthI"]
        refS = self.label("T", fillS)
        spcI = len("Table " + fillS + " - " + self.lineS.strip())
        lineS = "Table " + fillS + " - " + self.lineS.strip() \
            + refS.rjust(wI-spcI)
        self.incrD["tableI"] = tnumI + 1
        print(lineS)
        return lineS

    def line(self):
        """insert horizontal line _[line]

        :param lineS: _description_
        :type lineS: _type_
        """
        lineS = self.widthI * "_"
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

    def declare(self):
        """declare variable values

        :return: _description_
        :rtype: _type_
        """
        locals().update(self.localD)
        varS = str(self.lineS).split(":=")[0].strip()
        valS = str(self.lineS).split(":=")[1].strip()
        unit1S = str(self.incrD["unitS"]).split(",")[0]
        unit2S = str(self.incrD["unitS"]).split(",")[1]
        descripS = str(self.incrD["descS"])
        if unit1S.strip() != "-":
            cmdS = varS + "= " + valS + "*" + unit1S
        else:
            cmdS = varS + "= as_unum(" + valS + ")"

        exec(cmdS, globals(), locals())
        self.localD.update(locals())
        return [varS, valS, unit1S, unit2S, descripS]

    def assign(self):
        """assign value to equation

        :return: _description_
        :rtype: _type_
        """
        locals().update(self.localD)
        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.incrD["unitS"]).split(",")[0]
        unit2S = str(self.incrD["unitS"]).split(",")[1]
        descS = str(self.incrD["eqlabelS"])
        precI = int(self.incrD["descS"])  # trim result
        fmtS = "%." + str(precI) + "f"
        if unit1S.strip() != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())

                val1U = eval(varS).cast_unit(eval(unit1S))
                val1U.set_format(value_format=fmtS, auto_norm=True)
                val2U = val1U.cast_unit(eval(unit2S))
                # print(f"{val1U=}")
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())

            valU = eval(varS)
            valdec = round(valU.number(), precI)
            val1U = val2U = str(valdec)

        spS = "Eq(" + varS + ",(" + valS + "))"
        mdS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        mdS = "\n" + mdS + "\n"
        eqL = [varS, valS, unit1S, unit2S, descS]

        print(mdS)                      # print equation

        subS = " "
        if self.incrD["subB"]:
            subS = self.vsub(eqL, precI, varS, val1U)
            print(subS)                  # print with substition

        self.localD.update(locals())
        return [eqL, mdS + "\n" + subS + "\n\n"]

    def vsub(self, eqL, precI, varS, val1U):
        """substitute variables with values

        :param eqL: _description_
        :type eqL: _type_
        :param precI: _description_
        :type precI: _type_
        :param varS: _description_
        :type varS: _type_
        :param val1U: _description_
        :type val1U: _type_
        :return: _description_
        :rtype: _type_
        """

        locals().update(self.localD)
        fmtS = "%." + str(precI) + "f"
        varL = [str(eqL[0]), str(eqL[1])]
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        with sp.evaluate(False):
            symeq = sp.sympify(eqS.strip())
        # print(f"{symeq=}")
        symat = symeq.atoms(sp.Symbol)
        # print(f"{symat=}")
        for n1O in symat:
            if str(n1O) == varS:
                symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))
                continue
            # print(f"{n1O=}")
            n1U = eval(str(n1O))
            n1U.set_format(value_format=fmtS, auto_norm=True)
            # print(f"{n1U=}")
            evlen = len(str(n1U))  # get var length
            new_var = str(n1U).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            # print(f"{new_var=}")
            with sp.evaluate(False):
                symeq = symeq.subs(n1O, sp.Symbol(new_var))
            # print(f"{symeq=}")
        out2 = sp.pretty(symeq, wrap_line=False)
        # print('out2a\n', out2)
        # symat1 = symeq.atoms(sp.Symbol)  # adjust character length
        # for n2 in symat1:
        #     orig_var = str(n2).replace("~", "")
        #     orig_var = orig_var.replace("|", "_")
        #     expr = eval(varL[1])
        #     if type(expr) == float:
        #         form = "{%." + str(precI) + "f}"
        #         symeval1 = form.format(eval(str(expr)))
        #     else:
        #         try:
        #             symeval1 = eval(
        #                 orig_var.__str__()).__str__()
        #         except:
        #             symeval1 = eval(orig_var.__str__()).__str__()
        #     out2 = out2.replace(n2.__str__(), symeval1)   # substitute
        # print('out2b\n', out2)
        out3 = out2  # clean up unicode
        out3 = out3.replace("*", "\\u22C5")
        _cnt = 0
        for _m in out3:
            if _m == "-":
                _cnt += 1
                continue
            else:
                if _cnt > 1:
                    out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                _cnt = 0
        self.localD.update(locals())
        mdS = out3 + "\n\n"

        return mdS
