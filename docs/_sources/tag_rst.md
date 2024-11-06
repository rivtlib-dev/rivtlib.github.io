# Module tag_rst

??? example "View Source"
        import csv

        import logging

        import warnings

        from datetime import datetime

        from io import StringIO

        from pathlib import Path

        import matplotlib.image as mpimg

        import matplotlib.pyplot as plt

        import numpy.linalg as la

        import pandas as pd

        import sympy as sp

        from numpy import *

        from sympy.abc import _clash2

        from sympy.core.alphabets import greeks

        from sympy.parsing.latex import parse_latex

        from tabulate import tabulate

        from rivtlib.units import *

        

        class TagsRST():

            """convert rivt tags to reST

            """

            def __init__(self, lineS, labelD, folderD,  tagsD, localD):

                """convert rivt tags to md or reST

                """

                self.tagsD = tagsD

                self.localD = localD

                self.folderD = folderD

                self.labelD = labelD

                self.lineS = lineS

                self.vgap = "2"

                self.widthI = labelD["widthI"]

                self.errlogP = folderD["errlogP"]

                self.valL = []                         # accumulate values in list

                modnameS = self.labelD["modnameS"]

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

                secS = str(self.labelD["secnumI"]).zfill(2)

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

                enumI = int(self.labelD["equI"])

                fillS = str(enumI).zfill(2)

                refS = self.label("E", fillS)

                lineS = "\n\n" + "**" + "Eq. " + str(enumI) + ": "  \

                        + self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n\n"

                return lineS

            def figure(self):

                """figure label _[f]

                : return lineS: figure label

                : rtype: str

                """

                fnumI = int(self.labelD["figI"])

                fillS = str(fnumI).zfill(2)

                refS = self.label("F", fillS)

                lineS = "\n \n" + "**" + "Figure " + str(fnumI) + ": " + \

                        self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n \n"

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

                tnumI = int(self.labelD["tableI"])

                fillS = str(tnumI).zfill(2)

                refS = self.label("T", fillS)

                lineS = "\n" + "**" + "Table " + fillS + ": " + self.lineS.strip() + \

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

### TagsRST

```python3
class TagsRST(
    lineS,
    labelD,
    folderD,
    tagsD,
    localD
)
```

convert rivt tags to reST

#### Methods

    
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

                return "**" + self.lineS.strip() + "**"

    
#### boldcenter

```python3
def boldcenter(
    self
)
```

bold center text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def boldcenter(self):

                """bold center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = ".. raw:: latex \n\n" \

                    + "   ?x?begin{center} ?x?textbf{" + self.lineS +  \

                    "} ?x?end{center}" + "\n"

                return lineS

    
#### boldright

```python3
def boldright(
    self
)
```

bold right text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def boldright(self):

                """bold right text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = ".. raw:: latex \n\n" \

                    + "?x?hfill ?x?textbf{" + self.lineS + "}" \

                    + "\n"

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

                : return lineS: centered line

                : rtype: str

                """

                lineS = ".. raw:: latex \n\n" \

                    + "   ?x?begin{center} " + self.lineS + " ?x?end{center}" \

                    + "\n"

                return lineS

    
#### centerblk

```python3
def centerblk(
    self
)
```

_summary_

??? example "View Source"
            def centerblk(self):

                """_summary_

                """

                lineS = ".. raw:: latex \n\n" \

                    + "   ?x?begin{center} + ?x?parbox{5cm}" \

                    + self.lineS + " ?x?end{center}" \

                    + "\n\n"

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

                : return lineS: footnote

                : rtype: str

                """

                return ".. [*] " + self.lineS

    
#### equation

```python3
def equation(
    self
)
```

reST equation label _[e]

**Returns:**

| Type | Description |
|---|---|
| lineS | reST equation label |

??? example "View Source"
            def equation(self):

                """reST equation label _[e]

                : return lineS: reST equation label

                : rtype: str

                """

                enumI = int(self.labelD["equI"])

                fillS = str(enumI).zfill(2)

                refS = self.label("E", fillS)

                lineS = "\n\n" + "**" + "Eq. " + str(enumI) + ": "  \

                        + self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n\n"

                return lineS

    
#### figure

```python3
def figure(
    self
)
```

figure label _[f]

**Returns:**

| Type | Description |
|---|---|
| lineS | figure label |

??? example "View Source"
            def figure(self):

                """figure label _[f]

                : return lineS: figure label

                : rtype: str

                """

                fnumI = int(self.labelD["figI"])

                fillS = str(fnumI).zfill(2)

                refS = self.label("F", fillS)

                lineS = "\n \n" + "**" + "Figure " + str(fnumI) + ": " + \

                        self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n \n"

                return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    
#### footnumber

```python3
def footnumber(
    self
)
```

insert footnote number _[#]

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
            def footnumber(self):

                """insert footnote number _[#]

                :return: _description_

                :rtype: _type_

                """

                lineS = "".join(self.lineS)

                return lineS.replace("*]", "[*]_ ")

    
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

                return "*" + self.lineS.strip() + "*"

    
#### italiccenter

```python3
def italiccenter(
    self
)
```

italic center text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def italiccenter(self):

                """italic center text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = ".. raw:: latex \n\n" \

                    + "   ?x?begin{center} ?x?textit{" + self.lineS +  \

                    "} ?x?end{center}" + "\n"

                return lineS

    
#### italicright

```python3
def italicright(
    self
)
```

italic right text _[c]

**Returns:**

| Type | Description |
|---|---|
| lineS | centered line |

??? example "View Source"
            def italicright(self):

                """italic right text _[c]

                :return lineS: centered line

                :rtype: str

                """

                lineS = ".. raw:: latex \n\n" \

                    + "?x?hfill ?x?textit{" + self.lineS + "}" \

                    + "\n"

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

                    : return labelS: formatted label

                    : rtype: str

                """

                secS = str(self.labelD["secnumI"]).zfill(2)

                return secS + " - " + labelS + numS

    
#### latex

```python3
def latex(
    self
)
```

format latex _[l]

**Returns:**

| Type | Description |
|---|---|
| lineS | reST formatted latex |

??? example "View Source"
            def latex(self):

                """format latex _[l]

                :return lineS: reST formatted latex

                :rtype: str

                """

                return ".. raw:: math\n\n   " + self.lineS + "\n"

    
#### latexblk

```python3
def latexblk(
    self
)
```

??? example "View Source"
            def latexblk(self):

                pass

    
#### line

```python3
def line(
    self
)
```

insert line _[line]:

param lineS: _description_

??? example "View Source"
            def line(self):

                """insert line _[line]:

                param lineS: _description_

                :type lineS: _type_

                """

                return self.widthI * "-"

    
#### link

```python3
def link(
    self
)
```

url or internal link

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
            def link(self):

                """url or internal link

                :return: _description_

                :rtype: _type_

                """

                lineL = lineS.split(",")

                lineS = ".. _" + lineL[0] + ": " + lineL[1]

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

insert page break _[page]

**Returns:**

| Type | Description |
|---|---|
| lineS | page break line |

??? example "View Source"
            def page(self):

                """insert page break _[page]

                :return lineS: page break line

                :rtype: str

                """

                return ".. raw:: latex \n\n ?x?newpage \n"

    
#### plain

```python3
def plain(
    self
)
```

format plain literal _[p]

**Returns:**

| Type | Description |
|---|---|
| lineS | page break line |

??? example "View Source"
            def plain(self):

                """format plain literal _[p]

                :return lineS: page break line

                :rtype: str

                """

                return ".. raw:: latex \n\n ?x?newpage \n"

    
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

                return "?x?hfill " + self.lineS

    
#### rightblk

```python3
def rightblk(
    self
)
```

??? example "View Source"
            def rightblk(self):

                pass

    
#### sympy

```python3
def sympy(
    self
)
```

reST line of sympy _[s]

**Returns:**

| Type | Description |
|---|---|
| lineS | formatted sympy |

??? example "View Source"
            def sympy(self):

                """reST line of sympy _[s]

                :return lineS: formatted sympy

                :rtype: str

                """

                spS = self.lineS

                txS = sp.latex(S(spS))

                return ".. raw:: math\n\n   " + txS + "\n"

    
#### table

```python3
def table(
    self
)
```

table label _[t]

**Returns:**

| Type | Description |
|---|---|
| lineS | figure label |

??? example "View Source"
            def table(self):

                """table label _[t]

                :return lineS: figure label

                :rtype: str

                """

                tnumI = int(self.labelD["tableI"])

                fillS = str(tnumI).zfill(2)

                refS = self.label("T", fillS)

                lineS = "\n" + "**" + "Table " + fillS + ": " + self.lineS.strip() + \

                        "** " + " ?x?hfill " + refS + "\n"

                return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    
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

                return ":math: `?x?text?x?underline{" + self.lineS.strip() + "}"