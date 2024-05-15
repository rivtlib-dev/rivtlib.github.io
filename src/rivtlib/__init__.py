#! python
''' **rivt** is a lightweight markdown language for writing, organizing and
sharing engineering documents. **rivtlib** is a Python library for processing
rivt files. It runs on any platform that supports Python 3.11 or later.
**rivtlib** is designed for both simple one-off documents and multi-file
reports running to hundreds of pages. 

**rivt** and **rivtlib** are distributed under the open source MIT license and
are designed to work as a system with four established open souce projects:

- Interpreter - Python and third party open source libraries
- IDE - VSCode and extensions
- Typesetting - Latex TexLive Distribution
- Version control - GitHub

The rivt system can be downloaded as a portable zip file for Windows or
installed through a shell script on all OS's. It is also available as an online
service at https://rivtonline.net.

A rivt file imports **rivtlib**, which exposes 6 API functions:

*import rivtlib.rivtapi as rv*

rv.R(rS) - execute shell scripts (Run)
rv.I(rS) - insert static text, images, tables and math equations (Insert)
rv.V(rS) - evaluate values and equations (Values)
rv.T(rS) - execute Python functions and scripts (Tools)
rv.X(rS) - skip rivt-string processing (eXclude)
rv.W(rS) - output formatted rivt document (Write)

where rS is a triple quoted Python string. For clarity and simplicity rivt
implements a file and folder structure, wraps the reStrucutedText markup
language (see https://quickrestructuredtext.com), indents the input, and
includes several commands and tags (See user manual at https://rivt.net).

Commands
--------

A rivt command defines file processes and starts with | or || in the first
indented column.

================ ===============================================================
 API (snippet)                     Command Overview
================ ===============================================================

Run (run)            rv.R("""section label | pass;redact | color;none


                         """)

Insert (ins)         rv.I("""section label | pass;redact | color;none
                        
                         | .png, .jpg, .svg -- images
                         | .txt -- plain, sympy, rivt
                         | .tex -- latex
                         | .csv -- tables
                         | .pdf -- append 

                         """)

Values (val)         rv.V("""section label | pass;redact | color;none
                
                         | .png, .jpg, .svg -- images
                         | .txt -- equations, data  
                         | .csv -- values, data
                         | .xls -- data

                         """)

Tools (too)          rv.T("""section label | pass;redact | color;none
                

                         """)

Exclude              rv.X("""any API function

                         When a function is changed to X (by changing the
                         function letter) it is skipped (not evaluated). The
                         function may be used for testing, debugging and
                         comments.

                         """)

Write (wri)          rv.W("""doc; report

                         | output
                         | files
            
                          """)

The rv.W() function generates formatted documents in text (.txt), HTML (.html)
and PDF (.pdf) and formatted reports in reStructuredText (README.rst), HTML
(.html) and PDF (.pdf)

In VSCode each API function or groups of functions may be run interactively
using the standard cell decorator *# %%*. Interactive output (and output to
stdout when a rivt file is run from a terminal) is formatted as utf-8 text.


Tags
----

A rivt tag evaluates and formats text. Line tags are added at the end of a
line. Block tags are inserted at the beginning and end of a text block.
reStructuredText markup may also be used for formatting
(https://quickrestructuredtext.com).

===================== ========= ========================== ==================
 tags                   scope       description               API scope  
===================== ========= ========================== ==================
text _[u]               line        underline                   I                             
text _[r]               line        right justify               I                        
text _[c]               line        center                      I                 
text _[bc]              line        bold center                 I     
text _[bi]              line        bold italic                 I
text _[s]               line        numbered sympy              I
text _[m]               line        numbered latex math         I                           
text _[t]               line        numbered table              I
text _[bs]              line        bold numbered sympy         I     
text _[bl]              line        bold numbered latex         I    
label _[o]              line        lookup values               V             
title _[v]              line        numbered values table       V                                
label _[e]              line        numbered equation           V                                
var := a                line        declare value               V
var = a + b             line        assign value                V
text _[f]               line        numbered figure             V,I
text _[#]               line        footnote (autonumber)       V,I
text _[d]               line        footnote description        V,I   
_[page]                 line        new page                    V,I
_[[p]]                  block       start monospace             I 
_[[l]]                  block       start LaTeX                 I
_[[e]]                  block       end block                   I



rivt file example
-----------------

import rivtlib.rivtapi as rv

rv.R("""Introduction | pass; redact | nocolor

    The first line of any method is the heading line, which starts a new
    document section. If the section heading is preceded by two dashes (--) it
    becomes a section reference and a new section is not started. The toc
    parameter specifies whether a document table of contents is generated and
    inserted at the top of the document (not to be confused with a report table
    of contents). The page number is the starting page number for the doc, when
    processed as a stand alone document.

    File formatting conventions follow Python pep8 and ruff conventions. API
    function declarations start in column one. All other lines are indented 4
    spaces to facilitate section folding, bookmarks and legibility. The first line
    of each function defines the heading for a new document section, followed by
    section parameters. New sections may be suppressed by prepending the heading
    label with a double hyphen (--).


    """)

rv.I("""The Insert method | pass; redact | nocolor 

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

rv.V("""The Values method |  pass; redact | nocolor 

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

rv.W("""docs

    """)



Folders
-------

rivtlib can process single rivt files with no file references, but typically it
is used to generate reports from pre-existing files organized in the structure
shown below.

A rivt report is generated from the folder structure illustrated below. rivt
documents are organized into divisions. Document inputs and outputs may be
stored in or directed to publically shareable or private foldrers. Reports is
formatted with divisions, subdivisions and sections.

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


VSCode rivt profile
--------------------

============= ==============================================================
Keystroke            description
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
