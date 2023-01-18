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

        

            def refs(self, objnumI: int, typeS: str) -> str:

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

        

            def parseUTF(self, cmdL: list, methL: list, tagL: list):

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

        

            def parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list):

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

        

                self._parseRST("insert", icmdL, imethL, itagL)

        

                return self.restS, self.setsectD, self.setcmdD

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

        

                self._parseRST("insert", icmdL, imethL, itagL)

        

                return self.restS, self.setsectD, self.setcmdD

    
#### parseRST

```python3
def parseRST(
    self,
    typeS: str,
    cmdL: list,
    methL: list,
    tagL: list
)
```

    
parse rivt-string to reST

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| typeS | str | rivt-string type | None |
| cmdL | list | command list | None |
| methL | list | method list | None |
| tagL | list | tag list | None |

??? example "View Source"
            def parseRST(self, typeS: str, cmdL: list, methL: list, tagL: list):

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

    
#### parseUTF

```python3
def parseUTF(
    self,
    cmdL: list,
    methL: list,
    tagL: list
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
            def parseUTF(self, cmdL: list, methL: list, tagL: list):

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

    
#### refs

```python3
def refs(
    self,
    objnumI: int,
    typeS: str
) -> str
```

    
reference label for equations, tables and figures

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| objnumI | int | equation, table or figure section number | None |
| typeS | str | label type | None |

**Returns:**

| Type | Description |
|---|---|
| None | refS (str): reference label |

??? example "View Source"
            def refs(self, objnumI: int, typeS: str) -> str:

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