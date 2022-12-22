# Module rv_r

R2utf and R2rst classes

None

??? example "View Source"
        #!python

        """R2utf and R2rst classes

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

        

        

        class R2utf:

            """convert repo-string to UTF8 calc"""

        

            def __init__(self, strL: list, folderD: dict, tagD: dict):

                """process rivt-string to UTF8 calc-string

        

                The RvR2utf class converts repo-strings to calc-strings.

        

                Args:

                    strL (list): calc lines

                    folderD (dict): folder paths

                    cmdD (dict): command settings

                    sectD (dict): section settings

                """

        

                self.utfS = """"""  # utf calc string

                self.strL = strL

                self.folderD = folderD

                self.tagD = tagD

                self.valL = []  # value list

        

            def parseRutf(self, strL: list, cmdD: dict, cmdL: list, methL: list):

                """parse rivt-string to UTF

        

                Args:

                    cmdL (list): command list

                    methL (list): method list

                    tagL (list): tag list

                """

                for uS in self.strL:

                    if uS[0:2] == "##":

                        continue  # remove review comment

                    uS = uS[4:]  # remove indent

                    if len(uS) == 0:

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

        

                    self.utfS += uS.rstrip() + "\n"

        

                return self.calcS, self.setsectD

        

            def search(self, rutfL):

                """[summary]

        

                Args:

                    rsL ([type]): [description]

                """

                a = 4

        

            def project(self, rutfL):

                b = 5

        

            def attach(self, rutfL):

                """[summary]

        

                Args:

                    rsL ([type]): [description]

                """

                a = 4

        

            def report(self, rutfL):

                """skip info command for utf calcs

        

                Command is executed only for docs in order to

                separate protected information for shareable calcs.

        

                Args:

                    rL (list): parameter list

                """

        

                """       

                try:

                    filen1 = os.path.join(self.rpath, "reportmerge.txt")

                    print(filen1)

                    file1 = open(filen1, 'r')

                    mergelist = file1.readlines()

                    file1.close()

                    mergelist2 = mergelist[:]

                except OSError:

                    print('< reportmerge.txt file not found in reprt folder >')

                    return

                calnum1 = self.pdffile[0:5]

                file2 = open(filen1, 'w')

                newstr1 = 'c | ' + self.pdffile + ' | ' + self.calctitle

                for itm1 in mergelist:

                    if calnum1 in itm1:

                        indx1 = mergelist2.index(itm1)

                        mergelist2[indx1] = newstr1

                        for j1 in mergelist2:

                            file2.write(j1)

                        file2.close()

                        return

                mergelist2.append("\n" + newstr1)

                for j1 in mergelist2:

                    file2.write(j1)

                file2.close()

                return """

                pass

        

        

        class R2rst:

            """convert rivt-strings to reST strings

        

            Args:

            exportS (str): stores values that are written to file

            strL (list): calc rivt-strings

            folderD (dict): folder paths

            tagD (dict): tag dictionary

        

        

            """

        

            def __init__(self, strL: list, folderD: dict, tagD: dict):

        

                self.restS = """"""  # restructured text string

                self.strL = strL  # rivt-string list

                self.folderD = folderD

                self.tagD = tagD

        

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

        

            def r_rst(self) -> str:

                """parse repository string

        

                Returns:

                     rstS (list): utf formatted calc-string (appended)

                     setsectD (dict): section settings

                """

        

                rcmdL = ["search", "keys", "info", "text", "table", "pdf"]

                rmethL = [

                    self._rsearch,

                    self._rkeys,

                    self._rinfo,

                    self._itext,

                    self._itable,

                    self._rpdf,

                ]

        

                self._parseRST("repository", rcmdL, rmethL, rtagL)

        

            def search(self, rsL):

                a = 4

        

            def project(self, rL):

                """insert tables or text from csv, xlsx or txt file

        

                Args:

                    rL (list): parameter list

        

                Files are read from /docs/docfolder

                The command is identical to itable except file is read from docs/info.

        

                """

                alignD = {"S": "", "D": "decimal", "C": "center", "R": "right", "L": "left"}

                rtagL = [

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

                if len(rL) < 4:

                    rL += [""] * (4 - len(rL))  # pad parameters

                rstS = ""

                contentL = []

                sumL = []

                fileS = rL[1].strip()

                tfileS = Path(self.folderD["dpath0"] / fileS)

                extS = fileS.split(".")[1]

                if extS == "csv":

                    with open(tfileS, "r") as csvfile:  # read csv file

                        readL = list(csv.reader(csvfile))

                elif extS == "xlsx":

                    xDF = pd.read_excel(tfileS, header=None)

                    readL = xDF.values.tolist()

                else:

                    return

                incl_colL = list(range(len(readL[0])))

                widthI = self.setcmdD["cwidthI"]

                alignS = self.setcmdD["calignS"]

                saS = alignD[alignS]

                if rL[2].strip():

                    widthL = rL[2].split(",")  # new max col width

                    widthI = int(widthL[0].strip())

                    alignS = widthL[1].strip()

                    saS = alignD[alignS]  # new alignment

                    self.setcmdD.update({"cwidthI": widthI})

                    self.setcmdD.update({"calignS": alignS})

                totalL = [""] * len(incl_colL)

                if rL[3].strip():  # columns

                    if rL[3].strip() == "[:]":

                        totalL = [""] * len(incl_colL)

                    else:

                        incl_colL = eval(rL[3].strip())

                        totalL = [""] * len(incl_colL)

                ttitleS = readL[0][0].strip() + " [t]_"

                rstgS = self._tags(ttitleS, rtagL)

                self.restS += rstgS.rstrip() + "\n\n"

                for row in readL[1:]:

                    contentL.append([row[i] for i in incl_colL])

                wcontentL = []

                for rowL in contentL:

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

                rstS = output.getvalue()

                sys.stdout = old_stdout

        

                self.restS += rstS + "\n"

        

            def attach(self, rsL):

                b = 5

        

            def report(self, rL):

                """skip info command for utf calcs

        

                Command is executed only for docs in order to

                separate protected information for shareable calcs.

        

                Args:

                    rL (list): parameter list

                """

        

                """       

                try:

                    filen1 = os.path.join(self.rpath, "reportmerge.txt")

                    print(filen1)

                    file1 = open(filen1, 'r')

                    mergelist = file1.readlines()

                    file1.close()

                    mergelist2 = mergelist[:]

                except OSError:

                    print('< reportmerge.txt file not found in reprt folder >')

                    return

                calnum1 = self.pdffile[0:5]

                file2 = open(filen1, 'w')

                newstr1 = 'c | ' + self.pdffile + ' | ' + self.calctitle

                for itm1 in mergelist:

                    if calnum1 in itm1:

                        indx1 = mergelist2.index(itm1)

                        mergelist2[indx1] = newstr1

                        for j1 in mergelist2:

                            file2.write(j1)

                        file2.close()

                        return

                mergelist2.append("\n" + newstr1)

                for j1 in mergelist2:

                    file2.write(j1)

                file2.close()

                return """

                pass

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

### R2rst

```python3
class R2rst(
    strL: list,
    folderD: dict,
    tagD: dict
)
```

#### Methods

    
#### attach

```python3
def attach(
    self,
    rsL
)
```

    

??? example "View Source"
            def attach(self, rsL):

                b = 5

    
#### project

```python3
def project(
    self,
    rL
)
```

    
insert tables or text from csv, xlsx or txt file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| rL | list | parameter list
Files are read from /docs/docfolder
The command is identical to itable except file is read from docs/info. | None |

??? example "View Source"
            def project(self, rL):

                """insert tables or text from csv, xlsx or txt file

        

                Args:

                    rL (list): parameter list

        

                Files are read from /docs/docfolder

                The command is identical to itable except file is read from docs/info.

        

                """

                alignD = {"S": "", "D": "decimal", "C": "center", "R": "right", "L": "left"}

                rtagL = [

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

                if len(rL) < 4:

                    rL += [""] * (4 - len(rL))  # pad parameters

                rstS = ""

                contentL = []

                sumL = []

                fileS = rL[1].strip()

                tfileS = Path(self.folderD["dpath0"] / fileS)

                extS = fileS.split(".")[1]

                if extS == "csv":

                    with open(tfileS, "r") as csvfile:  # read csv file

                        readL = list(csv.reader(csvfile))

                elif extS == "xlsx":

                    xDF = pd.read_excel(tfileS, header=None)

                    readL = xDF.values.tolist()

                else:

                    return

                incl_colL = list(range(len(readL[0])))

                widthI = self.setcmdD["cwidthI"]

                alignS = self.setcmdD["calignS"]

                saS = alignD[alignS]

                if rL[2].strip():

                    widthL = rL[2].split(",")  # new max col width

                    widthI = int(widthL[0].strip())

                    alignS = widthL[1].strip()

                    saS = alignD[alignS]  # new alignment

                    self.setcmdD.update({"cwidthI": widthI})

                    self.setcmdD.update({"calignS": alignS})

                totalL = [""] * len(incl_colL)

                if rL[3].strip():  # columns

                    if rL[3].strip() == "[:]":

                        totalL = [""] * len(incl_colL)

                    else:

                        incl_colL = eval(rL[3].strip())

                        totalL = [""] * len(incl_colL)

                ttitleS = readL[0][0].strip() + " [t]_"

                rstgS = self._tags(ttitleS, rtagL)

                self.restS += rstgS.rstrip() + "\n\n"

                for row in readL[1:]:

                    contentL.append([row[i] for i in incl_colL])

                wcontentL = []

                for rowL in contentL:

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

                rstS = output.getvalue()

                sys.stdout = old_stdout

        

                self.restS += rstS + "\n"

    
#### r_rst

```python3
def r_rst(
    self
) -> str
```

    
parse repository string

**Returns:**

| Type | Description |
|---|---|
| None | rstS (list): utf formatted calc-string (appended)
setsectD (dict): section settings |

??? example "View Source"
            def r_rst(self) -> str:

                """parse repository string

        

                Returns:

                     rstS (list): utf formatted calc-string (appended)

                     setsectD (dict): section settings

                """

        

                rcmdL = ["search", "keys", "info", "text", "table", "pdf"]

                rmethL = [

                    self._rsearch,

                    self._rkeys,

                    self._rinfo,

                    self._itext,

                    self._itable,

                    self._rpdf,

                ]

        

                self._parseRST("repository", rcmdL, rmethL, rtagL)

    
#### report

```python3
def report(
    self,
    rL
)
```

    
skip info command for utf calcs

Command is executed only for docs in order to
separate protected information for shareable calcs.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| rL | list | parameter list | None |

??? example "View Source"
            def report(self, rL):

                """skip info command for utf calcs

        

                Command is executed only for docs in order to

                separate protected information for shareable calcs.

        

                Args:

                    rL (list): parameter list

                """

        

                """       

                try:

                    filen1 = os.path.join(self.rpath, "reportmerge.txt")

                    print(filen1)

                    file1 = open(filen1, 'r')

                    mergelist = file1.readlines()

                    file1.close()

                    mergelist2 = mergelist[:]

                except OSError:

                    print('< reportmerge.txt file not found in reprt folder >')

                    return

                calnum1 = self.pdffile[0:5]

                file2 = open(filen1, 'w')

                newstr1 = 'c | ' + self.pdffile + ' | ' + self.calctitle

                for itm1 in mergelist:

                    if calnum1 in itm1:

                        indx1 = mergelist2.index(itm1)

                        mergelist2[indx1] = newstr1

                        for j1 in mergelist2:

                            file2.write(j1)

                        file2.close()

                        return

                mergelist2.append("\n" + newstr1)

                for j1 in mergelist2:

                    file2.write(j1)

                file2.close()

                return """

                pass

    
#### search

```python3
def search(
    self,
    rsL
)
```

    

??? example "View Source"
            def search(self, rsL):

                a = 4

### R2utf

```python3
class R2utf(
    strL: list,
    folderD: dict,
    tagD: dict
)
```

#### Methods

    
#### attach

```python3
def attach(
    self,
    rutfL
)
```

    
[summary]

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| rsL | [type] | [description] | None |

??? example "View Source"
            def attach(self, rutfL):

                """[summary]

        

                Args:

                    rsL ([type]): [description]

                """

                a = 4

    
#### parseRutf

```python3
def parseRutf(
    self,
    strL: list,
    cmdD: dict,
    cmdL: list,
    methL: list
)
```

    
parse rivt-string to UTF

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| cmdL | list | command list | None |
| methL | list | method list | None |
| tagL | list | tag list | None |

??? example "View Source"
            def parseRutf(self, strL: list, cmdD: dict, cmdL: list, methL: list):

                """parse rivt-string to UTF

        

                Args:

                    cmdL (list): command list

                    methL (list): method list

                    tagL (list): tag list

                """

                for uS in self.strL:

                    if uS[0:2] == "##":

                        continue  # remove review comment

                    uS = uS[4:]  # remove indent

                    if len(uS) == 0:

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

        

                    self.utfS += uS.rstrip() + "\n"

        

                return self.calcS, self.setsectD

    
#### project

```python3
def project(
    self,
    rutfL
)
```

    

??? example "View Source"
            def project(self, rutfL):

                b = 5

    
#### report

```python3
def report(
    self,
    rutfL
)
```

    
skip info command for utf calcs

Command is executed only for docs in order to
separate protected information for shareable calcs.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| rL | list | parameter list | None |

??? example "View Source"
            def report(self, rutfL):

                """skip info command for utf calcs

        

                Command is executed only for docs in order to

                separate protected information for shareable calcs.

        

                Args:

                    rL (list): parameter list

                """

        

                """       

                try:

                    filen1 = os.path.join(self.rpath, "reportmerge.txt")

                    print(filen1)

                    file1 = open(filen1, 'r')

                    mergelist = file1.readlines()

                    file1.close()

                    mergelist2 = mergelist[:]

                except OSError:

                    print('< reportmerge.txt file not found in reprt folder >')

                    return

                calnum1 = self.pdffile[0:5]

                file2 = open(filen1, 'w')

                newstr1 = 'c | ' + self.pdffile + ' | ' + self.calctitle

                for itm1 in mergelist:

                    if calnum1 in itm1:

                        indx1 = mergelist2.index(itm1)

                        mergelist2[indx1] = newstr1

                        for j1 in mergelist2:

                            file2.write(j1)

                        file2.close()

                        return

                mergelist2.append("\n" + newstr1)

                for j1 in mergelist2:

                    file2.write(j1)

                file2.close()

                return """

                pass

    
#### search

```python3
def search(
    self,
    rutfL
)
```

    
[summary]

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| rsL | [type] | [description] | None |

??? example "View Source"
            def search(self, rutfL):

                """[summary]

        

                Args:

                    rsL ([type]): [description]

                """

                a = 4