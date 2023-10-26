
# Publish

<hr>

## Folders
<hr>

<pre>
[rivt]-Report-Label/               
    ├── .git
    ├── units.py                        (input: unit over-ride)
    ├── README.md                       (output: toc and summary) 
    ├── rivt01.ini                      (input: config file)
    ├── [doc0101]-div-label/            (first division - first file)
        ├── [data0101]/                     (inputs: data files)
            ├── data1.csv                   
            ├── paper1.pdf
            └── functions1.py                   
        ├── [rivt]-doc-label1.py            (input: rivt file)
        └── README.md                       (output: GFM doc)
    ├── [doc0102]/                      (first division - second file)
        ├── data[0102]/                     (inputs: data files)
            ├── data1.csv
            ├── fig1.png
            └── fig2.png
        ├── [rivt]-doc-label2.py            (input: rivt file)
        └── README.md                       (output: GFM doc)
    ├── [doc0201]-div-label/            (second division - first file)
        ├── [data0201]/                     (inputs: data files)
            ├── data1.csv
            ├── attachment.pdf
            ├── functions.py
            └── fig1.png
        ├── [rivt]-doc-label3.py            (input: rivt file)
        └── README.md                       (outputs: GFM doc)
    └── [private]/                      (private files)
        ├── [temp]/                         (outputs: temp files)
        ├── [report]/                       (report files)
            ├── 0101-Doc Label1.pdf         (outputs: PDF docs)
            ├── 0102-Doc Label2.pdf
            ├── 0201-Doc Label3.pdf
            └── Report Label.pdf            
        ├── images/                         (inputs: optional private data)
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
</pre>