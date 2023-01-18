---
layout: default
---

<table style="width:75%">
<colgroup>
  <col width="25%" />
  <col width="25%" />
  <col width="25%" />
</colgroup>
<thead>
<tr class="header">
  <th style="text-align: center;border:none"><a href="https://rivtdocs.net"><b>rivtDocs (installers)</b></a></th>
  <th style="text-align: center;border:none;background-color:#959396"><a href="https://rivtcode.net"><b>rivt (source code)</b></a></th>
  <th style="text-align: center;border:none"><a href="https://rivtdocs.net/search"><b>rivtSearch (GitHub)</b></a></th>
</tr>
</thead>
<tbody>
<tr>
  <td style="text-align:center;border:none"><a href="https://rivtdocs.net"><img src="./assets/img/rivtdocs03.png" width="95" height="70" /></a></td>
  <td style="text-align: center;border:none"><a href="https://rivtcode.net"><img src="./assets/img/rivt03.png" width="100" height="75"/></a></td>
  <td style="text-align: center;border:none"><a href="https://rivtdocs.net/search"><img src="./assets/img/search03.png" width="105" height="80" /></a></td>
</tr>
</tbody>
</table>

---------------------------

# Share Docs and Calcs Anyone Can Edit and Check

--------------------------

[<b>[rivt source code on GitHub]</b>](https://github.com/rivtDocs/rivt)

## **rivt** Overview

**rivt** is a Python package providing an API for **rivtText**, a simple,
readable document markup language designed for calculations. **rivtText** wraps
and extends [reStructuredText(reST).](https://docutils.sourceforge.io/rst.html). 
Ouptut documents include UTF8, HTML and PDF from the same **rivtText** file.

The program design prioritizes three principles:

- **Cut and Paste** - docs are plain text
- **Integration** - Python libraries connect broadly with numerous data sources
- **Legibility** - rivtText syntax is defined by less than 30 intuitive terms

The **rivt** API uses fixed file and folder conventions for input and output to
simplify formatting, navigation, and report assembly. Folder names are shown in
brackets. Fixed folder and file names and prefixes are shown italicized.


**rivt Folder Structure**

- **[*rivt*_project_name]** (user project_name)
    - **[text]**
        - **[*rv00_config*]** (calc configuration data)
            - units.py
            - config.py
        - **[*rv0101*_division_name]**  (folder report division name)
            - *rv0101*_doc_name.py (file name) 
            - README.txt (doc output file)
            - chart.csv (doc source file)
            - functions.py (doc function file)
        - **[*rv0102*_division_name]** 
            - *rv0102*_doc_name.py
            - README.txt
            - chart1.csv 
            - functions1.py 
         - **[*rv0201*_division_name]**
            - r0201_doc_name.py
            - README.txt
            - paragraph.txt
   - **[resource]**
        - **[r00]** (report configuration data)
            - pdf_style.sty
            - project_data.syk
            - *report.txt*
        - **[r01]**
            - image1.jpg
        - **[r02]**
            - image2.jpg
            - attachment.pdf    
   - **[reference]**
        - **[user_folders]** (files not used in docs)
            - file1
            - file2
    - **[report]** (pdf output files)
        - r0101_loads.pdf
        - r0102_foundation.pdf
        - r0201_floor.pdf
        - r0202_roof.pdf
        - report.pdf
    - **[site]** (html output files)
        - **[resources]**
            - image1.png
            - image2.png
        - index.html
        - s0101_loads.html
        - s0102_foundation.html
        - s0201_floor.html
        - s0202_roof.html

The four top-level folder names (text, resource, report and site) are required.
Other file names are user determined using the specified prefixes. Underscores
that separate words in file and folder names are stripped out when used as
document and division names in the report. The API is designed so that only
files in the text folder are uploaded for version control and sharing. They are
the essential core of the calculation - text, equations, functions, tables and
image references. Files in the resource folder are not shared and are typically
binary files such as images, pdf attachments and proprietary data (e.g. client
contact information and costs). This folder and file structure makes it easy to
share and assert version control on the primary calculation inputs. 

A rivt file is a Python file that imports rivtapi and calls one of four
functions on rivt-strings. Rivt-strings are free-form plain text strings
enclosed in triple quotes that include commands and tags defining the
calculation and formatting. rvddnn_docname.py is the file name where dd is the
division number, nn is the subdivision number and ddnn is the document number.
The text folder includes all of the plain text input files and output doc
files.

Refer to the [rivt user manual.](https://rivtmanual.net)