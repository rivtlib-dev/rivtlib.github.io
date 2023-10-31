# Module cmd_rst

??? example "View Source"
        #

        import logging

        import warnings

        import fnmatch

        import os

        import sys

        import textwrap

        from io import StringIO

        from pathlib import Path

        import csv

        import matplotlib.pyplot as plt

        import pandas as pd

        import sympy as sp

        import numpy.linalg as la

        import numpy as np

        from sympy.parsing.latex import parse_latex

        from sympy.abc import _clash2

        from sympy.core.alphabets import greeks

        from tabulate import tabulate

        from pathlib import Path

        from datetime import datetime

        from rivtlib import parse

        from rivtlib.cmd_parse import Commands

        from rivtlib.units import *

        

        class CmdRST(Commands):

            def __init__(self, paramL, incrD, folderD,  localD):

                """_summary_

                :param paramL: _description_

                :type paramL: _type_

                :param incrD: _description_

                :type incrD: _type_

                :param folderD: _description_

                :type folderD: _type_

                :param localD: _description_

                :type localD: _type_

                :return: _description_

                :rtype: _type_

                """

                self.localD = localD

                self.folderD = folderD

                self.incrD = incrD

                self.widthII = incrD["widthI"] - 1

                self.paramL = paramL

                self.errlogP = folderD["errlogP"]

                modnameS = self.incrD["modnameS"]

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

                fileS = paramL[0].strip()

                if fileS[0:4] == "data":

                    self.currP = folderD["docpathP"]

                    self.relP = fileS

                elif fnmatch.fnmatch(fileS[0:5], "r[0-9]"):

                    self.currP = Path(folderD["pubP"])

                else:

                    self.currP = Path(folderD["prvP"])

            def project(self):

                """insert project information from csv, xlsx or syk

                    :return lineS: md table

                    :rtype: str

                """

                alignD = {"s": "", "d": "decimal",

                          "c": "center", "r": "right", "l": "left"}

                tableS = ""

                plenI = 2

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} not evaluated: {plenI} parameters required")

                    return

                folderP = Path(self.folderD["prvP"])

                fileP = Path(self.paramL[0].strip())

                pathP = Path(folderP, fileP)                    # file path

                extS = (pathP.suffix).strip()

                txttypeS = self.paramL[1].strip()

                with open(pathP, "r", encoding="utf-8") as f2:

                    txtfileL = f2.readlines()

                j = ""

                if extS == ".txt":

                    # print(f"{txttypeS=}")

                    if txttypeS == "plain":

                        for iS in txtfileL:

                            j += "   " + iS

                        return "\n\n::\n\n" + j + "\n\n"

                    elif txttypeS == "code":

                        pass

                    elif txttypeS == "tags":

                        xtagC = parse.RivtParseTag(

                            self.folderD, self.incrD,  self.localD)

                        xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(

                            txtfileL)

                        return xrstS

                else:

                    logging.info(

                        f"{self.cmdS} not evaluated: {extS} file not processed")

                    return

            def image(self):

                """insert image from file

                Args:

                    il (list): image parameters

                """

                rstS = ""

                iL = self.paramL

                if len(iL[0].split(",")) == 1:

                    scale1S = iL[1].strip()

                    file1S = iL[0].strip()

                    img1S = str(Path(self.currP, file1S))

                    img1S = img1S.replace("\\", "/")

                    rstS = ("\n.. image:: "

                            + img1S + "\n"

                            + "   :scale: "

                            + scale1S + "%" + "\n"

                            + "   :align: center"

                            + "\n\n"

                            )

                elif len(iL[0].split(",")) == 2:

                    iL = iL[0].split(",")

                    file1S = iL[0].strip()

                    file2S = iL[1].strip()

                    iL = iL[1].split(",")

                    scale1S = iL[0]

                    scale2S = iL[1]

                    img1S = str(Path(self.currP, file1S))

                    img2S = str(Path(self.currP, file1S))

                    img1S = img1S.replace("\\", "/")

                    img2S = img2S.replace("\\", "/")

                    rstS = ("|L| . |R|"

                            + "\n\n"

                            + ".. |L| image:: "

                            + img1S + "\n"

                            + "   :width: "

                            + scale1S + "%"

                            + "\n\n"

                            + ".. |R| image:: "

                            + img2S + "\n"

                            + "   :width: "

                            + scale2S + "%"

                            + "\n\n"

                            )

                return rstS

            def table(self):

                """insert table from csv or xlsx file

                Args:

                    ipl (list): parameter list

                """

                alignD = {"s": "", "d": "decimal",

                          "c": "center", "r": "right", "l": "left"}

                tableS = ""

                plenI = 4

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} command not evaluated: {plenI} parameters required")

                    return

                if self.paramL[0] == "data":

                    folderP = Path(self.folderD["dataP"])

                else:

                    folderP = Path(self.folderD["dataP"])

                fileP = Path(self.paramL[1].strip())

                pathP = Path(folderP / fileP)                    # file path

                maxwI = int(self.paramL[2].split(",")[0])        # max column width

                alignS = alignD[self.paramL[2].split(",")[1].strip()]

                align2S = self.paramL[2].split(",")[1].strip()

                colS = self.paramL[3].strip()                    # rows read

                extS = (pathP.suffix).strip()                    # file suffix

                if extS == ".csv":                               # read csv file

                    with open(pathP, "r") as csvfile:

                        readL = list(csv.reader(csvfile))

                elif extS == ".xlsx":                            # read xls file

                    pdfO = pd.read_excel(pathP, header=None)

                    readL = pdfO.values.tolist()

                else:

                    logging.info(

                        f"{self.cmdS} command not evaluated: {extS} files not processed")

                    return

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(tabulate(readL, tablefmt="rst", maxcolwidths=maxwI,

                                      headers="firstrow", numalign="decimal"))

                rstS = output.getvalue()

                sys.stdout = old_stdout

                # restS = ".. raw:: latex" + "\n\n"       # align cells

                # # for i in rstS.split("\n"):

                # #     counter = i.count("&")

                # #     if counter > 0:

                # #         cS = "{|" + (align2S + "|") * (counter + 1) + "}"

                # #         cS = "{" + align2S * (counter + 1) + "}"

                # #         continue

                # restS += "  \\vspace{.15in}" + "\n"

                # inrstS = ""

                # for i in rstS.split("\n"):

                #     inrstS += "  " + i + "\n\n"

                # restS = restS + inrstS

                # restS += "  \\vspace{.15in}\n"

                restS = "\n" + rstS + "\n\n"

                return restS

            def text(self):

                """insert text from file

                || text | folder | file | type | shade

                """

                plenI = 3

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} command not evaluated:  \

                                            {plenI} parameters required")

                    return

                if self.paramL[0] == "data":

                    folderP = Path(self.folderD["dataP"])

                else:

                    folderP = Path(self.folderD["dataP"])

                fileP = Path(self.paramL[1].strip())

                pathP = Path(folderP / fileP)

                txttypeS = self.paramL[2].strip()

                extS = pathP.suffix

                with open(pathP, "r", encoding="md-8") as f1:

                    txtfileS = f1.read()

                with open(pathP, "r", encoding="md-8") as f2:

                    txtfileL = f2.readlines()

                j = ""

                if extS == ".txt":

                    # print(f"{txttypeS=}")

                    if txttypeS == "plain":

                        for iS in txtfileL:

                            j += "   " + iS

                        return "\n\n::\n\n" + j + "\n\n"

                    elif txttypeS == "code":

                        pass

                    elif txttypeS == "tags":

                        xtagC = parse.RivtParseTag(

                            self.folderD, self.incrD,  self.localD)

                        xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(

                            txtfileL)

                        return xrstS

                elif extS == ".html":

                    txtS = ".. raw:: html" + "\n\n"

                    for iS in txtfileL:

                        j += "   " + iS

                    return txtS + j + "\n\n"

                elif extS == ".tex":

                    if txttypeS == "plain":

                        txtS = ".. raw:: latex" + "\n\n"

                        for iS in txtfileL:

                            j += "   " + iS

                        return txtS + j + "\n\n"

                    if txttypeS == "math":

                        txtS = ".. math:: " + "\n\n"

                        for iS in txtfileL:

                            j += "   " + iS

                        return txtS + j + "\n\n"

## Variables

```python3
greeks
```

## Classes

### CmdRST

```python3
class CmdRST(
    paramL,
    incrD,
    folderD,
    localD
)
```

common methods for rivt to md, utf and reST

======================================================== ===========
                command syntax                              scope
======================================================== ===========

|| append | folder | file1, file2, ...                         R
|| github | folder | file |repository                          R
|| project | file | type                                       R
|| image | folder | file1, (file2)  | size1, (size2)           I 
|| table | folder | file  | max width | rows                   I
|| text | folder | file  | type                                I
|| declare | folder | file | rows                              V
|| assign | folder | file | rows                               V

??? example "View Source"
        class CmdRST(Commands):

            def __init__(self, paramL, incrD, folderD,  localD):

                """_summary_

                :param paramL: _description_

                :type paramL: _type_

                :param incrD: _description_

                :type incrD: _type_

                :param folderD: _description_

                :type folderD: _type_

                :param localD: _description_

                :type localD: _type_

                :return: _description_

                :rtype: _type_

                """

                self.localD = localD

                self.folderD = folderD

                self.incrD = incrD

                self.widthII = incrD["widthI"] - 1

                self.paramL = paramL

                self.errlogP = folderD["errlogP"]

                modnameS = self.incrD["modnameS"]

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

                fileS = paramL[0].strip()

                if fileS[0:4] == "data":

                    self.currP = folderD["docpathP"]

                    self.relP = fileS

                elif fnmatch.fnmatch(fileS[0:5], "r[0-9]"):

                    self.currP = Path(folderD["pubP"])

                else:

                    self.currP = Path(folderD["prvP"])

            def project(self):

                """insert project information from csv, xlsx or syk

                    :return lineS: md table

                    :rtype: str

                """

                alignD = {"s": "", "d": "decimal",

                          "c": "center", "r": "right", "l": "left"}

                tableS = ""

                plenI = 2

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} not evaluated: {plenI} parameters required")

                    return

                folderP = Path(self.folderD["prvP"])

                fileP = Path(self.paramL[0].strip())

                pathP = Path(folderP, fileP)                    # file path

                extS = (pathP.suffix).strip()

                txttypeS = self.paramL[1].strip()

                with open(pathP, "r", encoding="utf-8") as f2:

                    txtfileL = f2.readlines()

                j = ""

                if extS == ".txt":

                    # print(f"{txttypeS=}")

                    if txttypeS == "plain":

                        for iS in txtfileL:

                            j += "   " + iS

                        return "\n\n::\n\n" + j + "\n\n"

                    elif txttypeS == "code":

                        pass

                    elif txttypeS == "tags":

                        xtagC = parse.RivtParseTag(

                            self.folderD, self.incrD,  self.localD)

                        xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(

                            txtfileL)

                        return xrstS

                else:

                    logging.info(

                        f"{self.cmdS} not evaluated: {extS} file not processed")

                    return

            def image(self):

                """insert image from file

                Args:

                    il (list): image parameters

                """

                rstS = ""

                iL = self.paramL

                if len(iL[0].split(",")) == 1:

                    scale1S = iL[1].strip()

                    file1S = iL[0].strip()

                    img1S = str(Path(self.currP, file1S))

                    img1S = img1S.replace("\\", "/")

                    rstS = ("\n.. image:: "

                            + img1S + "\n"

                            + "   :scale: "

                            + scale1S + "%" + "\n"

                            + "   :align: center"

                            + "\n\n"

                            )

                elif len(iL[0].split(",")) == 2:

                    iL = iL[0].split(",")

                    file1S = iL[0].strip()

                    file2S = iL[1].strip()

                    iL = iL[1].split(",")

                    scale1S = iL[0]

                    scale2S = iL[1]

                    img1S = str(Path(self.currP, file1S))

                    img2S = str(Path(self.currP, file1S))

                    img1S = img1S.replace("\\", "/")

                    img2S = img2S.replace("\\", "/")

                    rstS = ("|L| . |R|"

                            + "\n\n"

                            + ".. |L| image:: "

                            + img1S + "\n"

                            + "   :width: "

                            + scale1S + "%"

                            + "\n\n"

                            + ".. |R| image:: "

                            + img2S + "\n"

                            + "   :width: "

                            + scale2S + "%"

                            + "\n\n"

                            )

                return rstS

            def table(self):

                """insert table from csv or xlsx file

                Args:

                    ipl (list): parameter list

                """

                alignD = {"s": "", "d": "decimal",

                          "c": "center", "r": "right", "l": "left"}

                tableS = ""

                plenI = 4

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} command not evaluated: {plenI} parameters required")

                    return

                if self.paramL[0] == "data":

                    folderP = Path(self.folderD["dataP"])

                else:

                    folderP = Path(self.folderD["dataP"])

                fileP = Path(self.paramL[1].strip())

                pathP = Path(folderP / fileP)                    # file path

                maxwI = int(self.paramL[2].split(",")[0])        # max column width

                alignS = alignD[self.paramL[2].split(",")[1].strip()]

                align2S = self.paramL[2].split(",")[1].strip()

                colS = self.paramL[3].strip()                    # rows read

                extS = (pathP.suffix).strip()                    # file suffix

                if extS == ".csv":                               # read csv file

                    with open(pathP, "r") as csvfile:

                        readL = list(csv.reader(csvfile))

                elif extS == ".xlsx":                            # read xls file

                    pdfO = pd.read_excel(pathP, header=None)

                    readL = pdfO.values.tolist()

                else:

                    logging.info(

                        f"{self.cmdS} command not evaluated: {extS} files not processed")

                    return

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(tabulate(readL, tablefmt="rst", maxcolwidths=maxwI,

                                      headers="firstrow", numalign="decimal"))

                rstS = output.getvalue()

                sys.stdout = old_stdout

                # restS = ".. raw:: latex" + "\n\n"       # align cells

                # # for i in rstS.split("\n"):

                # #     counter = i.count("&")

                # #     if counter > 0:

                # #         cS = "{|" + (align2S + "|") * (counter + 1) + "}"

                # #         cS = "{" + align2S * (counter + 1) + "}"

                # #         continue

                # restS += "  \\vspace{.15in}" + "\n"

                # inrstS = ""

                # for i in rstS.split("\n"):

                #     inrstS += "  " + i + "\n\n"

                # restS = restS + inrstS

                # restS += "  \\vspace{.15in}\n"

                restS = "\n" + rstS + "\n\n"

                return restS

            def text(self):

                """insert text from file

                || text | folder | file | type | shade

                """

                plenI = 3

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} command not evaluated:  \

                                            {plenI} parameters required")

                    return

                if self.paramL[0] == "data":

                    folderP = Path(self.folderD["dataP"])

                else:

                    folderP = Path(self.folderD["dataP"])

                fileP = Path(self.paramL[1].strip())

                pathP = Path(folderP / fileP)

                txttypeS = self.paramL[2].strip()

                extS = pathP.suffix

                with open(pathP, "r", encoding="md-8") as f1:

                    txtfileS = f1.read()

                with open(pathP, "r", encoding="md-8") as f2:

                    txtfileL = f2.readlines()

                j = ""

                if extS == ".txt":

                    # print(f"{txttypeS=}")

                    if txttypeS == "plain":

                        for iS in txtfileL:

                            j += "   " + iS

                        return "\n\n::\n\n" + j + "\n\n"

                    elif txttypeS == "code":

                        pass

                    elif txttypeS == "tags":

                        xtagC = parse.RivtParseTag(

                            self.folderD, self.incrD,  self.localD)

                        xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(

                            txtfileL)

                        return xrstS

                elif extS == ".html":

                    txtS = ".. raw:: html" + "\n\n"

                    for iS in txtfileL:

                        j += "   " + iS

                    return txtS + j + "\n\n"

                elif extS == ".tex":

                    if txttypeS == "plain":

                        txtS = ".. raw:: latex" + "\n\n"

                        for iS in txtfileL:

                            j += "   " + iS

                        return txtS + j + "\n\n"

                    if txttypeS == "math":

                        txtS = ".. math:: " + "\n\n"

                        for iS in txtfileL:

                            j += "   " + iS

                        return txtS + j + "\n\n"

------

#### Ancestors (in MRO)

* rivtlib.cmd_parse.Commands

#### Methods

    
#### append

```python3
def append(
    self
)
```

_summary_

??? example "View Source"
            def append(self):

                """_summary_

                """

                pass

    
#### cmd_parse

```python3
def cmd_parse(
    self,
    cmdS
)
```

_summary_

??? example "View Source"
            def cmd_parse(self, cmdS):

                """_summary_

                """

                self.cmdS = cmdS

                return eval("self." + cmdS+"()")

    
#### declare

```python3
def declare(
    self
)
```

import values from files

??? example "View Source"
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

    
#### github

```python3
def github(
    self
)
```

_summary_

??? example "View Source"
            def github(self):

                """_summary_

                """

                pass

    
#### image

```python3
def image(
    self
)
```

insert image from file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| il | list | image parameters | None |

??? example "View Source"
            def image(self):

                """insert image from file

                Args:

                    il (list): image parameters

                """

                rstS = ""

                iL = self.paramL

                if len(iL[0].split(",")) == 1:

                    scale1S = iL[1].strip()

                    file1S = iL[0].strip()

                    img1S = str(Path(self.currP, file1S))

                    img1S = img1S.replace("\\", "/")

                    rstS = ("\n.. image:: "

                            + img1S + "\n"

                            + "   :scale: "

                            + scale1S + "%" + "\n"

                            + "   :align: center"

                            + "\n\n"

                            )

                elif len(iL[0].split(",")) == 2:

                    iL = iL[0].split(",")

                    file1S = iL[0].strip()

                    file2S = iL[1].strip()

                    iL = iL[1].split(",")

                    scale1S = iL[0]

                    scale2S = iL[1]

                    img1S = str(Path(self.currP, file1S))

                    img2S = str(Path(self.currP, file1S))

                    img1S = img1S.replace("\\", "/")

                    img2S = img2S.replace("\\", "/")

                    rstS = ("|L| . |R|"

                            + "\n\n"

                            + ".. |L| image:: "

                            + img1S + "\n"

                            + "   :width: "

                            + scale1S + "%"

                            + "\n\n"

                            + ".. |R| image:: "

                            + img2S + "\n"

                            + "   :width: "

                            + scale2S + "%"

                            + "\n\n"

                            )

                return rstS

    
#### list

```python3
def list(
    self
)
```

import data from files

**Returns:**

| Type | Description |
|---|---|
| lineS | md table |

??? example "View Source"
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

    
#### project

```python3
def project(
    self
)
```

insert project information from csv, xlsx or syk

**Returns:**

| Type | Description |
|---|---|
| lineS | md table |

??? example "View Source"
            def project(self):

                """insert project information from csv, xlsx or syk

                    :return lineS: md table

                    :rtype: str

                """

                alignD = {"s": "", "d": "decimal",

                          "c": "center", "r": "right", "l": "left"}

                tableS = ""

                plenI = 2

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} not evaluated: {plenI} parameters required")

                    return

                folderP = Path(self.folderD["prvP"])

                fileP = Path(self.paramL[0].strip())

                pathP = Path(folderP, fileP)                    # file path

                extS = (pathP.suffix).strip()

                txttypeS = self.paramL[1].strip()

                with open(pathP, "r", encoding="utf-8") as f2:

                    txtfileL = f2.readlines()

                j = ""

                if extS == ".txt":

                    # print(f"{txttypeS=}")

                    if txttypeS == "plain":

                        for iS in txtfileL:

                            j += "   " + iS

                        return "\n\n::\n\n" + j + "\n\n"

                    elif txttypeS == "code":

                        pass

                    elif txttypeS == "tags":

                        xtagC = parse.RivtParseTag(

                            self.folderD, self.incrD,  self.localD)

                        xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(

                            txtfileL)

                        return xrstS

                else:

                    logging.info(

                        f"{self.cmdS} not evaluated: {extS} file not processed")

                    return

    
#### table

```python3
def table(
    self
)
```

insert table from csv or xlsx file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| ipl | list | parameter list | None |

??? example "View Source"
            def table(self):

                """insert table from csv or xlsx file

                Args:

                    ipl (list): parameter list

                """

                alignD = {"s": "", "d": "decimal",

                          "c": "center", "r": "right", "l": "left"}

                tableS = ""

                plenI = 4

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} command not evaluated: {plenI} parameters required")

                    return

                if self.paramL[0] == "data":

                    folderP = Path(self.folderD["dataP"])

                else:

                    folderP = Path(self.folderD["dataP"])

                fileP = Path(self.paramL[1].strip())

                pathP = Path(folderP / fileP)                    # file path

                maxwI = int(self.paramL[2].split(",")[0])        # max column width

                alignS = alignD[self.paramL[2].split(",")[1].strip()]

                align2S = self.paramL[2].split(",")[1].strip()

                colS = self.paramL[3].strip()                    # rows read

                extS = (pathP.suffix).strip()                    # file suffix

                if extS == ".csv":                               # read csv file

                    with open(pathP, "r") as csvfile:

                        readL = list(csv.reader(csvfile))

                elif extS == ".xlsx":                            # read xls file

                    pdfO = pd.read_excel(pathP, header=None)

                    readL = pdfO.values.tolist()

                else:

                    logging.info(

                        f"{self.cmdS} command not evaluated: {extS} files not processed")

                    return

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(tabulate(readL, tablefmt="rst", maxcolwidths=maxwI,

                                      headers="firstrow", numalign="decimal"))

                rstS = output.getvalue()

                sys.stdout = old_stdout

                # restS = ".. raw:: latex" + "\n\n"       # align cells

                # # for i in rstS.split("\n"):

                # #     counter = i.count("&")

                # #     if counter > 0:

                # #         cS = "{|" + (align2S + "|") * (counter + 1) + "}"

                # #         cS = "{" + align2S * (counter + 1) + "}"

                # #         continue

                # restS += "  \\vspace{.15in}" + "\n"

                # inrstS = ""

                # for i in rstS.split("\n"):

                #     inrstS += "  " + i + "\n\n"

                # restS = restS + inrstS

                # restS += "  \\vspace{.15in}\n"

                restS = "\n" + rstS + "\n\n"

                return restS

    
#### text

```python3
def text(
    self
)
```

insert text from file

|| text | folder | file | type | shade

??? example "View Source"
            def text(self):

                """insert text from file

                || text | folder | file | type | shade

                """

                plenI = 3

                if len(self.paramL) != plenI:

                    logging.info(

                        f"{self.cmdS} command not evaluated:  \

                                            {plenI} parameters required")

                    return

                if self.paramL[0] == "data":

                    folderP = Path(self.folderD["dataP"])

                else:

                    folderP = Path(self.folderD["dataP"])

                fileP = Path(self.paramL[1].strip())

                pathP = Path(folderP / fileP)

                txttypeS = self.paramL[2].strip()

                extS = pathP.suffix

                with open(pathP, "r", encoding="md-8") as f1:

                    txtfileS = f1.read()

                with open(pathP, "r", encoding="md-8") as f2:

                    txtfileL = f2.readlines()

                j = ""

                if extS == ".txt":

                    # print(f"{txttypeS=}")

                    if txttypeS == "plain":

                        for iS in txtfileL:

                            j += "   " + iS

                        return "\n\n::\n\n" + j + "\n\n"

                    elif txttypeS == "code":

                        pass

                    elif txttypeS == "tags":

                        xtagC = parse.RivtParseTag(

                            self.folderD, self.incrD,  self.localD)

                        xrstS, self.incrD, self.folderD, self.localD = xtagC.rst_parse(

                            txtfileL)

                        return xrstS

                elif extS == ".html":

                    txtS = ".. raw:: html" + "\n\n"

                    for iS in txtfileL:

                        j += "   " + iS

                    return txtS + j + "\n\n"

                elif extS == ".tex":

                    if txttypeS == "plain":

                        txtS = ".. raw:: latex" + "\n\n"

                        for iS in txtfileL:

                            j += "   " + iS

                        return txtS + j + "\n\n"

                    if txttypeS == "math":

                        txtS = ".. math:: " + "\n\n"

                        for iS in txtfileL:

                            j += "   " + iS

                        return txtS + j + "\n\n"

    
#### txthtml

```python3
def txthtml(
    self,
    txtfileL
)
```

9a _summary_

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
            def txthtml(self, txtfileL):

                """9a _summary_

                :return: _description_

                :rtype: _type_

                """

                txtS = ""

                flg = 0

                for iS in txtfileL:

                    if "src=" in iS:

                        flg = 1

                        continue

                    if flg == 1 and '"' in iS:

                        flg = 0

                        continue

                    if flg == 1:

                        continue

                    txtS += " "*4 + iS

                    txtS = htm.html2text(txtS)

                    mdS = txtS.replace("\n    \n", "")

                    return mdS

    
#### txttex

```python3
def txttex(
    self,
    txtfileS,
    txttypeS
)
```

9b _summary_

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
            def txttex(self, txtfileS, txttypeS):

                """9b _summary_

                :return: _description_

                :rtype: _type_

                """

                soup = TexSoup(txtfileS)

                soupL = list(soup.text)

                soupS = "".join(soupL)

                soup1L = []

                soupS = soupS.replace("\\\\", "\n")

                soupL = soupS.split("\n")

                for s in soupL:

                    sL = s.split("&")

                    sL = s.split(">")

                    try:

                        soup1L.append(sL[0].ljust(10) + sL[1])

                    except:

                        soup1L.append(s)

                soupS = [s.replace("\\", " ") for s in soup1L]

                soupS = "\n".join(soup1L)

                return soupS

    
#### vtable

```python3
def vtable(
    self,
    tbL,
    hdrL,
    tblfmt,
    alignL
)
```

write value table

??? example "View Source"
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