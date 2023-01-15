---
layout: default
---

<table>
<colgroup>
  <col width="30%" />
  <col width="30%" />
</colgroup>
<thead>
<tr class="header">
  <th style="text-align: center;border:none"><a href="https://rivtdocs.net"><b>rivtDocs (installers)</b></a></th>
  <th style="text-align: center;border:none;background-color:#959396"><a href="https://rivtcode.net"><b>rivt (source code)</b></a></th>
  <th style="text-align: center;border:none"><a href="https://rivtsearch.net"><b>rivtSearch (GitHub)</b></a></th>
</tr>
</thead>
<tbody>
<tr>
  <td style="text-align:center;border:none"><a href="https://rivtdocs.net"><img src="./assets/img/rivtdocs.png" width="85" height="60" style="border:2px solid #5c5962"/></a></td>
  <td style="text-align: center;border:none"><a href="https://rivtcode.net"><img src="./assets/img/rivt01.png" width="80" height="60" style="border:2px solid #5c5962"/></a></td>
  <td style="text-align: center;border:none"><a href="https://rivtsearch.net"><img src="./assets/img/search01.png" width="85" height="65" style="border:2px solid #5c5962"/></a></td>
</tr>
</tbody>
</table>
<p style="text-align:center; font-weight:bold"> Share Docs and Calcs Anywhere, Anytime </p>

---------------------------

## **rivt** Overview

**rivt** is a Python package providing an API for **rivtText**, a simple,
readable document markup language designed for calculations. **rivtText** wraps
and extends [reStructuredText(reST).](https://docutils.sourceforge.io/rst.html). 
Ouptut documents include UTF8, HTML and PDF from the same **rivtText** file.

The program design follows three principles:

- **Maximize Cut and Paste** - make it easy to include content from anywhere.
- **Integrate** - connect with external programs using standard interfaces.
- **Respect time** - intuitive, clear, easy to remember program conventions.

The **rivt** API uses fixed file and folder conventions for input and output to
simplify formatting, navigation, and report assembly. Folder names are shown in
brackets. Required folder and file name prefixes are shown italicized.


**rivt Folder Structure**

- **[*rivt*_user_project_name]** (user project_name)
    - **[calcs]**
        - **[*rv00*_user_config_name]** (calc configuration data)
            - units.py
            - config.py
        - **[*rv0101*_user_calc_division_name]**  (folder report division name)
            - *r0101*_calc_name.py (calc file name) 
            - README.txt (text calc output file)
            - chart.csv (text file used in calc)
            - functions.py (function file used in calc)
        - **[*rv0102*_user_calc_division_name]** 
            - *r0102*_calc_name.py
            - README.txt
            - chart1.csv 
            - functions1.py 
         - **[rv0201*_user_calc_division_name*]**
            - r0201_calc_name.py
            - README.txt
            - paragraph.txt
   - **[docs]**
        - **[d00]** (report configuration data)
            - pdf_style.sty
            - project_data.syk
        - **[d01]**
            - image1.jpg
        - **[d02]**
            - image2.jpg
            - attachment.pdf    
    - **[reports]** (pdf output files)
        - r0101_gravity.pdf
        - r0102_wind.pdf
        - r0201_floor.pdf
        - r0202_roof.pdf
        - report.pdf
    - **[sites]** (html output files)
        - **[resources]**
            - image1.png
            - image2.png
        - index.html
        - s0101_gravity.html
        - s0102_wind.html
        - s0201_gravity.html
        - s0202_wind.html

The four top-level folder names ("text", "binary", "reports" and "sites") are
required. Other file names are partially user determined, using the specified,
numbered prefixes. The API is designed so that only files in the text folder
are uploaded for version control and sharing. They constitute the essential
core of the calculation - the text, equations, functions and tables. Files in
the binary folder are not typically not shared and include files such as images
(may have copyrights), pdf attachments and proprietary data (e.g. client
contact information and costs).

A rivt file is a Python file that imports the rivt package and calls functions
on rivt strings. The file has the form **rddss_filename.py** where dd is the
division number and ss the subdivision number. Together they make up the unique
doc number.The **text** folder includes each rivt file and its supporting plain
text input files in a unique folder. The folder also includes the document
output as a README.txt that is displayed and searchable on github. The binary
folder includes all of the binary and protected inputs for its division number. 

A rivt project is started by copying the folder structure from a similar
existing project. Files are free-form plain text that may be edited with any
editor. To process a rivt file the command **python -m rivt** is run from the
command shell in the folder containing the file. It may also be processed in
and IDE. Refer to the [rivt user manual.](https://rivtmanual.net)