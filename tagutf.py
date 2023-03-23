#
import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import io
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

from rivt.units import *


class TagsUTF:

    def __init__(self, lineS, folderD, incrD, localD):
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

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.swidthII = incrD["widthI"] - 1
        self.errlogP = folderD["errlogP"]
        self.valL = []                          # accumulate values

        self.tagD = {"c]": "center",  "#]": "footnumber", "foot]": "footnote",
                     "-]": "line", "r]": "right",  "date]": "date",
                     "page]": "page", "e]": "equation", "f]": "figure", "sym]": "sympy",
                     "t]": "table", "x]": "latex", "lnk]": "link", "url]": "url",
                     "[o]]": "codeblk", "[c]]": "centerblk", "[x]]": "latexblk",
                     "[m]]": "mathblk", "[r]]": "rightblk",
                     ":=": "assign", "=": "result"}

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
        warnings.filterwarnings("ignore")

    def tag_parse(self, tagS):
        """_summary_
        """

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

        self.incrD["equalabelS"] = self.lineS
        enumI = int(self.incrD["equI"]) + 1
        self.incrD["equI"] = enumI
        refS = self.label(enumI, "[ Equ: ") + " ]"
        spcI = self.incrD["widthI"] - len(refS) - len(self.lineS)
        utfS = self.lineS + " " * spcI + refS

        return utfS

    def figure(self):
        """formats figure caption to reST

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.incrD["figI"]) + 1
        self.incrD["figI"] = fnumI
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

        tnumI = int(self.incrD["tableI"]) + 1
        self.incrD["tableI"] = tnumI
        refS = self.label(tnumI, "[ Table: ") + " ]"
        spcI = self.incrD["widthI"] - len(refS) - len(self.lineS)
        lineS = self.lineS + " " * spcI + refS

        return lineS

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
        """assign values to variables

        """
        locals().update(self.localD)

        varS = str(self.lineS).split(":=")[0].strip()
        valS = str(self.lineS).split(":=")[1].strip()
        unit1S = str(self.incrD["unitS"]).split(",")[0]
        unit2S = str(self.incrD["unitS"]).split(",")[1]
        descripS = str(self.incrD["descS"])

        cmdS = varS + "= " + valS + "*" + unit1S
        exec(cmdS, globals(), locals())

        locals().update(self.localD)
        self.localD.update(locals())

        return [varS, valS, unit1S, unit2S, descripS]

    def result(self):
        """evaluate equations

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
        fltfmtS = "." + rprecS.strip() + "f"
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
        print("\n" + utfS + "\n")  # pretty print equation
        utfS = "\n" + utfS + "\n"
        eqS = sp.sympify(valS)
        eqatom = eqS.atoms(sp.Symbol)
        # write equation table
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

        if self.incrD["subB"]:  # equations with numbers
            self.vsub(self.lineS)

        locals().update(self.localD)
        self.localD.update(locals())

        return utfS, [varS, valS, unit1S, unit2S, descS]

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
