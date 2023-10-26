
# Organize

<head>
<style>
.button {
  background-color: #3FB1C5; 
  border: 3 px solid black;
  color: black;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
</style>

<script> function searchRivt(){var strng2 = document.getElementById("terms").value;URL = `https://github.com/search?q=rivt+${strng2}+in%3Areadme`;window.open(URL,'_self')};document.addEventListener("keydown", function(e) {if ((e.keyCode == 10 || e.keyCode == 13) && e.ctrlKey){document.getElementById("searchBtn").click();}});
</script>

<script> function searchOrg(){var strng2 = document.getElementById("terms").value;URL = `https://github.com/search?q=rivt+${strng2}+in%3Areadme`;window.open(URL,'_self')};document.addEventListener("keydown", function(e) {if ((e.keyCode == 10 || e.keyCode == 13) && e.ctrlKey){document.getElementById("searchBtn").click();}});
</script>

<script> function clearRivt(){document.getElementById("terms").value="";document.addEventListener("keydown", function(e) {if ((e.keyCode == 10 || e.keyCode == 82) && e.ctrlKey){document.getElementById("clearBtn").click();}})};
</script>

</head>

The intention of rivt is to have the first 


<hr>

## Folders
<hr>

**rivtlib** can process single rivt files, but typically it is used to generate
reports. rivt documents are organized into divisions (folders) and documents
(files). Reprort section names are taken from the the file and folder names but
may be overridden by a configuration file.



Document inputs and outputs may be stored in or directed to publically
shareable or private foldrers. Reports is formatted with divisions,
subdivisions and sections.





Fixed folder and file prefixes are shown in [ ]. Report and document headings
are taken from the folder and file labels. 



<pre>
[rivt]_Report-Label/               
    ├── [div01]-div-label/            (division folder)
        ├── [data01]/                 (resource data)
            ├── data.csv                   
            ├── attachment.pdf
            └── fig.png            
             functions.py                   
        ├── [riv01]-label1.py         (rivt file)
        └── [riv02]-label2.py         (rivt file)   
    ├── [div02]-div-label/            (division folder)
        ├── [data02]/                 (resource data)
            ├── data.csv
            └── fig.png
        └── [riv01]_label3.py         (rivt file)
    ├── [data-private]/                 
        ├── [data]/                   (private data)                   
            ├── data.csv
            ├── attachment.pdf
            └── fig.png        
        ├── [functions]/              (private functions)                   
            ├── [data]/
            ├── [output]/
            └── function.py                
        ├── [rivt-docs]/              (private output documents)
            ├── [pdf]/                      
                ├── doc0101-label1.pdf      
                ├── doc0102-label2.pdf
                ├── doc0201-label3.pdf
                └── Report-Label.pdf 
            ├── [text]/                    
                ├── doc0101-label1.txt      
                └── doc0201-label3.txt       
            ├── doc0101-label1.md            
            └── doc0201-label3.md
        ├── [temp]/
            └── doc0201-label3.tex 
    ├── [functions]/                  (public functions)                   
        ├── [data]/
        ├── [output]/
        ├── function1.py
        └── function2.py                
    ├── [rivt-docs]/                  (public output documents)
        ├── [pdf]/                      
            ├── doc0101-label1.pdf      
            ├── doc0102-label2.pdf
            ├── doc0201-label3.pdf
            └── Report-Label.pdf 
        ├── [text]/                    
            ├── doc0101-label1.txt      
            ├── doc0102-label2.txt
            └── doc0201-label3.txt           
    ├── .gitignore
    ├── config.ini                    (config file)
    ├── doc0101-label1.md             (public output documents) 
    ├── doc0102-label2.md
    ├── doc0201-label3.md
    └── README.txt                    (cumulative documents - searchable) 
</pre>


### Make Folders

A starter report folder structure can be generated in the folder where the
following command is executed:

*python -m rivtlib.toy-report*

 ## **Examples**

<hr>

### Simple
<hr>

<pre style="background: #cfdde2; color: #000000">

import rivtlib.rivtapi as rv

rv.R("""Introduction | notoc, 1

    The Repo method (short for repository and report) is the first method of a
    rivt file which specifies document configuration settings.

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

rv.I("""The Insert method | default 

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
</pre>


### text output

<pre style="background: #cfdde2; color: #000000">

import rivt.rivtapi as rv

rv.R("""Introduction | notoc, 1

    The Repo method (short for repository and report) is the first method of a
    rivt file which specifies document configuration settings.

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

rv.I("""The Insert method | default 

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
    # the code and result of any print statement in the doc. New functions 
    # may be written explicitly or imported from other files. Line comments 
    # are printed. Triple quotes cannot be used. Use raw strings instead.
    
    # Four Python libraries, if installed, are imported by rivt and available as: 
    # pyplot -> plt
    # numpy -> np
    # pandas -> pd
    # sympy -> sy
    
    # Python code:
    
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

    Changing a function to X skips evaluation of that function and may be used
    for review comments and debugging.

    """) 
</pre>


### markdown output

some markdown


### PDF output

[PDF output from example](./_static/attach/rivt-toy-example.pdf)

<hr>

## Solar Canopy
<hr>
xyz

### text output

ccc

<hr>

## Seismic Strengthening
<hr>

xyz

### text output

ccc

<hr>

## GitHub
<hr>

Full text **rivt** document search across GitHub README files

Example: solar+steel+frame

<input type="text" id="terms" name="terms" size=60 style="height:40px;font-size:14pt; font-weight: normal"><br>

<button class="button" id="searchBtn" onclick="searchRivt()">Search [ Ctrl+Enter ]</button>
<button class="button" id="clearBtn" onclick="clearRivt()">Clear [ Ctrl+R ]</button>
<hr>

## GitHub Organizations
<hr>

Full text **rivt** document search across GitHub Organization README files

<input type="text" id="terms" name="terms" size=30 style="height:40px;font-size:14pt; font-weight: normal"> Organizations (comma separated)<br>


<input type="text" id="terms" name="terms" size=60 style="height:40px;font-size:14pt; font-weight: normal"> Search Terms<br>

<button class="button" id="searchBtn" onclick="searchOrg()">Search [ Ctrl+Enter ]</button>
<button class="button" id="clearBtn" onclick="clearRivt()">Clear [ Ctrl+R ]</button>

## Search Tips

- The GitHub search interface is [here](https://github.com/search).

- GitHub README searches only index the root directory README. The rivt function <code> rv.readme() </code> writes every README in a project into the root README so rivt projects on GitHub can be fully searched.

- The rivt search box automatically adds the rivt search term.
