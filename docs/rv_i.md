# Module rv_i

I2utf and I2rst classes

None

??? example "View Source"
        """I2utf and I2rst classes

        """

        

        

        import os

        import sys

        import csv

        import textwrap

        import subprocess

        import tempfile

        import re

        import logging

        import time

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

        from IPython.display import display as _display

        from IPython.display import Image as _Image

        

        try:

            from PIL import Image as PImage

            from PIL import ImageOps as PImageOps

        except:

            pass

        

        logging.getLogger("numexpr").setLevel(logging.WARNING)

        # tabulate.PRESERVE_WHITESPACE = True

        

        

        class I2utf:

            """convert insert-string to UTF8 calc"""

        

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

        

            def _refs(self, objnumI: int, typeS: str) -> str:

                """reference label for equations, tables and figures

        

                Args:

                    objnumI (int): equation, table or figure section number

                    typeS (str): label type

        

                Returns:

                    refS (str): reference label

                """

        

                objnumS = str(objnumI).zfill(2)

                cnumS = str(self.sectD["cnumS"])

        

                return typeS + cnumS + "." + objnumS

        

            def _parseUTF(self, cmdL: list, methL: list, tagL: list):

                """parse rivt-string to UTF

        

                Args:

                    cmdL (list): command list

                    methL (list): method list

                    tagL (list): tag list

                """

                locals().update(self.rivtD)

                uL = []  # command arguments

                indxI = -1  # method index

                _rgx = r"\[([^\]]+)]_"  # find tags

        

                for uS in self.strL:

                    if uS[0:2] == "##":

                        continue  # remove review comment

                    uS = uS[4:]  # remove indent

                    if len(uS) == 0:

                        if len(self.valL) > 0:  # print value table

                            hdrL = ["variable", "value", "[value]", "description"]

                            alignL = ["left", "right", "right", "left"]

                            self._vtable(self.valL, hdrL, "rst", alignL)

                            self.valL = []

                            print(uS.rstrip(" "))

                            self.calcS += " \n"

                            self.rivtD.update(locals())

                            continue

                        else:

                            print(" ")

                            self.calcS += "\n"

                            continue

                    try:

                        if uS[0] == "#":

                            continue  # remove comment

                    except:

                        print(" ")  # if uS[0] throws error

                        self.calcS += "\n"

                        continue

                    if re.search(_rgx, uS):  # check for tag

                        utgS = self._tags(uS, tagL)

                        print(utgS.rstrip())

                        self.calcS += utgS.rstrip() + "\n"

                        continue

                    if typeS == "values":

                        self.setcmdD["saveB"] = False

                        if "=" in uS and uS.strip()[-2] == "||":  # set save flag

                            uS = uS.replace("||", " ")

                            self.setcmdD["saveB"] = True

                        if "=" in uS:  # just assign value

                            uL = uS.split("|")

                            self._vassign(uL)

                            continue

                    if typeS == "table":

                        if uS[0:2] == "||":  # check for command

                            uL = uS[2:].split("|")

                            indxI = cmdL.index(uL[0].strip())

                            methL[indxI](uL)

                            continue

                        else:

                            exec(uS)  # otherwise exec Python code

                            continue

                    if uS[0:2] == "||":  # check for command

                        uL = uS[2:].split("|")

                        indxI = cmdL.index(uL[0].strip())

                        methL[indxI](uL)

                        continue

        

                    if typeS != "table":  # skip table print

                        print(uS)

                        self.calcS += uS.rstrip() + "\n"

                    self.rivtD.update(locals())

        

            def e_utf(self) -> tuple:

                """parse eval-string

        

                Returns:

                    calcS (list): utf formatted calc-string (appended)

                    setsectD (dict): section settings

                    setcmdD (dict): command settings

                """

        

                ecmdL = ["text", "table", "image"]

                emethL = [self._itext, self._itable, self._iimage]

                etagL = [

                    "[page]_",

                    "[line]_",

                    "[link]_",

                    "[literal]_",

                    "[foot]_",

                    "[latex]_",

                    "[s]_",

                    "[x]_",

                    "[r]_",

                    "[c]_",

                    "[e]_",

                    "[t]_",

                    "[f]_",

                    "[#]_",

                ]

        

                self._parseUTF("insert", icmdL, imethL, itagL)

        

                return self.calcS, self.setsectD, self.setcmdD

        

            def _itext(self, iL: list):

                """insert text from file

        

                Args:

                    iL (list): text command list

        

                || text | (file.txt) | literal; indent; html

        

                """

        

                txtP = Path(self.folderD["cpathcur"] / iL[1].strip())

                with open(txtP, "r", encoding="utf-8") as txtf1:

                    uL = txtf1.readlines()

                if iL[2].strip() == "indent":

                    txtS = "".join(uL)

                    widthI = self.setcmdD["cwidth"]

                    inS = " " * 4

                    uL = textwrap.wrap(txtS, width=widthI)

                    uL = [inS + S1 + "\n" for S1 in uL]

                    uS = "".join(uL)

                elif iL[2].strip() == "literal":

                    txtS = "  ".join(uL)

                    uS = "\n" + txtS

                elif iL[2].strip() == "literalindent":

                    txtS = "\n\n::\n\n"

                    for iS in uL:

                        txtS += "   " + iS

                    uS = txtS + "\n\n"

                elif iL[2].strip() == "html":

                    txtS = ""

                    flg = 0

                    for iS in uL:

                        if "src=" in iS:

                            flg = 1

                            continue

                        if flg == 1 and '"' in iS:

                            flg = 0

                            continue

                        if flg == 1:

                            continue

                        txtS += iS

                    txtS = htm.html2text(txtS)

                    uS = txtS.replace("\n    \n", "")

                else:

                    txtS = "".join(uL)

                    uS = "\n" + txtS

        

                # print(str(txtP))

                # self.calcS += str(txtP) + "\n"

                print(uS)

                self.calcS += uS + "\n"

        

            def _itable(self, iL: list):

                """insert table from csv or xlsx file

        

                Args:

                    ipl (list): parameter list

                """

                alignD = {"S": "", "D": "decimal",

                          "C": "center", "R": "right", "L": "left"}

                itagL = [

                    "[page]_",

                    "[line]_",

                    "[link]_",

                    "[literal]_",

                    "[foot]_",

                    "[r]_",

                    "[c]_",

                    "[e]_",

                    "[t]_",

                    "[f]_",

                    "[#]_",

                ]

                if len(iL) < 4:

                    iL += [""] * (4 - len(iL))  # pad parameters

                utfS = ""

                contentL = []

                sumL = []

                fileS = iL[1].strip()

                calpS = self.setsectD["fnumS"]

                tfileS = Path(self.folderD["cpathcur"] / fileS)

                extS = fileS.split(".")[1]

                if extS == "csv":

                    with open(tfileS, "r") as csvfile:  # read csv file

                        readL = list(csv.reader(csvfile))

                elif extS == "xlsx":

                    pDF1 = pd.read_excel(tfileS, header=None)

                    readL = pDF1.values.tolist()

                else:

                    return

                incl_colL = list(range(len(readL[1])))

                widthI = self.setcmdD["cwidthI"]

                alignS = self.setcmdD["calignS"]

                saS = alignD[alignS]

                if iL[2].strip():

                    widthL = iL[2].split(",")  # new max col width

                    widthI = int(widthL[0].strip())

                    alignS = widthL[1].strip()

                    saS = alignD[alignS]  # new align

                    self.setcmdD.update({"cwidthI": widthI})

                    self.setcmdD.update({"calignS": alignS})

                totalL = [""] * len(incl_colL)

                if iL[3].strip():  # columns

                    if iL[3].strip() == "[:]":

                        totalL = [""] * len(incl_colL)

                    else:

                        incl_colL = eval(iL[3].strip())

                        totalL = [""] * len(incl_colL)

                ttitleS = readL[0][0].strip() + " [t]_"

                utgS = self._tags(ttitleS, itagL)

                print(utgS.rstrip() + "\n")

                self.calcS += utgS.rstrip() + "\n\n"

                for row in readL[1:]:

                    contentL.append([row[i] for i in incl_colL])

                wcontentL = []

                for rowL in contentL:  # wrap columns

                    wrowL = []

                    for iS in rowL:

                        templist = textwrap.wrap(str(iS), int(widthI))

                        templist = [i.replace("""\\n""", """\n""") for i in templist]

                        wrowL.append("""\n""".join(templist))

                    wcontentL.append(wrowL)

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(

                    tabulate(

                        wcontentL,

                        tablefmt="rst",

                        headers="firstrow",

                        numalign="decimal",

                        stralign=saS,

                    )

                )

                utfS = output.getvalue()

                sys.stdout = old_stdout

        

                print(str(tfileS))

                print(utfS)

                self.calcS += str(tfileS) + "\n"

                self.calcS += utfS + "\n"

        

            def _iimage(self, iL: list):

                """insert one or two images from file

        

                Args:

                    iL (list): image parameters

                """

                utfS = ""

                if "," in iL[1]:  # two images

                    scaleF = iL[2].split(",")

                    scale1F = float(scaleF[0])

                    scale2F = float(scaleF[1])

                    self.setcmdD.update({"scale1F": scale1F})

                    self.setcmdD.update({"scale2F": scale2F})

                    fileS = iL[1].split(",")

                    file1S = fileS[0].strip()

                    file2S = fileS[1].strip()

                    docpS = "d" + self.setsectD["cnumS"]

                    img1S = str(Path(self.folderD["dpathcur"] / file1S))

                    img2S = str(Path(self.folderD["dpathcur"] / file2S))

                    # pshrt1S = str(Path(*Path(img1S).parts[-4:]))

                    # pshrt2S = str(Path(*Path(img2S).parts[-4:]))

                    for fS in [img1S, img2S]:

                        utfS += "Figure path: " + fS + "\n"

                        try:

                            _display(_Image(fS))

                        except:

                            pass

                    print(utfS)

                    self.calcS += utfS + "\n"

                else:  # one image

                    scale1F = float(iL[2])

                    self.setcmdD.update({"scale1F": scale1F})

                    fileS = iL[1].split(",")

                    file1S = fileS[0].strip()

                    docpS = "d" + self.setsectD["cnumS"]

                    img1S = str(Path(self.folderD["dpathcur"] / file1S))

                    utfS += "Figure path: " + img1S + "\n"

                    try:

                        _display(_Image(img1S))

                    except:

                        pass

                    print(utfS)

                    self.calcS += utfS + "\n"

        

            def _ilatex(self, iL: list):

                """insert latex text from file

        

                Args:

                    iL (list): text command list

                """

        

                calP = "c" + self.setsectD["cnumS"]

                txapath = Path(self.folderD["dpath0"] / iL[1].strip())

                with open(txapath, "r") as txtf1:

                    uL = txtf1.readlines()

                if iL[2].strip() == "indent":

                    txtS = "".join(uL)

                    widthI = self.setcmdD["cwidth"]

                    inS = " " * 4

                    uL = textwrap.wrap(txtS, width=widthI)

                    uL = [inS + S1 + "\n" for S1 in uL]

                    uS = "".join(uL)

                elif iL[2].strip() == "literal":

                    txtS = "  ".join(uL)

                    uS = "\n" + txtS

                else:

                    txtS = "".join(uL)

                    uS = "\n" + txtS

        

                self.calcS += uS + "\n"

        

                print(uS)

                self.calcS += uS + "\n"

        

        

        class I2rst:

            """convert rivt-strings to reST strings

        

            Args:

            exportS (str): stores values that are written to file

            strL (list): calc rivt-strings

            folderD (dict): folder paths

            setcmdD (dict): command settings

            setsectD (dict): section settings

            rivtD (dict): global rivt dictionary

        

            """

        

            def __init__(

                self,

                strL: list,

                folderD: dict,

                setcmdD: dict,

                setsectD: dict,

                rivtD: dict,

                exportS: str,

            ):

                self.restS = """"""  # restructured text string

                self.exportS = exportS  # value export string

                self.strL = strL  # rivt-string list

                self.valL = []  # value blocklist

                self.folderD = folderD

                self.setsectD = setsectD

                self.setcmdD = setcmdD

                self.rivtD = rivtD

        

            def _parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list):

                """parse rivt-string to reST

        

                Args:

                    typeS (str): rivt-string type

                    cmdL (list): command list

                    methL (list): method list

                    tagL (list): tag list

                """

                locals().update(self.rivtD)

                uL = []  # command arguments

                indxI = -1  # method index

                _rgx = r"\[([^\]]+)]_"  # find tags

        

                for uS in self.strL:

                    if uS[0:2] == "##":

                        continue  # remove comment

                    uS = uS[4:]  # remove indent

                    if len(uS) == 0:

                        if len(self.valL) > 0:  # print value table

                            fltfmtS = ""

                            hdrL = ["variable", "value", "[value]", "description"]

                            alignL = ["left", "right", "right", "left"]

                            self._vtable(self.valL, hdrL, "rst", alignL, fltfmtS)

                            self.valL = []

                            self.restS += "\n\n"

                            self.rivtD.update(locals())

                            continue

                        else:

                            # self.restS += "?x?vspace{7pt}"

                            self.restS += "\n"

                            continue

                    try:

                        if uS[0] == "#":

                            continue  # remove comment

                    except:

                        self.restS += "\n"

                        continue

                    if uS.strip() == "[literal]_":

                        continue

                    if re.search(_rgx, uS):  # check for tag

                        utgS = self._tags(uS, tagL)

                        self.restS += utgS.rstrip() + "\n"

                        continue

                    if typeS == "values":  # chk for values

                        self.setcmdD["saveB"] = False

                        if "=" in uS and uS.strip()[-2] == "||":  # value to file

                            uS = uS.replace("||", " ")

                            self.setcmdD["saveB"] = True

                        if "=" in uS:  # assign value

                            uL = uS.split("|")

                            self._vassign(uL)

                            continue

                    if typeS == "table":  # check for table

                        if uS[0:2] == "||":

                            uL = uS[2:].split("|")

                            indxI = cmdL.index(uL[0].strip())

                            methL[indxI](uL)

                            continue

                        else:

                            exec(uS)  # exec table code

                            continue

                    if uS[0:2] == "||":  # check for cmd

                        # print(f"{cmdL=}")

                        uL = uS[2:].split("|")

                        indxI = cmdL.index(uL[0].strip())

                        methL[indxI](uL)

                        continue  # call any cmd

        

                    self.rivtD.update(locals())

                    if typeS != "table":  # skip table prnt

                        self.restS += uS.rstrip() + "\n"

        

            def i_rst(self) -> tuple:

                """parse insert-string

        

                Returns:

                    calcS (list): utf formatted calc-string (appended)

                    setsectD (dict): section settings

                    setcmdD (dict): command settings

                """

        

                icmdL = ["text", "table", "image"]

                imethL = [

                    self._itext,

                    self._itable,

                    self._iimage,

                ]

                itagL = [

                    "[page]_",

                    "[line]_",

                    "[link]_",

                    "[literal]_",

                    "[foot]_",

                    "[s]_",

                    "[x]_",

                    "[r]_",

                    "[c]_",

                    "[e]_",

                    "[t]_",

                    "[f]_",

                    "[#]_",

                ]

        

                self._parseRST("insert", icmdL, imethL, itagL)

        

                return self.restS, self.setsectD, self.setcmdD

        

            def _itext(self, iL: list):

                """insert text from file

        

                Args:

                    iL (list): text command list

                """

                txapath = Path(self.folderD["cpathcur"] / iL[1].strip())

                with open(txapath, "r", encoding="utf-8") as txtf1:

                    rstL = txtf1.readlines()

                if iL[2].strip() == "indent":

                    txtS = "".join(rstL)

                    widthI = self.setcmdD["cwidth"]

                    inS = " " * 4

                    rstL = textwrap.wrap(txtS, width=widthI)

                    rstL = [inS + S1 + "\n" for S1 in rstL]

                    rstS = "".join(rstL)

                elif iL[2].strip() == "literal":

                    txtS = " ".join(rstL)

                    rstS = "\n\n::\n\n" + txtS + "\n\n"

                elif iL[2].strip() == "literalindent":

                    txtS = "\n\n::\n\n"

                    for iS in iL:

                        txtS += "   " + iS

                    rstS = txtS + "\n\n"

                elif iL[2].strip() == "html":

                    txtS = ""

                    flg = 0

                    for iS in rstL:

                        if "src=" in iS:

                            flg = 1

                            continue

                        if flg == 1 and '"' in iS:

                            flg = 0

                            continue

                        if flg == 1:

                            continue

                        txtS += iS

                    txtS = htm.html2text(txtS)

                    txtS = "   " + txtS.replace("\n    \n", "")

                    rstL = txtS.split("\n")

                    for num, iS in enumerate(rstL):

                        rstL[num] = "   " + iS

                    rstS = "\n".join(rstL[1:])

                    rstS = "\n\n::\n\n" + rstS + "\n\n"

                else:

                    txtS = "".join(rstL)

                    rstS = "\n" + txtS

        

                self.restS += rstS + "\n"

        

            def _itable(self, iL: list):

                """insert table from csv or xlsx file

        

                Args:

                    ipl (list): parameter list

                """

                alignD = {"S": "", "D": "decimal",

                          "C": "center", "R": "right", "L": "left"}

                itagL = [

                    "[page]_",

                    "[line]_",

                    "[link]_",

                    "[literal]_",

                    "[foot]_",

                    "[r]_",

                    "[c]_",

                    "[e]_",

                    "[t]_",

                    "[f]_",

                    "[#]_",

                    "[n]_",

                ]

                if len(iL) < 4:

                    iL += [""] * (4 - len(iL))  # pad parameters

                utfS = ""

                contentL = []

                sumL = []

                fileS = iL[1].strip()

                calpS = self.setsectD["fnumS"]

                tfileS = Path(self.folderD["cpathcur"] / fileS)

                extS = fileS.split(".")[1]

                if extS == "csv":

                    with open(tfileS, "r") as csvfile:  # read csv file

                        readL = list(csv.reader(csvfile))

                elif extS == "xlsx":

                    tDF1 = pd.read_excel(tfileS, header=None)

                    readL = tDF1.values.tolist()

                else:

                    return

                incl_colL = list(range(len(readL[1])))

                widthI = self.setcmdD["cwidthI"]

                alignS = self.setcmdD["calignS"]

                saS = alignD[alignS]

                if iL[2].strip():

                    widthL = iL[2].split(",")  # new max col width

                    widthI = int(widthL[0].strip())

                    alignS = widthL[1].strip()

                    self.setcmdD.update({"cwidthI": widthI})

                    self.setcmdD.update({"calignS": alignS})

                    saS = alignD[alignS]  # new align

                totalL = [""] * len(incl_colL)

                if iL[3].strip():  # columns

                    if iL[3].strip() == "[:]":

                        totalL = [""] * len(incl_colL)

                    else:

                        incl_colL = eval(iL[3].strip())

                        totalL = [""] * len(incl_colL)

                ttitleS = readL[0][0].strip() + " [t]_"

                utgS = self._tags(ttitleS, itagL)

                self.restS += utgS.rstrip() + "\n\n"

                for row in readL[1:]:

                    contentL.append([row[i] for i in incl_colL])

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(

                    tabulate(

                        contentL,

                        tablefmt="latex",

                        headers="firstrow",

                        numalign="decimal",

                        stralign=saS,

                    )

                )

                rstS = output.getvalue()

                sys.stdout = old_stdout

        

                # print(rstS)

                cS = 0

                self.restS += ".. raw:: latex" + "\n\n"

                for i in rstS.split("\n"):

                    counter = i.count("&")

                    if counter > 0:

                        cS = "{" + alignS * (counter + 1) + "}"

                        continue

                # self.restS += "  \\vspace{-.1in}"

                self.restS += "  \\begin{tabulary}{1.0\\textwidth}" + cS + "\n"

                inrstS = ""

                for i in rstS.split("\n"):

                    inrstS += "  " + i + "\n"

                self.restS += inrstS

                self.restS += "  \\end{tabulary}\n"

                self.restS += "  \\vspace{.15in}\n"

        

            def _iimage(self, iL: list):

                """insert one or two images from file

        

                Args:

                    il (list): image parameters

                """

                rstS = ""

                fileS = iL[1].split(",")

                file1S = fileS[0].strip()

                fileS = iL[1].split(",")

                file1S = fileS[0].strip()

                img1S = str(Path(self.folderD["dpathcur"] / file1S).as_posix())

                scaleF = iL[2].split(",")

                scale1S = str(int(scaleF[0])) + "%"

                self.setcmdD.update({"scale1F": scale1S})

                if "," in iL[1]:  # two images

                    scale2S = str(int(scaleF[1])) + "%"

                    self.setcmdD.update({"scale2F": scale2S})

                    file2S = fileS[1].strip()

                    img2S = str(Path(self.folderD["dpathcur"] / file2S).as_posix())

                    pic1S = "|pic" + str(self.setsectD["counter"] + 1) + "|"

                    pic2S = "|pic" + str(self.setsectD["counter"] + 2) + "|"

                    self.setsectD["counter"] = self.setsectD["counter"] + 3

                    rstS += (

                        pic1S

                        + "  ____  "

                        + pic2S

                        + "\n\n"

                        + ".. "

                        + pic1S

                        + " image:: "

                        + img1S

                        + "\n"

                        + "   :width: "

                        + scale1S

                        + "\n\n"

                        + ".. "

                        + pic2S

                        + " image:: "

                        + img2S

                        + "\n"

                        + "   :width: "

                        + scale2S

                        + "\n"

                    )

                else:  # one image

                    rstS += (

                        ".. image:: "

                        + img1S

                        + "\n"

                        + "   :width: "

                        + scale1S

                        + "\n"

                        + "   :align: left \n"

                    )

        

                self.restS += rstS + "\n"

                time.sleep(1)

## Variables

```python3
ALLOW_THREADS
```

```python3
BUFSIZE
```

```python3
CLIP
```

```python3
ERR_CALL
```

```python3
ERR_DEFAULT
```

```python3
ERR_IGNORE
```

```python3
ERR_LOG
```

```python3
ERR_PRINT
```

```python3
ERR_RAISE
```

```python3
ERR_WARN
```

```python3
FLOATING_POINT_SUPPORT
```

```python3
FPE_DIVIDEBYZERO
```

```python3
FPE_INVALID
```

```python3
FPE_OVERFLOW
```

```python3
FPE_UNDERFLOW
```

```python3
False_
```

```python3
Inf
```

```python3
Infinity
```

```python3
MAXDIMS
```

```python3
MAY_SHARE_BOUNDS
```

```python3
MAY_SHARE_EXACT
```

```python3
NAN
```

```python3
NINF
```

```python3
NZERO
```

```python3
NaN
```

```python3
PINF
```

```python3
PZERO
```

```python3
RAISE
```

```python3
SHIFT_DIVIDEBYZERO
```

```python3
SHIFT_INVALID
```

```python3
SHIFT_OVERFLOW
```

```python3
SHIFT_UNDERFLOW
```

```python3
ScalarType
```

```python3
True_
```

```python3
UFUNC_BUFSIZE_DEFAULT
```

```python3
UFUNC_PYVALS_NAME
```

```python3
WRAP
```

```python3
absolute
```

```python3
add
```

```python3
arccos
```

```python3
arccosh
```

```python3
arcsin
```

```python3
arcsinh
```

```python3
arctan
```

```python3
arctan2
```

```python3
arctanh
```

```python3
bitwise_and
```

```python3
bitwise_not
```

```python3
bitwise_or
```

```python3
bitwise_xor
```

```python3
cbrt
```

```python3
ceil
```

```python3
conj
```

```python3
conjugate
```

```python3
copysign
```

```python3
cos
```

```python3
cosh
```

```python3
deg2rad
```

```python3
degrees
```

```python3
divide
```

```python3
divmod
```

```python3
e
```

```python3
equal
```

```python3
euler_gamma
```

```python3
exp
```

```python3
exp2
```

```python3
expm1
```

```python3
fabs
```

```python3
float_power
```

```python3
floor
```

```python3
floor_divide
```

```python3
fmax
```

```python3
fmin
```

```python3
fmod
```

```python3
frexp
```

```python3
gcd
```

```python3
greater
```

```python3
greater_equal
```

```python3
greeks
```

```python3
heaviside
```

```python3
hypot
```

```python3
inf
```

```python3
infty
```

```python3
invert
```

```python3
isfinite
```

```python3
isinf
```

```python3
isnan
```

```python3
isnat
```

```python3
lcm
```

```python3
ldexp
```

```python3
left_shift
```

```python3
less
```

```python3
less_equal
```

```python3
little_endian
```

```python3
log
```

```python3
log10
```

```python3
log1p
```

```python3
log2
```

```python3
logaddexp
```

```python3
logaddexp2
```

```python3
logical_and
```

```python3
logical_not
```

```python3
logical_or
```

```python3
logical_xor
```

```python3
matmul
```

```python3
maximum
```

```python3
minimum
```

```python3
mod
```

```python3
modf
```

```python3
multiply
```

```python3
nan
```

```python3
negative
```

```python3
newaxis
```

```python3
nextafter
```

```python3
not_equal
```

```python3
pi
```

```python3
positive
```

```python3
power
```

```python3
rad2deg
```

```python3
radians
```

```python3
reciprocal
```

```python3
remainder
```

```python3
right_shift
```

```python3
rint
```

```python3
sctypeDict
```

```python3
sctypes
```

```python3
sign
```

```python3
signbit
```

```python3
sin
```

```python3
sinh
```

```python3
spacing
```

```python3
sqrt
```

```python3
square
```

```python3
subtract
```

```python3
tan
```

```python3
tanh
```

```python3
tracemalloc_domain
```

```python3
true_divide
```

```python3
trunc
```

```python3
typecodes
```

## Classes

### I2rst

```python3
class I2rst(
    strL: list,
    folderD: dict,
    setcmdD: dict,
    setsectD: dict,
    rivtD: dict,
    exportS: str
)
```

#### Methods

    
#### i_rst

```python3
def i_rst(
    self
) -> tuple
```

    
parse insert-string

**Returns:**

| Type | Description |
|---|---|
| None | calcS (list): utf formatted calc-string (appended)
setsectD (dict): section settings
setcmdD (dict): command settings |

??? example "View Source"
            def i_rst(self) -> tuple:

                """parse insert-string

        

                Returns:

                    calcS (list): utf formatted calc-string (appended)

                    setsectD (dict): section settings

                    setcmdD (dict): command settings

                """

        

                icmdL = ["text", "table", "image"]

                imethL = [

                    self._itext,

                    self._itable,

                    self._iimage,

                ]

                itagL = [

                    "[page]_",

                    "[line]_",

                    "[link]_",

                    "[literal]_",

                    "[foot]_",

                    "[s]_",

                    "[x]_",

                    "[r]_",

                    "[c]_",

                    "[e]_",

                    "[t]_",

                    "[f]_",

                    "[#]_",

                ]

        

                self._parseRST("insert", icmdL, imethL, itagL)

        

                return self.restS, self.setsectD, self.setcmdD

### I2utf

```python3
class I2utf(
    strL: list,
    folderD,
    cmdD,
    sectD
)
```

#### Methods

    
#### e_utf

```python3
def e_utf(
    self
) -> tuple
```

    
parse eval-string

**Returns:**

| Type | Description |
|---|---|
| None | calcS (list): utf formatted calc-string (appended)
setsectD (dict): section settings
setcmdD (dict): command settings |

??? example "View Source"
            def e_utf(self) -> tuple:

                """parse eval-string

        

                Returns:

                    calcS (list): utf formatted calc-string (appended)

                    setsectD (dict): section settings

                    setcmdD (dict): command settings

                """

        

                ecmdL = ["text", "table", "image"]

                emethL = [self._itext, self._itable, self._iimage]

                etagL = [

                    "[page]_",

                    "[line]_",

                    "[link]_",

                    "[literal]_",

                    "[foot]_",

                    "[latex]_",

                    "[s]_",

                    "[x]_",

                    "[r]_",

                    "[c]_",

                    "[e]_",

                    "[t]_",

                    "[f]_",

                    "[#]_",

                ]

        

                self._parseUTF("insert", icmdL, imethL, itagL)

        

                return self.calcS, self.setsectD, self.setcmdD