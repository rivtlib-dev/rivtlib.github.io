# Module write_public

??? example "View Source"
        def _tocs():

            # add table of contents to summary

            tocS = ""

            secI = 0

            for iS in rivtL:

                if iS[0:5] == "rv.I(" and "--" not in iS:

                    secI += 1

                    jS = iS.split('"""')

                    kS = jS.split("|").strip()

                    tocS += str(secI) + "'" + kS

                elif i[0:4] == "rv.V" and "--" not in iS:

                    secI += 1

                    jS = iS.split('"""')

                    kS = jS.split("|").strip()

                    tocS += str(secI) + "'" + kS

                elif i[0:4] == "rv.T" and "--" not in iS:

                    secI += 1

                    jS = iS.split('"""')

                    kS = jS.split("|").strip()

                    tocS += str(secI) + "'" + kS

                else:

                    pass

            mdeditL = mdS.split("## ", 1)

            mdS = mdeditL[0] + tocS + mdeditL[1]

        

        def _mod_tex(tfileP):

            """Modify TeX file to avoid problems with escapes:

                -  Replace marker "aaxbb " inserted by rivt with

                    \\hfill because it is not handled by reST).

                - Delete inputenc package

                - Modify section title and add table of contents

            """

            startS = str(incrD["pageI"])

            doctitleS = str(incrD["doctitleS"])

            with open(tfileP, "r", encoding="md-8", errors="ignore") as f2:

                texf = f2.read()

            # modify "at" command

            texf = texf.replace("""\\begin{document}""",

                                """\\renewcommand{\contentsname}{""" + doctitleS

                                + "}\n" +

                                """\\begin{document}\n""" +

                                """\\makeatletter\n""" +

                                """\\renewcommand\@dotsep{10000}""" +

                                """\\makeatother\n""")

            # add table of contents, figures and tables

            # texf = texf.replace("""\\begin{document}""",

            #                     """\\renewcommand{\contentsname}{""" + doctitleS

            #                     + "}\n" +

            #                     """\\begin{document}\n""" +

            #                     """\\makeatletter\n""" +

            #                     """\\renewcommand\@dotsep{10000}""" +

            #                     """\\makeatother\n""" +

            #                     """\\tableofcontents\n""" +

            #                     """\\listoftables\n""" +

            #                     """\\listoffigures\n""")

            texf = texf.replace("""inputenc""", """ """)

            texf = texf.replace("aaxbb ", """\\hfill""")

            texf = texf.replace("?x?", """\\""")

            texf = texf.replace(

                """fancyhead[L]{\leftmark}""",

                """fancyhead[L]{\\normalsize\\bfseries  """ + doctitleS + "}")

            texf = texf.replace("x*x*x", "[" + incrD["docnumS"] + "]")

            texf = texf.replace("""\\begin{tabular}""", "%% ")

            texf = texf.replace("""\\end{tabular}""", "%% ")

            texf = texf.replace(

                """\\begin{document}""",

                """\\begin{document}\n\\setcounter{page}{""" + startS + "}\n")

            with open(tfileP, "w", encoding="md-8") as f2:

                f2.write(texf)

            # with open(tfileP, 'w') as texout:

            #    print(texf, file=texout)

            return

        

        def _gen_pdf(self):

            """Write PDF file from TEX file

            """

            pdfD = {

                "xpdfP": Path(tempP, docbaseS + ".pdf"),

                "xhtmlP": Path(tempP, docbaseS + ".html"),

                "xrstP": Path(tempP, docbaseS + ".rst"),

                "xtexP": Path(tempP, docbaseS + ".tex"),

                "xauxP": Path(tempP, docbaseS + ".aux"),

                "xoutP": Path(tempP, docbaseS + ".out"),

                "xflsP": Path(tempP, docbaseS + ".fls"),

                "xtexmakP": Path(tempP, docbaseS + ".fdb_latexmk"),

            }

            # os.system('latex --version')

            os.chdir(tempP)

            texfS = str(pdfD["xtexP"])

            # pdf1 = 'latexmk -xelatex -quiet -f ' + texfS + " > latex-log.txt"

            pdf1 = 'xelatex -interaction=batchmode ' + texfS

            # print(f"{pdf1=}"")

            os.system(pdf1)

            srcS = ".".join([docbaseS, "pdf"])

            dstS = str(Path(reportP, srcS))

            shutil.copy(srcS, dstS)

            return dstS

        

        def _rest2tex(rstfileS):

            """convert reST to tex file

            0. insert [i] data into model (see _genxmodel())

            1. read the expanded model

            2. build the operations ordered dictionary

            3. execute the dictionary and write the md-8 calc and Python file

            4. if the pdf flag is set re-execute xmodel and write the PDF calc

            5. write variable summary to stdout

            :param pdffileS: _description_

            :type pdffileS: _type_

            """

            global folderD

            style_path = folderD["styleP"]

            # print(f"{style_path=}")

            # f2 = open(style_path)

            # f2.close

            pythoncallS = "python "

            if sys.platform == "linux":

                pythoncallS = "python3 "

            elif sys.platform == "darwin":

                pythoncallS = "python3 "

            rst2texP = Path(rivtP, "scripts", "rst2latex.py")

            # print(f"{str(rst2texP)=}")

            texfileP = Path(tempP, docbaseS + ".tex")

            rstfileP = Path(tempP, docbaseS + ".rst")

            with open(rstfileP, "w", encoding='md-8') as f2:

                f2.write(rstS)

            tex1S = "".join(

                [

                    pythoncallS,

                    str(rst2texP),

                    " --embed-stylesheet ",

                    " --documentclass=report ",

                    " --documentoptions=12pt,notitle,letterpaper ",

                    " --stylesheet=",

                    str(style_path) + " ",

                    str(rstfileP) + " ",

                    str(texfileP),

                ]

            )

            logging.info(f"tex call:{tex1S=}")

            os.chdir(tempP)

            try:

                os.system(tex1S)

                time.sleep(1)

                logging.info(f"tex file written: {texfileP=}")

                print(f"tex file written: {texfileP=}")

            except SystemExit as e:

                logging.exception('tex file not written')

                logging.error(str(e))

                sys.exit("tex file write failed")

            _mod_tex(texfileP)

            pdfS = _gen_pdf(texfileP)

            return pdfS