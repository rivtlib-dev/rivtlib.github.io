#!python
"""V2utf and V2rst classes
"""

import os
import sys
import csv
import textwrap
import subprocess
import tempfile
import re
import io
import logging
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate
from pathlib import Path
from numpy import *

logging.getLogger("numexpr").setLevel(logging.WARNING)
# tabulate.PRESERVE_WHITESPACE = True


class V2utf:
    """convert value-string to UTF8 calc"""

    def __init__(self, strL: list, folderD, cmdD, sectD):
        """convert insert-string to UTF8 calc-string

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
        """

        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.sectD = sectD
        self.cmdD = cmdD

    def _vconfig(self, vL: list):
        """update dictionary format values

        Args:
            vL (list): configuration parameters
        """
        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

    def _vassign(self, vL: list):
        """assign values to variables and equations

        Args:
            vL (list): list of assignments
        """
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                val1U = val2U = array(eval(valS))
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
            else:  # no units
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            utfS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"
            utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            print("\n" + utfS + "\n")  # pretty print equation
            self.calcS += "\n" + utfS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:  # substitute into equation
                self._vsub(vL)
            else:  # write equation table
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())

    def _vtable(self, tbl, hdrL, tblfmt, alignL):
        """write value table"""

        locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbl, tablefmt=tblfmt, headers=hdrL, showindex=False, colalign=alignL
            )
        )
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        print(utfS)
        self.calcS += utfS + "\n"
        self.rivtD.update(locals())

    def _vvalue(self, vL: list):
        """import values from files

        Args:
            vL (list): value command arguments
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        calpS = "c" + self.setsectD["cnumS"]
        vfileS = Path(self.folderD["cpathcur"] / vL[1].strip())
        with open(vfileS, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vaL += [""] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["---------", " ", " ", " "])  # totals
                continue
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            valL.append([varS, val1U, val2U, descripS])
        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

    def _vdata(self, vL: list):
        """import data from files

        Args:
            vL (list): data command arguments
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        valL.append(["variable", "values"])
        vfileS = Path(self.folderD["cpath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS, "r") as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]
            varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4:
                varL = str((varL[:2]).append(["..."]))
            valL.append([varS, varL])
        hdrL = ["variable", "values"]
        alignL = ["left", "right"]
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

    def _vsub(self, eqL: list, eqS: str):
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

    def _vfunc(self, vL: list):
        pass


class V2rst:
    def v_rst(self) -> tuple:
        """parse value-string and set method

        Return:
        calcS (list): utf formatted calc-string (appended)
        setsectD (dict): section settings
        setcmdD (dict): command settings
        rivtD (list): calculation results
        exportS (list): value strings for export
        """

        locals().update(self.rivtD)
        vcmdL = ["config", "value", "data", "func", "text", "table", "image"]
        vmethL = [
            self._vconfig,
            self._vvalue,
            self._vdata,
            self._vfunc,
            self._itext,
            self._itable,
            self._iimage,
        ]

        self._parseRST("values", vcmdL, vmethL, vtagL)
        self.rivtD.update(locals())
        return self.restS, self.setsectD, self.setcmdD, self.rivtD, self.exportS

    def _vconfig(self, vL: list):
        """update dictionary format values

        Args:
            vL (list): configuration parameters
        """

        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

    def _vassign(self, vL: list):
        """assign values to variables and equations

        Args:
            vL (list): list of assignments
        """

        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
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
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            rstS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"  # pretty print
            symeq = sp.sympify(spS, _clash2, evaluate=False)
            eqltxS = sp.latex(symeq, mul_symbol="dot")
            self.restS += "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:
                self._vsub(vL)
            else:
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL, fltfmtS)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                # print(f"{cmdS=}")
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())
        # print(self.rivtD)

    def _vtable(self, tbl, hdrL, tblfmt, alignL, fltfmtS):
        """write value table"""

        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        tableS = tabulate(
            tbl,
            tablefmt=tblfmt,
            headers=hdrL,
            showindex=False,
            colalign=alignL,
            floatfmt=fltfmtS,
        )
        output.write(tableS)
        rstS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        inrstS = ""
        self.restS += ":: \n\n"
        for i in rstS.split("\n"):
            inrstS = "  " + i
            self.restS += inrstS + "\n"
        self.restS += "\n\n"
        self.rivtD.update(locals())

    def _vvalue(self, vL: list):
        """import values from files

        Args:
            vL (list): value command arguments
        """

        locals().update(self.rivtD)
        valL = []
        fltfmtS = ""
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        calpS = self.setsectD["fnumS"]
        vfileS = Path(self.folderD["cpath"] / calpS / vL[1].strip())
        with open(vfileS, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vaL += [""] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["------", "------", "------", "------"])  # totals
                continue
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            valL.append([varS, val1U, val2U, descripS])
        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        self._vtable(valL, hdrL, "rst", alignL, fltfmtS)
        self.rivtD.update(locals())

    def _vdata(self, vL: list):
        """import data from files

        Args:
            vL (list): data command arguments
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        valL.append(["variable", "values"])
        vfileS = Path(self.folderD["apath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS, "r") as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]
            varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4:
                varL = str((varL[:2]).append(["..."]))
            valL.append([varS, varL])
        hdrL = ["variable", "values"]
        alignL = ["left", "right"]
        self._vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

    def _vsub(self, eqL: list, eqS: str):
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
            self.calcl.append(utfs)
        except:
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
        except:
            pass
