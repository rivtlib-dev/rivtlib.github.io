# Module commands

None

None

??? example "View Source"
        #

        

        def rvcmds(typeS: str):

            """_summary_

        

            :param str methodS: _description_

            :return _type_: _description_

            """

            cmdL = [

                "project",

                "report",

                "github",

                "append",

                "table",

                "text",

                "image1",

                "image2",

                "values",

                "list",

                "functions"

            ]

        

            cmdsetD = {

                "R": [0, 1, 2, 3, 4, 5],

                "I": [4, 5, 6, 7],

                "V": [4, 5, 6, 7, 8, 9, 10, 11],

                "T": [4, 5, 6, 7]

            }

        

            return [cmdL[i] for i in cmdsetD[typeS]]

        

        

        def text_md(self, iL: list):

            """insert text from file

        

            Args:

                iL (list): text command list

        

            || text | (file.txt) | literal; indent; html

        

            """

        

            txtP = Path(self.folderD["cpathcur"] / iL[1].strip())

            with open(txtP, "r", encoding="md-8") as txtf1:

                uL = txtf1.readlines()

            if iL[2].strip() == "indent":

                txtS = "".join(uL)

                widthI = self.setcmdD["cwidth"]

                inS = " " * 4

                uL = textwrap.wrap(txtS, width=widthI)

                uL = [inS + S1 + "\n" for S1 in uL]

                uS = "".join(uL)

            elif iL[2].strip() == "literal":

                txtS = "  ".join(uL)

                uS = "\n" + txtS

            elif iL[2].strip() == "literalindent":

                txtS = "\n\n::\n\n"

                for iS in uL:

                    txtS += "   " + iS

                uS = txtS + "\n\n"

            elif iL[2].strip() == "html":

                txtS = ""

                flg = 0

                for iS in uL:

                    if "src=" in iS:

                        flg = 1

                        continue

                    if flg == 1 and '"' in iS:

                        flg = 0

                        continue

                    if flg == 1:

                        continue

                    txtS += iS

                txtS = htm.html2text(txtS)

                uS = txtS.replace("\n    \n", "")

            else:

                txtS = "".join(uL)

                uS = "\n" + txtS

        

            # print(str(txtP))

            # self.calcS += str(txtP) + "\n"

            print(uS)

            self.calcS += uS + "\n"

        

        

        def table_md(self, iL: list):

            """insert table from csv or xlsx file

        

            Args:

                ipl (list): parameter list

            """

            alignD = {"S": "", "D": "decimal",

                      "C": "center", "R": "right", "L": "left"}

        

            if len(iL) < 4:

                iL += [""] * (4 - len(iL))  # pad parameters

            mdS = ""

            contentL = []

            sumL = []

            fileS = iL[1].strip()

            calpS = self.setsectD["fnumS"]

            tfileS = Path(self.folderD["cpathcur"] / fileS)

            extS = fileS.split(".")[1]

            if extS == "csv":

                with open(tfileS, "r") as csvfile:  # read csv file

                    readL = list(csv.reader(csvfile))

            elif extS == "xlsx":

                pDF1 = pd.read_excel(tfileS, header=None)

                readL = pDF1.values.tolist()

            else:

                return

            incl_colL = list(range(len(readL[1])))

            widthI = self.setcmdD["cwidthI"]

            alignS = self.setcmdD["calignS"]

            saS = alignD[alignS]

            if iL[2].strip():

                widthL = iL[2].split(",")  # new max col width

                widthI = int(widthL[0].strip())

                alignS = widthL[1].strip()

                saS = alignD[alignS]  # new align

                self.setcmdD.update({"cwidthI": widthI})

                self.setcmdD.update({"calignS": alignS})

            totalL = [""] * len(incl_colL)

            if iL[3].strip():  # columns

                if iL[3].strip() == "[:]":

                    totalL = [""] * len(incl_colL)

                else:

                    incl_colL = eval(iL[3].strip())

                    totalL = [""] * len(incl_colL)

            ttitleS = readL[0][0].strip() + " [t]_"

            utgS = self._tags(ttitleS, itagL)

            print(utgS.rstrip() + "\n")

            self.calcS += utgS.rstrip() + "\n\n"

            for row in readL[1:]:

                contentL.append([row[i] for i in incl_colL])

            wcontentL = []

            for rowL in contentL:  # wrap columns

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

            mdS = output.getvalue()

            sys.stdout = old_stdout

        

            print(str(tfileS))

            print(mdS)

            self.calcS += str(tfileS) + "\n"

            self.calcS += mdS + "\n"

        

        

        def image_md(self, iL: list):

            """insert one or two images from file

        

            Args:

                iL (list): image parameters

            """

            mdS = ""

            if "," in iL[1]:  # two images

                scaleF = iL[2].split(",")

                scale1F = float(scaleF[0])

                scale2F = float(scaleF[1])

                self.setcmdD.update({"scale1F": scale1F})

                self.setcmdD.update({"scale2F": scale2F})

                fileS = iL[1].split(",")

                file1S = fileS[0].strip()

                file2S = fileS[1].strip()

                docpS = "d" + self.setsectD["cnumS"]

                img1S = str(Path(self.folderD["dpathcur"] / file1S))

                img2S = str(Path(self.folderD["dpathcur"] / file2S))

                # pshrt1S = str(Path(*Path(img1S).parts[-4:]))

                # pshrt2S = str(Path(*Path(img2S).parts[-4:]))

                for fS in [img1S, img2S]:

                    mdS += "Figure path: " + fS + "\n"

                    try:

                        _display(_Image(fS))

                    except:

                        pass

                print(mdS)

                self.calcS += mdS + "\n"

            else:  # one image

                scale1F = float(iL[2])

                self.setcmdD.update({"scale1F": scale1F})

                fileS = iL[1].split(",")

                file1S = fileS[0].strip()

                docpS = "d" + self.setsectD["cnumS"]

                img1S = str(Path(self.folderD["dpathcur"] / file1S))

                mdS += "Figure path: " + img1S + "\n"

                try:

                    _display(_Image(img1S))

                except:

                    pass

                print(mdS)

                self.calcS += mdS + "\n"

        

        

        def latex_md(self, iL: list):

            """insert latex text from file

        

            Args:

                iL (list): text command list

            """

        

            calP = "c" + self.setsectD["cnumS"]

            txapath = Path(self.folderD["dpath0"] / iL[1].strip())

            with open(txapath, "r") as txtf1:

                uL = txtf1.readlines()

            if iL[2].strip() == "indent":

                txtS = "".join(uL)

                widthI = self.setcmdD["cwidth"]

                inS = " " * 4

                uL = textwrap.wrap(txtS, width=widthI)

                uL = [inS + S1 + "\n" for S1 in uL]

                uS = "".join(uL)

            elif iL[2].strip() == "literal":

                txtS = "  ".join(uL)

                uS = "\n" + txtS

            else:

                txtS = "".join(uL)

                uS = "\n" + txtS

        

            self.calcS += uS + "\n"

        

            print(uS)

            self.calcS += uS + "\n"

        

        

        def text_rst(self, iL: list):

            """insert text from file

        

            Args:

                iL (list): text command list

            """

            txapath = Path(self.folderD["cpathcur"] / iL[1].strip())

            with open(txapath, "r", encoding="md-8") as txtf1:

                rstL = txtf1.readlines()

            if iL[2].strip() == "indent":

                txtS = "".join(rstL)

                widthI = self.setcmdD["cwidth"]

                inS = " " * 4

                rstL = textwrap.wrap(txtS, width=widthI)

                rstL = [inS + S1 + "\n" for S1 in rstL]

                rstS = "".join(rstL)

            elif iL[2].strip() == "literal":

                txtS = " ".join(rstL)

                rstS = "\n\n::\n\n" + txtS + "\n\n"

            elif iL[2].strip() == "literalindent":

                txtS = "\n\n::\n\n"

                for iS in iL:

                    txtS += "   " + iS

                rstS = txtS + "\n\n"

            elif iL[2].strip() == "html":

                txtS = ""

                flg = 0

                for iS in rstL:

                    if "src=" in iS:

                        flg = 1

                        continue

                    if flg == 1 and '"' in iS:

                        flg = 0

                        continue

                    if flg == 1:

                        continue

                    txtS += iS

                txtS = htm.html2text(txtS)

                txtS = "   " + txtS.replace("\n    \n", "")

                rstL = txtS.split("\n")

                for num, iS in enumerate(rstL):

                    rstL[num] = "   " + iS

                rstS = "\n".join(rstL[1:])

                rstS = "\n\n::\n\n" + rstS + "\n\n"

            else:

                txtS = "".join(rstL)

                rstS = "\n" + txtS

        

            self.restS += rstS + "\n"

        

        

        def table_rst(self, iL: list):

            """insert table from csv or xlsx file

        

            Args:

                ipl (list): parameter list

            """

            alignD = {"S": "", "D": "decimal",

                      "C": "center", "R": "right", "L": "left"}

        

            if len(iL) < 4:

                iL += [""] * (4 - len(iL))  # pad parameters

            mdS = ""

            contentL = []

            sumL = []

            fileS = iL[1].strip()

            calpS = self.setsectD["fnumS"]

            tfileS = Path(self.folderD["cpathcur"] / fileS)

            extS = fileS.split(".")[1]

            if extS == "csv":

                with open(tfileS, "r") as csvfile:  # read csv file

                    readL = list(csv.reader(csvfile))

            elif extS == "xlsx":

                tDF1 = pd.read_excel(tfileS, header=None)

                readL = tDF1.values.tolist()

            else:

                return

            incl_colL = list(range(len(readL[1])))

            widthI = self.setcmdD["cwidthI"]

            alignS = self.setcmdD["calignS"]

            saS = alignD[alignS]

            if iL[2].strip():

                widthL = iL[2].split(",")  # new max col width

                widthI = int(widthL[0].strip())

                alignS = widthL[1].strip()

                self.setcmdD.update({"cwidthI": widthI})

                self.setcmdD.update({"calignS": alignS})

                saS = alignD[alignS]  # new align

            totalL = [""] * len(incl_colL)

            if iL[3].strip():  # columns

                if iL[3].strip() == "[:]":

                    totalL = [""] * len(incl_colL)

                else:

                    incl_colL = eval(iL[3].strip())

                    totalL = [""] * len(incl_colL)

            ttitleS = readL[0][0].strip() + " [t]_"

            utgS = self._tags(ttitleS, itagL)

            self.restS += utgS.rstrip() + "\n\n"

            for row in readL[1:]:

                contentL.append([row[i] for i in incl_colL])

            sys.stdout.flush()

            old_stdout = sys.stdout

            output = StringIO()

            output.write(

                tabulate(

                    contentL,

                    tablefmt="latex",

                    headers="firstrow",

                    numalign="decimal",

                    stralign=saS,

                )

            )

            rstS = output.getvalue()

            sys.stdout = old_stdout

        

            # print(rstS)

            cS = 0

            self.restS += ".. raw:: latex" + "\n\n"

            for i in rstS.split("\n"):

                counter = i.count("&")

                if counter > 0:

                    cS = "{" + alignS * (counter + 1) + "}"

                    continue

            # self.restS += "  \\vspace{-.1in}"

            self.restS += "  \\begin{tabulary}{1.0\\textwidth}" + cS + "\n"

            inrstS = ""

            for i in rstS.split("\n"):

                inrstS += "  " + i + "\n"

            self.restS += inrstS

            self.restS += "  \\end{tabulary}\n"

            self.restS += "  \\vspace{.15in}\n"

        

        

        def image_rst(self, iL: list):

            """insert one or two images from file

        

            Args:

                il (list): image parameters

            """

            rstS = ""

            fileS = iL[1].split(",")

            file1S = fileS[0].strip()

            fileS = iL[1].split(",")

            file1S = fileS[0].strip()

            img1S = str(Path(self.folderD["dpathcur"] / file1S).as_posix())

            scaleF = iL[2].split(",")

            scale1S = str(int(scaleF[0])) + "%"

            self.setcmdD.update({"scale1F": scale1S})

            if "," in iL[1]:  # two images

                scale2S = str(int(scaleF[1])) + "%"

                self.setcmdD.update({"scale2F": scale2S})

                file2S = fileS[1].strip()

                img2S = str(Path(self.folderD["dpathcur"] / file2S).as_posix())

                pic1S = "|pic" + str(self.setsectD["counter"] + 1) + "|"

                pic2S = "|pic" + str(self.setsectD["counter"] + 2) + "|"

                self.setsectD["counter"] = self.setsectD["counter"] + 3

                rstS += (

                    pic1S

                    + "  ____  "

                    + pic2S

                    + "\n\n"

                    + ".. "

                    + pic1S

                    + " image:: "

                    + img1S

                    + "\n"

                    + "   :width: "

                    + scale1S

                    + "\n\n"

                    + ".. "

                    + pic2S

                    + " image:: "

                    + img2S

                    + "\n"

                    + "   :width: "

                    + scale2S

                    + "\n"

                )

            else:  # one image

                rstS += (

                    ".. image:: "

                    + img1S

                    + "\n"

                    + "   :width: "

                    + scale1S

                    + "\n"

                    + "   :align: left \n"

                )

        

            self.restS += rstS + "\n"

            time.sleep(1)

        

        

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

            """skip info command for md calcs

        

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

## Functions

    
### attach

```python3
def attach(
    self,
    rsL
)
```

    

??? example "View Source"
        def attach(self, rsL):

            b = 5

    
### image_rst

```python3
def image_rst(
    self,
    iL: list
)
```

    
insert one or two images from file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| il | list | image parameters | None |

??? example "View Source"
        def image_rst(self, iL: list):

            """insert one or two images from file

        

            Args:

                il (list): image parameters

            """

            rstS = ""

            fileS = iL[1].split(",")

            file1S = fileS[0].strip()

            fileS = iL[1].split(",")

            file1S = fileS[0].strip()

            img1S = str(Path(self.folderD["dpathcur"] / file1S).as_posix())

            scaleF = iL[2].split(",")

            scale1S = str(int(scaleF[0])) + "%"

            self.setcmdD.update({"scale1F": scale1S})

            if "," in iL[1]:  # two images

                scale2S = str(int(scaleF[1])) + "%"

                self.setcmdD.update({"scale2F": scale2S})

                file2S = fileS[1].strip()

                img2S = str(Path(self.folderD["dpathcur"] / file2S).as_posix())

                pic1S = "|pic" + str(self.setsectD["counter"] + 1) + "|"

                pic2S = "|pic" + str(self.setsectD["counter"] + 2) + "|"

                self.setsectD["counter"] = self.setsectD["counter"] + 3

                rstS += (

                    pic1S

                    + "  ____  "

                    + pic2S

                    + "\n\n"

                    + ".. "

                    + pic1S

                    + " image:: "

                    + img1S

                    + "\n"

                    + "   :width: "

                    + scale1S

                    + "\n\n"

                    + ".. "

                    + pic2S

                    + " image:: "

                    + img2S

                    + "\n"

                    + "   :width: "

                    + scale2S

                    + "\n"

                )

            else:  # one image

                rstS += (

                    ".. image:: "

                    + img1S

                    + "\n"

                    + "   :width: "

                    + scale1S

                    + "\n"

                    + "   :align: left \n"

                )

        

            self.restS += rstS + "\n"

            time.sleep(1)

    
### image_md

```python3
def image_md(
    self,
    iL: list
)
```

    
insert one or two images from file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| iL | list | image parameters | None |

??? example "View Source"
        def image_md(self, iL: list):

            """insert one or two images from file

        

            Args:

                iL (list): image parameters

            """

            mdS = ""

            if "," in iL[1]:  # two images

                scaleF = iL[2].split(",")

                scale1F = float(scaleF[0])

                scale2F = float(scaleF[1])

                self.setcmdD.update({"scale1F": scale1F})

                self.setcmdD.update({"scale2F": scale2F})

                fileS = iL[1].split(",")

                file1S = fileS[0].strip()

                file2S = fileS[1].strip()

                docpS = "d" + self.setsectD["cnumS"]

                img1S = str(Path(self.folderD["dpathcur"] / file1S))

                img2S = str(Path(self.folderD["dpathcur"] / file2S))

                # pshrt1S = str(Path(*Path(img1S).parts[-4:]))

                # pshrt2S = str(Path(*Path(img2S).parts[-4:]))

                for fS in [img1S, img2S]:

                    mdS += "Figure path: " + fS + "\n"

                    try:

                        _display(_Image(fS))

                    except:

                        pass

                print(mdS)

                self.calcS += mdS + "\n"

            else:  # one image

                scale1F = float(iL[2])

                self.setcmdD.update({"scale1F": scale1F})

                fileS = iL[1].split(",")

                file1S = fileS[0].strip()

                docpS = "d" + self.setsectD["cnumS"]

                img1S = str(Path(self.folderD["dpathcur"] / file1S))

                mdS += "Figure path: " + img1S + "\n"

                try:

                    _display(_Image(img1S))

                except:

                    pass

                print(mdS)

                self.calcS += mdS + "\n"

    
### latex_md

```python3
def latex_md(
    self,
    iL: list
)
```

    
insert latex text from file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| iL | list | text command list | None |

??? example "View Source"
        def latex_md(self, iL: list):

            """insert latex text from file

        

            Args:

                iL (list): text command list

            """

        

            calP = "c" + self.setsectD["cnumS"]

            txapath = Path(self.folderD["dpath0"] / iL[1].strip())

            with open(txapath, "r") as txtf1:

                uL = txtf1.readlines()

            if iL[2].strip() == "indent":

                txtS = "".join(uL)

                widthI = self.setcmdD["cwidth"]

                inS = " " * 4

                uL = textwrap.wrap(txtS, width=widthI)

                uL = [inS + S1 + "\n" for S1 in uL]

                uS = "".join(uL)

            elif iL[2].strip() == "literal":

                txtS = "  ".join(uL)

                uS = "\n" + txtS

            else:

                txtS = "".join(uL)

                uS = "\n" + txtS

        

            self.calcS += uS + "\n"

        

            print(uS)

            self.calcS += uS + "\n"

    
### project

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

    
### report

```python3
def report(
    self,
    rL
)
```

    
skip info command for md calcs

Command is executed only for docs in order to
separate protected information for shareable calcs.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| rL | list | parameter list | None |

??? example "View Source"
        def report(self, rL):

            """skip info command for md calcs

        

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

    
### rvcmds

```python3
def rvcmds(
    typeS: str
)
```

    
_summary_

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| methodS | str | _description_ | None |

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
        def rvcmds(typeS: str):

            """_summary_

        

            :param str methodS: _description_

            :return _type_: _description_

            """

            cmdL = [

                "project",

                "report",

                "github",

                "append",

                "table",

                "text",

                "image1",

                "image2",

                "values",

                "list",

                "functions"

            ]

        

            cmdsetD = {

                "R": [0, 1, 2, 3, 4, 5],

                "I": [4, 5, 6, 7],

                "V": [4, 5, 6, 7, 8, 9, 10, 11],

                "T": [4, 5, 6, 7]

            }

        

            return [cmdL[i] for i in cmdsetD[typeS]]

    
### table_rst

```python3
def table_rst(
    self,
    iL: list
)
```

    
insert table from csv or xlsx file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| ipl | list | parameter list | None |

??? example "View Source"
        def table_rst(self, iL: list):

            """insert table from csv or xlsx file

        

            Args:

                ipl (list): parameter list

            """

            alignD = {"S": "", "D": "decimal",

                      "C": "center", "R": "right", "L": "left"}

        

            if len(iL) < 4:

                iL += [""] * (4 - len(iL))  # pad parameters

            mdS = ""

            contentL = []

            sumL = []

            fileS = iL[1].strip()

            calpS = self.setsectD["fnumS"]

            tfileS = Path(self.folderD["cpathcur"] / fileS)

            extS = fileS.split(".")[1]

            if extS == "csv":

                with open(tfileS, "r") as csvfile:  # read csv file

                    readL = list(csv.reader(csvfile))

            elif extS == "xlsx":

                tDF1 = pd.read_excel(tfileS, header=None)

                readL = tDF1.values.tolist()

            else:

                return

            incl_colL = list(range(len(readL[1])))

            widthI = self.setcmdD["cwidthI"]

            alignS = self.setcmdD["calignS"]

            saS = alignD[alignS]

            if iL[2].strip():

                widthL = iL[2].split(",")  # new max col width

                widthI = int(widthL[0].strip())

                alignS = widthL[1].strip()

                self.setcmdD.update({"cwidthI": widthI})

                self.setcmdD.update({"calignS": alignS})

                saS = alignD[alignS]  # new align

            totalL = [""] * len(incl_colL)

            if iL[3].strip():  # columns

                if iL[3].strip() == "[:]":

                    totalL = [""] * len(incl_colL)

                else:

                    incl_colL = eval(iL[3].strip())

                    totalL = [""] * len(incl_colL)

            ttitleS = readL[0][0].strip() + " [t]_"

            utgS = self._tags(ttitleS, itagL)

            self.restS += utgS.rstrip() + "\n\n"

            for row in readL[1:]:

                contentL.append([row[i] for i in incl_colL])

            sys.stdout.flush()

            old_stdout = sys.stdout

            output = StringIO()

            output.write(

                tabulate(

                    contentL,

                    tablefmt="latex",

                    headers="firstrow",

                    numalign="decimal",

                    stralign=saS,

                )

            )

            rstS = output.getvalue()

            sys.stdout = old_stdout

        

            # print(rstS)

            cS = 0

            self.restS += ".. raw:: latex" + "\n\n"

            for i in rstS.split("\n"):

                counter = i.count("&")

                if counter > 0:

                    cS = "{" + alignS * (counter + 1) + "}"

                    continue

            # self.restS += "  \\vspace{-.1in}"

            self.restS += "  \\begin{tabulary}{1.0\\textwidth}" + cS + "\n"

            inrstS = ""

            for i in rstS.split("\n"):

                inrstS += "  " + i + "\n"

            self.restS += inrstS

            self.restS += "  \\end{tabulary}\n"

            self.restS += "  \\vspace{.15in}\n"

    
### table_md

```python3
def table_md(
    self,
    iL: list
)
```

    
insert table from csv or xlsx file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| ipl | list | parameter list | None |

??? example "View Source"
        def table_md(self, iL: list):

            """insert table from csv or xlsx file

        

            Args:

                ipl (list): parameter list

            """

            alignD = {"S": "", "D": "decimal",

                      "C": "center", "R": "right", "L": "left"}

        

            if len(iL) < 4:

                iL += [""] * (4 - len(iL))  # pad parameters

            mdS = ""

            contentL = []

            sumL = []

            fileS = iL[1].strip()

            calpS = self.setsectD["fnumS"]

            tfileS = Path(self.folderD["cpathcur"] / fileS)

            extS = fileS.split(".")[1]

            if extS == "csv":

                with open(tfileS, "r") as csvfile:  # read csv file

                    readL = list(csv.reader(csvfile))

            elif extS == "xlsx":

                pDF1 = pd.read_excel(tfileS, header=None)

                readL = pDF1.values.tolist()

            else:

                return

            incl_colL = list(range(len(readL[1])))

            widthI = self.setcmdD["cwidthI"]

            alignS = self.setcmdD["calignS"]

            saS = alignD[alignS]

            if iL[2].strip():

                widthL = iL[2].split(",")  # new max col width

                widthI = int(widthL[0].strip())

                alignS = widthL[1].strip()

                saS = alignD[alignS]  # new align

                self.setcmdD.update({"cwidthI": widthI})

                self.setcmdD.update({"calignS": alignS})

            totalL = [""] * len(incl_colL)

            if iL[3].strip():  # columns

                if iL[3].strip() == "[:]":

                    totalL = [""] * len(incl_colL)

                else:

                    incl_colL = eval(iL[3].strip())

                    totalL = [""] * len(incl_colL)

            ttitleS = readL[0][0].strip() + " [t]_"

            utgS = self._tags(ttitleS, itagL)

            print(utgS.rstrip() + "\n")

            self.calcS += utgS.rstrip() + "\n\n"

            for row in readL[1:]:

                contentL.append([row[i] for i in incl_colL])

            wcontentL = []

            for rowL in contentL:  # wrap columns

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

            mdS = output.getvalue()

            sys.stdout = old_stdout

        

            print(str(tfileS))

            print(mdS)

            self.calcS += str(tfileS) + "\n"

            self.calcS += mdS + "\n"

    
### text_rst

```python3
def text_rst(
    self,
    iL: list
)
```

    
insert text from file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| iL | list | text command list | None |

??? example "View Source"
        def text_rst(self, iL: list):

            """insert text from file

        

            Args:

                iL (list): text command list

            """

            txapath = Path(self.folderD["cpathcur"] / iL[1].strip())

            with open(txapath, "r", encoding="md-8") as txtf1:

                rstL = txtf1.readlines()

            if iL[2].strip() == "indent":

                txtS = "".join(rstL)

                widthI = self.setcmdD["cwidth"]

                inS = " " * 4

                rstL = textwrap.wrap(txtS, width=widthI)

                rstL = [inS + S1 + "\n" for S1 in rstL]

                rstS = "".join(rstL)

            elif iL[2].strip() == "literal":

                txtS = " ".join(rstL)

                rstS = "\n\n::\n\n" + txtS + "\n\n"

            elif iL[2].strip() == "literalindent":

                txtS = "\n\n::\n\n"

                for iS in iL:

                    txtS += "   " + iS

                rstS = txtS + "\n\n"

            elif iL[2].strip() == "html":

                txtS = ""

                flg = 0

                for iS in rstL:

                    if "src=" in iS:

                        flg = 1

                        continue

                    if flg == 1 and '"' in iS:

                        flg = 0

                        continue

                    if flg == 1:

                        continue

                    txtS += iS

                txtS = htm.html2text(txtS)

                txtS = "   " + txtS.replace("\n    \n", "")

                rstL = txtS.split("\n")

                for num, iS in enumerate(rstL):

                    rstL[num] = "   " + iS

                rstS = "\n".join(rstL[1:])

                rstS = "\n\n::\n\n" + rstS + "\n\n"

            else:

                txtS = "".join(rstL)

                rstS = "\n" + txtS

        

            self.restS += rstS + "\n"

    
### text_md

```python3
def text_md(
    self,
    iL: list
)
```

    
insert text from file

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| iL | list | text command list
|| text | (file.txt) | literal; indent; html | None |

??? example "View Source"
        def text_md(self, iL: list):

            """insert text from file

        

            Args:

                iL (list): text command list

        

            || text | (file.txt) | literal; indent; html

        

            """

        

            txtP = Path(self.folderD["cpathcur"] / iL[1].strip())

            with open(txtP, "r", encoding="md-8") as txtf1:

                uL = txtf1.readlines()

            if iL[2].strip() == "indent":

                txtS = "".join(uL)

                widthI = self.setcmdD["cwidth"]

                inS = " " * 4

                uL = textwrap.wrap(txtS, width=widthI)

                uL = [inS + S1 + "\n" for S1 in uL]

                uS = "".join(uL)

            elif iL[2].strip() == "literal":

                txtS = "  ".join(uL)

                uS = "\n" + txtS

            elif iL[2].strip() == "literalindent":

                txtS = "\n\n::\n\n"

                for iS in uL:

                    txtS += "   " + iS

                uS = txtS + "\n\n"

            elif iL[2].strip() == "html":

                txtS = ""

                flg = 0

                for iS in uL:

                    if "src=" in iS:

                        flg = 1

                        continue

                    if flg == 1 and '"' in iS:

                        flg = 0

                        continue

                    if flg == 1:

                        continue

                    txtS += iS

                txtS = htm.html2text(txtS)

                uS = txtS.replace("\n    \n", "")

            else:

                txtS = "".join(uL)

                uS = "\n" + txtS

        

            # print(str(txtP))

            # self.calcS += str(txtP) + "\n"

            print(uS)

            self.calcS += uS + "\n"