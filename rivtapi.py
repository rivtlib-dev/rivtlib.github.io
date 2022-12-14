#! python
'''rivt API

    The rivtapi module is imported at the beginning of a rivt calc.  It
    defines the five API methods: R(rs), I(rs), V(rs), T(rs), X(rs); where rs
    represents a rivtText string.
    
    When running in an IDE (e.g. VSCode), each method can become an interactive
    cell by adding a preceding #%%. In run-file mode, where the entire
    calculation file is processed, the output is written to the screen and disk
    as a utf8, PDF, or HTML file.
    
    The primary calculation input files are separated into two folders labeled
    calcs and docs. calc folder files are text files under version control that
    contain the primary calculation and supporting files. They are designed to
    be shared. Doc files are supporting calculation files that are typically
    binary files (images, pdf etc.) or files that include confidential project
    information or copyrights. The docs folder is typically not shared.
    
    The rivt calculation input file is a Python file written in rivtText, a
    superset of the markup language reStructuredText (reST) defined at
    https://docutils.sourceforge.io/rst.html. rivtText (rvTxt) is designed to
    be more readable and efficient for calculations. It includes rivt commands
    and tags, reStructuredText (reST) and native Python code. Commands start a
    line with ||, and read and write files into and out of the calculation.
    Tags terminate a line with the symbol _[tag] and format the output. Block
    tags start the block with ___[tag] and end with a blank line. 
    
    rivtCalc is an integrated open source software stack for systematically
    writing and sharing engineering calculation input and output as text file
    input and PDF or HTML output. The stack includes Python, VSCode, TexLive,
    GitHub and rivt.

    In the syntax summary below, user input is separated by | and user
    selections are separated by semi-colons for a single selection and commas
    for multiply selectable settings.

    rivt methods ---------------------------------------------------------------
    
    name           method, first line settings and commands
    ========= ================================================================== 
    repo       R(""" section_title | calc_title | utf,pdf,html;none | start_page
                       ||text, ||table, ||github ||project""")
    
    insert     I(""" section_title | doc_folder_override;default 
                       ||text, ||table, ||image, ||append """)
    
    values     V(""" section_title | sub;nosub | doc_folder_override;default 
                        =, ||values, ||lists, ||import, I commands """)
    
    tables     T(""" section_title | doc_folder_override;default
                        Python simple statements, I commands """)
    
    exclude    X("""  any text           
                        any commands """)


    rivt commands --------------------------------------------------------------

    command syntax                                                     method
    =============================================================== ============
    || github | param1 | param2                                      R
                github repo parameters
    || project | /docfolder;default | filename                       R
                folder for private project information | project info file
    || text | file_name | rivt;plain | 0                             R,I,V,T
                plain or rivt .txt file | indent space
    || table | file_name |  60r;l;c                                  R,I,V,T
                .csv or .rst file | max col width,right;left;center
    || image | file_name  | .50                                        I,V,T
                .png or .jpg file | fraction of page width
    || image2 | file_name  | .40 | file_name  | .40 |                  I,V,T
                side by side images
    || append | file_name | count                                      I,V,T
                .pdf file | include page numbers
    || lists | file_name  |  [:];[x:y]                                   V
                .csv;.syk;.txt;.py | rows to import
    || values | file_name |                                              V
                .csv;.syk;.txt;.py | rows to import
    || import | file_name |  print; noprint                              V
                
    rivt tags ------------------------------------------------------------------

    tag syntax                 description (user input)                
    =====================  ===================================================== 
    section title _[n]         start new section, autonumber
    sympy eq _[s]              format sympy equation                
    latex eq _[x]              format LaTeX equation                
    title _[t]                 table title, autonumber            
    caption _[f]               figure caption, autonumber         
    text _[r]                  right justify text                     
    text _[c]                  center text                            
    text _[line]               horizontal line - width of page        
    text _[page]               new PDF page                           
    text _[#]                  footnote, autonumber                    
    footnote _[foot]           footnote description
    url _[link]                (http://xyz label) label               
    descrip _[2,2]             * equation title, autonumber, decimal places  
    a = b | u1, u2             * define equation | units of answer
    a = n | u1, u2 | descrip   * assign value | units of answer | description
    ___[literal]               literal block                          
    ___[latex]                 LateX block                            
    ___[math]                  LaTeX math block                       
    ___[r]                     right justify text block                
    ___[c]                     center text block                      
    
    * only applies to Value method

    The first line of a rivt file imports *rivtapi*. The first method is always
    the Repo method R(rs), followed by any of the other four methods in any
    number or order. R(rs) occurs only one time. It sets options for
    repository, report and output formats. Method names start in column 1 and
    subsequent lines must be indented 4 spaces. This structure facilitates
    section folding and navigation, bookmarking and improved legibility. Format
    conventions follow the Python auto-formatter Black.

example rivt calc file  --------------------------------------------------------

import rivt.rivtapi as rv

rv.R(
    """ Repo method summary _[n] | Example Calculation | utf, pdf | 1 

    The Repo method is the first section and it specifies repository and output
    formats, and typically includes a calculation summary.
    
    The ||github command specifies settings for updating a public calc repo. 

    || github  | param1 | param2

    || project |  
    
    """
) 
rv.I(""" Insert method summary | /doc folder/override

    The Insert method formats descriptive information with three commands;
    ||text, ||table, ||image and a dozen tags. Tags [t]_ and [f]_ format and
    autonumber tables and figures.
    
    || text | file.txt | rivt;plain | indent

    table title  [t]_ 
    || table | file.csv;.rst | 60r;l;c 

    || image | f1.png | 50 
    A figure caption [f]_

    Insert two images side by side: 
    || images | f2.png | 35 | f3.png | 45
    [a] The first figure caption [f]_ 
    [b] The second figure caption  [f]_

    The tags [x]_ and [s]_ format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  [x]_ x = 32 + (y/2)  [s]_

    http://wwww.someurl.suffix  (label) [link]_ {formats a URL link}

    The ||attach command attaches PDF documents to the front or back of a doc.
    Any existing PDF document stored in its corresponding doc folder can be
    attached to the doc. The command can also overlay a title block page
    template on each page of the calc.
    """
) 
rv.V(
    """ Value method summary | nosub | save | /docfolder/override

    The Value method assigns values to variables and evaluates equations. The
    first setting is the section title. The sub;nosub setting specifies whether
    equations are output with substituted numerical values. The save;nosave
    setting specifies whether equations and value assignments are written to a
    values.txt file when the calc file is run. The values write is not triggered in
    interactive mode. The docfolder setting overrides the folder containing image
    
    The = tag triggers the evaluation of values and equations. Rows of values
    are terminated with a blank line and formatted into tables. 

    a1 = 10.1    | unit, alt | description 
    d1 = 12.1    | unit, alt | description 
    
    Example equation tag - Area of circle  _[2,2]
    a1 = 3.14*(d1/2)^2 | unit, alt 

    An equation tag prior to an equation, 1) labels it with a description 2)
    auto numbers it and 3) specifies the printed decimal places in equations
    and results respectively. The decimal formatting options are retained until
    changed - they do not need to be specified each time. The equation tag is
    optional and defaults to the description "equation".

    The Values method 

    || values | file | [:]
    
    The ||values command imports all values from a file, where the content in
    each row follows the input order (variable name, value, primary unit,
    secondary unit, description). Selected values may be printed. 
    
    || list | file | [:] 
  
    The ||list command imports and printes data from a file, where the first
    column is the variable name and the subsequent values make up a vector of
    values assigned to the variable.
    
    || import | file | docs;nodocs

    Imported functions from Python, Fortran, C or C++. On import the
    function name, arguments and doc strings or comments are inserted in the
    calcs. Single line functions may be defined in the Table method.
    """
)
 rv.T(""" Table method summary

    The Table method generates tables, plots and functions from native Python
    code. The method may include any Python simple statement (single line), rivt
    commands or tags. Any library imported at the top of the calc may be used,
    along with pandas, numpy and matplotlib library methods, which are imported
    by rivtcalc. The three included libraries are available as:
    
    pandas pd.method() np.method() mp.method()

    Common single line Python statements for defining functions or reading
    a file include:
    
    def f1(x,y): z = x + y; print(z); return
    
    with open('file.csv', 'r') as f: output = f.readlines()
    """
)
rv.X("""[n]_ skip-string

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
import rivt._r as _rM
import rivt._i as _iM
import rivt._v as _vM
import rivt._t as _tM
import rivt.reports as _rptM
import rivt.tags as _tagM

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
