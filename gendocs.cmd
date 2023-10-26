echo Y | rmdir docs /S
pdocs as_markdown .\src\rivtlib\ 
pdocs as_markdown .\src\rivtlib\cmd_md.py
pdocs as_markdown .\src\rivtlib\cmd_parse.py
pdocs as_markdown .\src\rivtlib\cmd_rst.py
pdocs as_markdown .\src\rivtlib\cmd_utf.py
pdocs as_markdown .\src\rivtlib\config.py
pdocs as_markdown .\src\rivtlib\folders.py
pdocs as_markdown .\src\rivtlib\parse.py
pdocs as_markdown .\src\rivtlib\report.py
pdocs as_markdown .\src\rivtlib\rivtapi.py
pdocs as_markdown .\src\rivtlib\setup.py
pdocs as_markdown .\src\rivtlib\tag_md.py
pdocs as_markdown .\src\rivtlib\tag_parse.py
pdocs as_markdown .\src\rivtlib\tag_rst.py
pdocs as_markdown .\src\rivtlib\tag_utf.py
pdocs as_markdown .\src\rivtlib\units.py
pdocs as_markdown .\src\rivtlib\write_pdf.py
pdocs as_markdown .\src\rivtlib\write_private.py
pdocs as_markdown .\src\rivtlib\write_public.py
pdocs as_markdown .\src\rivtlib\__init__.py
pdocs as_markdown .\src\rivtlib\__main__.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
