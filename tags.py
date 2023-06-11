import csv
import logging
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings
from io import StringIO
from pathlib import Path


class Tags:
    """convert rivt tags to md

    """

    def __init__(self, lineS, incrD, folderD,  localD):
        """convert rivt tags to md or reST

            ============================ =======================================
            tags                                   description 
            ============================ =======================================

            I,V line format:        
            ---- can be combined 
            text _[b]                       bold 
            text _[c]                       center
            text _[i]                       italic
            text _[r]                       right justify
            ---------------------
            text _[u]                       underline   
            text _[l]                       LaTeX math
            text _[s]                       sympy math
            text _[e]                       equation label and autonumber
            text _[f]                       figure caption and autonumber
            text _[t]                       table title and autonumber
            text _[#]                       footnote and autonumber
            text _[d]                       footnote description 
            _[line]                         horizontal line
            _[page]                         new page
            _[address, label]               url, internal reference
            I,V  block format:          
            ---- can be combined 
            _[[b]]                          bold
            _[[c]]                          center
            _[[i]]                          italic
            _[[p]]                          plain  
            --------------------
            _[[l]]                          LaTeX
            _[[h]]                          HTML 
            _[[q]]                          quit block

        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.lineS = lineS
        self.widthI = incrD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

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
