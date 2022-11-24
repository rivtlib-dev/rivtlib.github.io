#! python
'''rivtlib API

    rivt is software for systematically writing engineering calculations and
    other documents. It includes an open source markup language and API written
    in Python. The rivt calculation input file is designed to be easily shared
    through version control ssytems e.g. GitHub. 
    
    The rivtlib API has five methods: R(rs), I(rs), V(rs), T(rs), X(rs); where
    rs represents a RivtText string. In interactive mode in an IDE (e.g.
    VSCode), each API method can made into a standard cell by adding a preceding
    #%%. Cells can be evaluated one at a time and the output is displayed
    interactively (utf8). In file or write mode the entire formatted calculation
    is written to disk as a calc (utf8) or doc (PDF).  rivt files and calcs are
    text files and are usually develoeped under version contol.  Doc files are
    PDF files that also include project specific information and images, which
    are typically not shared in their generic, executable form.
    
    RivtText may include commands, tags, reStructuredText (reST) and native
    Python code. Commands begin the line with || and process data files. Tags
    terminate a line with [tag]_ and format output. Tags also format  blocks of
    text starting with [tag]__ (double underscore) and terminale with a blank
    line. 

    API methods ----------------------------------------------------------------
    
    type    method             content and commands
    ======= =================================================================== 
    Repo    R(rs)   any text, ||output, ||project, ||append 
    Insert  I(rs)   any text, ||text, ||tables, ||image 
    Values  V(rs)   text, =,  ||values, ||lists, ||import, plus I commands 
    Tables  T(rs)   Python simple statements, plus all I and V commands 
    Exclude X(rs)   exclude evaluation - for debugging and review

    tags ----------------------------------------------------------------------

    line tags               description (user input in parenthesis)
    ===============  ==========================================================
    (description) [n]_  section description and autonumber 
    (title) [t]_        table title and autonumber 
    (caption) [f]_      figure caption and autonumber
    (sympy eq) [s]_     format sympy equation (latex eq) [x]_ format LaTeX equation 
    (text) [r]_         right justify text 
    (text) [c]_         center text
    (text) [#]_         footnote autonumber 
    (footnote) [foot]_  footnote description, placed at end of string
    section [line]_     horizontal line - width of
    page [page]_        new PDF page 
    (docs) [link]_      (http://xyz label) clickable url label 
    (description) (|n,n|sub;nosub) [e]_  equation, description,autonumber,format

    block tags                          description 
    =====================  ===================================================== 
    (text) [r]__                right justify text block 
    (text) [c]__                center text block 
    [literal]__                 literal block [latex]__             
    LaTeX block [math]__        math block

    In the example below, descriptive arguments to commands and tags (e.g.
    filenames) are in parenthesis. Selections (e.g. L;R;C) are separated by
    a semi-colon. Explanatory comments are in braces. The first line of a rivt
    file imports the rivtlib API,followed by methods. The Repo method (R(rs))
    is unique because it occurs first, and only one time.  It sets options for
    repository, report and output formats. Other methods can occur in any order
    and frequency.  Method declarations start in column 1 followed by optional
    section titles and tags on the same line. Subsequent lines in the function
    must be indented 4 spaces. This structures the calc for editor folding,
    bookmarking and improved legibility. Formatting conventions follow the rules
    used by the formatter Black.


example rivt file  -------------------------------------------------------------

from rivtlib import rivt as rv

rv.R("""Repo method [n]_ 

    The Repo method specifies repository and output formatting parameters and
    may include introductory calculation text. It is typically used once at the
    beginning of each file. 
    
    The ||output command specifies the type of output, calculation title
    override, starting page number and temporary file cleanup options. The
    |term setting is used for interactive calc editing. If an output type other
    than |term is specified the entire calc is evaluated and the output is
    written to the specified file type. If utf is specified, the calc output is
    written to README.txt for upload to the repository and searching.
    
    The ||project command inserts a project table from information in private
    doc folders. Other private files include image and PDF files read from the
    doc folders. The folder structure of rivt keeps confidential, binary and
    copyrighted information separate from shareable, version controlled text.

    The ||attach command attaches PDF documents to the front or back of a doc.
    Any existing PDF document stored in its corresponding doc folder can be
    attached to the doc. The command can also overlay a title block page
    template on each page of the calc.

    || output  | term;utf;pdf;html |  (title) | (page) |(cleanup)
    || project | (project_data.xlsx;.syk,.csv,.txt) | (width),L;R;C 
    || attach  | (file.pdf) | front; back; block 
    """) 
    
rv.I("""Insert method [n]_ 

    The Insert method formats descriptive information with three commands;
    ||text, ||table, ||image and a dozen tags. Tags [t]_ and [f]_ format and
    autonumber tables and figures.
    
    || text | (file.txt) | rivt;plain;indent

    table title  [t]_ 
    || table | (file.csv;.rst) | (60,r;l;c) {max col width,location }

    || image | (f1.png) | (50,l;c;r) {scale percent of page width, location} 
    A figure caption [f]_ {centered}

    Insert two images side by side using the following syntax: 
    || image | (f1.png) | (35,s) | image | (f2.png) | (45,s) {scale percent of page width}
    [a] The first figure caption [f]_ 
    [b] The second figure caption  [f]_

    The tags [x]_ and [s]_ format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  [x]_ x = 32 + (y/2)  [s]_

    http://wwww.someurl.suffix  (label) [link]_ {formats a URL link}

    """
) rv.V("""Value method [n]_ 

    The Value method assigns values to variables and numerically evaluates
    equations. The = sign is the tag that triggers the evaluation values. Rows
    of values are formatted into tables that are terminated with a blank line.
    Recorded values can be read from files into subsequent calcs.

    a1 = 10.1    | unit, alt unit | description 
    d1 = 12.1    | unit, alt unit | description # save {records to csv file - values.csv}

    Equations have the syntx:

    a1 = 3.14*(d1/2)^2   | unit, alt unit  # save {stores to file}

    An equation tag placed above an equation labels it with a description, auto
    numbers it, specifies the printed decimal places in equations and results
    respectively, and whether the equation is printed with substituted numerical
    values. The equation tag precedes the equation and has the syntax,
    
    Area of circle | 2,2 | nosub;sub [e]_ 

    The decimal and substitution formatting options are retained until changed -
    they do not need to be specified each time. The equation tag is optional and
    defaults to the description "equation" if stored.

    The commands ||values, ||list and ||import read values and functions from
    files.

    || values | (file.csv .xlxs .syk) | print([x:y]) {list of rows to print}
    
    The ||values command imports all values from a file, where the content in
    each row follows the input order (variable name, value, primary unit,
    secondary unit, description). Selected values may be printed. 
    
    || list | (file.csv .xlxs .syk) | [:];([x:y]) {rows to import}
  
    The ||list command imports data from a file, where the first column is the
    variable name and the subsequent csv values make up a vector of values assigned
    to the variable.
    
    || import | (file.py) | docs;nodocs

    Functions are imported from a Python file.  The function name, arguments and
    doc strings may be included in the calc. Single line functions may also be
    defined by the Table method.


    """
) rv.T("""Table method [n]_  

    The Table method generates tables, plots and functions from native Python
    code. The method may include any Python simple statement (single line), rivt
    commands or tags. Any library imported at the top of the calc may be used,
    along with pandas, numpy and matplotlib library methods, which are imported
    by rivtcalc. The three included libraries are available as:
    
    pandas pd.method() np.method() mp.method()

    Some common single line Python statements for defining functions or reading
    a file include:
    
    def f1(x,y): print(x,y); return x*y
    
    with open('file.csv', 'r') as f: output = f.readlines()
    
    """
) rv.X("""[n]_ skip-string

    Skips evaluation of the string. Used for comments and debugging. 

    """ 
) '''

import os
import sys
import subprocess
import time
import logging
import warnings
import shutil
import numpy as np
from pathlib import Path
from collections import deque
import rivtlib.str_r as _rM
import rivtlib.str_i as _iM
import rivtlib.str_v as _vM
import rivtlib.str_t as _tM
import rivtlib.write as _wrtM
import rivtlib.tags as _tagM

# import sympy as sp
# import numpy as np
# import pandas as pd
# import rivtcalc.check as _rchk

try:
    _cfileS = sys.argv[1]
except:
    _cfileS = sys.argv[0]
# print("argv0 argv1", sys.argv[0], sys.argv[1])
if ".py" not in _cfileS:  # get VSCode file reference
    # print(dir(__main__))
    import __main__

    _cfileS = __main__.__file__

# define path variables
_cwdS = os.getcwd()
_cfullP = Path(_cfileS)  # calc file full path
_cfileS = _cfullP.name  # calc file name
_cnameS = _cfileS.split(".py")[0]  # calc file basename
_cdescrip = _cnameS.split("_")[1]
_ddirS = "".join(["d", _cnameS[1:3], "_", _cdescrip])
_curcalcP = _cfullP.parent  # current calc folder path
_calcsP = _cfullP.parent.parent  # calcs folder path
_rivtP = _cfullP.parent.parent.parent  # project folder path
_docsP = Path(_rivtP / "docs")  # docs folder path
_dcfgP = Path(_docsP / "d00_docs")  # doc config folder
_htmlP = Path(_docsP / "html")  # doc folder path
_curdocP = Path(_docsP / _ddirS)  # doc folder path
_rivtcaldP = Path("rivtcalc.calc.py").parent  # rivtcalc program path
print("INFO: calc directory is ", _curcalcP)
print("INFO: doc directory is ", _curdocP)

# check that calc and doc directories exist
for root, dir, file in os.walk(_calcsP):
    for i in dir:
        if _cfileS[0:5] == i[0:5]:
            print("INFO: calc directory is ", i)
        else:
            print("INFO: calc directory ", _curcalcP, " not found")
for root, dir, file in os.walk(_docsP):
    for i in dir:
        if "".join(["d", _cfileS[1:3]]) == i[0:3]:
            print("INFO: doc directory is ", i)
        else:
            print("INFO: doc directory ", _curdocP, " not found")

# initialize objects
utfS = """"""  # utf accumulating calc-string
rstS = """"""  # reST accumulating calc-string
exportS = """"""  # values string export
rivtD = {}  # values dictionary
_foldD = {}  # folder dict
_rstB = False  # reST generation flag
for variable in ["_projP", "_calcsP", "_curcalcP"]:
    _foldD[variable] = eval(variable)
for variable in ["_curdocP", "_docsP", "_dcfgP", "_htmlP"]:
    _foldD[variable] = eval(variable)
_tagD = {
    "fnumS": _cnameS[0:5],  # file number
    "cnumS": _cnameS[1:5],  # calc number
    "dnumS": _cnameS[1:3],  # division number
    "sdnumS": _cnameS[3:5],  # subdivision number
    "snameS": "",  # section title
    "snumS": "",  # section number
    "swidthI": 80,  # utf section width
    "twidthI": 78,  # utf body width
    "enumI": 0,  # equation number
    "tnumI": 0,  # table number
    "fnumI": 0,  # figure number
    "ftqueL": deque([1]),  # footnote number
    "countI": 0,  # footnote counter
    "decI": 2,
    "decvI": 2,
    "subvB": False,
}
# run backups and logging
_logfileP = Path(_dcfgP / ".".join((_cnameS, "logging")))
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=_logfile,
    filemode="w",
)
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
warnings.filterwarnings("ignore")
_rshortP = Path(*Path(_cfullP).parts[-3:])
_lshortP = Path(*Path(_logfileP).parts[-4:])
logging.info(f"""calc path: {_rshortP}""")
logging.info(f"""log path: {_lshortP}""")
_rvbak = Path(_curcalcP / ".".join((_cnameS, "bak")))
with open(_cfullP, "r") as f2:
    calcbak = f2.read()
with open(_rvbak, "w") as f3:
    f3.write(calcbak)
logging.info(f"""calc backup written to calc folder""")
print(" ")

# set default output parameters
doctypeS = "term"
stylefileS = "rivt"
calctitleS = "Calculation"
startpageS = "1"
_rstB = False

# API methods
def R(rvS: str):
    """Repo-string

    Args:
        rvS (str): repository-string

    """
    global utfS, rstS, valuesD, _foldD, _tagD, _rstB
    cmdL = ["project", "search", "attach"]
    rvL = rvS.split("\n")

    # set output parameters
    for iS in rvL:
        if iS.strip()[:2] == "||":
            iL = iS[2:].split("|")
            if iL[0].strip == "output":
                doctypeS = iL[1].strip()
                stylefileS = iL[2].strip()
                calctitleS = iL[3].strip()
                startpageS = iL[4].strip()
                clrS = iL[5].strip()

    if doctypeS == "term":
        utfS += _tagM._tags(utfL[0])  # section
        rC = _rM._R2utf()
        for i in utfL[1:]:
            rC = _rM.R2utf
            utfS += rC.r_utf
        print(utfS)
    elif doctypeS == "utf":  # write utf calc file
        """write utf-calc to associated calc folder and exit"""
        f1 = open(_cfullP, "r")
        utfL = f1.readlines()
        f1.close()
        print("INFO calc file read: " + str(_cfullP))
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += _rM.r_utf(cmdL)
        # print(utfS)
        exec(utFS, globals(), locals())
        utffile = Path(_cpath / _setsectD["fnumS"] / ".".join([_cnameS, "txt"]))
        if filepathS == "default":  # check file write location
            utfpthS = Path(utffile)
        else:
            utfpthS = Path(_cpath / filepathS / ".".join((_cnameS, "txt")))

        with open(utfpthS, "wb") as f1:
            f1.write(utfcalcS.encode("UTF-8"))
        print("INFO: utf calc written to calc folder", flush=True)
        print("INFO: program complete")
        os._exit(1)
    elif doctypeS == "pdf" or doctypeS == "html":
        _rstB = True
        gen_rst(cmdS, doctypeS, stylefileS, calctitleS, startpageS)
        _rstB = True
        rcalc = _init(rvS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
        # clean temp files
        fileL = [
            Path(_dcfgP, ".".join([_cnameS, "pdf"])),
            Path(_dcfgP, ".".join([_cnameS, "html"])),
            Path(_dcfgP, ".".join([_cnameS, "rst"])),
            Path(_dcfgP, ".".join([_cnameS, "tex"])),
            Path(_dcfgP, ".".join([_cnameS, ".aux"])),
            Path(_dcfgP, ".".join([_cnameS, ".out"])),
            Path(_dcfgP, ".".join([_cnameS, ".fls"])),
            Path(_dcfgP, ".".join([_cnameS, ".fdb_latexmk"])),
        ]
        os.chdir(_dcfgP)
        tmpS = os.getcwd()
        if tmpS == str(_dcfgP):
            for f in fileL:
                try:
                    os.remove(f)
                except:
                    pass
            time.sleep(1)
            print("INFO: temporary Tex files deleted \n", flush=True)
        print("exit")
        os.exit(1)
    else:
        pass


def I(rvS: str):
    """Insert-string

    Args:
        rvS: rivt-string
    """
    global utfS, rstS, _rstB, _foldD, _tagD, _rivtD
    cmdL = ["text", "table", "image"]
    rvL = rvS.split("\n")
    iC = _iM._I2utf()

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += iC.i_utf(cmdL)
        print(utfS)


def V(rvS: str):
    """Value-string

    Args:
        rvS: rivt-string
    """
    global utfS, rstS, _rstB, _folderD, _tagD, _rivtD, exportS
    cmdL = ["=", "list", "values", "import", "text", "table", "image"]
    rvL = rvS.split("\n")
    vC = _vM._V2utf()

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += vC.v_utf(cmdL)
        print(utfS)


def T(rvS: str):
    """table-string to utf-string

    Args:
       rvS: rivt-string
    """
    global utfS, rstS, rivtD, _rstB, _folderD, _tagD
    cmdL = ["list", "values", "import", "text", "table", "image"]
    rvL = rvS.split("\n")
    tC = _tM._T2utf()

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += tC.t_utf(cmdL)
        print(utfS)


def X(rvS: str):
    """skip processing of rv-string

    Args:
       rvS: rivt-string
    """
    rvS
    pass
