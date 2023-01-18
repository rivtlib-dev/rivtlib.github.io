# Module rv_r

Class R2utf and R2rst

None

??? example "View Source"
        #!python

        """Class R2utf and R2rst"""

        

        import os

        import sys

        import csv

        import textwrap

        import subprocess

        import tempfile

        import re

        import io

        import logging

        import html2text as htm

        from io import StringIO

        from tabulate import tabulate

        from pathlib import Path

        import rivt.commands as cmdM

        import rivt.tags as tagM

        import rivt.config

        

        logging.getLogger("numexpr").setLevel(logging.WARNING)

        # tabulate.PRESERVE_WHITESPACE = True

        

        

        class R2utf:

            """convert repo-string to UTF8 calc"""

        

            def __init__(self, strL: list, folderD: dict, tagvalD: dict):

                """_summary_

        

                :param list strL: _description_

                :param dict folderD: _description_

                :param dict tagD: _description_

                """

        

                self.utfS = """"""  # utf calc string

                self.strL = strL

                self.folderD = folderD

                self.tagD = tagD

                self.valL = []  # value list

        

            def parseRutf(self, strL: list, cmdD: dict, cmdL: list, methL: list):

                """_summary_

        

                :param list strL: _description_

                :param dict cmdD: _description_

                :param list cmdL: _description_

                :param list methL: _description_

                :return _type_: _description_

                """

                # get valid tags and commands

                tagL = tagM.rvtags(typeS)

        

                # get valid commands

                for uS in self.strL:

                    if uS[0:2] == "##":

                        continue  # remove review comment

                    uS = uS[4:]  # remove indent

                    if len(uS) == 0:

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

        

                    self.utfS += uS.rstrip() + "\n"

        

                return self.calcS, self.setsectD

        

            def utf1():

                pass

        

        

        class R2rst:

            """convert rivt-strings to reST strings

        

            Args:

            exportS (str): stores values that are written to file

            strL (list): calc rivt-strings

            folderD (dict): folder paths

            tagD (dict): tag dictionary

        

        

            """

        

            def __init__(self, strL: list, folderD: dict, tagD: dict):

        

                self.restS = """"""  # restructured text string

                self.strL = strL  # rivt-string list

                self.folderD = folderD

                self.tagD = tagD

        

            def parseRrst(self, typeS: str, cmdL: list, methL: list, tagL: list):

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

                            self.rivtvalD.update(locals())

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

        

            def rst1():

                pass

## Classes

### R2rst

```python3
class R2rst(
    strL: list,
    folderD: dict,
    tagD: dict
)
```

#### Methods

    
#### parseRrst

```python3
def parseRrst(
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
            def parseRrst(self, typeS: str, cmdL: list, methL: list, tagL: list):

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

                            self.rivtvalD.update(locals())

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

    
#### rst1

```python3
def rst1(
    
)
```

    

??? example "View Source"
            def rst1():

                pass

### R2utf

```python3
class R2utf(
    strL: list,
    folderD: dict,
    tagvalD: dict
)
```

#### Methods

    
#### parseRutf

```python3
def parseRutf(
    self,
    strL: list,
    cmdD: dict,
    cmdL: list,
    methL: list
)
```

    
_summary_

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| strL | list | _description_ | None |
| cmdD | dict | _description_ | None |
| cmdL | list | _description_ | None |
| methL | list | _description_ | None |

**Returns:**

| Type | Description |
|---|---|
| _type_ | _description_ |

??? example "View Source"
            def parseRutf(self, strL: list, cmdD: dict, cmdL: list, methL: list):

                """_summary_

        

                :param list strL: _description_

                :param dict cmdD: _description_

                :param list cmdL: _description_

                :param list methL: _description_

                :return _type_: _description_

                """

                # get valid tags and commands

                tagL = tagM.rvtags(typeS)

        

                # get valid commands

                for uS in self.strL:

                    if uS[0:2] == "##":

                        continue  # remove review comment

                    uS = uS[4:]  # remove indent

                    if len(uS) == 0:

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

        

                    self.utfS += uS.rstrip() + "\n"

        

                return self.calcS, self.setsectD

    
#### utf1

```python3
def utf1(
    
)
```

    

??? example "View Source"
            def utf1():

                pass