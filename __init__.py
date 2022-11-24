#!/usr/bin/env python
# makes folder a package
"""rivtcalc

The rivtcalc Python package outputs formatted engineering calculation documents
as UTF8, HTML and PDF files from rivt-strings. The language is designed to
simplify document reuse, review and clarity. The program is here:

Program source: https://github.com/rivtcalc. 
User Manual: https://github.com/rivtcalc.

The package integrates with other free and open source tools as a complete
document editing system. A rivt-stack includes a Python installation with
science libraries (numpy, pandas, scipy, matplotlib, rivtcalc), an interactive open
source code editor (VS Code and Pyzo are examples), and a LaTeX distribution
(TexLive and MikTex are examples).  Single click installs 

A calc is a Python file importing the *rivt* library and containing calculation
strings in the **rivt** language format. Calc files have names of the form
*ddcc_calc_name.py* where dd and cc are two digit numbers identifying a
division and calculation number respectively. Calculation and Division numbers
are used to organize **rivt** reports.

The calcs and supporting ASCII input files are stored in a project 
folder tree set up by the user. Output calculations are written to the *calcs* 
directory in UTF8 format and the *docs* and *reports* directory in 
PDF and HTML formats::

  Project_Name (chosen by user)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
      |- docs
          |- HTML
              |- figures
      |- reports
          |- attachments
          |- temp

The program may be run in interactive mode, using an interactive 
code editor like VS Code, or from the command line.

.. code:: python

    python -m rivt rddcc_ design_filename.py 

An error will be raised if the program is run and the folder structure is not 
complete.  **r-i-v-e-t** calcs can be shared through the **on-c-e** (OpeN Calculation Exchange)
database at http://on-c-e.net.  For **on-c-e** overview see http://rivt-calcs.net .

The overall program flow is shown below:
                     /--------------------------------\                    
                     |                                |                    
                     |  Read rivt file (or strings   |                    
                     |  in interactive mode).  String |                    
                     |  types:                        |                    
                     |                                |                    
                     |     r__, i__, v__, e__, t__    |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     \----------------+---------------/                    
                                      |                                    
  +---------------+  +----------------\/--------------+  +-------------+   
  |               |  |                                |  |             |   
  |               |  |                                |  |             |   
  |    process    |  |    is string type r__?         |  | parse and   |   
  |    Python     |Y |                                | N| process     |   
  |    code       <--+                                +--> rivt       |   
  |               |  |                                |  | strings     |   
  |               |  |                                |  |             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |                                                      |          
         |           +================================+         |          
         |           |                                |         |          
         |           |                                |         |          
         |           |   generate utf-8 calcs to      |         |          
         |           |   terminal and files           |         |          
         +----------->                                <---------+          
                     |                                |                    
                     |                                |                    
                     +================================+                    
                     +================================+                    
                                      |                                    
                     +================\/==============+                    
                     |                                |                    
                     |                                |                    
                     |    write reST calcs to file    |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     +================================+                    
                     +================================+                    
                                      |                                    
  +===============+  +----------------\/--------------+                    
  |               |  |                                |  /-------------\   
  |               |  |                                |  |             |   
  | write HTML    |  |                                |  |             |   
  | or PDF doc    |Y |     write docs?                | N|   End       |   
  | files         <--+                                +-->             |   
  |               |  |                                |  |             |   
  |               |  |                                |  |             |   
  +===============+  |                                |  \-------------/   
  +=====+=========+  +--------------------------------+                    
        |                                                                  
        |            +--------------------------------+                    
        |            |                                |  /-------------\   
        |            |                                |  |             |   
        |            |     write reports?             |  |             |   
        |            |                                | N|   End       |   
        +------------>                                +-->             |   
                     |                                |  |             |   
                     |                                |  |             |   
                     |                                |  \-------------/   
                     +----------------+---------------+                    
                                      |Y                                   
                     +================\/==============+                    
                     |                                |                    
                     |                                |                    
                     |    write HTML or PDF report    |                    
                     |    files                       |                    
                     |                                |                    
                     |                                |                    
                     |                                |                    
                     +================================+                    
                     +================================+                    
                                      |                                    
                     /----------------\/--------------\                    
                     |                                |                    
                     |                                |                    
                     |           End                  |                    
                     |                                |                    
                     |                                |                    
                     \--------------------------------/                    
                                                                           
                                                                           



"""
