#! python
''' 
rivt and rivtlib
----------------

**rivt** is a lightweight markup language for writing, organizing and
sharing engineering documents and reports. It is designed to be legible,
flexible and efficient. **rivt** is also the name of an open source framework
used for producing rivt documents.

**rivtlib** is a Python library that processes rivt files and is distributed
under the open source MIT license. It runs on platforms that support Python
3.11 or later and works within a framework of five established, open souce
technologies:

- Language: Python with open source libraries including **rivtlib**
- IDE: VSCode and extensions
- Typesetting: Latex TexLive Distribution
- Diagrams: QCAD
- Version control: GitHub

The **rivt** framework can be downloaded as a portable Windows zip file or
installed through OS specific shell scripts (https://rivtcode.net). It is also
available as an online service at https://rivtonline.net.

A rivt document (doc) is a text, HTML or PDF ouput file from a processed rivt
file. A rivt report (report) is an organized collection of rivt docs.
**rivtlib** organizes and generates both large reports and single file docs.

A rivt file is a Python file that imports **rivtlib** and its 6 API
functions:

*import rivtlib.rivtapi as rv* 
# where rS is a triple quoted Python rivt-string

rv.R(rS) - (Run) Run shell scripts 
rv.I(rS) - (Insert) Insert static text, images, tables and math equations 
rv.V(rS) - (Values) Evaluate tables, values and equations 
rv.T(rS) - (Tools) Execute Python functions
rv.X(rS) - (eXclude) Skip rivt-string processing 
rv.W(rS) - (Write) Write formatted rivt documents 


The 6 API functions implement:

    - wrapper for reStructuredText markup (see https://quickrestructuredtext.com)

    - a folder and file structure

    - commands and tags for processing files and formatting output
    
**rivt** commands and tags are summarized below. See the user manual at
https://rivtdocs.net for futher details.



Tags: formatting
-----------------

Tags evaluate and format rivt strings. Line tags are inserted at the end
of a line and block tags at the start and end of a text block.
reStructuredText markup may also be used for formatting (see
https://quickrestructuredtext.com).

===================== ========= ========================== ==================
 tags                   scope       description               API scope  
===================== ========= ========================== ==================
text _[u]               line        underline                   I                             
text _[r]               line        right justify               I                        
text _[c]               line        center                      I                 
text _[bc]              line        bold center                 I     
text _[bi]              line        bold italic                 I
title _[t]              line        table title                 I
equation _[s]           line        sympy math equation         I
equation _[x]           line        latex math equation         I                           
equation _[bs]          line        bold numbered sympy         I     
equation _[bl]          line        bold numbered latex         I    
_[[p]]                  block       start monospace block       I 
_[[l]]                  block       start LaTeX block           I
_[[e]]                  block       end block                   I
label _[t]              line        lookup table title          V             
title _[v]              line        value table title           V                                
label _[e]              line        equation label              V                                
var :=, a               line        declare value               V
var = a + b             line        assign value                V
text _[f]               line        numbered figure             V,I
text _[#]               line        footnote (autonumber)       V,I
text _[d]               line        footnote description        V,I   
_[page]                 line        new page                    V,I
===================== ========= ========================== ==================



Commands: file processing
--------------------------

rivt commands process files e.g. image, equations, tables etc. They start with
a single or double bar (| or ||) and have the form:

    | (--) label or title (tag) | /relative/path/file.typ(:start-end) | params

where options are shown in parenthesis and parameters depend on the file type.
A leading double bar (||) optionally inserts the referenced file lines into the
input for legiblity and checking.

Command are shown below in the context of an API function. Within VSCode an API
function or sequence of functions may be run interactively using the standard
cell decorator *# %%*. Interactive output is formatted as utf-8 text, as is
output to stdout when a rivt file is run from a terminal.

================================================================================
                        Command Overview
================================================================================


rv.R("""run function label | pass;redact | color;none

    The Run function processes shell commands.
    
    | run |
    
    | capture | 
    
    | edit |
    
    """)


rv.I("""Insert Function Label | pass;redact | color;none
                        
    The Insert function formats static file objects including equations,
    images, tables and text.
            
    | append label | /append/path/.pdf | number; nonumber       

    | equation label (_[s,l]) | /text/path/.tex;txt(:start-end) | bold; plain
    
    | image label (_[i]) | /image/path/.jpg;.png;.svg | size, color

    | table title (_[t]) | /tables/path/.csv;.xls (:start-end) | width, align

    | text label | /text/path/.txt(:start-end) | plain; rivt

    """)


rv.V("""Values Function Label | pass;redact | color;none
            
    The Values function evaluates lookup tables, variables and equations from files.

    | image label (_[i])| /image/path/.jpg;.png;.svg | size, color

    | table title (_[t])| /tables/path/.csv;.xls (:start-end) | [cols]

    | value label (_[v])| /values/path/.csv(:start-end) | 

    | equation label (_[e]) | /values/path/.txt(:start-end) | ref; noref

    """)
  

rv.T("""Tools function label | pass;redact | color;none

        The Tools function imports and evaluates functions.
                
        | function label (_[f]) | /scripts/path/.py | function name; file
        
        f1(x)

    """)


rv.X("""  |   |

    The X function prevents evaluation of the function. Any API function may be
    changed to X for flow control, testing, debugging and comments.

    """)

rv.W("""Write function label | pass;redact | color;none

    The Write function generates a formatted doc file from a rivt file as text,
    HTML and PDF. It generates reports based on config file settings as
    README.txt, HTML and PDF.

    | output
    
    | files

    """)

Folders: document organization 
------------------------------

**rivt** implements a file and folder structure to simplify file sharing and
control. The privacy level of document inputs and outputs may be may be set at
the file or API function level. Each rivt file (and doc) is idenfiifed by a
unique rivt file prefix with the form rivddss-filename where dd is a two digit
division number and ss is a two digit subdivision number e.g., riv0203-loads.py
is the third subdivision of division two. Editing the rivt number also changes
the report organization.

Report and document headings are taken from folder and file names unless
overridden in the config file. An example folder structure is shown below.
Required file names or prefixes are shown in [ ].

Source files for rivt docs are stored in 6 folders::

    - append
    - images
    - scripts
    - tables
    - text
    - values

Output is written to the write folder with 4 sub-folders::

    - html
    - pdf
    - text
    - temp
    - xrivt

Doc files are the text, PDF or HTML output of a rivt file that are stored in
the *write* folder. rivt reports are collections of docs specified in the
config.ini. Resource files are stored in user-defined sub-folders which
organize the data allow for separation of public and private data.

[rivt]-Project-Name/               
    ├── [append]/            
        ├── app01/  
        └── app02/  
            ├── attach3.pdf                   
            └── attach4.pdf
    ├── [images]/            
        ├── img01/  
        └── img02/  
            ├── image3.jpg                   
            └── image4.jpg
    ├── [scripts]/
        ├── py01/                 
        └── py02/  
            ├── function3.py
            └── function4.py               
        ├── run01/  
        └── run02/  
            ├── script3.bat
            └── script4.sh  
    ├── [tables]/            
        ├── tbl01/  
        └── tbl02/  
            ├── table3.csv                   
            └── table4.csv
    ├── [text]/            
        ├── tex01/  
        ├── tex02/  
            ├── latex3.tex
            └── latex4.tex
        ├── txt01/  
        └── txt02/  
            ├── text3.txt                   
            └── text4.txt
    ├── [values]/                 
        ├── dat01/  
        ├── dat02/  
            ├── table3.csv                   
            └── table4.csv
        ├── equ01/                      
        ├── equ02/                    
            ├── equation1.txt      
            └── equation2.txt       
        ├── val01/                    
        └── val02/                    
            ├── values3.csv      
            └── values4.csv       
    ├── [write]/                        (output files)    
        ├── [html]/                     
            └── riv0101-codes.html      (html files)
                riv0202-frames.html
                Project-Name.html       (html report) 
        ├── [pdf]/                      
            └── riv0101-codes.pdf       (pdf files)        
                riv0202-frames.pdf
                Project-Name.pdf        (pdf report)        
        ├── [temp]/                     (temp files)     
            └── temp-files.tex
        └── [text]/                     
            └── riv0101-codes.txt       (text output)
                riv0201-frames.txt
        └── [xrivt-redacted]/            
            └── README.txt              (redacted report)
                xriv0101-codes.py       (redacted files)
                xriv0102-loads.py
                xriv0201-walls.py       
    └── config.ini                      (rivt config file)
        README.txt                      (searchable report in public repo)
        riv0000-report.py               (rivt input files)
        riv0101-codes.py
        riv0102-loads.py
        riv0201-walls.py
        riv0202-frames.py


Example rivt file
-----------------------------------------------------------------------------
API functions start in column 1. rivt-strings are indented 4 spaces (for
legibility and code folding).A rivt doc is assembled by each function in order
of the input order. Each function also, optionally, defines a doc section.

import rivtlib.rivtapi as rv

rv.R("""Run function | pass; redact | nocolor; color code

    The Run function processes shell commands.

    Each API function defines a new document section. The first line is a
    heading line which includes the section heading, a parameter for redacting
    sections in a mirror file intended for public sharing, and a parameter for
    the background color for the section. If the section heading is preceded by
    two dashes (--) the section is continued from the prior section without
    introducting a new number.
    
    File formatting follows pep8 and ruff. API functions start in column one.
    All other lines are indented 4 spaces to facilitate section folding,
    bookmarks and legibility.

    """)

rv.I("""Insert function | pass; redact | nocolor 

    The Insert function formats static objects including images, tables,
    equations and text.

    ||text | data01/describe.txt | rivt     

    The table command inserts and formats tabular data from csv or xls files.
    The _[t] tag formats and autonumbers table titles.

    A table title  _[t]
    || table | data/file.csv | 60,r

    The image command inserts and formats image data from png or jpg files. The
    _[f] tag formats and autonumbers figures.
        
    A figure caption _[f]
    || image | data/f1.png | 50

    Two images may be placed side by side as follows:

    The first figure caption  _[f]
    The second figure caption  _[f]
    || image | private/image/f2.png, private/image/f3.png | 45,35
    
    The tags _[x] and _[s] format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  _[x] 

    x = 32 + (y/2)  _[s]

    """)

rv.V("""Values function |  pass; redact | nocolor 

    The Values fucntion evaluates variables and equations. 
    
    The equal tag declares a value. A sequence of declared values terminated
    with a blank line is formatted as a table.
    
    Example of assignment list _[t]
    f1 = 10.1 * LBF |LBF, N| a force value
    d1 = 12.1 * IN  |IN, CM| a length value

    An equation tag provides an equation description and number. A colon-equal
    tag assigns a value and specifies the result units and the output decimal
    places printed in the result and equation.

    Example equation - Area of circle  _[e]
    a1 := 3.14(d1/2)^2 | IN^2, CM^2 | 1,2

    || declare | data01/values02.csv
    
    The declare command imports values from the csv file written by rivt when
    processing values in other documents. 

    """)

rv.T("""Tools function | pass; redact | nocolor

    The Tools function processes Python code.
        
    """)


rv.X("""Any text 

    Changing a function to X skips evaluation of that function. Its purposes
    include review commenting and debugging.

    """) 

rv.W("""Write function | pass; redact | nocolor

    The Write function generates docs and reports.

    | docs |
 
    | report |

    """)


VSCode rivt profile
-------------------

============== ==============================================================
Snippets/Keys            description
============== ==============================================================

run             API Run function
ins             API Insert function   
val             API Values function
too             API Tools function
wri             API Write function


alt+q                rewrap paragraph with hard line feeds (80 default)
alt+p                open file under cursor
alt+.                select correct spelling under cursor
alt+8                insert date
alt+9                insert time

ctl+1                focus on first editor
ctl+2                focus on next editor
ctl+3                focus on previous editor
ctl+8                focus on explorer pane
ctl+9                focus on github pane    

ctl+alt+x            reload window
ctl+alt+[            reload window
ctl+alt+]            unfold all code
ctl+alt+u            unfold all code
ctl+alt+f            fold code level 2 (rivt sections visible)
ctl+alt+a            fold code - all levels
ctl+alt+t            toggle local fold
ctl+alt+e            toggle explorer sort order
ctl+alt+s            toggle spell check
ctl+alt+g            next editor group

ctl+shift+u          open URL under cursor in browser
ctl+shift+s          open GitHub README search for rivt
ctl+shift+a          commit all 
ctl+shift+z          commit the current editor
ctl+shift+x          post to remote   
============== ==============================================================


============================================== ===============================
Extensions                                       description
============================================== ===============================

BUTTONS
tombonnike.vscode-status-bar-format-toggle          format button
gsppvo.vscode-commandbar                            command buttons
AdamAnand.adamstool                                 command buttons
nanlei.save-all                                     save all button
Ho-Wan.setting-toggle                               toggle settings
yasukotelin.toggle-panel                            toggle panel
fabiospampinato.vscode-commands                     user command buttons
jerrygoyal.shortcut-menu-bar                        menu bar

EDITING 
henryclayton.context-menu-toggle-comments           toggle comments
TroelsDamgaard.reflow-paragraph                     wrap paragraph
streetsidesoftware.code-spell-checker               spell check
jmviz.quote-list                                    quote elements in a list
njpwerner.autodocstring                             insert doc string
oijaz.unicode-latex                                 unicode symbols from latex
jsynowiec.vscode-insertdatestring                   insert date string
janisdd.vscode-edit-csv                             csv editor

VIEWS
GrapeCity.gc-excelviewer                            excel viewer
SimonSiefke.svg-preview                             svg viewer
tomoki1207.pdf                                      pdf viewer
RandomFractalsInc.vscode-data-preview               data viewing tools
Fr43nk.seito-openfile                               open file from path
vikyd.vscode-fold-level                             line folding tool
file-icons.file-icons                               icon library
tintinweb.vscode-inline-bookmarks                   inline bookmarks

MANAGEMENT
alefragnani.project-manager                         folder, project management
Anjali.clipboard-history                            clipboard history
dionmunk.vscode-notes                               notepad
hbenl.vscode-test-explorer                          test explorer
mightycoco.fsdeploy                                 save file to second location
lyzerk.linecounter                                  count lines in files
sandcastle.vscode-open                              open files in default app
zjffun.snippetsmanager                              snippet manager
spmeesseman.vscode-taskexplorer                     task explorer

GITHUB
GitHub.codespaces                                   run files in codespaces
GitHub.remotehub                                    run remote files
ettoreciprian.vscode-websearch                      search github within VSCode
donjayamanne.githistory                             git history
MichaelCurrin.auto-commit-msg                       git auto commit message     
github.vscode-github-actions                        github actions
GitHub.vscode-pull-request-github                   github pull request
k9982874.github-gist-explorer                       gist explorer
vsls-contrib.gistfs                                 gist tools

PYTHON
ms-python.autopep8                                  python pep8 formatting
ms-python.isort                                     python sort imports
donjayamanne.python-environment-manager             python library list
ms-python.python                                    python tools
ms-python.vscode-pylance                            python language server
ms-toolsai.jupyter                                  jupyter tools
ms-toolsai.jupyter-keymap                           jupyter tools
ms-toolsai.jupyter-renderers                        jupyter tools
ms-toolsai.vscode-jupyter-cell-tags                 jupyter tools
ms-toolsai.vscode-jupyter-slideshow                 jupyter tools

LANGUAGES 
qwtel.sqlite-viewer                                 sqlite tools
RDebugger.r-debugger                                R tools
REditorSupport.r                                    R tools
ms-vscode-remote.remote-wsl                         windows linux tools
James-Yu.latex-workshop                             latex tools
lextudio.restructuredtext                           restructured text tools
trond-snekvik.simple-rst                            restructured syntax
yzane.markdown-pdf                                  markdown to pdf
yzhang.markdown-all-in-one                          markdown tools
============================================== ===============================
'''
