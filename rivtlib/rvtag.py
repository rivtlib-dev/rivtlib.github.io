#
import sys
import textwrap
from io import StringIO

import sympy as sp
import tabulate
from numpy import *  # noqa: F403
from sympy.abc import _clash2

from rivtlib.rvunits import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Tag:
    """tag format object

    Methods:
        taglx(tagS): formats line
        tagbx(tagS): formats block
        tagex(tagS): formats equation
    """

    def __init__(self, folderD, labelD, rivtD, rivtL, strngS):
        """tag object
        Args:
            folderD (dict): _description_
            labelD (dict): _description_
            rivtD (dict): _description_
            rivtL (list): _description_
            strngS (str): _description_
        Vars:
            uS (str): utf string
            rS (str): rst2pdf string
            xS (str): reST string
        """
        # region
        self.folderD = folderD
        self.labelD = labelD
        self.rivtD = rivtD
        self.rivtL = rivtL
        self.strngS = strngS
        self.uS = ""
        self.rS = ""
        self.xS = ""
        # endregion

    def taglx(self, tagS):
        """format line
        text        _[C]    center
        text        _[B]    bold center
        text        _[D]    footnote description
        label       _[E]    equation label and number
        caption     _[F]    figure caption and number
        text        _[N]    number footnote
        text        _[R]    right justify
        equation    _[S]    sympy
        title       _[T]    table title and number
        url, label  _[U]    url
        equation    _[Y]    sympy with equation number
        ------  =>  _[H]    horizontal line (6 -- min.)
        ======  =>  _[P]    new page (6 == min.)
        Args:
            tagS (str): tag symbol
        Returns:
            uS, r2S, rS, folderD, labelD, rivtD, rivtL
        """
        # region
        cmdS = "l" + tagS[0]
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.rS,
            self.xS,
            self.folderD,
            self.labelD,
            self.rivtD,
            self.rivtL,
        )
        # endregion

    def tagbx(self, tagS):
        """format block
        title _[[B]]   bold indent
        title _[[C]]   code - literal indent
        title _[[I]]   italic indent
        title _[[L]]   literal
        title _[[S]]   indent
        title _[[X]]   latex
        title _[[V]]   values table
        color _[[Q]]   quit
        Args:
            tagS (str): tag symbol
        Returns:
            uS, r2S, rS, folderD, labelD, rivtD, rivtL
        """
        # region
        self.blockL = self.strngS.split("\n")
        cmdS = "b" + tagS[1]
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.rS,
            self.xS,
            self.folderD,
            self.labelD,
            self.rivtD,
            self.rivtL,
        )
        # endregion

    def tagex(self):
        """format equation

            equation tag  :=
            a := 1 + 2 | unit1, unit2, dec1, dec2 | ref

            ratio tags     :<  :>
            a :> b | Ok, Not Ok
            a :< b | Pass, Fail

        Returns:
            uS, r2S, rS, folderD, labelD, rivtD, rivtL
        """
        # region
        tbl1L = []
        hdr1L = []
        lineS = self.strngS
        print(f"{lineS}")
        lpL = lineS.split("|")
        eqS = lpL[0]
        eqS = eqS.replace(":=", "=").strip()
        unit1S, unit2S, dec1S, dec2S = lpL[1].split(",")
        refS = lpL[2].strip()
        unit1S, unit2S = unit1S.strip(), unit2S.strip()
        dec1S, dec2S = dec1S.strip(), dec2S.strip()
        fmt1S = "Unum.set_format(value_format='%." + dec1S + "f', auto_norm=True)"
        fmt2S = "Unum.set_format(value_format='%." + dec2S + "f', auto_norm=True)"
        # wI = self.labelD["widthI"]

        # equation
        spL = eqS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(sp.simplify(spS), _clash2, evaluate=False))
        eq1S = textwrap.indent(eq1S, "    ")
        refS = refS.rjust(self.labelD["widthI"])
        uS = refS + "\n" + eq1S + "\n\n"
        rS = "\n\n..  code:: \n\n\n" + refS + "\n" + eqS + "\n\n"
        xS = ".. raw:: math\n\n   " + eqS + "\n"
        if unit1S != "-":
            exec(eqS, globals(), self.rivtD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivtD)

        # rivtL and rivtD append
        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
        vxS = str(valU).strip()
        vxL = vxS.split(" ")
        exS = vxL[0] + " * " + vxL[1].upper()
        ex2S = spL[0].strip() + " = " + exS
        exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
        self.rivtL.append(exvS)

        # equation and table elements
        symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        hdr1L.append(spL[0])
        hdr1L.append("[" + spL[0] + "]")
        for vS in symaO:
            hdr1L.append(str(vS))
        numvarI = len(symaO) + 2
        # print("header----------", hdr1L)
        # eval value
        eval(fmt1S)
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        tbl1L.append(str(val1U))
        tbl1L.append(str(val2U))
        # print("table--------------", tbl1L)
        # loop over variables
        eval(fmt2S)
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivtD)
            tbl1L.append(str(a1U))
            # print("ao", aO, a1U)
        # write table
        # print(tbl1L)
        alignL = []
        tblL = [tbl1L]
        tblfmt = "rst"
        for nI in range(numvarI):
            alignL.append("center")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                headers=hdr1L,
                showindex=False,
                colalign=alignL,
            )
        )
        uS += output.getvalue()
        rS += output.getvalue()
        xS += output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return (
            self.uS,
            self.rS,
            self.xS,
            self.folderD,
            self.labelD,
            self.rivtD,
            self.rivtL,
        )

    # endregion

    def lC(self):
        """center text"""
        # region
        lineS = self.strngS
        self.uS = lineS.center(int(self.labelD["widthI"])) + "\n"
        self.rS = lineS.center(int(self.labelD["widthI"])) + "\n"
        self.xS = "\n::\n\n" + lineS.center(int(self.labelD["widthI"])) + "\n"
        # endregion

    def lD(self):
        """footnote description"""
        # region
        lineS = self.strngS
        ftnumI = self.labelD["noteL"].pop(0)
        self.uS = "[" + str(ftnumI) + "] " + lineS
        self.rS = "[" + str(ftnumI) + "] " + lineS
        self.xS = "[" + str(ftnumI) + "] " + lineS
        # endregion

    def lE(self):
        """number equation"""
        # region
        lineS = self.strngS
        enumI = int(self.labelD["equI"])
        self.labelD["equI"] = enumI + 1
        fillS = "Eq " + str(enumI)
        self.uS = fillS + " - " + lineS
        fillS = "**Eq " + str(enumI) + "**"
        self.rS = lineS + " - " + fillS + "\n"
        self.xS = lineS + " - " + fillS + "\n"
        # endregion

    def lF(self):
        """number figure"""
        # region
        lineS = self.strngS
        fnumI = int(self.labelD["figI"])
        self.labelD["figI"] = fnumI + 1
        self.uS = "Fig. " + str(fnumI) + " - " + lineS + "\n"
        self.rS = "**Fig. " + str(fnumI) + " -** " + lineS + "\n"
        self.xS = "**Fig. " + str(fnumI) + " -** " + lineS + "\n"
        # endregion

    def lN(self):
        """number footnote"""
        # region
        lineS = self.strngS
        ftnumI = self.labelD["footL"].pop(0)
        self.labelD["noteL"].append(ftnumI + 1)
        self.labelD["footL"].append(ftnumI + 1)
        self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.rS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.xS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        # endregion

    def lS(self):
        """format sympy"""
        # region
        lineS = self.strngS
        spS = lineS.strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        self.uS = textwrap.indent(lineS, "     ")
        self.rS = "\n\n.. code:: \n\n\n" + self.uS + "\n\n"
        self.xS = ".. raw:: math\n\n   " + lineS + "\n"
        # endregion

    def lT(self):
        """number table"""
        # region
        lineS = self.strngS
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.uS = "\nTable " + str(tnumI) + ": " + lineS
        self.rS = "\n**Table " + fillS + "**: " + lineS
        self.xS = "\n**Table " + fillS + "**: " + lineS
        # endregion

    def lU(self):
        "format url link"
        # region
        lineS = self.strngS
        lineL = lineS.split(",")
        self.uS = lineL[0] + ": " + lineL[1]
        self.rS = ".. _" + lineL[0] + ": " + lineL[1]
        self.xS = ".. _" + lineL[0] + ": " + lineL[1]
        # endregion

    def lY(self):
        "format and number sympy"
        # region
        lineS = self.strngS
        spS = lineS.strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        self.uS = textwrap.indent(lineS, "     ")
        self.rS = "\n\n.. code:: \n\n\n" + self.uS + "\n\n"
        self.xS = ".. raw:: math\n\n   " + lineS + "\n"
        # endregion

    def lH(self):
        "horizontal line"
        # region
        self.uS = "-" * 80
        self.rS = "-" * 80
        self.xS = "-" * 80
        # endregion

    def lP(self):
        "new page"
        # region
        pgnS = str(self.labelD["pageI"])
        self.uS = (
            "\n" + "=" * (int(self.labelD["widthI"]) - 10) + " Page " + pgnS + "\n"
        )
        # self.uS = self.labelD["headuS"].replace("p##", pagenoS)
        self.labelD["pageI"] = int(pgnS) + 1
        self.rS = (
            "\n"
            + "_" * self.labelD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.labelD["widthI"]
            + "\n"
        )
        self.xS = (
            "\n"
            + "_" * self.labelD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.labelD["widthI"]
            + "\n"
        )
        # endregion

    def bB(self):
        """bold-indent block"""
        # region
        blockL = self.blockL
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        self.uS = "Table " + str(tnumI) + " - " + blockS
        self.rS = "\n" + "Table " + fillS + ": " + blockS
        self.xS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bC(self):
        """code block"""
        # region
        iS = ""
        for s in blockL:
            s = "    " + s + "\n"
            iS += s

        uS = r2S = rS = iS
        # endregion

    def bI(self):
        """italic-indent block"""
        # region
        print("IIIIIIIIIIIIIIIIIII")
        # endregion

    def bL(self):
        """literal block"""
        # region
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bS(self):
        """indent block"""
        # region
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bX(self):
        """latex block"""
        # region
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "**" + "Table " + fillS + ": " + blockS
        # endregion

    def bV(self):
        """values block"""

        # region
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        tbL = []
        self.uS = "\nTable " + fillS + " - " + self.blockL[0] + "\n\n"
        self.rS = "\n**Table " + fillS + "**: " + self.blockL[0] + "\n\n"
        self.xS = "\n**Table " + fillS + "**: " + self.blockL[0] + "\n\n"

        # print(f"{self.blockL=}")
        for vaS in self.blockL[1:]:
            vaL = vaS.split("|")
            if len(vaL) != 3:
                continue
            if ":=" not in vaL[0]:
                continue
            # print(f"{vaS=}")
            # print(f"{vaL=}")
            eqS = vaL[0].strip()
            eqS = eqS.replace(":=", "=")
            varS = eqS.split("=")[0].strip()
            valS = eqS.split("=")[1].strip()
            unitL = vaL[1].split(",")
            unit1S, unit2S, dec1S = (
                unitL[0].strip(),
                unitL[1].strip(),
                unitL[2].strip(),
            )
            descripS = vaL[2].strip()
            fmt1S = "Unum.set_format(value_format='%." + dec1S + "f', auto_norm=True)"
            eval(fmt1S)

            # rivtL append
            exvS = ",".join((eqS, unit1S, unit2S, dec1S, descripS))
            self.rivtL.append(exvS)

            # rivtD append
            if unit1S != "-":
                try:
                    exec(eqS, globals(), self.rivtD)
                except ValueError as ve:
                    print(f"A ValueError occurred: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                valU = eval(varS, {}, self.rivtD)
                val1U = str(valU.cast_unit(eval(unit1S)))
                val2U = str(valU.cast_unit(eval(unit2S)))
                self.rivtD[varS] = val1U
                # print(f"{self.rivtvD=}")
            else:
                cmdS = varS + " = " + valS
                exec(cmdS, globals(), self.rivtD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])
            self.rivtD[varS] = valU

        # write value table
        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL,
                tablefmt=tblfmt,
                headers=hdrvL,
                showindex=False,
                colalign=alignL,
            )
        )
        self.uS += output.getvalue() + "\n"
        self.rS += output.getvalue() + "\n"
        self.xS += output.getvalue() + "\n"
        sys.stdout = old_stdout
        sys.stdout.flush()
        # endregion
