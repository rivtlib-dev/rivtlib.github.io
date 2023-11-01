# Module tag_utf

??? example "View Source"
        #

        import csv

        import logging

        import warnings

        import os

        import re

        import subprocess

        import sys

        import tempfile

        import textwrap

        from io import StringIO

        from pathlib import Path

        from io import StringIO

        from pathlib import Path

        import sympy as sp

        from numpy import *

        from sympy.abc import _clash2

        from sympy.core.alphabets import greeks

        from sympy.parsing.latex import parse_latex as parsx

        from tabulate import tabulate

        from rivtlib import parse

        from rivtlib.units import *

        from rivtlib.tag_parse import Tags

        

        class TagsUTF(Tags):

            """convert rivt tags to md

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

            def __init__(self, lineS, incrD, folderD, tagsD, localD):

                """convert rivt tags to md or reST

                """

                self.lineS = lineS

                self.tagsD = tagsD

                self.localD = localD

                self.folderD = folderD

                self.incrD = incrD

                self.lineS = lineS

                self.widthI = incrD["widthI"]

                self.errlogP = folderD["errlogP"]

                self.valL = []                         # accumulate values in list

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

            def bold(self):

                """bold text _[b]

                :return lineS: bold line

                :rtype: str

                """

                print(self.lineS)

                return self.lineS

            def center(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

            def italic(self):

                """italicize text _[i]

                :return lineS: centered line

                :rtype: str

                """

                print(self.lineS)

                return self.lineS

            def boldcenter(self):

                """center text _[bc]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

            def bolditalic(self):

                """center text _[bc]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

            def bolditaliccenter(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.rjust(int(self.widthI))

                print(lineS)

                return lineS

            def italiccenter(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

            def right(self):

                """right justify text _[r]

                :return lineS: right justified text

                :rtype: str

                """

                lineS = self.lineS.rjust(int(self.widthI))

                return lineS

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

            def description(self):

                """footnote description _[d]

                :return lineS: footnote

                :rtype: str

                """

                ftnumI = self.incrD["noteL"].pop(0)

                lineS = "[" + str(ftnumI) + "] " + self.lineS

                print(lineS)

                return lineS

            def equation(self):

                """md equation label _[e]

                :return lineS: md equation label

                :rtype: str

                """

                enumI = int(self.incrD["equI"]) + 1

                fillS = str(enumI).zfill(2)

                wI = self.incrD["widthI"]

                refS = self.label("E", fillS)

                spcI = len("Equ. " + fillS + " - " + self.lineS.strip())

                lineS = "Equ. " + fillS + " - " + self.lineS.strip() \

                    + refS.rjust(wI-spcI)

                self.incrD["equI"] = enumI

                print(lineS)

                return lineS

            def figure(self):

                """md figure caption _[f]

                :return lineS: figure label

                :rtype: str

                """

                fnumI = int(self.incrD["figI"])

                self.incrD["figI"] = fnumI + 1

                lineS = "Fig. " + str(fnumI) + " - " + self.lineS

                print(lineS + "\n")

                return lineS + "\n"

            def foot(self):

                """footnote number _[#]

        

                """

                ftnumI = self.incrD["footL"].pop(0)

                self.incrD["noteL"].append(ftnumI + 1)

                self.incrD["footL"].append(ftnumI + 1)

                lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")

                print(lineS)

                return lineS

            def latex(self):

                """format latex

                :return lineS: formatted latex

                :rtype: str

                """

                txS = self.lineS

                # txS = txs.encode('unicode-escape').decode()

                ptxS = sp.parse_latex(txS)

                lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))

                print(lineS)

                return lineS

            def plain(self):

                """format plain literal text _[p]

                :param lineS: _description_

                :type lineS: _type_

                """

                print(self.lineS)

                return self.lineS

            def sympy(self):

                """format line of sympy _[s]

                :return lineS: formatted sympy

                :rtype: str

                """

                spS = self.lineS.strip()

                # try:

                #     spL = spS.split("=")

                #     spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"

                #     # sps = sp.encode('unicode-escape').decode()

                # except:

                lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

                print(lineS)

                return lineS

            def table(self):

                """format table title  _[t]

                :return lineS: md table title

                :rtype: str

                """

                tnumI = int(self.incrD["tableI"])

                self.incrD["tableI"] = tnumI + 1

                lineS = "Table " + str(tnumI) + " - " + self.lineS

                print(lineS)

                return lineS

            def link(self):

                """format url or internal link _[link]

                :return: _description_

                :rtype: _type_

                """

                lineL = self.lineS.split(",")

                lineS = ".. _" + lineL[0] + ": " + lineL[1]

                print(lineS)

                return lineS

            def page(self):

                """insert new page header _[page]

                :return lineS: page header

                :rtype: str

                """

                pagenoS = str(self.incrD["pageI"])

                rvtS = self.incrD["headuS"].replace("p##", pagenoS)

                self.incrD["pageI"] = int(pagenoS)+1

                lineS = "\n"+"_" * self.incrD["widthI"] + "\n" + rvtS +\

                        "\n"+"_" * self.incrD["widthI"] + "\n"

                return "\n" + rvtS

            def underline(self):

                """underline _[u]

                :return lineS: underline

                :rtype: str

                """

                return self.lineS

            def centerblk(self):

                """

                """

                lineS = ""

                for i in self.lineS:

                    lineS += i.center(int(self.widthI))

                return lineS

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

                pass

            def quitblock(self):

                """ quit shade block _[[q]]

                :param lineS: _description_

                :type lineS: _type_

                """

                pass

            def tagblk(self):

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

### TagsUTF

```python3
class TagsUTF(
    lineS,
    incrD,
    folderD,
    tagsD,
    localD
)
```

convert rivt tags to md

#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| paramL | _type_ | _description_ | None |
| incrD | _type_ | _description_ | None |
| folderD | _type_ | _description_ | None |
| localD | _type_ | _description_ | None |

<<<<<<< HEAD
=======
??? example "View Source"
        class TagsUTF(Tags):

            """convert rivt tags to md

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

            def __init__(self, lineS, incrD, folderD, tagsD, localD):

                """convert rivt tags to md or reST

                """

                self.lineS = lineS

                self.tagsD = tagsD

                self.localD = localD

                self.folderD = folderD

                self.incrD = incrD

                self.lineS = lineS

                self.widthI = incrD["widthI"]

                self.errlogP = folderD["errlogP"]

                self.valL = []                         # accumulate values in list

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

            def bold(self):

                """bold text _[b]

                :return lineS: bold line

                :rtype: str

                """

                print(self.lineS)

                return self.lineS

            def center(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

            def italic(self):

                """italicize text _[i]

                :return lineS: centered line

                :rtype: str

                """

                print(self.lineS)

                return self.lineS

            def boldcenter(self):

                """center text _[bc]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

            def bolditalic(self):

                """center text _[bc]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

            def bolditaliccenter(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.rjust(int(self.widthI))

                print(lineS)

                return lineS

            def italiccenter(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

            def right(self):

                """right justify text _[r]

                :return lineS: right justified text

                :rtype: str

                """

                lineS = self.lineS.rjust(int(self.widthI))

                return lineS

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

            def description(self):

                """footnote description _[d]

                :return lineS: footnote

                :rtype: str

                """

                ftnumI = self.incrD["noteL"].pop(0)

                lineS = "[" + str(ftnumI) + "] " + self.lineS

                print(lineS)

                return lineS

            def equation(self):

                """md equation label _[e]

                :return lineS: md equation label

                :rtype: str

                """

                enumI = int(self.incrD["equI"]) + 1

                fillS = str(enumI).zfill(2)

                wI = self.incrD["widthI"]

                refS = self.label("E", fillS)

                spcI = len("Equ. " + fillS + " - " + self.lineS.strip())

                lineS = "Equ. " + fillS + " - " + self.lineS.strip() \

                    + refS.rjust(wI-spcI)

                self.incrD["equI"] = enumI

                print(lineS)

                return lineS

            def figure(self):

                """md figure caption _[f]

                :return lineS: figure label

                :rtype: str

                """

                fnumI = int(self.incrD["figI"])

                self.incrD["figI"] = fnumI + 1

                lineS = "Fig. " + str(fnumI) + " - " + self.lineS

                print(lineS + "\n")

                return lineS + "\n"

            def foot(self):

                """footnote number _[#]

        

                """

                ftnumI = self.incrD["footL"].pop(0)

                self.incrD["noteL"].append(ftnumI + 1)

                self.incrD["footL"].append(ftnumI + 1)

                lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")

                print(lineS)

                return lineS

            def latex(self):

                """format latex

                :return lineS: formatted latex

                :rtype: str

                """

                txS = self.lineS

                # txS = txs.encode('unicode-escape').decode()

                ptxS = sp.parse_latex(txS)

                lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))

                print(lineS)

                return lineS

            def plain(self):

                """format plain literal text _[p]

                :param lineS: _description_

                :type lineS: _type_

                """

                print(self.lineS)

                return self.lineS

            def sympy(self):

                """format line of sympy _[s]

                :return lineS: formatted sympy

                :rtype: str

                """

                spS = self.lineS.strip()

                # try:

                #     spL = spS.split("=")

                #     spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"

                #     # sps = sp.encode('unicode-escape').decode()

                # except:

                lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

                print(lineS)

                return lineS

            def table(self):

                """format table title  _[t]

                :return lineS: md table title

                :rtype: str

                """

                tnumI = int(self.incrD["tableI"])

                self.incrD["tableI"] = tnumI + 1

                lineS = "Table " + str(tnumI) + " - " + self.lineS

                print(lineS)

                return lineS

            def link(self):

                """format url or internal link _[link]

                :return: _description_

                :rtype: _type_

                """

                lineL = self.lineS.split(",")

                lineS = ".. _" + lineL[0] + ": " + lineL[1]

                print(lineS)

                return lineS

            def page(self):

                """insert new page header _[page]

                :return lineS: page header

                :rtype: str

                """

                pagenoS = str(self.incrD["pageI"])

                rvtS = self.incrD["headuS"].replace("p##", pagenoS)

                self.incrD["pageI"] = int(pagenoS)+1

                lineS = "\n"+"_" * self.incrD["widthI"] + "\n" + rvtS +\

                        "\n"+"_" * self.incrD["widthI"] + "\n"

                return "\n" + rvtS

            def underline(self):

                """underline _[u]

                :return lineS: underline

                :rtype: str

                """

                return self.lineS

            def centerblk(self):

                """

                """

                lineS = ""

                for i in self.lineS:

                    lineS += i.center(int(self.widthI))

                return lineS

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

                pass

            def quitblock(self):

                """ quit shade block _[[q]]

                :param lineS: _description_

                :type lineS: _type_

                """

                pass

            def tagblk(self):

                pass

------

>>>>>>> 77ef858e0000ebef82dbb2b50239d340baf1c633
#### Ancestors (in MRO)

* rivtlib.tag_parse.Tags

#### Methods

    
#### assign

```python3
def assign(
    self
)
```

= assign result to equation

**Returns:**

| Type | Description |
|---|---|
| assignL | assign results |

??? example "View Source"
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

    
#### bold

```python3
def bold(
    self
)
```

bold text _[b]

**Returns:**

| Type | Description |
|---|---|
| lineS | bold line |

??? example "View Source"
            def bold(self):

                """bold text _[b]

                :return lineS: bold line

                :rtype: str

                """

                print(self.lineS)

                return self.lineS

    
#### boldcenter

```python3
def boldcenter(
    self
)
```

center text _[bc]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def boldcenter(self):

                """center text _[bc]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

    
#### bolditalic

```python3
def bolditalic(
    self
)
```

center text _[bc]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def bolditalic(self):

                """center text _[bc]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

    
#### bolditaliccenter

```python3
def bolditaliccenter(
    self
)
```

center text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def bolditaliccenter(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.rjust(int(self.widthI))

                print(lineS)

                return lineS

    
#### center

```python3
def center(
    self
)
```

center text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def center(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

    
#### centerblk

```python3
def centerblk(
    self
)
```

??? example "View Source"
            def centerblk(self):

                """

                """

                lineS = ""

                for i in self.lineS:

                    lineS += i.center(int(self.widthI))

                return lineS

    
#### codeblk

```python3
def codeblk(
    self
)
```

??? example "View Source"
            def codeblk(self):

                pass

    
#### declare

```python3
def declare(
    self
)
```

:= declare variable value

:return assignL: assign results
:rtype: list
:return rstS: restruct string 
:rtype: string

??? example "View Source"
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

    
#### description

```python3
def description(
    self
)
```

footnote description _[d]

**Returns:**

| Type | Description |
|---|---|
| lineS | footnote |

??? example "View Source"
            def description(self):

                """footnote description _[d]

                :return lineS: footnote

                :rtype: str

                """

                ftnumI = self.incrD["noteL"].pop(0)

                lineS = "[" + str(ftnumI) + "] " + self.lineS

                print(lineS)

                return lineS

    
#### equation

```python3
def equation(
    self
)
```

md equation label _[e]

**Returns:**

| Type | Description |
|---|---|
| lineS | md equation label |

??? example "View Source"
            def equation(self):

                """md equation label _[e]

                :return lineS: md equation label

                :rtype: str

                """

                enumI = int(self.incrD["equI"]) + 1

                fillS = str(enumI).zfill(2)

                wI = self.incrD["widthI"]

                refS = self.label("E", fillS)

                spcI = len("Equ. " + fillS + " - " + self.lineS.strip())

                lineS = "Equ. " + fillS + " - " + self.lineS.strip() \

                    + refS.rjust(wI-spcI)

                self.incrD["equI"] = enumI

                print(lineS)

                return lineS

    
#### figure

```python3
def figure(
    self
)
```

md figure caption _[f]

**Returns:**

| Type | Description |
|---|---|
| lineS | figure label |

??? example "View Source"
            def figure(self):

                """md figure caption _[f]

                :return lineS: figure label

                :rtype: str

                """

                fnumI = int(self.incrD["figI"])

                self.incrD["figI"] = fnumI + 1

                lineS = "Fig. " + str(fnumI) + " - " + self.lineS

                print(lineS + "\n")

                return lineS + "\n"

    
#### foot

```python3
def foot(
    self
)
```

footnote number _[#]

??? example "View Source"
            def foot(self):

                """footnote number _[#]

        

                """

                ftnumI = self.incrD["footL"].pop(0)

                self.incrD["noteL"].append(ftnumI + 1)

                self.incrD["footL"].append(ftnumI + 1)

                lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")

                print(lineS)

                return lineS

    
#### italic

```python3
def italic(
    self
)
```

italicize text _[i]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def italic(self):

                """italicize text _[i]

                :return lineS: centered line

                :rtype: str

                """

                print(self.lineS)

                return self.lineS

    
#### italiccenter

```python3
def italiccenter(
    self
)
```

center text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def italiccenter(self):

                """center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = self.lineS.center(int(self.widthI))

                print(lineS)

                return lineS

    
#### label

```python3
def label(
    self,
    labelS,
    numS
)
```

format labels for equations, tables and figures

**Returns:**

| Type | Description |
|---|---|
| labelS | formatted label |

??? example "View Source"
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

    
#### latex

```python3
def latex(
    self
)
```

format latex

**Returns:**

| Type | Description |
|---|---|
| lineS | formatted latex |

??? example "View Source"
            def latex(self):

                """format latex

                :return lineS: formatted latex

                :rtype: str

                """

                txS = self.lineS

                # txS = txs.encode('unicode-escape').decode()

                ptxS = sp.parse_latex(txS)

                lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))

                print(lineS)

                return lineS

    
#### latexblk

```python3
def latexblk(
    self
)
```

??? example "View Source"
            def latexblk(self):

                pass

    
#### link

```python3
def link(
    self
)
```

format url or internal link _[link]

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
            def link(self):

                """format url or internal link _[link]

                :return: _description_

                :rtype: _type_

                """

                lineL = self.lineS.split(",")

                lineS = ".. _" + lineL[0] + ": " + lineL[1]

                print(lineS)

                return lineS

    
#### mathblk

```python3
def mathblk(
    self
)
```

??? example "View Source"
            def mathblk(self):

                pass

    
#### page

```python3
def page(
    self
)
```

insert new page header _[page]

**Returns:**

| Type | Description |
|---|---|
| lineS | page header |

??? example "View Source"
            def page(self):

                """insert new page header _[page]

                :return lineS: page header

                :rtype: str

                """

                pagenoS = str(self.incrD["pageI"])

                rvtS = self.incrD["headuS"].replace("p##", pagenoS)

                self.incrD["pageI"] = int(pagenoS)+1

                lineS = "\n"+"_" * self.incrD["widthI"] + "\n" + rvtS +\

                        "\n"+"_" * self.incrD["widthI"] + "\n"

                return "\n" + rvtS

    
#### plain

```python3
def plain(
    self
)
```

format plain literal text _[p]

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| lineS | _type_ | _description_ | None |

??? example "View Source"
            def plain(self):

                """format plain literal text _[p]

                :param lineS: _description_

                :type lineS: _type_

                """

                print(self.lineS)

                return self.lineS

    
#### quitblock

```python3
def quitblock(
    self
)
```

quit shade block _[[q]]

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| lineS | _type_ | _description_ | None |

??? example "View Source"
            def quitblock(self):

                """ quit shade block _[[q]]

                :param lineS: _description_

                :type lineS: _type_

                """

                pass

    
#### right

```python3
def right(
    self
)
```

right justify text _[r]

**Returns:**

| Type | Description |
|---|---|
| lineS | right justified text |

??? example "View Source"
            def right(self):

                """right justify text _[r]

                :return lineS: right justified text

                :rtype: str

                """

                lineS = self.lineS.rjust(int(self.widthI))

                return lineS

    
#### rightblk

```python3
def rightblk(
    self
)
```

??? example "View Source"
            def rightblk(self):

                pass

    
#### shadeblk

```python3
def shadeblk(
    self
)
```

start shade block _[[s]]

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| lineS | _type_ | _description_ | None |

??? example "View Source"
            def shadeblk(self):

                """ start shade block _[[s]]

                :param lineS: _description_

                :type lineS: _type_

                """

                pass

    
#### sympy

```python3
def sympy(
    self
)
```

format line of sympy _[s]

**Returns:**

| Type | Description |
|---|---|
| lineS | formatted sympy |

??? example "View Source"
            def sympy(self):

                """format line of sympy _[s]

                :return lineS: formatted sympy

                :rtype: str

                """

                spS = self.lineS.strip()

                # try:

                #     spL = spS.split("=")

                #     spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"

                #     # sps = sp.encode('unicode-escape').decode()

                # except:

                lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

                print(lineS)

                return lineS

    
#### table

```python3
def table(
    self
)
```

format table title  _[t]

**Returns:**

| Type | Description |
|---|---|
| lineS | md table title |

??? example "View Source"
            def table(self):

                """format table title  _[t]

                :return lineS: md table title

                :rtype: str

                """

                tnumI = int(self.incrD["tableI"])

                self.incrD["tableI"] = tnumI + 1

                lineS = "Table " + str(tnumI) + " - " + self.lineS

                print(lineS)

                return lineS

    
#### tag_parse

```python3
def tag_parse(
    self,
    tagS
)
```

convert rivt tags to md

??? example "View Source"
            def tag_parse(self, tagS):

                """convert rivt tags to md

                """

                if tagS in self.tagsD:

                    return eval("self." + self.tagsD[tagS] + "()")

                if "b" in tagS and "c" in tagS:

                    return self.boldcenter()

                if "b" in tagS and "i" in tagS:

                    return self.bolditalic()

                if "b" in tagS and "i" in tagS and "c" in tagS:

                    return self.bolditaliccenter()

                if "i" in tagS and "c" in tagS:

                    return self.italiccenter()

    
#### tagblk

```python3
def tagblk(
    self
)
```

??? example "View Source"
            def tagblk(self):

                pass

    
#### underline

```python3
def underline(
    self
)
```

underline _[u]

**Returns:**

| Type | Description |
|---|---|
| lineS | underline |

??? example "View Source"
            def underline(self):

                """underline _[u]

                :return lineS: underline

                :rtype: str

                """

                return self.lineS

    
#### vsub

```python3
def vsub(
    self,
    eqL,
    precI,
    varS,
    val1U
)
```

substitute numbers for variables in printed output

**Returns:**

| Type | Description |
|---|---|
| assignL | assign results |

??? example "View Source"
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