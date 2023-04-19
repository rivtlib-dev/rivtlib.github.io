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
    """process rivt-text"""

    def __init__(self, methS, folderD, incrD,  localD):
        """process rivt-text to UTF8 or reST string

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
            self.cmdL = ["append", "pages", "project"]

        elif methS == "I":
            self.cmdL = ["image", "table", "text", ]

        elif methS == "V":
            self.cmdL = ["image", "table", "values", "functions"]

        elif methS == "T":
            self.cmdL = ["image", "table"]

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
        hdrvL = ["variable", "value", "[value]", "description"]
        alignvL = ["left", "right", "right", "left"]
        hdraL = ["variable", "value", "[value]", "description [eq. number]"]
        alignaL = ["left", "right", "right", "left"]
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
                continue
            if blockB and uS.strip() == "[q]]":
                rvtS = tagutf.TagsUTF(lineS, tagS, strL)
                utfS += rvtS + "\n"
                rvtS = tagrst.TagsRST(lineS, tagS, strL)
                rstS += rvtS + "\n"
                blockB = False
            if blockevalB and len(uS.strip()) < 2:     # values table
                vtableL += blockevalL
                if tfS == "declare":
                    vS = self.dtable(blockevalL, hdrvL,
                                     "rst", alignvL) + "\n\n"
                    utfS += vS
                    rstS += vS
                if tfS == "assign":
                    resultS = self.atable(blockevalL, hdraL,
                                          "rst", alignaL) + "\n\n"
                    utfS += resultS
                    rstS += resultS
                blockevalL = []
                blockevalB = False
            elif uS[0:2] == "||":                      # command
                usL = uS[2:].split("|")
                parL = usL[1:]
                cmdS = usL[0].strip()
                if cmdS in self.cmdL:
                    rvtM = cmdutf.CmdUTF(parL, self.incrD, self.folderD,
                                         self.localD)  # utf cmd ******
                    utS = rvtM.cmd_parse(cmdS)
                    if cmdS == "pages":                 # header page
                        self.folderD["styleP"] == utS
                        rvtuS = self.incrD["headuS"]
                        pagenoS = str(self.incrD["pageI"])
                        rvtuS = rvtuS.replace("p##", pagenoS)
                        self.incrD["pageI"] = int(pagenoS) + 1
                        continue
                    utfS += utS
                    rvtM = cmdrst.CmdRST(parL, self.incrD, self.folderD,
                                         self.localD)  # rst cmd ******
                    reS = rvtM.cmd_parse(cmdS)
                    rstS += reS
            elif "_[" in uS:                          # end of line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                     # block tag
                    blockB = True
                rvtM = tagutf.TagsUTF(lineS, self.incrD, self.folderD,
                                      self.localD)     # utf tag ******
                utS = rvtM.tag_parse(tagS)
                utfS += utS + "\n"                     # rst tag ******
                rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                      self.localD)
                reS = rvtM.tag_parse(tagS)
                rstS += reS + "\n"
            elif "=" in uS:                             # assign tag
                # print(f"{uS=}")
                usL = uS.split("|")
                lineS = usL[0]
                self.incrD["unitS"] = usL[1].strip()
                self.incrD["descS"] = usL[2].strip()
                rvtM = tagutf.TagsUTF(lineS, self.incrD, self.folderD,
                                      self.localD)
                if ":=" in uS:
                    tfS = "declare"
                    blockevalL.append(rvtM.tag_parse(":="))
                    rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                          self.localD)
                    eqL = rvtM.tag_parse(":=")
                    blockevalB = True
                    continue
                else:
                    tfS = "assign"
                    eqL = rvtM.tag_parse("=")
                    utfS += eqL[1]
                    print(eqL[1])
                    blockevalL.append(eqL[0])

                    rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                          self.localD)
                    eqL = rvtM.tag_parse("=")
                    rstS += eqL[1]
                    blockevalB = True
                    continue
            else:                                 # delay R str title
                if self.methS != "R":
                    print(uS)
                utfS += uS + "\n"
                rstS += uS + "\n"

        if self.incrD["saveP"] != None:            # write saved values
            valP = Path(self.folderD["dataP"] / self.incrD["saveP"])
            with open(valP, "w", newline="") as f:
                writecsv = csv.writer(f)
                writecsv.writerow(hdrvL)
                writecsv.writerows(vtableL)

        return (utfS, rvtuS), (rstS, rvtrS),  self.incrD, self.folderD, self.localD

    def atable(self, tblL, hdreL, tblfmt, aligneL):
        """write assign values table"""

        locals().update(self.localD)

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
                showindex=False,  colalign=aligneL))
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.localD.update(locals())
        print("\n" + utfS+"\n")
        return utfS

    def dtable(self, tblL, hdrvL, tblfmt, alignvL):
        """write declare values table"""

        locals().update(self.localD)

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
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.localD.update(locals())

        print("\n" + utfS+"\n")
        return utfS


class RivtParseTag:
    """process rivt-text tags from external txt file"""

    def __init__(self, folderD, incrD,  localD):
        """process rivt-text tags called from text command

            :param dict folderD: folder paths
            :param dict incrD: numbers that increment
        """

        self.localD = localD
        self.folderD = folderD  # folder paths
        self.incrD = incrD      # incrementing formats
        self.errlogP = folderD["errlogP"]

        # valid commands and tags
        self.tagL = ["page]", "line]", "link]", "b]", "c]", "i]",  "r]",
                     "#]", "d]", "e]",  "f]", "m]", "s]", "t]",
                     "[b]]", "[c]]", "[i]]", "[p]]", "[s]]", "[l]]", "[h]]"]

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

    def utf_parse(self, strL):
        """parse insert string

            :param list strL: split rivt string
            :return utfS: utf formatted string
            :return incrD: increment references
            :return folderD: folder paths
            :rtype utfS: string
            :rtype folderD: dictionary
            :rtype incrD: dictionary
        """

        xutfS = """"""
        uS = """"""
        blockB = False
        for uS in strL:
            # print(f"{blockassignB=}")
            # print(f"{uS=}")
            if uS[0:2] == "##":                        # remove comments
                continue
            uS = uS[4:]                                # remove indent
            if blockB:                                 # accumulate block
                lineS += uS
                continue
            if blockB and uS.strip() == "[q]]":
                rvtS = tagutf.TagsUTF(lineS, tagS, strL)
                xutfS += rvtS + "\n"
                blockB = False
            elif "_[" in uS:                              # end of line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                        # block tag
                    blockB = True
                    continue
                if tagS in self.tagL:
                    rvtM = tagutf.TagsUTF(lineS, self.incrD, self.folderD,
                                          self.localD)
                    utS = rvtM.tag_parse(tagS)
                    xutfS += utS + "\n"                 # rst ********

        return xutfS,  self.incrD, self.folderD, self.localD

    def rst_parse(self, strL):
        """parse insert string

            :param list strL: split rivt string
            :return rstS: reST formatted string
            :return incrD: increment references
            :return folderD: folder paths
            :rtype rstS: string
            :rtype folderD: dictionary
            :rtype incrD: dictionary
        """

        xrstS = """"""
        uS = """"""
        blockB = False
        for uS in strL:
            # print(f"{blockassignB=}")
            # print(f"{uS=}")
            if uS[0:2] == "##":                        # remove comments
                continue
            uS = uS[4:]                                # remove indent
            if blockB:                                 # accumulate block
                lineS += uS
                continue
            if blockB and uS.strip() == "[q]]":
                rvtS = tagrst.TagsRST(lineS, tagS, strL)
                xrstS += rvtS + "\n"
                blockB = False
            elif "_[" in uS:                              # end of line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                        # block tag
                    blockB = True
                    continue
                if tagS in self.tagL:
                   # rst ********
                    rvtM = tagrst.TagsRST(lineS, self.incrD, self.folderD,
                                          self.localD)
                    reS = rvtM.tag_parse(tagS)
                    xrstS += reS + "\n"

        return xrstS,  self.incrD, self.folderD, self.localD
