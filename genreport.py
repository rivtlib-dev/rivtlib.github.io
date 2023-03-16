#! python

"""
    Collate pdf docs into a report
"""

#!python
""" rivt write methods for pdf and html files"""




import os
import time
def write_utf(utfS):
    pass


def gen_rst(cmdS, doctypeS, stylefileS, calctitleS, startpageS):
    """write calc rSt file to d00_docs folder

    Args:
        cmdS (str): [description]
        doctypeS ([type]): [description]
        stylefileS ([type]): [description]
        calctitleS ([type]): [description]
        startpageS ([type]): [description]
    """

    global rstcalcS, _rstflagB

    _rstflagB = True
    rstcalcS = """"""
    exec(cmdS, globals(), locals())
    docdir = os.getcwd()
    with open(_rstfileP, "wb") as f1:
        f1.write(rstcalcS.encode("UTF-8"))
    print("INFO: rst calc written ", docdir, flush=True)

    f1 = open(_rstfileP, "r", encoding="utf-8", errors="ignore")
    rstcalcL = f1.readlines()
    f1.close()
    print("INFO: rst file read: " + str(_rstfileP))

    if doctypeS == "tex" or doctypeS == "pdf":
        gen_tex(doctypeS, stylefileS, calctitleS, startpageS)
    elif doctypeS == "html":
        gen_html()
    else:
        print("INFO: doc type not recognized")

    os._exit(1)


def gen_tex(doctypeS, stylefileS, calctitleS, startpageS):

    global rstcalcS, _rstflagB

    pdfD = {
        "cpdfP": Path(_dpathP0 / ".".join([_cnameS, "pdf"])),
        "chtml": Path(_dpathP0 / ".".join([_cnameS, "html"])),
        "trst": Path(_dpathP0 / ".".join([_cnameS, "rst"])),
        "ttex1": Path(_dpathP0 / ".".join([_cnameS, "tex"])),
        "auxfile": Path(_dpathP0 / ".".join([_cnameS, ".aux"])),
        "outfile": Path(_dpathP0 / ".".join([_cnameS, ".out"])),
        "texmak2": Path(_dpathP0 / ".".join([_cnameS, ".fls"])),
        "texmak3": Path(_dpathP0 / ".".join([_cnameS, ".fdb_latexmk"])),
    }
    if stylefileS == "default":
        stylefileS = "pdf_style.sty"
    else:
        stylefileS == stylefileS.strip()
    style_path = Path(_dpathP0 / stylefileS)
    print("INFO: style sheet " + str(style_path))
    pythoncallS = "python "
    if sys.platform == "linux":
        pythoncallS = "python3 "
    elif sys.platform == "darwin":
        pythoncallS = "python3 "

    rst2xeP = Path(rivtpath / "scripts" / "rst2xetex.py")
    texfileP = pdfD["ttex1"]
    tex1S = "".join(
        [
            pythoncallS,
            str(rst2xeP),
            " --embed-stylesheet ",
            " --documentclass=report ",
            " --documentoptions=12pt,notitle,letterpaper ",
            " --stylesheet=",
            str(style_path) + " ",
            str(_rstfileP) + " ",
            str(texfileP),
        ]
    )

    os.chdir(_dpathP0)
    os.system(tex1S)
    print("INFO: tex file written " + str(texfileP))

    # fix escape sequences
    fnumS = _setsectD["fnumS"]
    with open(texfileP, "r", encoding="utf-8", errors="ignore") as texin:
        texf = texin.read()
    texf = texf.replace("?x?", """\\""")
    texf = texf.replace(
        """fancyhead[L]{\leftmark}""",
        """fancyhead[L]{\\normalsize  """ + calctitleS + "}",
    )
    texf = texf.replace("x*x*x", fnumS)
    texf = texf.replace("""\\begin{tabular}""", "%% ")
    texf = texf.replace("""\\end{tabular}""", "%% ")
    texf = texf.replace(
        """\\begin{document}""",
        """\\begin{document}\n\\setcounter{page}{""" + startpageS + "}\n",
    )

    # texf = texf.replace(
    #     """\\begin{document}""",
    #     """\\renewcommand{\contentsname}{"""
    #     + self.calctitle
    #     + "}\n"
    #     + """\\begin{document}"""
    #     + "\n"
    #     + """\\makeatletter"""
    #     + """\\renewcommand\@dotsep{10000}"""
    #     + """\\makeatother"""
    #     + """\\tableofcontents"""
    #     + """\\listoftables"""
    #     + """\\listoffigures"""
    # )

    time.sleep(1)
    with open(texfileP, "w", encoding="utf-8") as texout:
        texout.write(texf)
    print("INFO: tex file updated")

    if doctypeS == "pdf":
        gen_pdf(texfileP)

    os._exit(1)


def write_pdf(texfileP):
    """write pdf calc to reports folder and open

    Args:
        texfileP (path): doc config folder
    """

    global rstcalcS, _rstflagB

    os.chdir()
    time.sleep(1)  # cleanup tex files
    os.system("latexmk -c")
    time.sleep(1)

    pdfmkS = (
        "perl.exe c:/texlive/2020/texmf-dist/scripts/latexmk/latexmk.pl "
        + "-pdf -xelatex -quiet -f "
        + str(texfileP)
    )

    os.system(pdfmkS)
    print("\nINFO: pdf file written: " + ".".join([_cnameS, "pdf"]))

    dnameS = _cnameS.replace("c", "d", 1)
    docpdfP = Path(_dpathP / ".".join([dnameS, "pdf"]))
    doclocalP = Path(_dpathP0 / ".".join([_cnameS, "pdf"]))
    time.sleep(2)  # move pdf to doc folder
    shutil.move(doclocalP, docpdfP)
    os.chdir(_dpathPcurP)
    print("INFO: pdf file moved to docs folder", flush=True)
    print("INFO: program complete")

    cfgP = Path(_dpathP0 / "rv_cfg.txt")  # read pdf display program
    with open(cfgP) as f2:
        cfgL = f2.readlines()
        cfg1S = cfgL[0].split("|")
        cfg2S = cfg1S[1].strip()
    cmdS = cfg2S + " " + str(Path(_dpathP) / ".".join([dnameS, "pdf"]))
    # print(cmdS)
    subprocess.run(cmdS)

    os._exit(1)


def gen_pdf(cmdS, doctypeS, stylefileS, calctitleS, startpageS):
    """write calc rSt file to d00_docs folder

    Args:
        cmdS (str): [description]
        doctypeS ([type]): [description]
        stylefileS ([type]): [description]
        calctitleS ([type]): [description]
        startpageS ([type]): [description]
    """

    # clean temp files
    fileL = [
        Path(fileconfigP, ".".join([calcbaseS, "pdf"])),
        Path(fileconfigP, ".".join([calcbaseS, "html"])),
        Path(fileconfigP, ".".join([calcbaseS, "rst"])),
        Path(fileconfigP, ".".join([calcbaseS, "tex"])),
        Path(fileconfigP, ".".join([calcbaseS, ".aux"])),
        Path(fileconfigP, ".".join([calcbaseS, ".out"])),
        Path(fileconfigP, ".".join([calcbaseS, ".fls"])),
        Path(fileconfigP, ".".join([calcbaseS, ".fdb_latexmk"])),
    ]
    os.chdir(fileconfigP)
    tmpS = os.getcwd()
    if tmpS == str(fileconfigP):
        for f in fileL:
            try:
                os.remove(f)
            except:
                pass
        time.sleep(1)
        print("INFO: temporary Tex files deleted \n", flush=True)


def write_html(rstS):
    pass


def project(self, rL):
    """insert tables or text from csv, xlsx or txt file

    Args:
        rL (list): parameter list

    Files are read from /docs/docfolder
    The command is identical to itable except file is read from docs/info.

    """
    alignD = {"S": "", "D": "decimal",
              "C": "center", "R": "right", "L": "left"}

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

    # from values

        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()
        # write dictionary from value-string
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                val1U = val2U = array(eval(valS))
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:  # no units
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            utfS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"
            utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            print("\n" + utfS + "\n")  # pretty print equation
            self.calcS += "\n" + utfS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:  # substitute into equation
                self._vsub(vL)
            else:  # write equation table
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())

        # update dictionary
        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

        # assign values
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            rstS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"  # pretty print
            symeq = sp.sympify(spS, _clash2, evaluate=False)
            eqltxS = sp.latex(symeq, mul_symbol="dot")
            self.restS += "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:
                self._vsub(vL)
            else:
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL, fltfmtS)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                # print(f"{cmdS=}")
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())
        # print(self.rivtD)

        # write values to table
        tbl = "x"
        hdrL = "y"
        tlbfmt = "z"
        alignL = "true"
        fltfmtS = "x"
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        tableS = tabulate(
            tbl,
            tablefmt=tblfmt,
            headers=hdrL,
            showindex=False,
            colalign=alignL,
            floatfmt=fltfmtS,
        )
        output.write(tableS)
        rstS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        inrstS = ""
        self.restS += ":: \n\n"
        for i in rstS.split("\n"):
            inrstS = "  " + i
            self.restS += inrstS + "\n"
        self.restS += "\n\n"
        self.rivtD.update(locals())

    if vsub:
        eqL = [1]
        eqS = "descrip"
        locals().update(self.rivtd)

        eformat = ""
        utfS = eqL[0].strip()
        descripS = eqL[3]
        parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try:
            eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
            # sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
            self.calcl.append(utfs)
        except:
            self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eqS.strip())  # substitute
            symat = symeq.atoms(sp.Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, "~")
                new_var = new_var.replace("_", "|")
                symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
            out2 = sp.pretty(symeq1, wrap_line=False)
            # print('out2a\n', out2)
            symat1 = symeq1.atoms(sp.Symbol)  # adjust character length
            for _n1 in symat1:
                orig_var = str(_n1).replace("~", "")
                orig_var = orig_var.replace("|", "_")
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = "{:." + eformat + "f}"
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            # print('out2b\n', out2)
            out3 = out2  # clean up unicode
            out3.replace("*", "\\u22C5")
            # print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == "-":
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                    _cnt = 0
        except:
            pass

                    if typeS != "table":  # skip table print
                print(uS)
                self.calcS += uS.rstrip() + "\n"
            self.rivtD.update(locals())

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

        self._parseRST("values", vcmdL, vmethL, vtagL)
        self.rivtD.update(locals())
        return self.restS, self.setsectD, self.setcmdD, self.rivtD, self.exportS

def project(self, rL):
    """insert tables or text from csv, xlsx or txt file

    Args:
        rL (list): parameter list

    Files are read from /docs/docfolder
    The command is identical to itable except file is read from docs/info.

    """
    alignD = {"S": "", "D": "decimal",
              "C": "center", "R": "right", "L": "left"}

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

    # from values

        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()
        # write dictionary from value-string
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                val1U = val2U = array(eval(valS))
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:  # no units
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            utfS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"
            utfS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            print("\n" + utfS + "\n")  # pretty print equation
            self.calcS += "\n" + utfS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:  # substitute into equation
                self._vsub(vL)
            else:  # write equation table
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())

        # update dictionary
        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

        # assign values
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            rstS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"  # pretty print
            symeq = sp.sympify(spS, _clash2, evaluate=False)
            eqltxS = sp.latex(symeq, mul_symbol="dot")
            self.restS += "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:
                self._vsub(vL)
            else:
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL, fltfmtS)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                # print(f"{cmdS=}")
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())
        # print(self.rivtD)

        # write values to table
        tbl = "x"
        hdrL = "y"
        tlbfmt = "z"
        alignL = "true"
        fltfmtS = "x"
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        tableS = tabulate(
            tbl,
            tablefmt=tblfmt,
            headers=hdrL,
            showindex=False,
            colalign=alignL,
            floatfmt=fltfmtS,
        )
        output.write(tableS)
        rstS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        inrstS = ""
        self.restS += ":: \n\n"
        for i in rstS.split("\n"):
            inrstS = "  " + i
            self.restS += inrstS + "\n"
        self.restS += "\n\n"
        self.rivtD.update(locals())

    if vsub:
        eqL = [1]
        eqS = "descrip"
        locals().update(self.rivtd)

        eformat = ""
        utfS = eqL[0].strip()
        descripS = eqL[3]
        parD = dict(eqL[1])
        varS = utfS.split("=")
        resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        try:
            eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
            # sps = sps.encode('unicode-escape').decode()
            utfs = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
            self.calcl.append(utfs)
        except:
            self.calcl.append(utfs)
        try:
            symeq = sp.sympify(eqS.strip())  # substitute
            symat = symeq.atoms(sp.Symbol)
            for _n2 in symat:
                evlen = len((eval(_n2.__str__())).__str__())  # get var length
                new_var = str(_n2).rjust(evlen, "~")
                new_var = new_var.replace("_", "|")
                symeq1 = symeq.subs(_n2, sp.Symbols(new_var))
            out2 = sp.pretty(symeq1, wrap_line=False)
            # print('out2a\n', out2)
            symat1 = symeq1.atoms(sp.Symbol)  # adjust character length
            for _n1 in symat1:
                orig_var = str(_n1).replace("~", "")
                orig_var = orig_var.replace("|", "_")
                try:
                    expr = eval((self.odict[orig_var][1]).split("=")[1])
                    if type(expr) == float:
                        form = "{:." + eformat + "f}"
                        symeval1 = form.format(eval(str(expr)))
                    else:
                        symeval1 = eval(orig_var.__str__()).__str__()
                except:
                    symeval1 = eval(orig_var.__str__()).__str__()
                out2 = out2.replace(_n1.__str__(), symeval1)
            # print('out2b\n', out2)
            out3 = out2  # clean up unicode
            out3.replace("*", "\\u22C5")
            # print('out3a\n', out3)
            _cnt = 0
            for _m in out3:
                if _m == "-":
                    _cnt += 1
                    continue
                else:
                    if _cnt > 1:
                        out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                    _cnt = 0
        except:
            pass

                    if typeS != "table":  # skip table print
                print(uS)
                self.calcS += uS.rstrip() + "\n"
            self.rivtD.update(locals())

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

        self._parseRST("values", vcmdL, vmethL, vtagL)
        self.rivtD.update(locals())
        return self.restS, self.setsectD, self.setcmdD, self.rivtD, self.exportS
