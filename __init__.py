#! python
''' See https://rivtDocs.net  for user manual

Introduction
============

rivt is a Python package that processes a calculation oriented plain text
markup language - rivtapi. It runs on any platform that supports Python 3.8 or
later and prioritizes simplicity, universal access and reports in its design.

rivtapi wraps and extends the markup language reStructuredText (reST) defined
at https://docutils.sourceforge.io/rst.html. A rivt document begins with
the import statement:

import rivt.rivtapi as rv 
 
This Python module provides four API functions:
    
rv.R(rvtS) - repository and report information (Repo)
rv.I(rvtS) - static text, images, tables and math (Insert)
rv.V(rvtS) - equations (Values)
rv.T(rvtS) - Python functions and scripts (Tools)

A rivt document is made up of an arbitrary sequence of three string methods
following the initial method rv.R. Each method takes a single literal (triple)
string argument referred to as a rivt string (rs). When running in an IDE (e.g.
VSCode), each method may be run interactively using the standard cell decorator
(# %%). The rv.writedoc() and rv.reportdoc() functions generate documents and
compilations in GitHub Markdown (ghmd), PDF or HTML formats.

rivt works for simple short documents and extensive reports. The rivt folder
structure shown below is designed to support both. A rivt project includes
top-level folder names: *rivtpublic-*project-name, and
*rivtprivate-*project-name. Folder and file name prefixes that are fixed are
shown as *name* in the example below. Sub-folders are combinations of specified
prefixes and user titles. Hyphens that separate words in file and folder names
are stripped out when used as document and division names in the document.

The *rivtpublic-* folder contains the document input in text format. The
*rivtprivate-* folder includes confidential document files including project
and clinet information or copyrighted material. The *rivtprivate-* folder is
typically not shared.

Output files are written to three folders, depending on the output type. The
Markdown output is written to a README.md file within the *rivtpublic-*
subfolder and may be read, searched and shared on version control platforms like
GitHub. The PDF and HTML output is written to the doc folder in *rivtprivate-*.

Each separate document file is both a standalone document, and a subdivision
document in an overall report structure.

Folder Structure Example (folders in [])
========================================

- [*rivtpublic-*Project-Name]       (repo name and shared public files)
    - README.md                     (project README - table of contents)
    - [*r000-config]                (public config files)        
        - units.py                  (unit over-ride)              
        - rivt.ini                  (config file)
    - [*r0101-*Gravity-Loads]       (sub-division title)
        -[*data*]                   (static data input)
            - data1.csv             (public data)
            - pic1.png              (public data)
        - *r0101.py*                (rivt file name) 
        - README.md                 (output file)
        - functions1.py             (function file)
    - [*r0102-*Seismic-Loads] 
        -[*data*]      
            - data2.csv 
            - functions2.py 
        - *r0102.py*
        - README.md
    - [*r0201-*Pile-Design] 
        -[*data*]                      
            - paragraph1.txt
            - functions3.py 
        - *r0201.py*
        - README.md
- [*rivtprivate-*Project-Name]      (private files)
    - [*r00-*config]                (private config files)
        - pdf_style.sty             (LaTeX style override)
        - project-info.txt          (private project information)
    - [*r01-*Overview-and-Loads]    (division title)
        - image1.jpg                (private data)
        - project_data.txt          (private data)
    - [*r02-*Foundations]   
        - image2.jpg
        - attachment.pdf    
    - [*docs*]                      (pdf and html output files)
        - [*resources*]             (html resources)      
            - image1.png
            - image2.png
            - html-style.css
        - index.html                (site html)                    
        - project-name.pdf          (compiled PDF report)        
        - r0101-Gravity-Loads.pdf   (subdivision outputs)
        - r0102-Seismic-Loads.pdf
        - r0201-Pile-Design.pdf           
        - r0101-Gravity-Loads.html
        - r0102-Seismic-Loads.html
        - r0201-Pile-Design.html

The API is designed for sharing files in the *rivtpublic-* folder. They
represent the core information in the document - the text, equations, functions
and tables. Files in the *rivtprivate-* folder are typically not shared. This
two-part folder and file structure simplifies protection of confidential
content, while applying version control and sharing for the primary calculation
inputs.

Commands and Tags
=================

rivt syntax includes arbitrary unicode text, commands, tags and simple (single
line) Python statements. Syntax is interepreted by the particular rivt method.
Commands read or write extrnal files denoted by || at the beginning of a line.
Command parameters are separated by |. In the summary below single parameter
options are separated by semi-colons and list parameters are separated by
commas. The first line of each method is a section label followed by section
parameters. Section labels may be hidden by prepending with a double hyphen --.

Tags format a line or block of text and are generally denoted with _[tag] at
the end of a line. Block tags start the block of text with _[[tag]] and end
with _[[q]]. The "=" and ":=" tags used in the Value method are the
exceptions.


======= ===================================================================
 name             API Functions and commands (VSCode snippet prefix)
======= ===================================================================

Repo    rv.R("""label | page
(rep)
                ||github (git)
                ||project (proj)
                ||append (app)

                """)

Insert  rv.I("""label | rgb; default
(ins)
                ||image (img)
                ||text (tex)
                ||table (tab)

                """)

Values  rv.V("""label | sub; nosub 
(val)
                ||image (img)
                ||text (tex)
                ||table (tab)
                ||declare (dec)

                """)

Tools  rv.T("""label | rgb; default; noprint | name; noname
(too)
                Python code

                """)

exclude rv.X("""any method

                A method is changed to X is not evaluated and may be used for
                comments and debugging.

                """)

write   rv.writedoc()

=============================================================== ============
    command syntax and description (snippet)                         API 
=============================================================== ============

|| append | folder | file_name                                        R
    (app)   pdf folder | .pdf; .txt  

|| github | folder | file_name                                        R
    (git)   pdf folder | .pdf; .txt  
    
|| project | folder | file_name | text type                           R
    (pro)   .txt; .tex; .html | plain; tags; latex

|| text | folder | file_name | text type                             I,V
    (tex)   .txt; .tex; .html | plain; tags; code; math; latex

|| image  | folder | file_name, .. | .50, ..                         I,V
    (ima)   .png; .jpg |  page width fraction

|| table  | folder | file | 60,r;l;c | [:]                           I,V
    (tab)   .csv; syk; xls  | max col width, locate | rows

|| declare | folder | file | type |                                   V
    (dec)    .csv; .xlsx;  | list, dict, rivt

|| assign | folder | file | type |                                    V
    (val)    .csv; .xlsx;  | list, dict, rivt

============================ ============================================
 tags                                   description 
============================ ============================================

I,V line format:        
text _[b]                       bold 
text _[c]                       center
text _[i]                       italic
text _[r]                       right justify
text _[u]                       underline   
text _[l]                       LaTeX math
text _[s]                       sympy math
text _[e]                       equation label and autonumber
text _[f]                       figure caption and autonumber
text _[t]                       table title and autonumber
text _[#]                       footnote and autonumber
text _[d]                       footnote description 
_[page]                         new page
_[address, label]               url, internal reference

I,V  block format:          
_[[b]]                          bold
_[[c]]                          center
_[[i]]                          italic
_[[p]]                          plain  
_[[l]]                          LaTeX
_[[h]]                          HTML 
_[[q]]                          quit block

V calculation format: 
a = n | unit, alt | descrip    declare = 
a := b + c | unit, alt | n,n   assign := 

The first line of a rivt file is always *import rivt.rivtapi as rv* followed by
the Repo method rv.R() which occurs once. rv.R is followed by any of the other
three methods in any number or order. rv.R() sets options for repository and
report output formats.

File format conventions follow the Python formatter pep8, and linter ruff.
Method names start in column one. All other lines must be indented 4 spaces to
facilitate section folding, bookmarks and legibility.

The first line of each rivt method defines the section title and section
parameters. 

============================================================================
rivt example
============================================================================

import rivt.rivtapi as rv

rv.R("""Introduction | rgb-fore,background; default

    The Repo method (short for repository or report) is the first method of a
    rivt doc and specifies repository settings and output formats.

    The setting line specifies the section label and colors. if any. If the
    label is preceded by two dashes "--", the the label becomes a reference and
    a new section is not started. If the color parameter (applies to PDF and
    HTML output) is omitted then default black text and no background is used.

    The ||github command specifies a project README.md file in the public r00
    folder and the GitHub repository url where public project files are
    uploaded. It overwrites any existing README file. Files may also be
    uploaded directly using standard upload procedures.

    || github | file | upload repository

    The ||project command imports data from the private r00 folder. Its
    formatted output depends on the file type.

    || project | file | default

    The ||append command attaches PDF files to the end of the document.

    || append | file1 | title1
    || append | file2 | title2

    """)

rv.I("""Insert method | rgb-fore,background

    The Insert method formats descriptive information that is static, as
    opposed to dynamic calculations and values.

    The ||text command inserts and formats text files. Text files may be plain
    text, latex, code, sympy math or include rivt tags.

    || text | file | text type
    plain; tags; code; math; latex

    Tags _[t] and _[f] format and autonumber tables and figures.

    table title  _[t]
    || table | data | file.csv | 60,r

    || image | resource | f1.png | 50
    A figure caption _[f]

    Insert two images side by side:

    || image | f2.png,f3.png | 45,35
    The first figure caption  _[f]
    The second figure caption  _[f]

    The tags [x]_ and [s]_ format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  _[x] 

    x = 32 + (y/2)  _[s]

    The url tag formats a url link.
    _[http://wwww.url, link label]

    The link tag formats an internal document link to a table, equation,
    section or paragraph title:
    _[lnk, existing label]

    """)

rv.V("""Value method | sub; nosub | rgb fore,background

    The Value method assigns values to variables and evaluates equations. The
    sub;nosub setting specifies whether equations are also printed with
    substituted numerical values. 

    Example of values list _[t]
    a1 = 10.1    | LBF, N | a force
    d1 = 12.1    | IN, CM | a length

    An table tag provides a table title and number.  The equal tag declares a
    value. A sequence of declared values terminated with a blank line are
    formatted as a table.

    Example equation tag - Area of circle  _[e]
    b1 := 3.14(d1/2)^2 | in^2, cm^2 | 2,2

    An equation tag provides an equation description and number. The
    colon-equal tag triggers the assignment of a value and specifies the
    result units and printed output decimal places in the equation and results.

    || value | file | type | [:]
    
    The ||value command imports values from a csv file, where each row includes
    the variable name, value, primary unit, secondary unit, description and
    equation where applicable.

""")

rv.T("""Tool method | print;noprint | include; exclude| rgb fore,background

    
    # The Tool method includes Python code. The "print" parameter specifies
    # whether the code is echoed in the document. The "include" parameter
    # specifies whether the code values are subsequently available (i.e. 
    # included in the document namespace).
    
    # Four libraries are imported by rivt and accessed as: 

    # pyplot: plt.method()
    # numpy: np.method()
    # pandas: pd.method()
    # sympy: sy.method()

    # Examples of single line Python statements include: 
    
    def f1(x,y): z = x + y; print(z); return
    
    # for defining functions and
        
    with open('file.csv', 'r') as f: input = f.readlines()
    var = range(10)
    with open('fileout.csv', 'w') as f: f.write(var)

    # for reading and writing files
        
    """)

rv.X("""any text

    Replacing any method letter with X skips evaluation of thhat string. Its
    uses include review comments, checking and editing.

    """) 

============== =========================================================
Keystroke                   VSCode rivt shortcuts and extensions
============== =========================================================

alt+q                rewrap paragraph with hard line feeds (80 default)
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
ctl+shift+s          open GitHub rivt README search
ctl+shift+a          commit all 
ctl+shift+z          commit current editor
ctl+shift+x          post to remote   


rivt
====

The minimum software needed to run rivt with markdown output is:

- Python 3.8 or higher 
- rivt + a dozen Python libraries 

A complete rivt system also includes:

- VSCode + two dozen extensions 
- LaTeX 
- Github account

rivt-sys installs the complete rivt system in a portable folder via a zip file,
and is available for every OS platform. rivt also runs in the cloud using
GitHub CodeSpaces or other cloud service providers. Installation details are
provided in the [rivtDocs User Manual](https://www.rivt-sys.net>)

'''
