# Module parse

??? example "View Source"
        import csv

        import logging

        import re

        import sys

        import warnings

        from io import StringIO

        from pathlib import Path

        import matplotlib.image as mpimg

        import matplotlib.pyplot as plt

        import numpy.linalg as la

        import pandas as pd

        import sympy as sp

        from IPython.display import Image as _Image

        from IPython.display import display as _display

        from numpy import *

        from sympy.abc import _clash2

        from sympy.core.alphabets import greeks

        from sympy.parsing.latex import parse_latex

        from tabulate import tabulate

        from rivtlib import units

        from rivtlib import cmd_utf

        from rivtlib import cmd_rst

        from rivtlib import tag_utf

        from rivtlib import tag_rst

        # tabulate.PRESERVE_WHITESPACE = True

        

        class RivtParse:

            """format rivt-strings as utf and rst files"""

            def __init__(self, methS, folderD, labelD,  rivtD):

                """ rivt-strings as utf and reST line by line

                    :param dict folderD: folder paths

                    :param dict labelD: numbers that increment

                    :param dict outputS: output type

                    :param dict outputS: output type

                """

                self.rivtD = rivtD

                self.folderD = folderD  # folder paths

                self.labelD = labelD      # incrementing formats

                self.errlogP = folderD["errlogP"]

                self.methS = methS

                hdrstS = """"""

                hdreadS = """"""

                hdutfS = """"""""

                # section headings

                xmdS = xrstS = xutfS = ""

                rL = rS.split("\n")

                rsL = rS.split("|")              # function string as list

                titleS = rsL[0].strip()          #

                labelD["tocS"] = rsL[1].strip()  # set redaction

                labelD["pageI"] = int(rsL[2])    # set background color

                if rS.strip()[0:2] == "--":         # omit section heading

                    return "\n", "\n", "\n"

                headS = datetime.now().strftime("%Y-%m-%d | %I:%M%p") + "\n"

                labelD["docS"] = titleS

                bordrS = labelD["widthI"] * "="

                hdutfS = (headS + "\n" + bordrS + "\n" + titleS + "\n" + bordrS + "\n")

                hdmdS = (headS + "\n## " + titleS + "\n")

                snumI = labelD["secnumI"] + 1

                labelD["secnumI"] = snumI

                docnumS = labelD["docnumS"]

                dnumS = docnumS + "-[" + str(snumI) + "]"

                headS = dnumS + " " + titleS

                bordrS = labelD["widthI"] * "-"

                hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"

                hdmdS = "### " + headS + "\n"

                hdrstS += (

                    ".. raw:: latex"

                    + "   \n\n ?x?vspace{.2in} "

                    + "   ?x?begin{tcolorbox} "

                    + "   ?x?textbf{ " + titleS + "}"

                    + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"

                    + "   ?x?end{tcolorbox}"

                    + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"

                    + "\n\n")

        #        print(hdutfS)

        #        return hdutfS, hdmdS, hdrstS

                utfS += hutfS

                rstS += hrstS

                # valid commands and tags

                if methS == "R":

                    self.cmdL = ["run", "process"]

                    self.tagsD = {"link]": "link", "line]": "line", "page]": "page"}

                elif methS == "I":

                    self.cmdL = ["image", "table", "text"]

                    self.tagsD = {"b]": "bold", "i]": "italic", "u]": "underline",

                                  "c]": "center", "r]": "right",

                                  "e]": "equation", "f]": "figure", "t]": "table",

                                  "#]": "foot", "d]": "description",

                                  "l]": "latex", "s]": "sympy",

                                  "link]": "link", "line]": "line", "page]": "page",

                                  "[c]]": "centerblk",  "[p]]": "plainblk",

                                  "[l]]": "latexblk", "[m]]": "mathblk",

                                  "[o]]": "codeblk", "[q]]": "quitblk"}

                elif methS == "V":

                    self.cmdL = ["image", "table", "text", "assign", "declare"]

                    self.tagsD = {"e]": "equation", "f]": "figure", "t]": "table",

                                  "#]": "foot", "d]": "description",

                                  "l]": "latex", "s]": "sympy",

                                  ":=": "declare",  "=": "assign"}

                elif methS == "T":

                    self.cmdL = []

                    self.tagsD = {}

                elif methS == "W":

                    self.cmdL = []

                    self.tagsD = {}

                else:

                    pass

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

                # self.rivtD.update(locals())

            def str_parse(self, strL):

                """parse method string line by line starting with second line

                    :param list strL: split method string

                    :return mdS: md formatted string

                    :return rstS: reST formatted string

                    :return labelD: increment references

                    :return folderD: folder paths

                    :rtype mdS: string

                    :rtype rstS: string

                    :rtype folderD: dictionary

                    :rtype labelD: dictionary

                """

                xutfS = """"""      # utfS local string

                xmdS = """"""       # mdS local string

                xrstS = """"""      # rstS local string

                uS = """"""         # raw local line

                blockB = False

                # table alignment

                hdrdL = ["variable", "value", "[value]", "description"]

                aligndL = ["left", "right", "right", "left"]

                hdraL = ["variable", "value", "[value]", "description [eq. number]"]

                alignaL = ["left", "right", "right", "left"]

                blockevalL = []     # current value table

                blockevalB = False  # stop accumulation of values

                vtableL = []        # value table for export

                eqL = []            # equation result table

                lineS = ""

                for uS in strL:

                    # print(f"{blockassignB=}")

                    # print(f"{uS=}")

                    uS = uS[4:]                                # remove indent

                    if blockB:                                 # accumulate block

                        lineS += uS

                        continue

                    if blockB and uS.strip() == "[q]]":        # end of block

                        tagS = self.tagsD["[q]"]

                        rvtS = tag_utf.TagsUTF(lineS, tagS,

                                               self.labelD, self.folderD,  self.rivtD)

                        xutfS += rvtS + "\n"

                        rvtS = tag_md.TagsMD(lineS, tagS,

                                             self.labelD, self.folderD,  self.rivtD)

                        xmdS += rvtS + "\n"

                        rvtS = tag_rst.TagsRST(lineS, tagS,

                                               self.labelD, self.folderD,  self.rivtD)

                        xrstS += rvtS + "\n"

                        blockB = False

                    if blockevalB and len(uS.strip()) < 2:    # value tables

                        vtableL += blockevalL

                        if tfS == "declare":

                            vutfS = self.dtable(blockevalL, hdrdL,

                                                "rst", aligndL) + "\n\n"

                            vmdS = self.dtable(blockevalL, hdrdL,

                                               "html", aligndL) + "\n\n"

                            xutfS += vutfS

                            xmdS += vmdS

                            xrstS += vutfS

                        if tfS == "assign":

                            vutfS = self.dtable(blockevalL, hdrdL,

                                                "rst", aligndL) + "\n\n"

                            vmdS = self.atable(blockevalL, hdraL,

                                               "html", alignaL) + "\n\n"

                            xutfS += vutfS

                            xmdS += vmdS

                            xrstS += vutfS

                        blockevalL = []

                        blockevalB = False

                    elif uS[0:2] == "||":                      # commands

                        usL = uS[2:].split("|")

                        parL = usL[1:]

                        cmdS = usL[0].strip()

                        if cmdS in self.cmdL:

                            rvtC = cmd_utf.CmdUTF(

                                parL, self.labelD, self.folderD, self.rivtD)

                            utfS = rvtC.cmd_parse(cmdS)

                            # print(f"{utfS=}")

                            xutfS += utfS

                            rvtC = cmd_md.CmdMD(

                                parL, self.labelD, self.folderD, self.rivtD)

                            mdS = rvtC.cmd_parse(cmdS)

                            # print(f"{mdS=}")

                            xmdS += mdS

                            rvtC = cmd_rst.CmdRST(

                                parL, self.labelD, self.folderD, self.rivtD)

                            reS = rvtC.cmd_parse(cmdS)

                            xrstS += reS

                    elif "_[" in uS:                           # line tag

                        usL = uS.split("_[")

                        lineS = usL[0]

                        tagS = usL[1].strip()

                        if tagS[0] == "[":                     # block tag

                            blockB = True

                        if tagS in self.tagsD:

                            rvtC = tag_utf.TagsUTF(lineS, self.labelD, self.folderD,

                                                   self.tagsD, self.rivtD)

                            utfxS = rvtC.tag_parse(tagS)

                            xutfS += utfxS + "\n"

                            rvtC = tag_md.TagsMD(lineS, self.labelD, self.folderD,

                                                 self.tagsD, self.rivtD)

                            mdS = rvtC.tag_parse(tagS)

                            xmdS += mdS + "\n"

                            rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,

                                                   self.tagsD, self.rivtD)

                            reS = rvtC.tag_parse(tagS)

                            xrstS += reS + "\n"

                    elif "=" in uS and self.methS == "V":       # equation tag

                        # print(f"{uS=}")

                        usL = uS.split("|")

                        lineS = usL[0]

                        self.labelD["unitS"] = usL[1].strip()

                        self.labelD["descS"] = usL[2].strip()

                        rvtC = tag_md.TagsMD(lineS, self.labelD, self.folderD,

                                             self.localD)

                        if ":=" in uS:                         # declare tag

                            tfS = "declare"

                            blockevalL.append(rvtC.tag_parse(":="))

                            rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,

                                                   self.localD)

                            eqL = rvtC.tag_parse(":=")

                            blockevalB = True

                            continue

                        else:

                            tfS = "assign"                     # assign tag

                            eqL = rvtC.tag_parse("=")

                            mdS += eqL[1]

                            blockevalL.append(eqL[0])

                            rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,

                                                   self.localD)

                            eqL = rvtC.tag_parse("=")

                            rstS += eqL[1]

                            blockevalB = True

                            continue

                    else:

                        print(uS)       # pass unformatted string

                # export values

                valP = Path(self.folderD["dataP"], self.folderD["valfileS"])

                with open(valP, "w", newline="") as f:

                    writecsv = csv.writer(f)

                    writecsv.writerow(hdraL)

                    writecsv.writerows(vtableL)

                return (xutfS, xmdS, xrstS,  self.labelD, self.folderD, self.rivtD)

            def atable(self, tblL, hdreL, tblfmt, alignaL):

                """write assign values table"""

                locals().update(self.rivtD)

                valL = []

                for vaL in tblL:

                    varS = vaL[0].strip()

                    valS = vaL[1].strip()

                    unit1S, unit2S = vaL[2], vaL[3]

                    descripS = vaL[4].strip()

                    if unit1S != "-":

                        if type(eval(valS)) == list:

                            val1U = array(eval(valS)) * eval(unit1S)

                            val2U = [q.cast_unit(eval(unit2S)) for q in val1U]

                        else:

                            cmdS = varS + "= " + valS

                            exec(cmdS, globals(), locals())

                            valU = eval(varS)

                            val1U = str(valU.cast_unit(eval(unit1S)))

                            val2U = str(valU.cast_unit(eval(unit2S)))

                    else:

                        cmdS = varS + "= " + valS

                        exec(cmdS, globals(), locals())

                        valU = eval(varS)

                        val1U = str(valU)

                        val2U = str(valU)

                    valL.append([varS, val1U, val2U, descripS])

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(

                    tabulate(

                        valL, tablefmt=tblfmt, headers=hdreL,

                        showindex=False,  colalign=alignaL))

                mdS = output.getvalue()

                sys.stdout = old_stdout

                sys.stdout.flush()

                self.localD.update(locals())

                print("\n" + mdS+"\n")

                return mdS

            def dtable(self, tblL, hdrvL, tblfmt, alignvL):

                """write declare values table"""

                locals().update(self.rivtD)

                valL = []

                for vaL in tblL:

                    varS = vaL[0].strip()

                    valS = vaL[1].strip()

                    unit1S, unit2S = vaL[2], vaL[3]

                    descripS = vaL[4].strip()

                    if unit1S != "-":

                        if type(eval(valS)) == list:

                            val1U = array(eval(valS)) * eval(unit1S)

                            val2U = [q.cast_unit(eval(unit2S)) for q in val1U]

                        else:

                            cmdS = varS + "= " + valS + " * " + unit1S

                            exec(cmdS, globals(), locals())

                            valU = eval(varS)

                            val1U = str(valU.cast_unit(eval(unit1S)))

                            val2U = str(valU.cast_unit(eval(unit2S)))

                    else:

                        cmdS = varS + "= " + valS

                        exec(cmdS, globals(), locals())

                        valU = eval(varS)

                        val1U = str(valU)

                        val2U = str(valU)

                    valL.append([varS, val1U, val2U, descripS])

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(

                    tabulate(

                        valL, tablefmt=tblfmt, headers=hdrvL,

                        showindex=False,  colalign=alignvL))

                mdS = output.getvalue()

                sys.stdout = old_stdout

                sys.stdout.flush()

                self.rivtD.update(locals())

                print("\n" + mdS+"\n")

                return mdS

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

### RivtParse

```python3
class RivtParse(
    methS,
    folderD,
    labelD,
    rivtD
)
```

format rivt-strings as utf and rst files

#### Methods

    
#### atable

```python3
def atable(
    self,
    tblL,
    hdreL,
    tblfmt,
    alignaL
)
```

write assign values table

??? example "View Source"
            def atable(self, tblL, hdreL, tblfmt, alignaL):

                """write assign values table"""

                locals().update(self.rivtD)

                valL = []

                for vaL in tblL:

                    varS = vaL[0].strip()

                    valS = vaL[1].strip()

                    unit1S, unit2S = vaL[2], vaL[3]

                    descripS = vaL[4].strip()

                    if unit1S != "-":

                        if type(eval(valS)) == list:

                            val1U = array(eval(valS)) * eval(unit1S)

                            val2U = [q.cast_unit(eval(unit2S)) for q in val1U]

                        else:

                            cmdS = varS + "= " + valS

                            exec(cmdS, globals(), locals())

                            valU = eval(varS)

                            val1U = str(valU.cast_unit(eval(unit1S)))

                            val2U = str(valU.cast_unit(eval(unit2S)))

                    else:

                        cmdS = varS + "= " + valS

                        exec(cmdS, globals(), locals())

                        valU = eval(varS)

                        val1U = str(valU)

                        val2U = str(valU)

                    valL.append([varS, val1U, val2U, descripS])

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(

                    tabulate(

                        valL, tablefmt=tblfmt, headers=hdreL,

                        showindex=False,  colalign=alignaL))

                mdS = output.getvalue()

                sys.stdout = old_stdout

                sys.stdout.flush()

                self.localD.update(locals())

                print("\n" + mdS+"\n")

                return mdS

    
#### dtable

```python3
def dtable(
    self,
    tblL,
    hdrvL,
    tblfmt,
    alignvL
)
```

write declare values table

??? example "View Source"
            def dtable(self, tblL, hdrvL, tblfmt, alignvL):

                """write declare values table"""

                locals().update(self.rivtD)

                valL = []

                for vaL in tblL:

                    varS = vaL[0].strip()

                    valS = vaL[1].strip()

                    unit1S, unit2S = vaL[2], vaL[3]

                    descripS = vaL[4].strip()

                    if unit1S != "-":

                        if type(eval(valS)) == list:

                            val1U = array(eval(valS)) * eval(unit1S)

                            val2U = [q.cast_unit(eval(unit2S)) for q in val1U]

                        else:

                            cmdS = varS + "= " + valS + " * " + unit1S

                            exec(cmdS, globals(), locals())

                            valU = eval(varS)

                            val1U = str(valU.cast_unit(eval(unit1S)))

                            val2U = str(valU.cast_unit(eval(unit2S)))

                    else:

                        cmdS = varS + "= " + valS

                        exec(cmdS, globals(), locals())

                        valU = eval(varS)

                        val1U = str(valU)

                        val2U = str(valU)

                    valL.append([varS, val1U, val2U, descripS])

                sys.stdout.flush()

                old_stdout = sys.stdout

                output = StringIO()

                output.write(

                    tabulate(

                        valL, tablefmt=tblfmt, headers=hdrvL,

                        showindex=False,  colalign=alignvL))

                mdS = output.getvalue()

                sys.stdout = old_stdout

                sys.stdout.flush()

                self.rivtD.update(locals())

                print("\n" + mdS+"\n")

                return mdS

    
#### str_parse

```python3
def str_parse(
    self,
    strL
)
```

parse method string line by line starting with second line

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| strL | list | split method string | None |

**Returns:**

| Type | Description |
|---|---|
| mdS | md formatted string |

??? example "View Source"
            def str_parse(self, strL):

                """parse method string line by line starting with second line

                    :param list strL: split method string

                    :return mdS: md formatted string

                    :return rstS: reST formatted string

                    :return labelD: increment references

                    :return folderD: folder paths

                    :rtype mdS: string

                    :rtype rstS: string

                    :rtype folderD: dictionary

                    :rtype labelD: dictionary

                """

                xutfS = """"""      # utfS local string

                xmdS = """"""       # mdS local string

                xrstS = """"""      # rstS local string

                uS = """"""         # raw local line

                blockB = False

                # table alignment

                hdrdL = ["variable", "value", "[value]", "description"]

                aligndL = ["left", "right", "right", "left"]

                hdraL = ["variable", "value", "[value]", "description [eq. number]"]

                alignaL = ["left", "right", "right", "left"]

                blockevalL = []     # current value table

                blockevalB = False  # stop accumulation of values

                vtableL = []        # value table for export

                eqL = []            # equation result table

                lineS = ""

                for uS in strL:

                    # print(f"{blockassignB=}")

                    # print(f"{uS=}")

                    uS = uS[4:]                                # remove indent

                    if blockB:                                 # accumulate block

                        lineS += uS

                        continue

                    if blockB and uS.strip() == "[q]]":        # end of block

                        tagS = self.tagsD["[q]"]

                        rvtS = tag_utf.TagsUTF(lineS, tagS,

                                               self.labelD, self.folderD,  self.rivtD)

                        xutfS += rvtS + "\n"

                        rvtS = tag_md.TagsMD(lineS, tagS,

                                             self.labelD, self.folderD,  self.rivtD)

                        xmdS += rvtS + "\n"

                        rvtS = tag_rst.TagsRST(lineS, tagS,

                                               self.labelD, self.folderD,  self.rivtD)

                        xrstS += rvtS + "\n"

                        blockB = False

                    if blockevalB and len(uS.strip()) < 2:    # value tables

                        vtableL += blockevalL

                        if tfS == "declare":

                            vutfS = self.dtable(blockevalL, hdrdL,

                                                "rst", aligndL) + "\n\n"

                            vmdS = self.dtable(blockevalL, hdrdL,

                                               "html", aligndL) + "\n\n"

                            xutfS += vutfS

                            xmdS += vmdS

                            xrstS += vutfS

                        if tfS == "assign":

                            vutfS = self.dtable(blockevalL, hdrdL,

                                                "rst", aligndL) + "\n\n"

                            vmdS = self.atable(blockevalL, hdraL,

                                               "html", alignaL) + "\n\n"

                            xutfS += vutfS

                            xmdS += vmdS

                            xrstS += vutfS

                        blockevalL = []

                        blockevalB = False

                    elif uS[0:2] == "||":                      # commands

                        usL = uS[2:].split("|")

                        parL = usL[1:]

                        cmdS = usL[0].strip()

                        if cmdS in self.cmdL:

                            rvtC = cmd_utf.CmdUTF(

                                parL, self.labelD, self.folderD, self.rivtD)

                            utfS = rvtC.cmd_parse(cmdS)

                            # print(f"{utfS=}")

                            xutfS += utfS

                            rvtC = cmd_md.CmdMD(

                                parL, self.labelD, self.folderD, self.rivtD)

                            mdS = rvtC.cmd_parse(cmdS)

                            # print(f"{mdS=}")

                            xmdS += mdS

                            rvtC = cmd_rst.CmdRST(

                                parL, self.labelD, self.folderD, self.rivtD)

                            reS = rvtC.cmd_parse(cmdS)

                            xrstS += reS

                    elif "_[" in uS:                           # line tag

                        usL = uS.split("_[")

                        lineS = usL[0]

                        tagS = usL[1].strip()

                        if tagS[0] == "[":                     # block tag

                            blockB = True

                        if tagS in self.tagsD:

                            rvtC = tag_utf.TagsUTF(lineS, self.labelD, self.folderD,

                                                   self.tagsD, self.rivtD)

                            utfxS = rvtC.tag_parse(tagS)

                            xutfS += utfxS + "\n"

                            rvtC = tag_md.TagsMD(lineS, self.labelD, self.folderD,

                                                 self.tagsD, self.rivtD)

                            mdS = rvtC.tag_parse(tagS)

                            xmdS += mdS + "\n"

                            rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,

                                                   self.tagsD, self.rivtD)

                            reS = rvtC.tag_parse(tagS)

                            xrstS += reS + "\n"

                    elif "=" in uS and self.methS == "V":       # equation tag

                        # print(f"{uS=}")

                        usL = uS.split("|")

                        lineS = usL[0]

                        self.labelD["unitS"] = usL[1].strip()

                        self.labelD["descS"] = usL[2].strip()

                        rvtC = tag_md.TagsMD(lineS, self.labelD, self.folderD,

                                             self.localD)

                        if ":=" in uS:                         # declare tag

                            tfS = "declare"

                            blockevalL.append(rvtC.tag_parse(":="))

                            rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,

                                                   self.localD)

                            eqL = rvtC.tag_parse(":=")

                            blockevalB = True

                            continue

                        else:

                            tfS = "assign"                     # assign tag

                            eqL = rvtC.tag_parse("=")

                            mdS += eqL[1]

                            blockevalL.append(eqL[0])

                            rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,

                                                   self.localD)

                            eqL = rvtC.tag_parse("=")

                            rstS += eqL[1]

                            blockevalB = True

                            continue

                    else:

                        print(uS)       # pass unformatted string

                # export values

                valP = Path(self.folderD["dataP"], self.folderD["valfileS"])

                with open(valP, "w", newline="") as f:

                    writecsv = csv.writer(f)

                    writecsv.writerow(hdraL)

                    writecsv.writerows(vtableL)

                return (xutfS, xmdS, xrstS,  self.labelD, self.folderD, self.rivtD)