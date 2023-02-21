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
  <th style="text-align: center;border:none"><a href="https://rivtdocs.net"><b>rivtDocs (installer)</b></a></th>
  <th style="text-align: center;border:none;background-color:#959396"><a href="https://rivtcode.net"><b>rivt (code)</b></a></th>
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

### Universally Shared Calculation Documents [<b>[rivt source code on GitHub]</b>](https://github.com/rivtDocs/rivt)

## **rivt** Overview

**rivt** is a Python package providing an API for **rivtText**, a simple,
readable document markup language designed for calculations. **rivtText** wraps
and extends [reStructuredText (reST)](https://docutils.sourceforge.io/rst.html). 
Ouptut documents include UTF8, HTML and PDF from the same **rivtText** file.

The program prioritizes four design principles:

- *Cut and Paste Everything* - **rivtText** content is plain text
- *Short Learning Curve* - **rivtText** uses less than 30 intuitive terms
- *Integration* - **rivt** is built on the highly integrated Python language
- *Standardization* - **rivt** uses a standard folder structure for input and output

**rivt** is designed for simple, single calculations as well as large, extensive
reports. The **rivt** report folder structure shown below is designed to
support both. Folder names are shown in brackets. Folder and file name prefixes
that are fixed are shown italicized. The four top-level folder names (text,
resource, report and site) are required verbatim. Other file names are
combinations of specified prefixes and user titles. Underscores and hyphens
that separate words in file and folder names are stripped out when used as
document and division names in the document.

Document input files are separated into folders labeled text and resource.
Files in the text folder are shareable rivtText files that contain the primary
calculation information. The resource folder includes supporting files (images,
pdf etc.) and other files that may include confidential project information or
copyrighted material. The resource folder often contains binary information and
is not designed to share.

Output files are written to three folders, depending on the output type. The
UTF8 output is written to a README.txt file within the text folder. It is
displayed and searchable on version control platforms like GitHub. PDF output
is written to the report folder, and HTML output to the website folder.

**Folder Structure Example**

- **[*rivt*_Design-Project]** (user project / report name)
    - **[*text*]**
        - **[*rv00*_config]** (document configuration data)
            - units.py
            - config.py
        - **[*rv01*_Overview-and-Loads]**  (division name)
            - README.txt (output file)
            - **[*r0101*_Gravity-Loads]**  (document name)
                - *r0101.py* (document file) 
                - README.txt (utf output file)
                - data1.csv (source file)
                - functions1.py (function file)
            - **[*r0102_Seismic-Loads*]** (document name)
                - *r0102.py*  
                - README.txt
                - data2.csv 
                - functions2.py 
         - **[*rv02*_Foundations]** (division name)
             - README.txt
             - **[*r0201*_Pile-Design]** (document name)
                 - *r0201.py*
                 - README.txt
                 - paragraph1.txt
                 - functions3.py 
    - **[resource]**
        - **[rv00]** (report configuration data)
            - report_gen.py (report generation file)
            - site_gen.py (site generation file)
            - pdf_style.sty (LaTeX style override)
            - project_data.syk
            - report.txt
        - **[rv01]**    (division resources)
            - image1.jpg
        - **[rv02]**    (division resources)
            - image2.jpg
            - attachment.pdf    
    - **[report]** (PDF output files)
        - r0101_Gravity-Loads.pdf
        - r0102_Seismic-Loads.pdf
        - r0201_Pile-Design.pdf
        - Design-Project.pdf  (collated report)
    - **[site]** (HTML output files)
        - **[resources]** (HTML resource files)
            - image1.png
            - image2.png
            - html_style.css (HTML style override)
        - index.html  (table of contents)
        - s0101_Gravity-Loads.html
        - s0102_Seismic-Loads.html
        - s0201_Pile-Design.html

The four top-level folder names (text, resource, report and site) are required.
Other file names are user determined using the specified prefixes. Underscores
that separate words in file and folder names are stripped out when used as
document and division names in the report. The API is designed so that only
files in the text folder are uploaded for version control and sharing. They are
the essential core of the calculation. Files in the resource folder are not
shared and are typically binary files such as images, pdf attachments and
proprietary data (e.g. client contact information and costs). The folder and
file structure makes it easy to share and assert version control on the primary
calculation inputs.

A rivt file is a Python file that imports the rivt API and calls one of four
functions on rivt-strings - R(rs), I(rs), V(rs), T(rs). Rivt-strings (rs) are
free-form plain text strings enclosed in triple quotes that include text and
commands and tags defining the calculation and formatting.

Refer to the [rivtDocs user manual.](https://rivtDocs.net)