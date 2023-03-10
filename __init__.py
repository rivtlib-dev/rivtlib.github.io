#! python
''' See https://rivtDocs.net  for user manual

Introduction
============

rivt is a Python package that processes a calculation oriented plain text
markup language - rivtText. It runs on any platform that supports Python 3.8 or
later and prioritizes simplicity, universal access and reports in its design.

rivtText wraps and extends the markup language reStructuredText (reST) defined
at https://docutils.sourceforge.io/rst.html. A rivt document begins with
the import statement:

import rivt.text as rv 
 
This Python module exposes four API functions:
    
rv.R(rvtS) - specify repo and report information (occurs first and only once)
rv.I(rvtS) - insert static text, images, tables and math
rv.V(rvtS) - calculate values from equations
rv.T(rvtS) - calculate tables and functions using Python statements 

A rivt document is made up of an arbitrary collection of the four methods. Each
method takes a single literal string argument, rvtS. When running in an
IDE (e.g. VSCode), methods can be run interactively using the standard cell
decorator (# %%). Parameters in rv.R() will generate documents in UTF, PDF or
HTML formats.

rivt is designed for single simple calculations as well as large, extensive
reports. The rivt report folder structure shown below is designed to
support both. Folder names are shown in brackets. The four top-level folder
names (text, resource, report and site) are required verbatim. Other file names
are combinations of specified prefixes and user titles. Folder and file names
and prefixes that are fixed are shown as *name*. Underscores and hyphens that
separate words in file and folder names are stripped out when used as document
and division names in the document.

Document input files are separated into folders labeled text and resource.
Files in the text folder are shareable rivtText files that contain the primary
calculation information. The resource folder includes supporting binary files
(images, pdf etc.) and other files that may include confidential project
information or copyrighted material. The resource folder is not designed to
share.

Output files are written to three folders, depending on the output type. The
UTF8 output is written to a README.txt file within the text folder. It is
displayed and searchable on version control platforms like GitHub. PDF output
is written to the report folder, and HTML output to the site folder.

Folder Structure Example (folders in [])
========================================

- [*rivt_*Design-Project] (user project and report name)
    - [*text*]
        - README.txt                        (project abstract)
        - units.py                          (units over-ride)
        - [*r0101_*Gravity-Loads]           (rivt document title)
            - *r0101.py*                    (file name) 
            - README.txt                    (utf output file)
            - data1.csv                     (a source file)
            - functions1.py                 (a function file)
        - [*r0102_*Seismic-Loads] 
            - *r0102.py*
            - README.txt
            - data2.csv 
            - functions2.py 
        - [*r0201_*Pile-Design] 
            - *r0201.py*
            - README.txt
            - paragraph1.txt
            - functions3.py 
    - [*resource*]
            - report_gen.txt                (report generation style)
            - site_gen.txt                  (website generation style)
            - pdf_style.sty                 (LaTeX style override)
            - utf_style.txt                 (utf style override)
            - project_data.xls              (project data)
        - [*rv01_*Overview-and-Loads]       (division title)
            - image1.jpg
        - [*rv02_*Foundations]   
            - image2.jpg
            - attachment.pdf    
    - [*report*]                            (PDF document output files)
        - r0101_Gravity-Loads.pdf
        - r0102_Seismic-Loads.pdf
        - r0201_Pile-Design.pdf
        - Design-Project.pdf                (PDF collated report)
    - [*site*]                              (HTML site)
        - [*resources*]             
            - image1.png
            - image2.png
            - html_style.css                (HTML style override)
        - index.html                        (table of contents)
        - s0101_Gravity-Loads.html
        - s0102_Seismic-Loads.html
        - s0201_Pile-Design.html

The API is designed so that only files in the text folder are uploaded for
version control and sharing. They are the essential core of the calculation -
the text, equations, functions, tables and image references. Files in the
resource folder are not shared and are typically binary and proprietary files
such as images, pdf attachments and proprietary data (e.g. client contact
information and costs). This folder and file structure makes it easy to share
and apply version control on the primary calculation inputs.

Commands and Tags
=================

rivtText syntax includes arbitrary text, commands, tags and simple (single
line) Python statements. Commands read or write files in and out of the
calculation and are denoted by || at the beginning of a line. Tags format a
line of text and are generally denoted with _[tag] at the end of a line and
<tag> for inline text. Block tags start the block of text with _[[tag]] and end
with _[[end]].

Command parameters are separated by |. In the summary below, user parameter
options are separated by semi-colons for single value selections and commas for
lists. The first line of each method specifies formatting and section labeling
for that rivt-string. The method label can be a section or paragraph title, or
used for navigation (see tags for syntax).

======= ===================================================================
name                     API Functions (VSCode snippet prefix)
======= ===================================================================

repo    rv.R("""label | folder;default | int;utf;pdf;html;both | width,page
(rvr)
                ||text ||table ||github ||project ||append

                """)

insert  rv.I("""label | docs_folder;default
(rvi)
                ||text ||table ||image ||image2 

                """)

values  rv.V("""label | docs_folder;default | sub;nosub | save;nosave
(rvv)
                = ||value ||list ||function

                ||text ||table ||image ||image2 

                """)

tables  rv.T("""label | docs_folder;default | show;noshow
(rvt)
                Python simple statements
                (any valid expression or statment on a single line)

                ||text ||table ||image ||image2 

                """)

exclude rv.X("""any text

                used to modify a function for comments and debugging

                """)

=============================================================== ============
    command syntax and description (VSCode snippets)                 API
=============================================================== ============

|| github | repo_name; none | readme; noneparam |                      R 
    (git)     github repo parameters

|| project | file_name | /docfolder; default                           R
    (pro)    .txt; rst; csv; syk; xls | project info folder

|| append | file_name | ./docfolder; default / resize;default          R
    (app)    .pdf; .txt | pdf folder / rescale to page size

|| list | file_name  | [:];[x:y]                                       V
   (lis)   .csv;.syk;.txt;.py | rows to import

|| values | file_name | [:];[x:y]                                      V
   (val)    .csv; .syk; .txt; .py | rows to import

|| functions | file_name | docs; nodocs                                V
    (fun)      .for; .py; .c; .c++; .jl | insert docstrings

|| image  | file_name  | .50                                         I,V,T
   (img)   .png; .jpg |  page width fraction

|| image2 | file_name  | .40 | file_name  | .40                      I,V,T
   (img2)   side by side images

|| text | file_name | shade; noshade                                 I,V,T
   (tex)   .txt; .py; .tex | shade background

|| table | file_name |  [:] | 60 r;l;c                               I,V,T
   (tab)   .csv;.rst file | rows | max col width, locate text

============================ ============================================
 tag syntax (one per line)                     description 
============================ ============================================

I,V,T Line Formats:
text _[b]                       bold line 
text _[c]                       center line
_[date]                         date insert
text _[e]                       equation label, autonumber
text _[f]                       figure caption, autonumber
text <#>                        footnote, autonumber
text _[foot]                    footnote description 
_[-]                            horizontal divider insert
text _[i]                       italicize line
<reference, opt. label>         internal link, section etc
latex equation _[x]             LaTeX equation format
text _[r]                       right justify line
text _[s]                       sympy equation
<sympy text>                    sympy inline (no commas)
_[page]                         new page (PDF)
_[time]                         time (insert)
text _[t]                       table title, autonumber
<http: address, opt. label>     url reference, http:\\xyz


I,V,T Block Formats:
_[[c]]                          center text block
_[[o]]                          code text block
_[[e]]                          end of block
_[[l]]                          literal block
_[[r]]                          right justify text block
_[[x]]                          LateX block
_[[m]]                          LaTeX math block

V Formats: 
a = n | unit, alt | descrip     assign tag =; units and description
a := b + c | unit, alt | n,n    result tag :=; units and decimals

The first line of a rivt file is always import rivt.text as rv. The import
statement must precede the Repo method rv.R(rs) which is the first method and
occurs once. rv.R is followed by any of the other three methods (or X method)
in any number or order. rv.R(rs) sets options for repository and report output
formats.

File format conventions incorporate the Python formatter pep8. Method
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

The ||project command imports data from the resource folder. Its formatted output depends on the file type.

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

Table of values
a1 = 10.1    | unit, alt | description
d1 = 12.1    | unit, alt | description

An equation tag labels it with a description and auto number. The <= tag
triggers the evaluation of an equation and specifies the result units and
printed decimal places in the equation and results. Decimal places are retained
until changed.

Example equation tag - Area of circle  _[e]
a1 <= 3.14(d1/2)^2 | in^2, cm^2 | 2,2

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

rv.X("""skip this string

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

rivtDocs
========

The minimum software needed to run rivt with plain text output is a Python
installation and a plain text processor. rivtDocs is an installer that
integrates five open source programs to provide a complete document production
system:

- Python 3.8 or higher (required)  
- rivt + other Python libraries (required)
- VSCode + extensions (recommended for efficiency)
- LaTeX (recommended for output quality)
- Github (recommended for collaboration and version control)

rivtDocs installs as a system level program or portable folder, and is
available for every OS platforms. It alos runs in the cloud using GitHub
CodeSpaces or other cloud service providers. Installation details are provided
in the [rivtDocs User Manual](https://www.rivtDocs.net>)
'''
