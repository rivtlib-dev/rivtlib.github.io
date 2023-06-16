import sys
import csv
import textwrap
import logging
from pathlib import Path


class Commands():
    """subclass - convert rivt commands to MD and reST

        ======================================================== ===========
                        command syntax                              scope
        ======================================================== ===========

        || append | folder | file1, file2, ...                         R
        || github | folder | file |repository                          R
        || project | file | type                                       R
        || image | folder | file1, (file2)  | size1, (size2)          I,V
        || table | folder | file  | max width | rows                  I,V
        || text | folder | file  | type                               I,V
        || declare | folder | file | rows                              V
        || assign | folder | file | rows                               V

        """

    def cmd_parse(self, cmdS):
        """_summary_
        """
        self.cmdS = cmdS
        return eval("self." + cmdS+"()")

    def append(self):
        """_summary_
        """
        pass

    def github(self):
        """_summary_
        """
        pass

    def declare(self):
        """import values from files

        """

        locals().update(self.localD)

        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        plenI = 2                       # number of parameters
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        valL = []
        fltfmtS = ""
        with open(pathP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vL = len(vaL)
                vaL += [" "] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["-", "-", "-", "Total"])  # totals
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

        mdS = self.vtable(valL, hdrL, "rst", alignL)

        self.localD.update(locals())

        print(mdS + "\n")
        return mdS

    def list(self):
        """import data from files


            :return lineS: md table
            :rtype: str
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
        self.vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

        return

    def declare(self):
        """import values from files

        """

        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        plenI = 2                       # number of parameters
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        valL = []
        fltfmtS = ""
        with open(pathP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vL = len(vaL)
                vaL += [""] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["_ _", "_ _", "_ _", "Total"])  # totals
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

        rstS = self.vtable(valL, hdrL, "rst", alignL)

        # print(mdS + "\n")
        return rstS

    def vtable(self, tbL, hdrL, tblfmt, alignL):
        """write value table"""

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbL, headers=hdrL, tablefmt=tblfmt,
                showindex=False, colalign=alignL
            )
        )
        mdS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return mdS

        # self.calcS += mdS + "\n"
        # self.rivtD.update(locals())
