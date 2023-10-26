# Module cmd_parse

??? example "View Source"
        import sys

        import csv

        import textwrap

        import logging

        from pathlib import Path

        import tabulate

        from numpy import *

        

        class Commands():

            """common methods for rivt to md, utf and reST

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

### Commands

```python3
class Commands(
    /,
    *args,
    **kwargs
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