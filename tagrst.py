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
from rivt.units import *


class TagsRST():

    def __init__(self, lineS, incrD, folderD,  localD):
        """format tags to reST


        ============================ ============================================
        tag syntax                      description (one tag per line)
        ============================ ============================================

        Line Format:
        1  text  _[b]                    bold
        2  text  _[c]                    center
        3  text  _[d]                    description for footnote
        4  text  _[e]                    equation label
        5  text  _[f]                    figure label
        6  text  _[#]                    foot number
        7  text  _[i]                    italicize
        8        _[-]                    line 
        9  latex _[l]                    LaTeX equation
        10 text  _[p]                    plain literal
        11    _[page]                    new page
        12 text  _[r]                    right justify line
        13 sympy _[s]                    sympy equation

        14 text  _[t]                    table label
        15 <url, label>                  url or internal link inline

        Block Format:
        16 _[[c]]                        center block
        17 _[[e]]                        end block
        18 _[[l]]                        LateX block
        19 _[[m]]                        LaTeX math block
        20 _[[o]]                        code block
        21 _[[p]]                        plain literal block
        22 _[[r]]                        right justify block
        23 _[[t]]                        block with tags

        Values Only Formats:
        24 a := n | unit, alt | descrip   = declare tag
        25 a = b + c | unit, alt | n,n    := assign tag


        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.widthI = incrD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                          # accumulate values

        self.tagD = {"c]": "center", "d]": "footnote", "e]": "equation",
                     "f]": "figure", "#]": "footnumber", "i]": "italic",
                     "l]": "latex", "-]": "line", "page]": "page",
                     "r]": "right", "s]": "sympy", "t]": "table",
                     "[c]]": "centerblk", "[e]]": "endblk", "[l]]": "latexblk",
                     "[m]]": "mathblk", "[o]]": "codeblk", "[p]]": "plainblk",
                     "[r]]": "rightblk", ":=": "declare", "=": "assign"}

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

        return eval("self." + self.tagD[tagS] + "()")

    def label(self, objI, text):
        """reST labels equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """

        objfillS = str(objI).zfill(2)

        labelS = "[" + str(self.incrD["secnumI"]).zfill(2) + \
            "]" + text + objfillS

        return labelS

    def bold(self):
        """1 bold text _[b]

        :return lineS: bold line of text
        :rtype: str
        """

        lineS = "**"+lineS+"**"

        return lineS

    def center(self):
        """2 center text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = "?x?begin{center} " + self.lineS + "?x?end{center}"

        return lineS

    def footnote(self):
        """4 footnote description _[d]

        :return lineS: footnote
        :rtype: str
        """

        lineS = ".. [*] " + self.lineS

        return lineS

    def equation(self):
        """3 reST equation label _[e]

        :return lineS: reST equation label
        :rtype: str
        """

        enumI = int(self.incrD["equI"]) + 1
        self.incrD["equI"] = enumI
        refS = self.label(enumI, " Equ. ")
        lineS = "**" + self.lineS + "**" + " ?x?hfill " + refS

        return lineS

    def figure(self):
        """5 figure label _[f]

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.incrD["figI"]) + 1
        self.incrD["figI"] = fnumI
        refS = self.label(fnumI, " Fig. ") + " - " + str(self.incrD["secnumI"])
        lineS = "**" + self.lineS + "**" + " ?x?hfill " + refS

        return lineS

    def footnumber(self):
        """6 insert footnote number _[#]
        """

        ftnumI = self.incrD["footL"].pop(0)
        self.incrD["noteL"].append(ftnumI + 1)
        self.incrD["footL"].append(ftnumI + 1)

        lineS = "".join(self.lineS)
        lineS = lineS.replace("*]", "[*]_ ")

        return lineS

    def italic(self):
        """7 italicizes line _[i]

        :return lineS: italicized line
        :rtype: str
        """

        lineS = "*"+lineS+"*"

        return lineS

    def line(self):
        """8 insert line _[-]

        :param lineS: _description_
        :type lineS: _type_
        """

        lineS = self.widthI * "-"

        return lineS

    def latex(self):
        """9 format latex _[l]

        :return lineS: reST formatted latex
        :rtype: str
        """

        lineS = ".. raw:: math\n\n   " + self.lineS + "\n"

        return lineS

    def plain(self):
        """10 format plain literal _[p]

        :return lineS: page break line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n ?x?newpage \n"

        return lineS

    def page(self):
        """11 insert page break _[page]

        :return lineS: page break line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n ?x?newpage \n"

        return lineS

    def right(self):
        """12 right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """

        lineS = "?x?hfill " + lineS

        return lineS

    def sympy(self):
        """13 reST format line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """

        spS = self.lineS
        txS = sp.latex(S(spS))
        lineS = ".. raw:: math\n\n   " + txS + "\n"

        return lineS

    def table(self):
        """14 table label _[t]

        :return lineS: figure label
        :rtype: str
        """

        self.incrD["eqlabels"] = self.lineS
        tnumI = int(self.incrD["tableI"]) + 1
        self.incrD["tableI"] = tnumI
        refS = self.label(tnumI, " Table: ")
        spcI = self.widthI - len(refS) - len(self.lineS)
        lineS = "**" + refS + "**" + " ?x?hfill  " + refS

        return lineS

    def url(self):
        """15 url or internal link

        :return: _description_
        :rtype: _type_
        """

        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

    def centerblk(self):
        pass

    def endblk(self):
        pass

    def latexblk(self):
        pass

    def mathblk(self):
        pass

    def codeblk(self):
        pass

    def rightblk(self):
        pass

    def tagblk(self):
        pass

    def assign(self):
        """assign result to equation =

        """
        locals().update(self.localD)

        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.incrD["unitS"]).split(",")[0]
        unit2S = str(self.incrD["unitS"]).split(",")[1]
        descS = str(self.incrD["equlabelS"])
        rprecS = str(self.incrD["descS"].split(",")[0])  # trim result
        eprecS = str(self.incrD["descS"].split(",")[1])  # trim equations
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + eprecS + "f')")
        # fltfmtS = "." + rprecS.strip() + "f"
        if type(eval(valS)) == list:
            val1U = array(eval(valS)) * eval(unit1S)
            val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
        else:
            cmdS = varS + "= " + valS
            exec(cmdS, globals(), locals())
            valU = eval(varS).cast_unit(eval(unit1S))
            valdec = ("%." + str(rprecS) + "f") % valU.number()
            val1U = str(valdec) + " " + str(valU.unit())
            val2U = valU.cast_unit(eval(unit2S))
        spS = "Eq(" + varS + ",(" + valS + "))"
        utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        utfS = utfS + "\n"
        # write equation table
        # eqS = sp.sympify(valS)
        # eqatom = eqS.atoms(sp.Symbol)
        # hdrL = []
        # valL = []
        # hdrL.append(varS)
        # valL.append(str(val1U) + "  [" + str(val2U) + "]")
        # for sym in eqatom:
        #     hdrL.append(str(sym))
        #     symU = eval(str(sym))
        #     valL.append(str(symU.simplify_unit()))
        # alignL = ["center"] * len(valL)
        # self._vtable([valL], hdrL, "rst", alignL)

        if self.incrD["subB"]:              # replace variables with numbers
            self.vsub(self.lineS)

        locals().update(self.localD)
        self.localD.update(locals())

        return [[varS, str(val1U), unit1S, unit2S, descS], utfS]

    def declare(self):
        """declare variable value :=

        """
        locals().update(self.localD)

        varS = str(self.lineS).split(":=")[0].strip()
        valS = str(self.lineS).split(":=")[1].strip()
        unit1S = str(self.incrD["unitS"]).split(",")[0]
        unit2S = str(self.incrD["unitS"]).split(",")[1]
        descripS = str(self.incrD["descS"])

        cmdS = varS + "= " + valS + "*" + unit1S
        exec(cmdS, globals(), locals())

        self.localD.update(locals())

        return [varS, valS, unit1S, unit2S, descripS]

    def vsub(self, eqL: list, eqS: str):
        """substitute numbers for variables in printed output

        Args:
            epL (list): equation and units
            epS (str): [description]
        """

        locals().update(self.rivtd)

        eformat = ""
        utfS = eqL[0].strip()
        descripS = eqL[3]
        parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try:
            eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
            # sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
            print(utfs)
            self.calcl.append(utfs)
        except:
            print(utfs)
            self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eqS.strip())  # substitute
            symat = symeq.atoms(sp.Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, "~")
                new_var = new_var.replace("_", "|")
                symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
            out2 = sp.pretty(symeq1, wrap_line=False)
            # print('out2a\n', out2)
            symat1 = symeq1.atoms(sp.Symbol)  # adjust character length
            for _n1 in symat1:
                orig_var = str(_n1).replace("~", "")
                orig_var = orig_var.replace("|", "_")
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = "{:." + eformat + "f}"
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            # print('out2b\n', out2)
            out3 = out2  # clean up unicode
            out3.replace("*", "\\u22C5")
            # print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == "-":
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                    _cnt = 0
            # print('out3b \n', out3)
            self._write_text(out3, 1, 0)  # print substituted form
            self._write_text(" ", 0, 0)
        except:
            pass
