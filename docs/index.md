---
layout: default
---

<p style="text-align:center; font-weight:bold"> share docs and calcs anywhere anytime </p>
<table>
<colgroup>
  <col width="20%" />
  <col width="20%" />
  <col width="20%" />
  <col width="20%" />
  <col width="20%" />
</colgroup>
<thead>
<tr class="header">
  <th style="text-align: center">rivtDocs</th>
  <th style="text-align: center">rivt</th>
  <th style="text-align: center">rivtSearch</th>
  <th style="text-align: center">rivtDocs Install</th>
  <th style="text-align: center">rivtDocs Manual</th>
</tr>
</thead>
<tbody>
<tr>
  <td style="text-align:center"><a href="https://rivtdocs.net"> <img src="./assets/img/rivtdocs.png" width="75" height="55" /></a></td>
  <td style="text-align: center;background-color:#999290"><a href="https://rivtcode.net"> <img src="./assets/img/rivt01.png" width="75" height="55" /></a></td>
  <td style="text-align: center"><a href="https://github.com/search?q=rivt+in%3Areadme"> <img src="./assets/img/search01.png" width="70" height="60" /></a></td>
  <td style="text-align: center"><a href="https://rivtinstall.net"> <img src="./assets/img/rivtdocs.png" width="75" height="55" /></a></td>
  <td style="text-align: center"><a href="https://rivtmanual.net"> <img src="./assets/img/rivtmanual.png" width="80" height="60" /></a></td>
</tr>
</tbody>
</table>

---------------------------

## **rivt** Overview

**rivt** is a Python package providing an API for **rivtText**, a highly
readable and shareable document markup language designed for calculations. It
implements a markup language - **rivtText** - that wraps and extends
[reStructuredText (reST).](https://docutils.sourceforge.io/rst.html). Ouptut
document types include HTML, PDF and UTF8 from the same **rivtText** file.

The program design follows three principles:

- **Don't reinvent the wheel** - make it easy to create, share and reuse documents
- **Play well with others** - integrate with existing programs using standard interfaces
- **Respect people's time** - prioritize clarity, efficiency and intuition.

The API uses fixed file and folder conventions for input and output to simplify
formatting, navigation and code folding. rivt folders (names shown in brackets)
have the following structure:


**rivt Folder Structure**

- **[rivt*_user_project_name*]** (user project_name)
    - **[calcs]**
        - **[rv00*_user_config_name*]** (calc configuration data)
            - units.py
            - config.py
        - **[rv0101*_user_calc_division_name*]**  (folder report division name)
            - *r0101*_calc_name.py (calc file name) 
            - README.txt (text calc output file)
            - chart.csv (text file used in calc)
            - functions.py (function file used in calc)
        - **[rv0102*_user_calc_division_name*]** 
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