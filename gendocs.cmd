echo Y | rmdir docs /S
pdoc -d markdown -o  ./src/rivtlib/cmd_md.py
pdoc -d markdown -o  .\src\rivtlib\cmd_parse.py
pdoc -d markdown -o  .\src\rivtlib\cmd_rst.py
pdoc -d markdown -o  .\src\rivtlib\cmd_utf.py
pdoc -d markdown -o  .\src\rivtlib\config.py
pdoc -d markdown -o  .\src\rivtlib\folders.py
pdoc -d markdown -o  .\src\rivtlib\parse.py
pdoc -d markdown -o  .\src\rivtlib\report.py
pdoc -d markdown -o  .\src\rivtlib\rivtapi.py
pdoc -d markdown -o  .\src\rivtlib\setup.py
pdoc -d markdown -o  .\src\rivtlib\tag_md.py
pdoc -d markdown -o  .\src\rivtlib\tag_parse.py
pdoc -d markdown -o  .\src\rivtlib\tag_rst.py
pdoc -d markdown -o  .\src\rivtlib\tag_utf.py
pdoc -d markdown -o  .\src\rivtlib\units.py
pdoc -d markdown -o  .\src\rivtlib\write_pdf.py
pdoc -d markdown -o  .\src\rivtlib\write_private.py
pdoc -d markdown -o  .\src\rivtlib\write_public.py
pdoc -d markdown -o  .\src\rivtlib\__init__.py
pdoc -d markdown -o  .\src\rivtlib\__main__.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
