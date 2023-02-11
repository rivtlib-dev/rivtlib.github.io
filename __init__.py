#! python
''' See https://rivtDocs.net  for user manual

Introduction
============

*rivt* is a Python package that processes the markup language *rivtText*. It runs on any platform that supports Python 3.8 or later and prioritizes universal access and processing.

*rivtText* wraps and extends the markup language reStructuredText (reST)
defined at https://docutils.sourceforge.io/rst.html. It was designed to
simplify writing and sharing engineering calculation documents. The syntax
prioritizes clarity and brevity. A *rivtText" document begins with the import
statement:

**import rivt.text as rv** 
 
which exposes four API methods:
    
rv.R(rs) - specify repo and report information
rv.I(rs) - insert static text, images, tables and math
rv.V(rs) - calculate values from equations
rv.T(rs) - calculate tables and functions using Python statements 

A rivt document is made up of a collection of methods. The single argument,
*rs*, is a *rivtText* triple quoted string. When running in an IDE (e.g.
VSCode), each separate method can be run interactively using the standard cell
decorator (# %%). Parameters in rv.R() will generate documents in UTF, PDF or HTML formats.

Document input files are separated into folders labeled *text* and *resources*.
Files in the *text* folder are shareable text files under version control that
contain the primary calculation information. The *resource* folder includes
supporting binary files (images, pdf etc.) and other files that may include
confidential project information or copyrights. The *resource* folder is not
designed to share.

Output files are written to three places. The UTF8 output is written to a
*README.txt* file within the *text* folder. It is displayed and searchable on
version control platforms like GitHub. PDF output is written to the *report*
folder, and HTML output to the *website* folder.

rivt Folder Structure (**folders in []**)
========================================

- **[*rivt_Design_Project]** (user report name after rivt)
- **[text]**
    README.txt (project description)
    - **[*rv00_config*]** (doc configuration data)
        - units.py
        - config.py
    - **[*rv0101*_Overview_and_Loads]**  (division name)
        - *r0101*_Gravity_Loads.py (doc name) 
        - README.txt (output file)
        - data1.csv (source file)
        - functions1.py (function file)
    - **[*rv0102_seismic*]**  (folder label) 
        - *r0102*_Seismic_Loads.py
        - README.txt
        - data2.csv 
        - functions2.py 
        - **[*rv0201*_Foundations]**  (division name)
        - *r0201*_Pile_Design.py
        - README.txt
        - paragraph1.txt
- **[resource]**
    - **[r00]** (report configuration data)
        - pdf_style.sty
        - project_data.syk
        - report.txt
    - **[r01]** (division resources)
        - image1.jpg
    - **[r02]**
        - image2.jpg
        - attachment.pdf    
- **[reference]**
    - **[user_folders]** (files not directly used in docs)
        - file1
        - file2
- **[report]** (pdf output files)
    - r0101_Gravity_Loads.pdf
    - r0102_Seismic_Loads.pdf
    - r0201_Pile_Design.pdf
    - Design_Project.pdf  (collated report)
- **[site]** (html output files)
    - **[resources]**
        - image1.png
        - image2.png
    - index.html  (table of contents)
    - r0101_Gravity_Loads.html
    - r0102_Seismic_Loads.html
    - r0201_Pile_Design.html

*rivtDoc* is an open source software stack for writing, sharing and
publishing engineering documents and calculations in document and online
formats. The generic stack includes:

- *Python 3.8* or greater with science and engineering libraries, 
- an IDE
- a LateX distribution
- a version controlled distribution service

The standard rivtDocs stack includes:

- *Python 3.8* with science and engineering libraries, 
- VSCode and extensions
- Texlive
- GitHub

The standard stack is available as a portable system in a single zipped folder, a system level install, or as a remote service.

Commands and Tags
=================

*rivtText* syntax includes arbitrary text, commands, tags and simple (single
line) Python statements. Commands read or write files in and out of the
calculation and are denoted by || at the beginning of a line. Tags format a
line of text and are generally denoted with _[tag] at the end of a line. The
exceptions are method labels and value assignments. Block tags start the block
of text with _[[tag]] and end with _[[end]].

Command parameters are separated by |. In the summary below, user parameter
options are separated by semi-colons for single value selections and commas for
lists. The first line of each method specifies formatting and section labeling
for that rivt-string. The method label can be a section or paragraph title, or
used for navigation (see tags for syntax).

======= ===================================================================
 method             settings, snippet prefix
======= ===================================================================

repo    rv.R("""label | folder;default | int;utf;pdf;html;both | width,n
rvr
                ||text ||table ||github ||project ||append

                """)

insert  rv.I("""label | docs_folder;default
rvi
                ||text ||table ||image ||image2 

                """)

values  rv.V("""label | docs_folder;default | sub;nosub | save;nosave
rvv
                = ||value ||list ||function

                ||text ||table ||image ||image2 

                """)

tables  rv.T("""label | docs_folder;default | show;noshow
rvt
                Python simple statements
                (any valid expression or statment on a single line)

                ||text ||table ||image ||image2 

                """)

exclude rv.X("""any text

                any commands, used for comments and debugging

                """)

=============================================================== ============
    command syntax / snippet prefix and description                 methods
=============================================================== ============

|| github | repo_name; none | readme; noneparam | R
    git        github repo parameters

|| project | file_name | /docsfolder; default                      R
    pro       .txt; rst; csv; syk; xls | project info folder

|| append | file_name | ./docfolder; default / resize;default      R
    app      .pdf; .txt | pdf folder / rescale to page size

|| list | file_name  | [:];[x:y]                                       V
    lis       .csv;.syk;.txt;.py | rows to import

|| values | file_name | [:];[x:y]                                      V
    val       .csv; .syk; .txt; .py | rows to import

|| functions | file_name | docs; nodocs                                V
    fun       .for; .py; .c; .c++; .jl | insert docstrings

|| image1 | file_name  | .50                                         I,V,T
    im1       .png; .jpg |  page width fraction

|| image2 | file_name  | .40 | file_name  | .40                      I,V,T
    im2       side by side images

|| text | file_name | shade; noshade                                 I,V,T
    tex      .txt; .py; .tex | shade background

|| table | file_name |  [:] | 60 r;l;c                               I,V,T
    tab      .csv;.rst file | rows | max col width, locate text

============================ ============================================
    tag syntax                       description: snippet prefix
============================ ===========================================

Method format:                applies only to first line of method
"""section label | ....       No hyphen;denotes section title, autonumber
"""-paragraph label | ....    Single hyphen; denotes paragraph heading
"""--bookmark label | ....    Double hyphen; denotes non-printing label

Values format:                applies only to Values rivt-string
a = n | unit, alt | descrip   tag is =, units and description: _v
a <= b + c | unit, alt | n,n  tag is <=, units and decimals: _=

Text format:                  applies to I,V and T methods
text _[p]                     paragraph heading: _p
text _[l]                     literal text: _l
text _[i]                     italic: _i
text _[b]                     bold: _b
text _[r]                     right justify line of text: _r
text _[c]                     center line of text: _c
text _[-]                     draw horizontal line: _-
text _[#]                     insert footnote, autonumber: _#
text _[foot]                  footnote description: _o

Element format:               applies to I,V and T methods
caption _[f]                  figure caption, autonumber: _f
title _[t]                    table title, autonumber: _t
sympy equation _[s]           format sympy equation: _s
latex equation _[x]           format LaTeX equation: _x
label _[e]                    equation label, autonumber: _e

Link format:                  applies to I,V and T methods
_[address, label              http://xyz, link label: _u
_[lnk, user label             section, paragraph, title, caption: _k
_[new]                        new PDF page: _n
_[date]                       insert date
_[time]                       insert time

Blocks                        tag precedes first line of block
------                        ------------------------------------------
Text format:                  applies to I,V and T method
_[[r]]                        right justify text block: _[[r
_[[c]]                        center text block: _[[c
_[[lit]]                      literal block: _[[l
_[[tex]]                      LateX block: _[[x
_[[texm]]                     LaTeX math block: _[[m
_[[shade]]                    shade text block: _[[s
_[[code]]                     * code text block: _[[o 
_[[end]]                      terminates block: _[[e

* within a Table string inserts Python code into doc (omitted by default)

The first line of a rivt file is *import rivt.text as rv*. The import statement
must precede the Repo method rv.R(rs) which is the first method and occurs
once. rv.R is followed by any of the other three methods (or X method) in any
number or order. rv.R(rs) sets options for repository and report output formats.

File format conventions incorporate the Python formatter *pep8*. Method
names start in column one. All other lines are indented 4 spaces to faciliate
section folding, bookmarking and legibility.

============================================================================
rivt calculation example
============================================================================

import rivt.text as rv

rv.R("""Introduction | inter | 80,1

The Repo method (short for repository or report) is the first method of a rivt
doc and specifies repository settings and output formats.

The setting line specifies the method, paragraph or section label, the
processing type and the output width and starting page number for the output.

The ||github command defines GitHub repository parameters and a rivt-string to
be written to the project level folder as a README file. It is specified only
once in a project, and when specified includes the text in the method. It overwrites any existing README file.

|| github | none | readme | none 

The ||project command imports data from the *resource* folder. Its formatted output depends on the file type.

|| project | file | default

The ||append command attaches PDF files to the end of the document.

|| append | file1 | title1
|| append | file2 | title2

""")

rv.I("""Insert method summary | default

The Insert method formats static, descriptive information as opposed to
dynamic calculations and values.

The ||text command inserts and formats text files. Text files are always
inserted as is, without formatting. They may include rivt commands and
tags.

|| text | file | shade

Tags _[t] and _[f] format and autonumber tables and figures.

table title  _[t]
|| table | file.csv | 60,r

|| image | f1.png | 50
A figure caption _[f]

Insert two images side by side:

|| image2 | f2.png | 35 | f3.png | 45
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

Attach PDF documents at the end of the method:

""")

rv.V("""Value method summary | default | nosub | save

The Value method assigns values to variables and evaluates equations. The
sub;nosub setting specifies whether equations are also fornatted with
substituted numerical values. The save;nosave setting specifies whether
equations and value assignments are written to a values.txt file for reuse
in other docs. The write mode is not triggered in interactive mode. 

The = tag triggers the evaluation of a value. A block of values terminated with
a blank line are formatted as a table.

**Table of values**
a1 = 10.1    | unit, alt | description
d1 = 12.1    | unit, alt | description

An equation tag labels it with a description and auto number. The <= tag
triggers the evaluation of an equation and specifies the result units and
printed decimal places in the equation and results. Decimal places are retained
until changed.

Example equation tag - Area of circle  _[e]
a1 <= 3.14*(d1/2)^2 | in^2, cm^2 | 2,2

The ||value command imports values from a csv file, where each row
includes the variable name, value, primary unit, secondary unit, description and equation where applicable.

|| value | file | default | [:]

The ||list command inserts lists from a csv, text or Python file where the
first column is the variable name and the subsequent values make up a
vector of values assigned to the variable.

|| list | file | default | [:]

The ||function command imports Python, Fortran, C or C++ functions in a
file. The function signature and docstrings are inserted into the doc if
specified.

|| function | file | default | docs;nodocs

""")

rv.T("""Table method summary | default

The Table method generates tables, plots and functions from native Python code.
The method may include any Python simple statement (single line), and
recognized commands or tags (see list above). Any library initially imported
may be used, along with pandas, numpy, matplotlib and sympy library methods,
which are imported by rivt. The four available import names are:

pandas: pd.method()
numpy: np.method()
matplotlib: mp.method()
sympy: sy.method()

Examples of common single line Python statements for defining functions and
reading or writing a file include:

def f1(x,y): z = x + y; print(z); return

with open('file.csv', 'r') as f: input = f.readlines()

var = range(10)
with open('fileout.csv', 'w') as f: f.write(var)

""")

rv.X("""skip-string - can be anything.

Skips evaluation of the string and is used for review comments, checking and editing.

""") 

================== =========================================================
Keystroke                   VSCode shortcuts with rivt extensions
================== =========================================================

alt+q                rewrap paragraph with hard line feeds
alt+8                toggle explorer sort order
alt+9                toggle spell check
ctl+.                select correct spelling under cursor

ctl+alt+x            reload window
ctl+alt+u            unfold all code
ctl+alt+f            fold code - rivt sections visible
ctl+alt+a            fold code - all levels
ctl+alt+t            toggle local fold at cursor
ctl+alt+g            open GitHub rivt README search
ctl+alt+s            open URL under cursor in browser
ctl+alt+9            insert date
ctl+alt+8            insert time

ctl+shift+e          focus on explorer pane
ctl+shift+g          focus on github pane
ctl+shift+a          commit all 
ctl+shift+z          commit current editor
ctl+shift+x          post to remote        
ctl+shift+1          focus on recent editor
ctl+shift+2          focus on next editor
ctl+shift+3          focus on previous editor
'''
