import csv
import logging
import warnings
from datetime import datetime
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
from sympy.parsing.latex import parse_latex
from tabulate import tabulate

from rivt.units import *

try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass


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
        self.valL = []                          # list of accumulated results

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
        return "**" + self.lineS.strip() + "**"

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
        return "*" + self.lineS.strip() + "*"

    def right(self):
        """right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """
        return "?x?hfill " + self.lineS

    def boldcenter(self):
        """bold center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textbf{" + self.lineS +  \
            "} ?x?end{center}" + "\n"
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
            + "   ?x?begin{center} ?x?textit{" + self.lineS +  \
            "} ?x?end{center}" + "\n"
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
        return secS + " - " + labelS + numS

    def description(self):
        """footnote description _[d]

        : return lineS: footnote
        : rtype: str
        """
        return ".. [*] " + self.lineS

    def equation(self):
        """reST equation label _[e]

        : return lineS: reST equation label
        : rtype: str
        """
        enumI = int(self.incrD["equI"])
        fillS = str(enumI).zfill(2)
        refS = self.label("E", fillS)
        lineS = "\n\n" + "**" + "Eq. " + str(enumI) + ": " + self.lineS + \
            + "** " + " ?x?hfill " + refS + "\n\n"
        return lineS

    def figure(self):
        """figure label _[f]

        : return lineS: figure label
        : rtype: str
        """
        fnumI = int(self.incrD["figI"])
        fillS = str(fnumI).zfill(2)
        refS = self.label("F", fillS)
        lineS = "\n \n" + "**" + "Figure " + str(fnumI) + ": " + self.lineS + \
                          "** " + " ?x?hfill " + refS + "\n \n"
        return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    def footnumber(self):
        """insert footnote number _[#]

        :return: _description_
        :rtype: _type_
        """
        lineS = "".join(self.lineS)
        return lineS.replace("*]", "[*]_ ")

    def latex(self):
        """format latex _[l]

        :return lineS: reST formatted latex
        :rtype: str
        """
        return ".. raw:: math\n\n   " + self.lineS + "\n"

    def link(self):
        """url or internal link

        :return: _description_
        :rtype: _type_
        """
        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

    def line(self):
        """insert line _[line]:

        param lineS: _description_
        :type lineS: _type_
        """
        return self.widthI * "-"

    def plain(self):
        """format plain literal _[p]

        :return lineS: page break line
        :rtype: str
        """
        return ".. raw:: latex \n\n ?x?newpage \n"

    def sympy(self):
        """reST line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """
        spS = self.lineS
        txS = sp.latex(S(spS))
        return ".. raw:: math\n\n   " + txS + "\n"

    def underline(self):
        """underline _[u]

        :return lineS: underline
        :rtype: str
        """
        return ":math: `?x?text?x?underline{" + self.lineS.strip() + "}"

    def page(self):
        """insert page break _[page]

        :return lineS: page break line
        :rtype: str
        """
        return ".. raw:: latex \n\n ?x?newpage \n"

    def table(self):
        """table label _[t]

        :return lineS: figure label
        :rtype: str
        """
        tnumI = int(self.incrD["tableI"])
        fillS = str(tnumI).zfill(2)
        refS = self.label("T", fillS)
        lineS = "\n" + "**" + "Table " + fillS + + ": " + self.lineS + \
            "** " + " ?x?hfill " + refS + "\n"
        return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    def centerblk(self):
        """_summary_
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} + ?x?parbox{5cm}" \
            + self.lineS + " ?x?end{center}" \
            + "\n\n"
        return lineS

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
        """ := declare variable value

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string 
        :rtype: string
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
        """ = assign result to equation

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string 
        :rtype: string
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
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())

            valU = eval(varS)
            valdec = round(valU.number(), precI)
            val1U = val2U = str(valdec)
        spS = "Eq(" + varS + ",(" + valS + "))"
        # symeq = sp.sympify(spS, _clash2, evaluate=False)
        # eqltxS = sp.latex(symeq, mul_symbol="dot")
        eqS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        indeqS = eqS.replace("\n", "\n   ")
        rstS = "\n::\n\n   " + indeqS + "\n\n"
        eqL = [varS, valS, unit1S, unit2S, descS]
        self.localD.update(locals())

        subS = "\n\n"
        if self.incrD["subB"]:              # replace variables with numbers
            subS = self.vsub(eqL, precI, varS, val1U) + "\n\n"

        assignL = [varS, str(val1U), unit1S, unit2S, descS]
        return [assignL, rstS + subS]

    def vsub(self, eqL, precI, varS, val1U):
        """substitute numbers for variables in printed output

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string 
        :rtype: string
        """
        locals().update(self.localD)
        fmtS = "%." + str(precI) + "f"
        varL = [str(eqL[0]), str(eqL[1])]
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        with sp.evaluate(False):
            symeq = sp.sympify(eqS.strip())
        symat = symeq.atoms(sp.Symbol)
        for n1O in symat:
            if str(n1O) == varS:
                symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))
                continue
            n1U = eval(str(n1O))
            n1U.set_format(value_format=fmtS, auto_norm=True)
            evlen = len(str(n1U))  # get var length
            new_var = str(n1U).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            with sp.evaluate(False):                # sub values
                symeq = symeq.subs(n1O, sp.Symbol(new_var))
        out2 = sp.pretty(symeq, wrap_line=False)
        # symat1 = symeq.atoms(sp.Symbol)
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
        indeqS = out3.replace("\n", "\n   ")
        rstS = "\n::\n\n   " + indeqS + "\n\n"

        return rstS
