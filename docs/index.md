---
layout: default
---

<table>
<colgroup>
  <col width="30%" />
  <col width="30%" />
  <col width="30%" />
</colgroup>
<thead>
<tr class="header">
  <th>rivt (API)</th>
  <th>RivtCalc (installers)</th>
  <th>RivtDocs (documentation)</th></tr>
</thead>
<tbody>
<tr>
  <td><a href="https://github.com/rivtcalc/rivt"> <img src="./assets/img/rivt_install.png" width="50" height="35" /></a></td>
  <td><a href="https://github.com/rivtcalc/rivtinstall"> <img src="./assets/img/rivt_install.png" width="50" height="35" /></a></td>
  <td><a href="https://github.com/rivtcalc/rivtdoc"> <img src="./assets/img/rivt_install.png" width="50" height="35" /></a></td>
</tr>
</tbody>
</table>

## Introduction

Open source software tools applied to general engineering calculations will
increase sharing and reuse.

Since engineering technologies change slowly, design procedures are often fixed
by legal codes and standards that persist for decades. The core of engineering
work lies in understanding established technologies and then fitting those
to specific project requirements. Calculations define how things fit together. 
If they are easy to share and edit, a prior similar design should be an efficient starting point for a new design. This intial draft can then be refined to a final design and reshared in a virtuous cycle.  

Through this sharing process the engineering professions have an opportunity to
produce large, general calculation libraries that can be recombined in
efficient and productive ways. The model of shared, incremental improvement
using text-based documents has proven very effective in open source software
programming. An extension of the approach to engineering calculations is
natural.

A number of powerful calculation programs exist, but they include barriers to
widespread sharing (see table). Most of them are commerical with high initial
and recurring software costs and strict limitations on number of computing
devices. File formats and features often change in a way that require continual
program upgrades or subscriptions. File incompatibility between different
programs requires multiple software purchases and rewrites. And they do not
produce collated reports or easily allow version control.

Taken together these are barriers to widespread calculation sharing. Instead
they promote rewriting nearly identical calculations thousands of times,
sometimes incomplete, confusing organization or with errors. The barriers to
sharing also slow technology transfer, which almost always includes understanding of the underlying calculations.

**rivt** is an open source Python API that minimizes these barriers to sharing
and collaboration. It

**Table: Program Comparison**

<img src="./assets/img/table1.png" width="1000" height="180" />

## rivtcalc Overview

**rivtcalc** is an open source software stack for writing calculation documents. It
defines the **rivtText** markup language and a default installation that
includes **rivtlib**, **VSCode**, and **Github**. **rivtText** is a plain text,
human readable language built on restructuredText. It can be used to write
standalone calculations or included in any Python program. **rivtlib** is the
Python library and API that processes **rivtText**. **VSCode** and **Github**
are the extensible, customizable editor and searchable repository system from
Microsoft.

**rivtcalc** can be installed on the desktop or mobile devices, or run remotely in
the cloud.  The minimum software needed to process rivtText (with text output
only) is Python 3.8 and above plus a few Python libraries and a plain text
processor.  This minimum implementation can be explored online at 
[**link to repl.it**](https://repl.it)

For efficient workflow and formal document production the minimum **rivt**
installation requires: 

1. Python 3.8 or above + libraries
2. VSCode + extensions
3. LaTeX 
4. Github account

**rivtcalc** installers are available for every OS platforms.  **rivt** in the cloud
is discussed using GitHub CodeSpaces in the documentation here 
[**link to rivtDocs**](https://github.com/ShareCalcs/rivtdocs). Installation 
programs are provided here - [**link to rivt**](https://github.com/ShareCalcs/rivt)


## rivtText Overview

An API for **rivtText** is the **rivt** Python package and API that includes five methods:
R(rs), I(rs), V(rs), T(rs), X(rs). The argument rs is a triple quoted Python
string containing rivtText commands and tags. 

**rivtText** was designed for simplicity and readability. It includes commands,
tags, reStructuredText (reST) markup and native Python code. **rivt** strings
are interpreted line by line, as Python itself is. Lines that begin with ||
process external data files. Lines that terminate with [tag]_ format output.
Tags that end in double underscore [tag]__ format blocks of text. 

In interactive mode using an IDE (e.g. VSCode), each API call can be called
separately using the cell tag (#%%) in the preceding line. Cells can be
evaluated one at a time and the output (utf8) displayed interactively. 

In file execution mode the entire input file is executed and the formatted
calculation is written to disk as a calc (utf8) or doc (PDF or HTML). **rivt**
input files are Python files and calcs are text files. Doc files also include
project specific and copyrighted information (clients, images etc), which are typically not
shared in the generic text input and output files.
    

## **rivt** Overview

**rivt** is a Python package providing a calculation API for **rivtText**.
The API uses file and folder naming conventions to organize and assemble calcs
into a collated report. The file, folder and prefix naming divide the
calculation report into modular, easily edited and shareable components.
Folders are shown in bold, user names in italics and notes in parenthesis.

- **rivt_*project_name*** 
    - .gitignore (share text folder only)
    - .vscode (rivt settings)
    - **calcs**
        - **rv00*_config_name*** (calc configuration data)
            - units.py
        - **rv01*_calc_division_name1***  (report division name)
            - **rv0101_calc_name1**
                - rv0101_*calc_name1*.py (input file)
                - *chart1*.csv (csv resource)
                - *functions1*.py (functions resource)
                - README.txt (calc output)
            - **rv0102_calc_name2**
                - rv0102_*calc_name2*.py
                - *functions2*.py
                - README.txt
         - **rv02*_calc_division_name2***
            - **rv0201_calc_name3**
                - rv0201_*calc_name3*.py 
                - *paragraph*.txt (text file resource)
                - README.txt 
            - **rv0202_calc_name4**
                - rv0102_*calc_name4*.py
                - *functions3*.py
                - README.txt
   - **docs**
        - **d00** (project and report configuration data)
            - report.txt
            - *pdf_style*.sty
            - *project_data*.xlsx
        - **d01** (corresponds to the division calc folder)
            - *image1*.jpg
        - **d02**
            - *image2*.jpg
            - *attachment*.pdf    
    - **reports** (PDF output)
        - d0101_*calc_name1*.pdf
        - d0102_*calc_name2*.pdf
        - d0201_*calc_name3*.pdf
        - d0202_*calc_name4*.pdf
        - *report*.pdf
    - **sites** (HTML output)
        - **resources**
            - *image1*.png
            - *image2*.png
        - index.html
        - d0101_*calc_name1*.html
        - d0102_*calc_name2*.html
        - d0201_*calc_name3*.html
        - d0202_*calc_name4*.html
            
The **rivt_** prefix for the project folder, the three top-level folder names
(text, docs and files) and the two output doc folders (html and pdf) are
required. The file prefix determines the report document organization with the
form rvddnn_*filename*.py where dd is the division number and ddnn is the calc
number.  The rest of the file name is a user chosen label for the calc name.
Underscores that separate words in file and folder names are stripped out when
used in the output. 

The API is designed so that only the **calcs**
folder can be copied to version control and sharing. The folder constitutes the
essential core of the calculation. Files in the docs
folder are typically binary and proprietary files such as images, PDF
attachments and client data.

Files File type	File description rivt file (.py) input model written in RivtText
calc (.txt)	formatted UTF-8 output, written to screen and file doc (.pdf or
.html)	formatted HTML or PDF calc output written to a file report (.pdf)
collated PDF docs written to a file API Functions The rivtlib API consists of
five functions that take a rivt-string as input (only four produce output) and a
function that controls the output format. The library is imported with:

A project is started by searching **Github** README files using the primary
search term **rivt** and including additional specific terms - then cloning the
repo of interest and editing. 

```
                +-------------------------+
                |     Edit and run rivt   | 
                |         as file or      |
                |     interactive cells.  |
                +-----------||------------+
+-------------+ +-----------||------------+  
|  Write cell | |   interactive IDE?      | 
|  output to  | |  (VSCode,Spyder,Pyzo)   |
|  terminal   === YES       NO            |  
+------+------+ +-----------||------------+  
       |        +===========||============+      
       |        |    Write calc files:    |        
       +=========     utf-8, reST, TeX    |          
                +===========||============+
+=============+ +-----------||------------+
| Write doc   | |                         | +------+
| files:      | |       Write docs?       | | End  |
| HTML, PDF   === YES                  NO ===      |
+======+======+ +-------------------------+ +------+
       |        +-------------------------+ +------+
       |        |      Write report?      | | End  |
       +=========           YES        NO ===      |
                +-----------||------------+ +------+
                +===========||============+
                |    Write PDF or HTML    |
                |       report file       |
                +=========================+

```

## **rivt** Installation Overview

**rivt** may be run in a number of different ways:

1. Local install (all desktop OS). The installer does a system install of
   - Python 3.8 with science and engineering libraries
   - VSCode xxxx with extensions
   - TexLive 2022
2. Zip file (Windows only).  
    - The zip file unzips to  single folder, that may be copied
    anywhere, and includes portable versions of the following:
      - Python 3.8 with science and engineering libraries
      - VSCode xxxx with extensions
      - TexLive 2022
3. Github Codespace
      - clone environment into your repository from here [**link to rivtDocs**](https://github.com/ShareCalcs/rivt)

[**rivt User Manual**] (https://github.com/rivtcalc/rivtdocs)

