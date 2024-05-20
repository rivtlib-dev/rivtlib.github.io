# Module tag_parse

??? example "View Source"
        import sympy as sp

        from sympy.abc import _clash2

        from numpy import *

        from rivtlib.units import *

        

        class Tags:

            """subclass - convert rivt tags to MD or reST

                    ============================ =======================================

                    tags                                   description 

                    ============================ =======================================

                    I,V line format:

                    text _[h1-h6]                     heading type        

                    text _[b]                       bold 

                    text _[i]                       italic

                    text _[c]                       center

                    text _[bic]                     combined formatting

                    text _[u]                       underline   

                    text _[r]                       right justify

                    text _[l]                       LaTeX math

                    text _[s]                       sympy math

                    text _[l,s;bic]                 combined formatting

                    text _[e]                       equation label and autonumber

                    text _[f]                       figure caption and autonumber

                    text _[t]                       table title and autonumber

                    text _[#]                       footnote and autonumber

                    text _[d]                       footnote description 

                    _[line]                         horizontal line

                    _[page]                         new page

                    _[address, label]               url, internal reference

                    I,V  block format:          

                    _[[b]]                          bold

                    _[[c]]                          center

                    _[[i]]                          italic

                    _[[p]]                          plain  

                    _[[bcip]]                       combined formatting

                    _[[l]]                          LaTeX

                    _[[h]]                          HTML 

                    _[[q]]                          quit block

                """

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

            def declare(self):

                """declare variable values

                :return: _description_

                :rtype: _type_

                """

                locals().update(self.localD)

                varS = str(self.lineS).split(":=")[0].strip()

                valS = str(self.lineS).split(":=")[1].strip()

                unit1S = str(self.labelD["unitS"]).split(",")[0]

                unit2S = str(self.labelD["unitS"]).split(",")[1]

                descripS = str(self.labelD["descS"])

                if unit1S.strip() != "-":

                    cmdS = varS + "= " + valS + "*" + unit1S

                else:

                    cmdS = varS + "= as_unum(" + valS + ")"

                exec(cmdS, globals(), locals())

                self.localD.update(locals())

                return [varS, valS, unit1S, unit2S, descripS]

            def assign(self):

                """assign value to equation

                :return: _description_

                :rtype: _type_

                """

                locals().update(self.localD)

                varS = str(self.lineS).split("=")[0].strip()

                valS = str(self.lineS).split("=")[1].strip()

                unit1S = str(self.labelD["unitS"]).split(",")[0]

                unit2S = str(self.labelD["unitS"]).split(",")[1]

                descS = str(self.labelD["eqlabelS"])

                precI = int(self.labelD["descS"])  # trim result

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

                        # print(f"{val1U=}")

                else:

                    cmdS = varS + "= as_unum(" + valS + ")"

                    exec(cmdS, globals(), locals())

                    valU = eval(varS)

                    valdec = round(valU.number(), precI)

                    val1U = val2U = str(valdec)

                spS = "Eq(" + varS + ",(" + valS + "))"

                mdS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

                mdS = "\n" + mdS + "\n"

                eqL = [varS, valS, unit1S, unit2S, descS]

                print(mdS)                      # print equation

                subS = " "

                if self.labelD["subB"]:

                    subS = self.vsub(eqL, precI, varS, val1U)

                    print(subS)                  # print with substition

                self.localD.update(locals())

                return [eqL, mdS + "\n" + subS + "\n\n"]

            def vsub(self, eqL, precI, varS, val1U):

                """substitute variables with values

                :param eqL: _description_

                :type eqL: _type_

                :param precI: _description_

                :type precI: _type_

                :param varS: _description_

                :type varS: _type_

                :param val1U: _description_

                :type val1U: _type_

                :return: _description_

                :rtype: _type_

                """

                locals().update(self.localD)

                fmtS = "%." + str(precI) + "f"

                varL = [str(eqL[0]), str(eqL[1])]

                # resultS = vars[0].strip() + " = " + str(eval(vars[1]))

                # sps = sps.encode('unicode-escape').decode()

                eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"

                with sp.evaluate(False):

                    symeq = sp.sympify(eqS.strip())

                # print(f"{symeq=}")

                symat = symeq.atoms(sp.Symbol)

                # print(f"{symat=}")

                for n1O in symat:

                    if str(n1O) == varS:

                        symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))

                        continue

                    # print(f"{n1O=}")

                    n1U = eval(str(n1O))

                    n1U.set_format(value_format=fmtS, auto_norm=True)

                    # print(f"{n1U=}")

                    evlen = len(str(n1U))  # get var length

                    new_var = str(n1U).rjust(evlen, "~")

                    new_var = new_var.replace("_", "|")

                    # print(f"{new_var=}")

                    with sp.evaluate(False):

                        symeq = symeq.subs(n1O, sp.Symbol(new_var))

                    # print(f"{symeq=}")

                out2 = sp.pretty(symeq, wrap_line=False)

                # print('out2a\n', out2)

                # symat1 = symeq.atoms(sp.Symbol)  # adjust character length

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

                mdS = out3 + "\n\n"

                return mdS

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

                unit1S = str(self.labelD["unitS"]).split(",")[0]

                unit2S = str(self.labelD["unitS"]).split(",")[1]

                descripS = str(self.labelD["descS"])

                if unit1S.strip() != "-":

                    cmdS = varS + "= " + valS + "*" + unit1S

                else:

                    cmdS = varS + "= as_unum(" + valS + ")"

                exec(cmdS, globals(), locals())

                self.localD.update(locals())

                return [varS, valS, unit1S, unit2S, descripS]

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

                unit1S = str(self.labelD["unitS"]).split(",")[0]

                unit2S = str(self.labelD["unitS"]).split(",")[1]

                descS = str(self.labelD["eqlabelS"])

                precI = int(self.labelD["descS"])  # trim result

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

                if self.labelD["subB"]:              # replace variables with numbers

                    subS = self.vsub(eqL, precI, varS, val1U) + "\n\n"

                assignL = [varS, str(val1U), unit1S, unit2S, descS]

                return [assignL, rstS + subS]

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

### Tags

```python3
class Tags(
    /,
    *args,
    **kwargs
)
```

subclass - convert rivt tags to MD or reST

============================ =======================================
tags                                   description 
============================ =======================================

I,V line format:
text _[h1-h6]                     heading type        
text _[b]                       bold 
text _[i]                       italic
text _[c]                       center
text _[bic]                     combined formatting
text _[u]                       underline   
text _[r]                       right justify
text _[l]                       LaTeX math
text _[s]                       sympy math
text _[l,s;bic]                 combined formatting
text _[e]                       equation label and autonumber
text _[f]                       figure caption and autonumber
text _[t]                       table title and autonumber
text _[#]                       footnote and autonumber
text _[d]                       footnote description 
_[line]                         horizontal line
_[page]                         new page
_[address, label]               url, internal reference
I,V  block format:          
_[[b]]                          bold
_[[c]]                          center
_[[i]]                          italic
_[[p]]                          plain  
_[[bcip]]                       combined formatting
_[[l]]                          LaTeX
_[[h]]                          HTML 
_[[q]]                          quit block

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

                unit1S = str(self.labelD["unitS"]).split(",")[0]

                unit2S = str(self.labelD["unitS"]).split(",")[1]

                descS = str(self.labelD["eqlabelS"])

                precI = int(self.labelD["descS"])  # trim result

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

                if self.labelD["subB"]:              # replace variables with numbers

                    subS = self.vsub(eqL, precI, varS, val1U) + "\n\n"

                assignL = [varS, str(val1U), unit1S, unit2S, descS]

                return [assignL, rstS + subS]

    
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

                unit1S = str(self.labelD["unitS"]).split(",")[0]

                unit2S = str(self.labelD["unitS"]).split(",")[1]

                descripS = str(self.labelD["descS"])

                if unit1S.strip() != "-":

                    cmdS = varS + "= " + valS + "*" + unit1S

                else:

                    cmdS = varS + "= as_unum(" + valS + ")"

                exec(cmdS, globals(), locals())

                self.localD.update(locals())

                return [varS, valS, unit1S, unit2S, descripS]

    
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