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
from sympy.parsing.latex import parse_latex as parsx
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
from rivt.units import *


class TagsUTF:

    def __init__(self, lineS, incrD, folderD,  localD):
        """format tags to utf
            ============================ ======================================
            tags                                   description 
            ============================ ======================================

            I,V,T line formats:               one at the end of a line
            ---- can be combined 
            1 text _[b]                       bold 
            2 text _[c]                       center
            3 text _[i]                       italicize
            4 text _[u]                       underline   
            5 text _[r]                       right justify
            ---------
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

            I,V,T block formats:              one at the start and end of block
            ---- can be combined 
            16 _[[b]]                        bold
            17 _[[c]]                        center
            18 _[[i]]                        italic
            19 _[[p]]                        plain  
            20 _[[s]]                        shade 
            -------
            21 _[[l]]                        LateX
            22 _[[h]]                        HTML 
            23 _[[q]]                        quit block

            V calculation formats: 
            24 a := n | unit, alt | descrip    declare = ; units, description
            25 a := b + c | unit, alt | n,n    assign := ; units, decimals

        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.widthI = incrD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                          # accumulated values

        self.multiD = {"b": "bold", "c": "center", "i": "italic", "r": "right",
                       "u": "underline", }

        self.singleD = {"d]": "description", "e]": "equation", "f]": "figure",
                        "#]": "footnumber", "l]": "latex", "s]": "sympy",
                        "t]": "table", ":=": "declare", "=": "assign"}

        self.wordD = {"link]": "line", "line]": "line", "page]": "page", }

        self.blockD = {"[c]]": "centerblk", "[e]]": "endblk", "[l]]": "latexblk",
                       "[m]]": "mathblk", "[o]]": "codeblk", "[p]]": "plainblk",
                       "[r]]": "rightblk", "[q]]": "shadeblk", "[s]]": "quitblk"}

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
        if tagS in self.wordD:
            return eval("self." + self.tagD[tagS] + "()")

        if tagS in self.singleD:
            return eval("self." + self.tagD[tagS] + "()")

        if tagS in self.blockD:
            return eval("self." + self.tagD[tagS] + "()")

        cmdL = []
        xutfS = ""
        for s in tagS:
            if s in self.multiD:
                cmdL.append("self." + self.multiD[tagS] + "()")

        for j in cmdL:
            return eval(j)

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

    def bold(self):
        """1 bold text _[b]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS

        print(lineS)
        return lineS

    def center(self):
        """2 center text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.center(int(self.widthI))

        print(lineS)
        return lineS

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
        """3 utf equation label _[e]

        :return lineS: utf equation label
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

    def footnumber(self):
        """6 footnote number _[#]
        """

        ftnumI = self.incrD["footL"].pop(0)
        self.incrD["noteL"].append(ftnumI + 1)
        self.incrD["footL"].append(ftnumI + 1)
        lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")

        print(lineS)
        return lineS

    def italic(self):
        """7 italicize line
        """

        lineS = self.lineS

        return lineS

    def latex(self):
        """8 format latex

        :return lineS: formatted latex
        :rtype: str
        """
        txS = self.lineS
        # txS = txs.encode('unicode-escape').decode()
        ptxS = sp.parse_latex(txS)
        lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))

        return lineS

    def line(self):
        """9 insert horizontal line _[-]

        :param lineS: _description_
        :type lineS: _type_
        """
        lineS = self.widthI * "_"

        print(lineS)
        return lineS

    def plain(self):
        """10 format plain literal text _[p]

        :param lineS: _description_
        :type lineS: _type_
        """

        pass

    def page(self):
        """11 insert new page header _[page]

        :return lineS: page header
        :rtype: str
        """

        pagenoS = str(self.incrD["pageI"])
        rvtS = self.incrD["headuS"].replace("p##", pagenoS)
        self.incrD["pageI"] = int(pagenoS)+1

        print("\n" + rvtS)
        return "\n" + rvtS

    def right(self):
        """12 right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """

        lineS = lineS.rjust(int(self.widthI))

        print(lineS)
        return lineS

    def sympy(self):
        """13 format line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """

        spS = self.lineS.strip()
        try:
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            # sps = sp.encode('unicode-escape').decode()
        except:
            lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

        print(lineS)
        return lineS

    def table(self):
        """14 format table title  _[t]

        :return lineS: utf table title
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

    def url(self):
        """15 format url or internal link

        :return: _description_
        :rtype: _type_
        """

        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

    def centerblk(self):
        """_summary_
        """

        lineS = self.lineS.center(int(self.widthI))

    def centerblk(self):
        """

        """
        for i in self.lineS:
            lineS += i.center(int(self.widthI))

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
        lineS = self.widthI * "_   "

        print(lineS)
        return lineS

    def quitblock(self):
        """ quit shade block _[[q]]

        :param lineS: _description_
        :type lineS: _type_
        """
        lineS = self.widthI * "_   "

        print(lineS)
        return lineS

    def tagblk(self):
        pass

    def declare(self):
        """ := declare variable value

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

    def assign(self):
        """ = assign result to equation

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
            valtS = str(valdec)
            val2U = valU.cast_unit(eval(unit2S))
        spS = "Eq(" + varS + ",(" + valS + "))"
        utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        utfS = "\n" + utfS + "\n"
        eqL = [varS, valS, unit1S, unit2S, descS]

        self.localD.update(locals())

        subS = "\n"
        if self.incrD["subB"]:              # replace variables with numbers
            subS = self.vsub(eqL)

        return [eqL, utfS + "\n" + subS + "\n\n"]

    def vsub(self, eqL):
        """substitute numbers for variables in printed output

        Args:
            epL (list): equation and units
            epS (str): [description]
        """
        locals().update(self.localD)

        eformat = ""
        utfS = eqL[0] + " = " + eqL[1]
        varS = utfS.split("=")
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        # utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
        symeq = sp.sympify(eqS.strip())
        symat = symeq.atoms(sp.Symbol)
        for n2 in symat:
            evlen = len((eval(n2.__str__())).__str__())  # get var length
            new_var = str(n2).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            symeq = symeq.subs(n2, sp.Symbol(new_var))
        out2 = sp.pretty(symeq, wrap_line=False)
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
        # print('out2b\n', out2)
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

        utfS = out3
        return utfS
