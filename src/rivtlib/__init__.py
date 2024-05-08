#! python
''' **rivt** is a lightweight markdown language for writing, organizing and
sharing engineering documents. **rivtlib** is a Python library for processing
rivt files. It runs on any platform that supports Python 3.10 or later. rivtlib
can process single and multiple-file documents running to hundreds of pages.
**rivt** and **rivtlib** are distributed under the open source MIT license.

A rivt file is a Python file that imports six API functions through:

*import rivtlib.rivtapi as rv*


=============== ===============================================================
 API function                   Description
=============== ===============================================================

Each function takes a single, triple quoted unicode string (rS) as argument.

rv.R(rS) - execute shell scripts (Run)
rv.I(rS) - insert static text, images, tables and math (Insert)
rv.V(rS) - evaluate equations (Values)
rv.T(rS) - execute Python functions and scripts (Tools)
rv.X(rS) - skip rivt-string processing (eXclude)
rv.W(rS) - output formatted rivt document (Write)


**rivt** is built from four open souce projects:

- Python and third party open source libraries
- VSCode
- Latex (TexLive)
- Git (GitHub)

In addition to file commands and formatting tags, rivt-text may include
arbitrary unicode text. (See the user manual at https://rivt-doc.net). A rivt
command processes files and is triggered by a line that starts with | or ||.  A
rivt tag formats a line or block of code. Commands and tags are summarized
below.

================ ===============================================================
 name (snippet)                     Command Overview
================ ===============================================================

Run (run)            rv.R("""section label | pass;redact | color;none


                         """)

Insert (ins)         rv.I("""section label | pass;redact | color;none
                        
                         | .png, .jpg, .svg (images)
                         | .txt (text - plain, latex, sympy, rivt, eq)
                         | .csv (tables) 

                         """)

Values (val)         rv.V("""section label | pass;redact | color;none
                
                         | .png, .jpg, .svg (images)
                         | .txt (text - plain)
                         | .csv (tables) 

                         := declare
                         = assign

                         """)

Tools (too)          rv.T("""section label | pass;redact | color;none
                

                         """)

Write (wri)          rv.W("""report;doc

                         | output
                         | files
            
                          """)

Exclude              rv.X("""any API function

                         When a method is changed to X it is not evaluated. It
                         may be used for comments and debugging.

                         """)

Format tags are inserted at the end of a line. Line tags format a single line
and block tags apply to blocks of text. reStructuredText may also be used for
formatting ( e.g. bold, italic, etc.)

===================== ========= ========================== ==================
 tags                   scope       description               API scope  
===================== ========= ========================== ==================
text _[u]               line        underline                   I                             
text _[r]               line        right justify               I                        
text _[c]               line        center                      I                 
text _[bc]              line        bold center                 I     
text _[bi]              line        bold italic                 I
text _[s]               line        numbered sympy              I
text _[l]               line        numbered latex              I                           
text _[bs]              line        bold numbered sympy         I     
text _[bl]              line        bold numbered latex         I    
_[[p]]                  block       start monospace             I 
_[[l]]                  block       start LaTeX                 I
_[[e]]                  block       end block                   I
text _[e]               line        numbered equation           V                                
text _[t]               line        numbered table              I,V
text _[#]               line        footnote (autonumber)       I,V     
text _[d]               line        footnote description        I,V   
_[page]                 line        new page                    I,V

When running in an IDE (e.g. VSCode), each function may be run interactively
using the standard cell decorator *# %%*. Interactive output and output to
stdout (terminal) is formatted as utf-8 text. The rv.write() function generates
formatted documents in text, reStructuredText (GitHub README), HTML and PDF.


=================
rivt file example
=================

File formatting conventions follow Python pep8 and ruff conventions. API
function declarations start in column one. All other lines are indented 4
spaces to facilitate section folding, bookmarks and legibility. The first line
of each function defines the heading for a new document section, followed by
section parameters. New sections may be suppressed by prepending the heading
label with a double hyphen (--).

--------------------------------------

import rivtlib.rivtapi as rv

rv.R("""Introduction | notoc, 1

    The Rivtinit method is the first method of a rivt file and specifies
    repository, report and document settings.

    The first line of any method is the heading line, which starts a new
    document section. If the section heading is preceded by two dashes (--) it
    becomes a section reference and a new section is not started. The toc
    parameter specifies whether a document table of contents is generated and
    inserted at the top of the document (not to be confused with a report table
    of contents). The page number is the starting page number for the doc, when
    processed as a stand alone document.

    The init command specifies the name of the configuration file which is read
    from the rivt-doc folder. Report formatting can be easily modified by
    specifying a different init file.

    ||init | rivt01.ini

    The text command inserts text from an external file. Text files may be
    plain text or include rivt tags.

    ||text | private/data/proj.txt | plain
    
    The append command attaches PDF files to the end of the doc.

    || append | append/report1.pdf
    || append | append/report2.pdf

    
    """)

rv.I("""The Insert method | nocolor 

    The Insert method formats static information e.g. images and text. The
    color command specifies a background color for the section.

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

rv.V("""The Values method |  nosub 

    The Values method assigns values to variables and evaluates equations. The
    sub or nosub setting specifies whether equations are also printed with
    substituted numerical values.
    
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

rv.T("""The Tools method | summary

    # The Tools method processes Python code in the rivt namespace and prints
    # the code and the result of any print statement in the doc. 
    # Functions may be written explicitly or imported from other
    # files. Line comments (#) are printed. Triple quotes cannot be used. Use
    # raw strings instead.
    
    # Four Python libraries are imported by rivt and available as: 
    # pyplot -> plt
    # numpy -> np
    # pandas -> pd
    # sympy -> sy
    
    # Python code example:
    
    def f1(x,y): z = x + y
        print(z)
        return Z

    with open('file.csv', 'r') as f: 
        input = f.readlines()
    
    var = range(10)
    with open('fileout.csv', 'w') as f: 
        f.write(var)
        
    """)

rv.X("""any text

    Changing a function to X skips evaluation of that function. Its uses
    include review comments and debugging.

    """) 

-----------------------------------------------

=======
folders
=======

rivtlib can process single rivt files, but typically it is used to generate
reports. A rivt report is generated from the folder structure illustrated
below. rivt documents are organized into divisions. Document inputs and outputs
may be stored in or directed to publically shareable or private foldrers.
Reports is formatted with divisions, subdivisions and sections.

Fixed folder and file prefixes are shown in [ ]. Report and document headings
are taken from the folder and file labels. Tools are available to generate
starter folder templates.

[rivt]_Report-Label/               
    ├── [div01]-div-label/            (division folder)
        ├── [data01]/                 (resource data)
            ├── data.csv                   
            ├── attachment.pdf
            └── fig.png            
             functions.py                   
        ├── [riv01]-label1.py         (rivt file)
        └── [riv02]-label2.py         (rivt file)   
    ├── [div02]-div-label/            (division folder)
        ├── [data02]/                 (resource data)
            ├── data.csv
            └── fig.png
        └── [riv01]_label3.py         (rivt file)
    ├── [data-private]/                 
        ├── [data]/                   (private data)                   
            ├── data.csv
            ├── attachment.pdf
            └── fig.png        
        ├── [functions]/              (private functions)                   
            ├── [data]/
            ├── [output]/
            └── function.py                
        ├── [rivt-docs]/              (private output documents)
            ├── [pdf]/                      
                ├── doc0101-label1.pdf      
                ├── doc0102-label2.pdf
                ├── doc0201-label3.pdf
                └── Report-Label.pdf 
            ├── [text]/                    
                ├── doc0101-label1.txt      
                └── doc0201-label3.txt       
            ├── doc0101-label1.md            
            └── doc0201-label3.md
        ├── [temp]/
            └── doc0201-label3.tex 
    ├── [functions]/                  (public functions)                   
        ├── [data]/
        ├── [output]/
        ├── function1.py
        └── function2.py                
    ├── [rivt-docs]/                  (public output documents)
        ├── [pdf]/                      
            ├── doc0101-label1.pdf      
            ├── doc0102-label2.pdf
            ├── doc0201-label3.pdf
            └── Report-Label.pdf 
        ├── [text]/                    
            ├── doc0101-label1.txt      
            ├── doc0102-label2.txt
            └── doc0201-label3.txt           
    ├── .gitignore
    ├── config.ini                    (config file)
    ├── doc0101-label1.md             (public output documents) 
    ├── doc0102-label2.md
    ├── doc0201-label3.md
    └── README.txt                    (cumulative documents - searchable) 

========
rivt-doc
========

rivt-doc is an open source framework that faciliates working with rivt files.
It includes an editor, typesetting and mnay utilities and extensions that
reduce the steps needed to produce rivt documents. rivt-doc may be installed on
every major OS platform as set of system programs, or as a single, portable zip
file. The framework can also be implemented as a cloud service. It includes:

- Python 3.8 or higher 
- rivt Python library and dependencies
- VSCode + extensions 
- LaTeX 
- Github 

The minimum software needed to run rivt is:

- Python 3.8 or higher 
- rivt Python library and dependencies

[rivt-doc User Manual](https://www.rivt-doc.net>)

============= =============================================================
Keystroke             VSCode rivt profile shortcut description
============= ==============================================================

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

============================================== ===============================
VSCode extension                                       Description
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

VIEWER
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
'''
