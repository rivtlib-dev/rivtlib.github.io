echo Y | rmdir docs /S
pdocs as_markdown -o .\  .\src\rivtlib\cmd_md.py 
pdocs as_markdown -o .\  .\src\rivtlib\cmd_parse.py
pdocs as_markdown -o .\  .\src\rivtlib\cmd_rst.py
pdocs as_markdown -o .\  .\src\rivtlib\cmd_utf.py
pdocs as_markdown -o .\  .\src\rivtlib\config.py
pdocs as_markdown -o .\  .\src\rivtlib\parse.py
pdocs as_markdown -o .\  .\src\rivtlib\report.py
pdocs as_markdown -o .\  .\src\rivtlib\rivtapi.py
pdocs as_markdown -o .\  .\src\rivtlib\setup.py
pdocs as_markdown -o .\  .\src\rivtlib\tag_md.py
pdocs as_markdown -o .\  .\src\rivtlib\tag_parse.py
pdocs as_markdown -o .\  .\src\rivtlib\tag_rst.py
pdocs as_markdown -o .\  .\src\rivtlib\tag_utf.py
pdocs as_markdown -o .\  .\src\rivtlib\units.py
pdocs as_markdown -o .\  .\src\rivtlib\write_pdf.py
pdocs as_markdown -o .\  .\src\rivtlib\write_private.py
pdocs as_markdown -o .\  .\src\rivtlib\write_public.py
pdocs as_markdown -o .\  .\src\rivtlib\__init__.py
pdocs as_markdown -o .\  .\src\rivtlib\__main__.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
