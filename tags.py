#!python
"""Manages and processes rivt tags"""

import logging
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from tabulate import tabulate


def rvtags(typeS: str):

    tagL = [
        "_[new]",
        "_[line]",
        "_[link]",
        "_[lit]",
        "_[foot]",
        "_[r]",
        "_[c]",
        "_[e]",
        "_[t]",
        "_[f]",
        "_[x]",
        "_[s]"
        "_[#]",
        "_[-]",
        "_[url]",
        "_[lnk]",
        "_[[r]]",
        "_[[c]]",
        "_[[lit]]",
        "_[[tex]]",
        "_[[texm]]",
        "_[[end]]",
    ]

    tagvL = tagL.append("=")
    tagrL = ["_[[read]]", "_[[end]]"]

    tagD = {
        "R": tagrL,
        "I": tagL,
        "V": tagvL,
        "T": tagL,
    }

    return eval(str(tagD[typeS]))


def e_utf(self) -> tuple:
    """parse eval-string

    Returns:
        calcS (list): utf formatted calc-string (appended)
        setsectD (dict): section settings
        setcmdD (dict): command settings
    """

    ecmdL = ["text", "table", "image"]
    emethL = [self._itext, self._itable, self._iimage]
    etagL = [
        "[page]_",
        "[line]_",
        "[link]_",
        "[literal]_",
        "[foot]_",
        "[latex]_",
        "[s]_",
        "[x]_",
        "[r]_",
        "[c]_",
        "[e]_",
        "[t]_",
        "[f]_",
        "[#]_",
    ]

    self._parseUTF("insert", icmdL, imethL, itagL)

    return self.calcS, self.setsectD, self.setcmdD


def taglist(lineS: str) -> tuple:
    """check for tags

    Parameters:
    lineS: line from rivt file

    Returns:
    (str, bool): tag or


    """

    tagL = [
        "[page]_",
        "[line]_",
        "[link]_",
        "[foot]_",
        "[n]_",
        "[s]_",
        "[x]_",
        "[r]_",
        "[c]_",
        "[e]_",
        "[t]_",
        "[f]_",
        "[#]_",
        "[math]__",
        "[literal]__",
        "[latex]__",
        "[r]__",
        "[c]__",
    ]
    try:
        tag = list(set(tagL).intersection(lineS.split()))[0]
        return (tag, True)
    except:
        return (lineS, False)


def label(self, objnumI: int, tagD: dict, typeS: str) -> str:
    """labels for equations, tables and figures

    Args:
        objnumI (int): equation, table or figure numbers
        setsectD (dict): section dictionary
        typeS (str): label type

    Returns:
        str: formatted label
    """

    objfillS = str(objnumI).zfill(2)
    if type(typeS) == str:
        sfillS = str(self.tagD["snumS"]).strip().zfill(2)
        labelS = typeS + sfillS
    else:
        cnumSS = str(self.tagD["cnumS"])
        labelS = typeS + cnumSS + "." + objfillS

    return labelS


def tags(self, lineS: str, sectD: dict) -> tuple:
    """format line with tag
    Parameters:
        lineS (str): rivt-string line with tag
        sectD (dict): section dictionary

    Return:
        uS (str): utf string
    """
    swidthII = sectD["swidthI"] - 1
    lineS = lineS.rstrip()
    tag = _taglist(lineS)
    uS = ""

    if tag == "[#]_":  # auto increment footnote mark
        ftnumII = self.setsectD["ftqueL"][-1] + 1
        self.setsectD["ftqueL"].append(ftnumII)
        uS = tagS.replace("[x]_", "[" + str(ftnumII) + "]")
    elif tag == "[foot]_":  # footnote label
        tagS = tagS.strip("[foot]_").strip()
        uS = self.setsectD["ftqueL"].popleft() + tagS
    elif tag == "[page]_":  # new page
        uS = int(self.setsectD["swidthI"]) * "."
    elif tag == "[line]_":  # horizontal line
        uS = int(self.setsectD["swidthI"]) * "-"
    elif tag == "[link]_":  # url link
        tgS = tagS.strip("[link]_").strip()
        tgL = tgS.split("|")
        uS = tgL[0].strip() + " : " + tgL[1].strip()
    elif tag == "[literal]_":  # literal text
        uS = "\n"
    elif tag == "[latex]_":  # literal text
        uS = "\n"
    elif tag == "[r]_":  # right adjust text
        tagL = tagS.strip().split("[r]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    elif tag == "[c]_":  # center text
        tagL = tagS.strip().split("[c]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    elif tag == "[f]_":  # figure caption
        tagL = tagS.strip().split("[f]_")
        fnumI = int(self.setsectD["fnumI"]) + 1
        self.setsectD["fnumI"] = fnumI
        refS = self._label(fnumI, "[ Fig: ") + " ]"
        spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
        uS = tagL[0].strip() + " " * spcI + refS
    elif tag == "[e]_":  # equation label
        tagL = tagS.strip().split("[e]_")
        enumI = int(self.setsectD["enumI"]) + 1
        self.setsectD["enumI"] = enumI
        refS = self._label(enumI, "[ Equ: ") + " ]"
        spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
        uS = tagL[0].strip() + " " * spcI + refS
    elif tag == "[t]_":  # table label
        tagL = tagS.strip().split("[t]_")
        tnumI = int(self.setsectD["tnumI"]) + 1
        self.setsectD["tnumI"] = tnumI
        refS = self._label(tnumI, "[Table: ") + " ]"
        spcI = self.setsectD["swidthI"] - len(refS) - len(tagL[0].strip())
        uS = tagL[0].strip() + " " * spcI + refS
    elif tag == "[x]_":  # format tex
        tagL = tagS.strip().split("[x]_")
        txS = tagL[0].strip()
        # txS = txs.encode('unicode-escape').decode()
        ptxS = sp.parse_latex(txS)
        uS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))
    elif tag == "[s]_":  # format sympy
        tagL = tagS.strip().split("[s]_")
        spS = tagL[0].strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        # sps = sp.encode('unicode-escape').decode()
        uS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
    elif tag == "[n]_":  # section number
        rgx = r"\[\d\d\]"
        nameSS = hdrS
        snumSS = ""
        cnumSS = ""
        widthI = int(_setsectD["swidthI"])
        headS = hdrS
        if re.search(rgx, hdrS):
            nameSS = _setsectD["snameS"] = hdrS[hdrS.find("]") + 2:].strip()
            snumSS = _setsectD["snumS"] = hdrS[hdrS.find(
                "[") + 1: hdrS.find("]")]
            cnumSS = str(_sectD["cnumS"])
            widthI = int(_setsectD["swidthI"])
            if _rstB:
                # draw horizontal line
                headS = (
                    ".. raw:: latex"
                    + "\n\n"
                    + "   ?x?vspace{.2in}"
                    + "   ?x?textbf{"
                    + nameSS
                    + "}"
                    + "   ?x?hfill?x?textbf{SECTION "
                    + snumSS
                    + "}\n"
                    + "   ?x?newline"
                    + "   ?x?vspace{.05in}   {?x?color{black}?x?hrulefill}"
                    + "\n\n"
                )
                uS = headS
            else:
                headS = (
                    " "
                    + nameSS
                    + (cnumSS + " " + ("[" + snumSS + "]")).rjust(
                        widthI - len(nameSS) - 1
                    )
                )
                bordrS = widthI * "_"
                uS = headS + "\n" + bordrS + "\n"
    else:
        uS = lineS

    return uS, sectD


def _blocktags(self, lineS: str, sectD: dict) -> tuple:
    """parse block tags

    Args:
        tagS (str): rivt-string with tag
        tagL (list): list of tag parameters
        setsectD (dict): section dictionary

    Return:
        uS (str): utf string
    """

    swidthII = sectD["swidthI"] - 1

    tagS = tagS.rstrip()
    uS = ""
    try:
        tag = list(set(tagL).intersection(lineS.split()))[0]
    except:
        return lineS

    if tag == "[literal]__":  # footnote label
        tagS = tagS.strip("[foot]_").strip()
        uS = self.setsectD["ftqueL"].popleft() + tagS
    elif tag == "[math]__":  # new page
        uS = int(self.setsectD["swidthI"]) * "."
    elif tag == "[latex]__":  # horizontal line
        uS = int(self.setsectD["swidthI"]) * "-"
    elif tag == "[link]_":  # url link
        tgS = tagS.strip("[link]_").strip()
        tgL = tgS.split("|")
        uS = tgL[0].strip() + " : " + tgL[1].strip()
    elif tag == "[literal]_":  # literal text
        uS = "\n"
    elif tag == "[latex]_":  # literal text
        uS = "\n"
    elif tag == "[r]_":  # right adjust text
        tagL = tagS.strip().split("[r]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    elif tag == "[c]_":  # center text
        tagL = tagS.strip().split("[c]_")
        uS = (tagL[0].strip()).rjust(swidthII)
    else:
        uS = lineS

    return uS, sectD
