# Module write

rivt write methods for pdf and html files

None

??? example "View Source"
        #!python

        """ rivt write methods for pdf and html files"""

        

        import os

        import time

        

        

        def write_md(mdS):

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

                f1.write(rstcalcS.encode("md-8"))

            print("INFO: rst calc written ", docdir, flush=True)

        

            f1 = open(_rstfileP, "r", encoding="md-8", errors="ignore")

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

                "omdile": Path(_dpathP0 / ".".join([_cnameS, ".out"])),

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

            with open(texfileP, "r", encoding="md-8", errors="ignore") as texin:

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

            with open(texfileP, "w", encoding="md-8") as texout:

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

## Functions

    
### gen_pdf

```python3
def gen_pdf(
    cmdS,
    doctypeS,
    stylefileS,
    calctitleS,
    startpageS
)
```

    
write calc rSt file to d00_docs folder

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| cmdS | str | [description] | None |
| doctypeS | [type] | [description] | None |
| stylefileS | [type] | [description] | None |
| calctitleS | [type] | [description] | None |
| startpageS | [type] | [description] | None |

??? example "View Source"
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

    
### gen_rst

```python3
def gen_rst(
    cmdS,
    doctypeS,
    stylefileS,
    calctitleS,
    startpageS
)
```

    
write calc rSt file to d00_docs folder

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| cmdS | str | [description] | None |
| doctypeS | [type] | [description] | None |
| stylefileS | [type] | [description] | None |
| calctitleS | [type] | [description] | None |
| startpageS | [type] | [description] | None |

??? example "View Source"
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

                f1.write(rstcalcS.encode("md-8"))

            print("INFO: rst calc written ", docdir, flush=True)

        

            f1 = open(_rstfileP, "r", encoding="md-8", errors="ignore")

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

    
### gen_tex

```python3
def gen_tex(
    doctypeS,
    stylefileS,
    calctitleS,
    startpageS
)
```

    

??? example "View Source"
        def gen_tex(doctypeS, stylefileS, calctitleS, startpageS):

        

            global rstcalcS, _rstflagB

        

            pdfD = {

                "cpdfP": Path(_dpathP0 / ".".join([_cnameS, "pdf"])),

                "chtml": Path(_dpathP0 / ".".join([_cnameS, "html"])),

                "trst": Path(_dpathP0 / ".".join([_cnameS, "rst"])),

                "ttex1": Path(_dpathP0 / ".".join([_cnameS, "tex"])),

                "auxfile": Path(_dpathP0 / ".".join([_cnameS, ".aux"])),

                "omdile": Path(_dpathP0 / ".".join([_cnameS, ".out"])),

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

            with open(texfileP, "r", encoding="md-8", errors="ignore") as texin:

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

            with open(texfileP, "w", encoding="md-8") as texout:

                texout.write(texf)

            print("INFO: tex file updated")

        

            if doctypeS == "pdf":

                gen_pdf(texfileP)

        

            os._exit(1)

    
### write_html

```python3
def write_html(
    rstS
)
```

    

??? example "View Source"
        def write_html(rstS):

            pass

    
### write_pdf

```python3
def write_pdf(
    texfileP
)
```

    
write pdf calc to reports folder and open

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| texfileP | path | doc config folder | None |

??? example "View Source"
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

    
### write_md

```python3
def write_md(
    mdS
)
```

    

??? example "View Source"
        def write_md(mdS):

            pass