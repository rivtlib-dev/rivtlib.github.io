from rivt.units import *
import csv
import sys
import re
import logging
import warnings
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import html2text as htm
from numpy import *
from IPython.display import display as _display
from IPython.display import Image as _Image
from io import StringIO
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass
from rivt import cmdutf
from rivt import cmdrst
from rivt import tagutf
from rivt import tagrst

# tabulate.PRESERVE_WHITESPACE = True


class RivtParse:
    """process rivt-string"""

    def __init__(self, folderD, incrD, methS, localD):
        """process rivt-string to UTF8 calc

            :param dict folderD: folder paths
            :param dict incrD: numbers that increment
            :param dict outputS: output type
            :param dict outputS: output type
        """

        self.localD = localD
        self.folderD = folderD  # folder paths
        self.incrD = incrD      # incrementing formats
        self.errlogP = folderD["errlogP"]
        self.methS = methS

        # valid commands and tags
        if methS == "R":
            self.cmdL = ["project", "github", "append", "pages"]
            self.tagL = ["[literal]]"]
            self.blockL = ["[readme]]"]
        elif methS == "I":
            self.cmdL = ["table", "text", "image", "image2"]
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        elif methS == "V":
            self.cmdL = ["table", "text", "image", "image2",
                         "values", "list", "functions"]
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]",
                         "=", ":="]
        elif methS == "T":
            self.cmdL = ["table", "text", "image", "image2"]
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        elif methS == "itag":
            self.cmdL = []
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
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
        """parse insert string

            :param list strL: split rivt string
            :return utfS: utf formatted string
            :return rstS: reST formatted string
            :return incrD: increment references
            :return folderD: folder paths
            :rtype utfS: string
            :rtype rstS: string
            :rtype folderD: dictionary
            :rtype incrD: dictionary
        """

        utfS = """"""
        rstS = """"""
        rvtuS = rvtrS = ""
        uS = """"""
        blockB = False
        ttypeS = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignvL = ["left", "right", "right", "left"]
        hdreL = ["variable", "value", "[value]", "description [eq. number]"]
        aligneL = ["left", "right", "right", "left"]
        blockevalL = []     # current value table
        blockevalB = False  # stop accumulation of values
        vtableL = []        # value table export
        eqL = []            # equation result table
        for uS in strL:
            # print(f"{blockassignB=}")
            # print(f"{uS=}")
            if uS[0:2] == "##":                        # remove comments
                continue
            uS = uS[4:]                                # remove indent
            if blockB:                                 # accumulate block
                lineS += uS
            if blockB and uS.strip() == "[end]]":
                rvtS = tagutf.TagsUTF(lineS, tagS, strL)
                utfS += rvtS + "\n"
                blockB = False
            if blockevalB and len(uS.strip()) < 2:     # compose value table
                vtableL += blockevalL
                if tfS == "declare":
                    utfS += self.vtable(blockevalL, hdrvL,
                                        ttypeS, alignvL) + "\n\n"
                if tfS == "assign":
                    resultS = self.etable(blockevalL, hdreL,
                                          ttypeS, aligneL) + "\n\n"
                    utfS += resultS
                blockevalL = []
                blockevalB = False
            elif uS[0:2] == "||":                         # command
                usL = uS[2:].split("|")
                parL = usL[1:]
                cmdS = usL[0].strip()
                if cmdS in self.cmdL:
                    rvtM = cmdutf.CmdUTF(parL, self.incrD, self.folderD,
                                         self.localD)
                    utS = rvtM.cmd_parse(cmdS)
                    if cmdS == "pages":                 # header page number
                        rvtuS = self.incrD["headuS"]
                        rvtrS = self.incrD["headrS"]
                        pagenoS = str(self.incrD["pageI"])
                        if "page" in utS:
                            rvtuS = rvtuS.replace(
                                "page", "page " + pagenoS)
                            rvtrS = rvtrS.replace(
                                "page", "page " + pagenoS)
                        self.incrD["pageI"] = int(pagenoS) + 1
                        continue
                    rvtM = cmdrst.CmdRST(parL, self.incrD, self.folderD,
                                         self.localD)   # rst *********
                    retS = rvtM.cmd_parse(cmdS)
                    rstS += retS
                utfS += utS
            elif "_[" in uS:                              # end of line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                        # block tag
                    blockB = True
                if tagS == "*]":
                    lineS = usL                           # inline tag
                if tagS in self.tagL:
                    rvtM = tagutf.TagsUTF(lineS, self.incrD, self.folderD,
                                          self.localD)
                    utS = rvtM.tag_parse(tagS)
                    utfS += utS + "\n"                 # rst ********
                    rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                          self.localD)
                    reS = rvtM.tag_parse(tagS)
                    rstS += reS + "\n"
            elif "=" in uS:                               # assign tag
                # print(f"{uS=}")
                if "=" in self.tagL:
                    usL = uS.split("|")
                    lineS = usL[0]
                    self.incrD["unitS"] = usL[1].strip()
                    self.incrD["descS"] = usL[2].strip()
                    rvtM = tagutf.TagsUTF(lineS, self.incrD, self.folderD,
                                          self.localD)
                    if ":=" in uS:
                        tfS = "declare"
                        blockevalL.append(rvtM.tag_parse(":="))
                        # rst ********
                        rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                              self.localD)
                        rvtS = rvtM.tag_parse(":=")
                        blockevalL.append(rvtM.tag_parse(":="))
                        blockevalB = True
                        continue
                    else:
                        tfS = "assign"
                        eqL = rvtM.tag_parse("=")
                        blockevalL.append(eqL[0])
                        blockevalB = True
                        utfS += eqL[1]
                        print(eqL[1])
                        # rst ********
                        rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                              self.localD)
                        rvtS = rvtM.tag_parse(tagS)
                        rstS += rvtS + "\n"
            else:                                           # delay R str title
                if self.methS != "R":
                    print(uS)
                utfS += uS + "\n"
                rstS += uS + "\n"

        if self.incrD["saveP"] != None:                     # write saved values
            valP = Path(self.folderD["dataP"] / self.incrD["saveP"])
            with open(valP, "w", newline="") as f:
                writecsv = csv.writer(f)
                writecsv.writerow(hdrvL)
                writecsv.writerows(vtableL)

        return (utfS, rvtuS), (rstS, rvtrS),  self.incrD, self.folderD, self.localD

    def etable(self, tblL, hdreL, tblfmt, aligneL):
        """write equation table"""

        locals().update(self.localD)

        valL = []
        for vaL in tblL:
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            descripS = vaL[4].strip()
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

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdreL,
                showindex=False, colalign=aligneL
            )
        )
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        locals().update(self.localD)
        self.localD.update(locals())

        print(utfS+"\n")
        return utfS

    def vtable(self, tblL, hdrvL, tblfmt, alignvL):
        """write value table"""

        locals().update(self.localD)

        valL = []
        for vaL in tblL:
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            descripS = vaL[4].strip()
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

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdrvL,
                showindex=False, colalign=alignvL
            )
        )
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        locals().update(self.localD)
        self.localD.update(locals())

        print(utfS+"\n")
        return utfS
