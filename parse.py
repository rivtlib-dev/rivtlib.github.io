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
from IPython.display import display as _display
from IPython.display import Image as _Image
try:
    from PIL import Image as PImage
    from PIL import ImageOps as PImageOps
except:
    pass
from rivt import cmdrst
from rivt import cmdutf
from rivt import tagrst
from rivt import tagutf
from rivt.units import *
# tabulate.PRESERVE_WHITESPACE = True


class RivtParse:
    """process rivt-string"""

    def __init__(self, folderD, incrD,  outputS, methS):
        """process rivt-string to UTF8 calc

            :param dict folderD: folder paths
            :param dict incrD: numbers that increment
            :param dict outputS: output type
            :param dict outputS: output type
        """

        self.folderD = folderD  # folder paths
        self.incrD = incrD      # incrementing formats
        self.outputS = outputS  # output type
        self.outputL = ["pdf", "html", "both"]  # reST formats
        self.errlogP = folderD["errlogP"]

        # valid commands and tags
        if methS == "R":
            self.cmdL = ["project", "github", "append", "text"]
            self.tagL = ["[literal]]"]
            self.blockL = ["[readme]]"]
        elif methS == "I":
            self.cmdL = ["table", "text", "image1", "image2"]
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        elif methS == "V":
            self.cmdL = ["table", "text", "image1", "image2",
                         "values", "list", "functions"]
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]",
                         "=", ":="]
        elif methS == "T":
            self.cmdL = ["table", "text", "image1", "image2"]
            self.tagL = ["page]", "link]", "lit]", "foot]", "url]", "lnk]",
                         "b]", "c]", "e]", "t]", "f]", "x]", "r]", "s]", "#]", "-]",
                         "[c]]", "[e]]", "[l]]", "[o]]", "[r]]", "[x]]", "[m]]"]
        else:
            pass

        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        # print(f"{modnameS=}")
        logconsole = logging.StreamHandler()
        logconsole.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(levelname)-8s" + modnameS + "   %(message)s")
        logconsole.setFormatter(formatter)
        logging.getLogger("").addHandler(logconsole)
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
        uS = """"""
        blockB = False
        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        blockassignL = []
        blockassignB = False
        for uS in strL:
            # print(f"{blockB=}")
            # print(f"{uS=}")
            if uS[0:2] == "##":
                continue                            # remove review comments
            uS = uS[4:]                             # remove indent
            if blockB:                              # accumulate block
                lineS += uS
            if blockB and uS.strip() == "[end]]":
                rvtS = tagutf.TagsUTF(lineS, tagS, strL)
                utfS += rvtS + "\n"
                blockB = False
            if blockassignB and len(uS.strip()) < 2:    # write assign block
                blockassignB = False
                utfS += self.vtable(blockassignL, hdrL, "rst", alignL)+"\n\n"
                if self.incrD["saveP"] != None:
                    valP = Path(self.folderD["data"] / self.incrD["saveP"])
                    with open(valP, "w", newline="") as f:
                        writecsv = csv.writer(f)
                        writecsv.writerow(hdrL)
                        writecsv.writerows(blockassignL)
                continue
            if uS[0:2] == "||":                   # process commands
                usL = uS[2:].split("|")
                parL = usL[1:]
                cmdS = usL[0].strip()
                if cmdS in self.cmdL:
                    rvtM = cmdutf.CmdUTF(parL, self.incrD, self.folderD)
                    rvtS = rvtM.cmd_parse(cmdS)
                    utfS += rvtS + "\n"
                    # if self.outputS in self.outputL:
                    #     rvtM = cmdrst.CmdRST(parL, self.incrD, self.folderD)
                    #     rvtS = rvtM.cmd_parse(cmdS)
                    #     rstS += rvtS + "\n"
                continue
            if "_[" in uS:                        # process tags
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":
                    blockB = True
                if tagS in self.tagL:
                    rvtM = tagutf.TagsUTF(lineS, self.folderD, self.incrD)
                    rvtS = rvtM.tag_parse(tagS)
                    utfS += rvtS + "\n"
                    # if self.outputS in self.outputL:
                    #     rvtM = tagrst.TagsRST(lineS, self.folderD, self.incrD)
                    #     rvtS = rvtM.tag_parse(tagS)
                    #     rstS += rvtS + "\n"
                continue
            if "=" in uS:                   # process assign and result tags
                # print(f"{uS=}")
                if "=" in self.tagL:
                    usL = uS.split("|")
                    lineS = usL[0]
                    self.incrD["unitS"] = usL[1].strip()
                    self.incrD["descS"] = usL[2].strip()
                    if ":=" in uS:
                        rvtM = tagutf.TagsUTF(lineS, self.folderD, self.incrD)
                        blockassignL.append(rvtM.tag_parse(":="))
                        blockassignB = True
                        # if self.outputS in self.outputL:
                        #     rvtM = tagrst.TagsRST(
                        #         lineS, self.folderD, self.incrD)
                        #     rvtS = rvtM.tag_parse(":=")
                        #     rstS += rvtS + "\n"
                        continue
                    else:
                        rvtM = tagutf.TagsUTF(lineS, self.folderD, self.incrD)
                        [valL], hdrL, etypeS, alignL = rvtM.tag_parse("=")
                        rvtS = self.etable([valL], hdrL, etypeS, alignL)
                        utfS += rvtS + "\n"
                        # if self.outputS in self.outputL:
                        #     rvtM = tagrst.TagsRST(
                        #         lineS, self.folderD, self.incrD)
                        #     rvtS = rvtM.tag_parse(tagS)
                        #     rstS += rvtS + "\n"
                        pass
                    continue
            else:
                utfS += uS + "\n"

        return utfS, rstS, self.folderD, self.incrD

    def etable(self, tblL, hdrL, tblfmt, alignL):
        """write equation table"""

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

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdrL,
                showindex=False, colalign=alignL
            )
        )
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return utfS

    def vtable(self, tblL, hdrL, tblfmt, alignL):
        """write value table"""

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

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdrL,
                showindex=False, colalign=alignL
            )
        )
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return utfS

        #self.calcS += utfS + "\n"

        #self.calcS += utfS + "\n"
