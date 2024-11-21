echo Y | rmdir docs /S
pdocs as_markdown -o .\  ..\rivtlib\cmd_rst.py
pdocs as_markdown -o .\  ..\rivtlib\cmd_utf.py
pdocs as_markdown -o .\  ..\rivtlib\parse.py
pdocs as_markdown -o .\  ..\rivtlib\rivtapi.py
pdocs as_markdown -o .\  ..\rivtlib\folders.py
pdocs as_markdown -o .\  ..\rivtlib\tag_rst.py
pdocs as_markdown -o .\  ..\rivtlib\tag_utf.py
pdocs as_markdown -o .\  ..\rivtlib\units.py
pdocs as_markdown -o .\  ..\rivtlib\write.py
pdocs as_markdown -o .\  ..\rivtlib\__init__.py
pdocs as_markdown -o .\  ..\rivtlib\__main__.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
