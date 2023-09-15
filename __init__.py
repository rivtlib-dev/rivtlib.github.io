#! python
''' See https://rivt-doc.net  for user manual

rivt is both an open source engineering document markdown language and the Python
library that processes it. It is written in Python as is designed to write,
assemble and share engineering documents. It runs on any platform that supports
Python 3.8 or later and prioritizes legibility, flexibility, efficiency and
universal access. rivt-doc has a number of dependencies (see below).

A rivt file is a Python file that begins with the import statement:

*import rivt.rivtapi as rv*
 
which in turn provides four API functions (referred to as Repo, Insert, Values
and Tools). Each function takes a single, triple quoted string as an
argument.

rv.R(rmS) - repository and report information 
rv.I(rmS) - static text, images, tables and math
rv.V(rmS) - equations
rv.T(rmS) - Python functions and scripts

A rivt file begins with rv.R followed by an arbitrary sequence of the
three other string methods.

When running in an IDE (e.g. VSCode), each method may be run interactively
using the standard cell decorator (# %%). Interactive output is formatted as
utf-8 text. The rv.writemd() and rv.writepdf() functions generate documents and
compilations in GitHub Markdown (ghmd) and PDF formats. 

rivt works with both simple, single file documents as well as extensive reports
with hundreds of files. Multi-file reports can be structured in an efficient
folder based framework.


rivt syntax
===========

rivt syntax includes arbitrary unicode text including rivt commands and tags. A
rivt command reads or writes external files and is denoted by || at the
beginning of a line. Command parameters are separated by |. In the summary
below parameter options are desginated with semi-colons and list parameters
with commas.

Tags format a line or block of text and are denoted with _[tag] at the end of a
line. Block tags start a block of text with _[[tag]] and end with _[[q]]. The
"=" and ":=" tags used in the Value method are exceptions.

======= ===================================================================
 name    Commands per API function (VSCode snippet prefix)
======= ===================================================================

Repo    rv.R("""label | toc; notoc | page
(re)
                ||init (ini)
                ||text (tex)
                ||append (app)

                """)

Insert  rv.I("""label | color  
(in)
                ||image (img)
                ||text (tex)
                ||table (tab)

                """)

Values  rv.V("""label | sub; nosub 
(va)
                ||declare (dec)

                """)

Tools  rv.T("""label | color | print; noprint 
(to)
                Python code

                """)

exclude rv.X("""any method

                Any method changed to X is not evaluated. It may be used for
                comments and debugging.

                """)

write   rv.writemd()
(wm)

write   rv.writepdf()
(wp)


==================================================== ==============
    command syntax                                          API 
==================================================== ==============

|| init | rel file path                                      R

|| append | rel file path                                    R

|| image  | rel file path, .. | .50, ..                      I

|| table  | rel file path | 60,r; l; c                       I

|| declare | rel file path |  print; noprint                 V

|| text | rel file path | rivt; plain                      R I V

============================ ================================= ==========
   line tags                        description                   API
============================ ================================ ===========
text _[b]                       bold                            R I V 
text _[c]                       center                          R I V  
text _[i]                       italic                          R I V  
text _[bc]                      bold center                     R I V  
text _[bi]                      bold italic                     R I V
text _[r]                       right justify                   R I V
text _[u]                       underline                       R I V   
text _[l]                       LaTeX math                        I V
text _[s]                       sympy math                        I V
text _[bs]                      bold sympy math                   I V
text _[e]                       equation label, autonumber        I V
text _[f]                       figure caption, autonumber        I V
text _[t]                       table title, autonumber           I V
text _[#]                       footnote, autonumber              I V
text _[d]                       footnote description              I V
_[page]                         new page                          I V
_[address, label]               url or internal reference         I V
a = 1.2 | unit, alt | descrip   declare =                           V
a := b + c | unit, alt | n,n    assign :=                           V

============================ ================================= ==========
   block tags                        description                   API
============================ ================================ ===========
_[[b]]                          bold                            R I V
_[[c]]                          center                          R I V
_[[i]]                          italic                          R I V
_[[p]]                          plain                           R I V
_[[q]]                          quit block                      R I V
_[[l]]                          LaTeX                             I V


The first line of a rivt file is *import rivt.rivtapi as rv* followed by the
Repo method rv.R(). rv.R is followed by any of the other three methods in any
number or order. The first line of each method is a section label followed by
section parameters. Section labels may be converted into editing references by
prepending a double hyphen --.

File format conventions follow the Python formatter pep8, and linter ruff.
Method names start in column one. All other lines must be indented 4 spaces to
facilitate section folding, bookmarks and legibility. The first line of each
rivt function defines the section title and parameters.

============================================================================
rivt example
============================================================================

import rivtlib.rivtapi as rv

rv.R("""Introduction | notoc, 1

    The Rivitinit method is the first method of a rivt file and specifies
    repository, report and document settings.

    The first line of any method is the heading line, which starts a new
    document section. If the section heading is preceded by two dashes (--) it
    becomes a section reference and a new section is not started. The toc
    parameter specifies whether a document table of contents is generated (not
    to be confused with a report table of contents). The page number is the
    starting page number for the doc when processed as a stand alone document.

    The init command specifies the name of the configuration file which is read
    from the rivt-doc folder. Report formatting can be easily modified by
    specifying a different init file.

    ||init | rivt01.ini

    The text command inserts text from an external file. Text files may be
    plain text or include rivt tags.

    ||text | private/text/proj.txt | plain
    
    The append command attaches PDF files to the end of the doc.

    || append | append/report1.pdf
    || append | append/report2.pdf

    
    """)

rv.I("""The Insert method | color 

    The Insert method formats static information e.g. images and text. The
    color command specifies a background color for the section.

    The text command inserts and formats text from external files into the
    rivt file. Text files may be plain text or text with rivt tags.

    ||text | data0101/describe.txt | rivt     

    The table command inserts and formats tabular data from csv or xls files.
    
    The _[t] tag formats and autonumbers table titles.

    A table title  _[t]
    || table | data0101/file.csv | 60,r

    The image command inserts and formats image data from png or jpg files.
`
    The _[f] tag formats and autonumbers figures.
        
    A figure caption _[f]
    || image | data0101/f1.png | 50

    Two images may be placed side by side as follows:

    The first figure caption  _[f]
    The second figure caption  _[f]
    || image | private/image/f2.png, private/image/f3.png | 45,35
    
    The tags _[x] and _[s] format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  _[x] 

    x = 32 + (y/2)  _[s]

    """)

rv.V("""The Values method |  sub; nosub 

    The Values method assigns values to variables and evaluates equations. The
    sub; nosub setting specifies whether the equations are printed a second
    time with substituted numerical values.

    A table tag provides a table title and number.  
    
    The equal tag declares a value. A sequence of declared values terminated
    with a blank line are formatted as a table.
    
    Example of assignment list _[t]
    f1 = 10.1 * LBF | N | a force
    d1 = 12.1 * IN | CM | a length

    An equation tag provides an equation description and number. A colon-equal
    tag assigns a value and specifies the result units and printed output
    decimal places in the result and equation.

    Example equation - Area of circle  _[e]
    a1 := 3.14(d1/2)^2 | IN^2, CM^2 | 1,2

    || declare | data0102/values0102.csv
    
    The declare command imports values from a csv file written by rivt when
    processing assigned and declared values from another doc in the same
    project.

""")

rv.T("""The Tools method | color 

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

rivt-doc
========

rivt-doc is the framework for writing, assembling and sharing rivt documents.
It uses a folder structure that divides a report into publically shareable and
private files. Report documents may draw from both sources.

It also includes editors and utilities designed to work with rivt, and may be
installed as a system program or used as single, portable zip file. It works
with Github as a cloud service for sharing rivt files and documents.

In the example folder structure below, fixed folder and file prefixes are shown
in [ ]. Report, division and documents names are taken from the folder and file
naming. The folder structure will generate a two level organization, with
individual rivt documents grouped into divisions. Tools are available to
generate report folder templates.

[rivtdoc]-Report-Label/               
    ├── .git
    ├── units.py                      (input: unit over-ride)
    ├── README.md                     (output: toc and summary) 
    ├── rivt01.ini                    (input: config file)
    ├── [doc0101]-div-label/          (division file and label)
        ├── [data0101]/                     (resource data)
            ├── data1.csv                   
            ├── paper1.pdf
            └── functions1.py                   
        ├── [rivt]-doc-label1.py            (input: rivt file)
        └── README.md                       (output: GFM doc)
    ├── [doc0102]/                    (division file)
        ├── data[0102]/                     (input: resource data)
            ├── data1.csv
            ├── fig1.png
            └── fig2.png
        ├── [rivt]-doc-label2.py            (input: rivt file)
        └── README.md                       (output: GFM doc)
    ├── [doc0201]-div-label/          (division file and label)
        ├── [data0201]/                     (input: resource data)                   
            ├── data1.csv
            ├── attachment.pdf
            ├── functions.py
            └── fig1.png
        ├── [rivt]-doc-label3.py            (input: rivt file)   
        └── README.md                       (output: GFM doc)
    └── [private]/                    (private files)
        ├── [temp]/                         (output: temp files)
        ├── [report]/                       (report files)
            ├── 0101-Doc Label1.pdf         (output: PDF docs)
            ├── 0102-Doc Label2.pdf
            ├── 0201-Doc Label3.pdf
            └── Report Label.pdf            
        ├── images/                         (input: optional data folders)
            ├── fig1.png
            └── fig2.png
        ├── text/    
            ├── text1.txt
            └── text2.txt
        ├── append/    
            ├── report1.pdf
            └── report2.pdf
        └── tables/
            ├── data1.csv
            └── data1.xls

rivt installation
=================

The minimum software needed to run rivt:

- Python 3.8 or higher 
- rivt Python library

A complete rivt-doc system additionally includes:

- Python libraries
- VSCode + extensions 
- LaTeX 
- Github account

rivt-doc may be installed as a system level program or as a single portable
folder via a zip file. It runs on every OS major platform and in the cloud (e.g.
GitHub CodeSpaces). [rivt-doc User Manual](https://www.rivt-doc.net>)


============== =========================================================
Keystroke         VSCode shortcuts and extensions using rivt profile
============== =========================================================

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
ctl+shift+s          open GitHub rivt README search
ctl+shift+a          commit all 
ctl+shift+z          commit current editor
ctl+shift+x          post to remote   


'''
