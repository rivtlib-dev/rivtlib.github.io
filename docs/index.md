---
layout: default
---

### share docs and calcs anywhere, anytime

---------------------------

<table>
<colgroup>
  <col width="25%" />
  <col width="25%" />
  <col width="25%" />
  <col width="25%" />
</colgroup>
<thead>
<tr class="header">
  <th style="text-align: center">rivt</th>
  <th style="text-align: center">rivtSearch</th>
  <th style="text-align: center">rivtInstall</th>
  <th style="text-align: center">rivtManual</th>
</tr>
</thead>
<tbody>
<tr>
  <td style="text-align: center"><a href="https://github.com/rivtdocs/rivt"> <img src="./assets/img/rivt01.png" width="75" height="55" /></a></td>
  <td style="text-align: center"><a href="https://github.com/search?q=rivt&ref=simplesearch"> <img src="./assets/img/search01.png" width="70" height="60" /></a></td>
  <td style="text-align: center"><a href="https://rivtinstall.net"> <img src="./assets/img/rivtcalc01.png" width="75" height="55" /></a></td>
  <td style="text-align: center"><a href="https://rivtmanual.net"> <img src="./assets/img/codedocs09.png" width="80" height="60" /></a></td>
</tr>
</tbody>
</table>

---------------------------

## **rivt** Overview

**rivt** is a Python package providing an API for *rivtText*, a highly readable
and shareable markup language designed in particular for calculation documents.
It implements a markup language - **rivtText** - that wraps and extends
[reStructuredText (reST).][https://docutils.sourceforge.io/rst.html]

The design of the program follows three principles with regard to document
production:

    - Don't reinvent the wheel
    - Respect people's time and attention
    - Simple integration with other tools


The
API uses file and folder conventions to simplify formatting, navigation and
code folding. Text, PDF or HTML output are easily organized and assembled into
collated reports. The folder structure (shown bracketed) is shown below.


**rivt Folder Structure**

- **[rivt*_user_project_name*]** (user project_name)
    - **[calcs]**
        - **[rv00*_user_config_name*]** (calc configuration data)
            - units.py
            - config.py
        - **[rv0101*_user_calc_division_name*]**  (folder report division name)
            - *c0101*_calc_name.py (calc file name) 
            - README.txt (text calc output file)
            - chart.csv (text file used in calc)
            - functions.py (function file used in calc)
        - **[rv0102*_user_calc_division_name*]** 
            - *c0102*_calc_name.py
            - README.txt
            - chart1.csv 
            - functions1.py 
         - **[rv0201*_user_calc_division_name*]**
            - c0201_calc_name.py
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
    - **[sites]** (html calc output files)
        - **[resources]**
            - image1.png
            - image2.png
        - index.html
        - s0101_gravity.html
        - s0102_wind.html
        - s0201_gravity.html
        - s0202_wind.html

The four top-level folder names ("calcs", "docs", "reports" and "sites") are
required. Other file names are partially user determined, using the specified
prefixes. The API is designed so that only files in the text folder are
uploaded for version control and sharing. They constitute the essential core of
the calculation - the text, equations, functions and tables. Files in the binary
folder are not shared and are typically binary input files such as images, pdf
attachments and proprietary data (e.g. client contact information and costs).

A rivt file is a Python file that imports rivt and calls functions on rivt
strings. The file has the form rddnn_filename.py where dd is the division
file and its supporting files are stored in a separate folder. The text folder
includes all plain text input files and the output file in the form of a
README.txt. The binary folder includes all of the binary inputs (i.e. images) and
private, undistributable files.

A rivt project is started by copying the folder structure from a similar
existing project. Files are free-form plain textthat may be edited in any text
editor. To process a file the command below is run in the folder containing the
file.

python -m rivt
