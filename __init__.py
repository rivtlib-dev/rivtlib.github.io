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

import rivt.text as rv 
 
This Python module provides four API functions:
    
rv.R(rvtS) - specify repo and report information (occurs first)
rv.I(rvtS) - insert static text, images, tables and math
rv.V(rvtS) - specify and calculat values from equations
rv.T(rvtS) - run rivt and external tools 

A rivt document is made up of an arbitrary sequence of three methods, after the
initial rv.R. Each method takes a single literal string argument - rvtS. When
running in an IDE (e.g. VSCode), methods may be run interactively using the
standard cell decorator (# %%). The rv.writedoc function generates documents in
UTF, PDF or HTML formats.

rivt is designed for both simple short documents and extensive reports. The
rivt folder structure shown below supports both. A project with rivt documents
requires four top level folders within the parent folder. The two top-level
folder names are *rivtpublic-*project-name, and *rivtprivate-*project-name.
Folder and file name prefixes that are fixed are shown as *name*. Sub folders
are combinations of specified prefixes and user titles. Hyphens that separate
words in file and folder names are stripped out when used as document and
division names in the document. Sentence case is also applied.

The *rivt-* folder contains most of the document input information as text
files. The resource folder includes supporting binary files (images, pdf etc.)
and other files that may include confidential project information or
copyrighted material. The resource folder is not designed to share.

Output files are written to three folders, depending on the output type. The
UTF8 output is written to a README.txt file within the rivt folder. It is
displayed and searchable on version control platforms like GitHub. PDF output
is written to the report folder, and HTML output to the site folder.

Folder Structure Example (folders in [])
========================================

- [project-folder] (may contain arbitrary folders besides the required four)
    - [*rivtpublic-*project-name]
        - README.md                     (project table of contents)
        - units.py                      (units over-ride)              
        - rivt.ini                      
        - [*r0101-*gravity-loads]       (rivt document title)
            -[*data*]      
                - data1.csv             (a data source file)
                - functions1.py         (a function file)
            - *r0101.py*                (rivt file name) 
            - README.md                 (markdown output)
        - [*r0102-*seismic-loads] 
            -[*data*]      
                - data2.csv 
                - functions2.py 
            - *r0102.py*
            - README.md
        - [*r0201-*pile-design] 
            -[*data*]                      
                - paragraph1.txt
                - functions3.py 
            - *r0201.py*
            - README.md
    - [*rivtprivate-*project-name]
        - [*r00-*config]
            - pdf_style.sty            (LaTeX style override)
        - [*r01-*overview-and-loads]   (division title)
            - image1.jpg
            - project_data.txt         (project data)
        - [*r02-*foundations]   
            - image2.jpg
            - attachment.pdf    
        - [*docs*]                     (pdf and html output files)
            - [*resources*]             
                - image1.png
                - image2.png
                - html-style.css           
            - rv0101-gravity-loads.pdf
            - rv0102-seismic-loads.pdf
            - rv0201-pile-design.pdf
            - project-name.pdf              
            - index.html                    
            - rv0101-gravity-loads.html
            - rv0102-seismic-loads.html
            - rv0201-pile-design.html

The API is designed so that only files in the text folder are uploaded for
version control and sharing. They are the essential core of the calculation -
the text, equations, functions, tables and image references. Files in the
resource folder are not shared and are typically binary or proprietary files
such as images, pdf attachments and proprietary data (e.g. client contact
information and costs). This folder and file structure makes it easy to share
and apply version control on the primary calculation inputs.

Commands and Tags
=================

rivtapi syntax includes arbitrary text, commands, tags and simple (single
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

repo    rv.R("""label | std out width
(rvr)
                ||project ||append

                """)

insert  rv.I("""label 
(rvi)
                ||text ||table ||image

                """)

values  rv.V("""label | sub;nosub 
(rvv)

                = =: ||text ||table ||image ||value ||list ||dict

                """)

tools  rv.T("""label | hide;show
(rvt)
                Python simple statements
                (any valid expression or statment on a single line)

                ||text ||table ||image ||value ||list ||dict

                """)

exclude rv.X("""any text

                used for comments and debugging

                """)

write   rv.Write()

=============================================================== ============
    command syntax and description (snippet)                         API 
=============================================================== ============

|| append | folder | file_name                                        R
    (app)   pdf folder | .pdf; .txt  

|| project | folder | file_name | text type                           R
    (tex)   .txt; .tex; .html | plain; tags; latex

|| text | folder | file_name | text type                             I,V
    (tex)   .txt; .tex; .html | plain; tags; code; math; latex

|| image  | folder | file_name, .. | .50, ..                         I,V
    (img)   .png; .jpg |  page width fraction

|| table  | folder | file | 60,r;l;c | [:]                           I,V
    (tab)   .csv; syk; xls  | max col width, locate | rows
    
|| values | folder | file | type |                                    V
    (val)    .csv; .xlsx;  | list, dict, rivt

============================ ============================================
 tags                                   description 
============================ ============================================

I,V line formats:        
---- can be combined 
text _[b]                       bold 
text _[c]                       center
text _[i]                       italic
text _[r]                       right justify
---------
text _[u]                       underline   
text _[m]                       LaTeX math
text _[s]                       sympy math
text _[e]                       equation label and autonumber
text _[f]                       figure caption and autonumber
text _[t]                       table title and autonumber
text _[#]                       footnote and autonumber
text _[d]                       footnote description 
_[line]                         horizontal line
_[page]                         new page
address, label _[link]          url or internal reference

I,V  block formats:          
---- can be combined 
_[[b]]                          bold
_[[c]]                          center
_[[i]]                          italic
_[[p]]                          plain  
-------
_[[s]]                          shade 
_[[l]]                          LateX
_[[h]]                          HTML 
_[[q]]                          quit block

V calculation formats: 
a = n | unit, alt | descrip    declare = 
a := b + c | unit, alt | n,n   assign := 

The first line of a rivt file is always *import rivt.rivtapi as rv* followed by
the Repo method rv.R(rvtxt) which occurs once. rv.R is followed by any of the
other three methods in any number or order. rv.R(rvtxt) sets options for
repository and report output formats.

File format conventions follow the Python formatter pep8. Method names start in
column one. All other lines must be indented 4 spaces which faciliates section
folding, bookmarks and legibility.

The first line of each rivt method sets the section title and section
parameters. 

============================================================================
rivt example
============================================================================

import rivt.rivtapi as rv

rv.R("""Introduction | rgb background, foreground

The Repo method (short for repository or report) is the first method of a rivt
doc and specifies repository settings and output formats.

The setting line specifies the section label and and background color if any.
If the label is preceded by a two dashes "--", the the label is only a
reference and a new section is not started. If the color parameter (applies to
PDF and HTML output) is ignored then the default black text and no background
is used.

The ||github command defines a project README.md file in the public r00 folder
and the GitHub repository where public project files are uploaded. It
overwrites any existing README file.

|| github | file | upload repository | 

The ||project command imports data from the private r00 folder. Its formatted
output depends on the file type.

|| project | file | default

The ||append command attaches PDF files to the end of the document.

|| append | file1 | title1
|| append | file2 | title2

""")

rv.I("""Insert method | rgb background, foreground

The Insert method formats static, descriptive information as opposed to
dynamic calculations and values.

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

rv.V("""Value method | rgb background, foreground

The Value method assigns values to variables and evaluates equations. The
sub;nosub setting specifies whether equations are also fornatted with
substituted numerical values. The save;nosave setting specifies whether
equations and value assignments are written to a values.txt file for reuse
in other docs. The write mode is not triggered in interactive mode. 

Example of values list
a1 = 10.1    | LBF, N | a force
d1 = 12.1    | IN, CM | a length

The equal tag triggers the assignment of a value. A block of values terminated with
a blank line are formatted as a table.

Example equation tag - Area of circle  _[e]
b1 := 3.14(d1/2)^2 | in^2, cm^2 | 2,2

An equation tag labels it with a description and auto number. The colon-equal tag
triggers the evaluation of an equation and specifies the result units and
printed decimal places in the equation and results. Decimal places are retained
until changed.

The ||value command imports values from a csv file, where each row includes the
variable name, value, primary unit, secondary unit, description and equation
where applicable.

|| value | file | type | [:]

""")

rv.T("""Tool method summary | print;noprint | include

The Tool method includes Python code. 
imports. Four libraries are imported by rivt and accessed with the following
names:

pandas: pd.method()
numpy: np.method()
matplotlib: mp.method()
sympy: sy.method()

Examples of single line Python statements for defining functions and reading or
writing a file include:

def f1(x,y): z = x + y; print(z); return

with open('file.csv', 'r') as f: input = f.readlines()

var = range(10)
with open('fileout.csv', 'w') as f: f.write(var)

""")

rv.X("""skip string

Skips evaluation of the string - is used for review comments, checking and
editing.

""") 

============== =========================================================
Keystroke                   VSCode shortcuts and rivt extensions
============== =========================================================

alt+q                rewrap paragraph with hard line feeds
alt+.                select correct spelling under cursor
alt+8                insert date
alt+9                insert time

ctl+alt+x            reload window
ctl+alt+u            unfold all code
ctl+alt+f            fold code level 2 (rivt sections visible)
ctl+alt+a            fold code - all levels
ctl+alt+t            toggle local fold
ctl+alt+e            toggle explorer sort order
ctl+alt+s            toggle spell check
ctl+alt+g            next editor group
ctl+1                focus on first editor
ctl+2                focus on next editor
ctl+3                focus on previous editor
ctl+8                focus on explorer pane
ctl+9                focus on github pane     

ctl+shift+u          open URL under cursor in browser
ctl+shift+s          open GitHub rivt README search
ctl+shift+a          commit all 
ctl+shift+z          commit current editor
ctl+shift+x          post to remote   


rivt
====

The minimum software needed to run rivt with markdown output is:

- Python 3.8 or higher (required)  
- rivt + a dozen Python libraries (required)

A complete rivt system also includes:

- VSCode + extensions (recommended for efficiency)
- LaTeX (recommended for output quality)
- Github (recommended for collaboration and version control)

rivt-sys installs the complete rivt system in a portable folder, and is
available for every OS platforms. 

rivt also runs in the cloud using GitHub CodeSpaces or other cloud service
providers. Installation details are provided in the [rivtDocs User
Manual](https://www.rivt-sys.net>) '''
