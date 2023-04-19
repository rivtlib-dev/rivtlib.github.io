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
            ============================ ======================================
            tags                                   description 
            ============================ ======================================

            I,V,T line formats:               one at the end of a line
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

            I,V,T block formats:             blocks end with quit block
            ---- can be combined 
            16 _[[p]]                        plain  
            17 _[[s]]                        shade 
            -------
            18 _[[l]]                        LateX
            19 _[[h]]                        HTML 
            20 _[[q]]                        quit block

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
        self.valL = []                          # accumulated values

        self.tagsD = {"b]": "bold", "i]": "italic", "c]": "center", "r]": "right",
                      "d]": "description", "e]": "equation", "f]": "figure",
                      "#]": "foot", "l]": "latex", "s]": "sympy", "t]": "table",
                      "u]": "underline", ":=": "declare",  "=": "assign",
                      "link]": "link", "line]": "line", "page]": "page",
                      "[c]]": "centerblk", "[e]]": "endblk", "[l]]": "latexblk",
                      "[m]]": "mathblk", "[o]]": "codeblk", "[p]]": "plainblk",
                      "[q]]": "quitblk", "[s]]": "shadeblk"}

        self.vgap = (
            "\n\n" +
            ".. raw:: latex"
            + "\n\n"
            + "   ?x?vspace{.05in}"
            + "\n\n"
        )

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

        lineS = "**" + self.lineS.strip() + "**"

        return lineS

    def center(self):
        """center text _[c]

        : return lineS: centered line
        : rtype: str
        """

        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} " + self.lineS + " ?x?end{center}" \
            + "\n"

        return lineS

    def italic(self):
        """italicize text _[i]

        :return lineS: centered line
        :rtype: str
        """

        lineS = "*" + self.lineS.strip() + "*"

        return lineS

    def right(self):
        """right justify text _[r]:return lineS: right justified text:rtype: str
        """

        lineS = "?x?hfill " + lineS

        return lineS

    def boldcenter(self):
        """bold center text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textbf{" + self.lineS + "} ?x?end{center}" \
            + "\n"

        return lineS

    def boldright(self):
        """bold right text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "?x?hfill ?x?textbf{" + self.lineS + "}" \
            + "\n"

        return lineS

    def italiccenter(self):
        """italic center text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textit{" + self.lineS + "} ?x?end{center}" \
            + "\n"

        return lineS

    def italicright(self):
        """italic right text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = ".. raw:: latex \n\n" \
            + "?x?hfill ?x?textit{" + self.lineS + "}" \
            + "\n"

        return lineS

    def label(self, labelS, numS):
        """format labels for equations, tables and figures

            : return labelS: formatted label
            : rtype: str
        """

        secS = str(self.incrD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS

        return labelS

    def description(self):
        """footnote description _[d]

        : return lineS: footnote
        : rtype: str
        """

        lineS = ".. [*] " + self.lineS

        return lineS

    def equation(self):
        """reST equation label _[e]

        : return lineS: reST equation label
        : rtype: str
        """

        enumI = int(self.incrD["equI"])
        fillS = str(enumI).zfill(2)
        refS = self.label("E", fillS)
        lineS = "\n\n" + "**" + "Eq. " + str(enumI) + "** " + \
            self.lineS + " ?x?hfill " + refS + "\n\n"

        return lineS

    def figure(self):
        """figure label _[f]

        : return lineS: figure label
        : rtype: str
        """

        fnumI = int(self.incrD["figI"])
        fillS = str(fnumI).zfill(2)
        refS = self.label("F", fillS)
        lineS = "\n \n" + "**" + "Figure " + str(fnumI) + "** " + \
            self.lineS + " ?x?hfill " + refS + "\n \n"
        lineS = self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

        return lineS

    def footnumber(self):
        """insert footnote number _[  # ]
        """

        lineS = "".join(self.lineS)
        lineS = lineS.replace("*]", "[*]_ ")

        return lineS

    def latex(self):
        """format latex _[l]:return lineS: reST formatted latex:rtype: str
        """

        lineS = ".. raw:: math\n\n   " + self.lineS + "\n"

        return lineS

    def plain(self):
        """10 format plain literal _[p]:return lineS: page break line:rtype: str
        """
        lineS = ".. raw:: latex \n\n ?x?newpage \n"

        return lineS

    def sympy(self):
        """13 reST format line of sympy _[s]:return lineS: formatted sympy:rtype: str
        """

        spS = self.lineS
        txS = sp.latex(S(spS))
        lineS = ".. raw:: math\n\n   " + txS + "\n"

        return lineS

    def underline(self):
        """underline _[u]

        :return lineS: underline
        :rtype: str
        """

        lineS = ":math: `?x?text?x?underline{" + self.lineS.strip() + "}"

        return lineS

    def page(self):
        """11 insert page break _[page]:return lineS: page break line:rtype: str
        """
        lineS = ".. raw:: latex \n\n ?x?newpage \n"

        return lineS

    def link(self):
        """15 url or internal link:return: _description_:rtype: _type_
        """

        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

    def line(self):
        """insert line _[line]:

        param lineS: _description_
        :type lineS: _type_
        """

        lineS = self.widthI * "-"

        return lineS

    def table(self):
        """14 table label _[t]:return lineS: figure label:rtype: str
        """

        tnumI = int(self.incrD["tableI"])
        fillS = str(tnumI).zfill(2)
        refS = self.label("T", fillS)
        lineS = "\n" + "**" + "Table " + fillS + "** " + \
            self.lineS + " ?x?hfill " + refS + "\n"
        lineS = self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

        return lineS

    def centerblk(self):
        """_summary_
        """

        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} + ?x?parbox{5cm}" \
            + self.lineS + " ?x?end{center}" \
            + "\n\n"

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

    def declare(self):
        """declare variable value :=

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
        """assign result to equation=

        """
        locals().update(self.localD)

        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.incrD["unitS"]).split(",")[0]
        unit2S = str(self.incrD["unitS"]).split(",")[1]
        descS = str(self.incrD["eqlabelS"])
        rprecS = str(self.incrD["descS"].split(",")[0])  # trim result
        eprecS = str(self.incrD["descS"].split(",")[1])  # trim equations
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + eprecS + "f')")
        fltfmtS = "%." + rprecS.strip() + "f"
        if unit1S.strip() != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())
                valU = eval(varS).cast_unit(eval(unit1S))
                valdec = fltfmtS % valU.number()
                val1U = str(valdec) + " " + str(valU.unit())
                val2U = valU.cast_unit(eval(unit2S))
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())
            valU = eval(varS).cast_unit(eval(unit1S))
            valdec = fltfmtS % valU.number()
            val1U = str(valdec) + " " + str(valU.unit())
            val2U = valU.cast_unit(eval(unit2S))
        spS = "Eq(" + varS + ",(" + valS + "))"
        symeq = sp.sympify(spS, _clash2, evaluate=False)
        eqltxS = sp.latex(symeq, mul_symbol="dot")
        rstS = "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
        rstS = "\n" + rstS + "\n"
        eqL = [varS, valS, unit1S, unit2S, descS]

        self.localD.update(locals())

        subS = "\n"
        if self.incrD["subB"]:              # replace variables with numbers
            subS = self.vsub(eqL)

        return [[varS, str(val1U), unit1S, unit2S, descS], rstS + subS]

    def vsub(self, eqL):
        """substitute numbers for variables in printed output

        Args:
            epL(list): equation and units
            epS(str): [description]
        """

        locals().update(self.localD)

        eformat = ""
        utfS = eqL[0] + " = " + eqL[1]
        varS = utfS.split("=")
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"

        utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
        symeq = sp.sympify(eqS.strip())
        symat = symeq.atoms(sp.Symbol)
        for n2 in symat:
            evlen = len((eval(n2.__str__())).__str__())  # get var length
            new_var = str(n2).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            symeq = symeq.subs(n2, sp.Symbol(new_var))
        eqltxS = sp.latex(symeq, mul_symbol="dot")
        out2 = "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
        out2 = "\n" + out2 + "\n"
        # print('out2a\n', out2)
        symat1 = symeq.atoms(sp.Symbol)  # adjust character length
        for n1 in symat1:
            orig_var = str(n1).replace("~", "")
            orig_var = orig_var.replace("|", "_")
            expr = eval(varS[1])
            if type(expr) == float:
                form = "{:." + eformat + "f}"
                symeval1 = form.format(eval(str(expr)))
            else:
                try:
                    symeval1 = eval(
                        orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
            out2 = out2.replace(n1.__str__(), symeval1)   # substitute
        out3 = out2  # clean up unicode
        out3 = out3.replace("*", "\\u22C5")
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

        self.localD.update(locals())

        rstS = "\n" + out3 + "\n"
        return rstS
