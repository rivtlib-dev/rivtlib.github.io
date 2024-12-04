echo Y | rmdir docs /S
echo Y | rmdir src /S
echo F | xcopy /y /i E:\python313\Lib\site-packages\rivtlib\*.* .\src\
pdoc --html --force --output-dir .\ .\src\__init__.py
pdoc --html --force --output-dir .\ .\src\__main__.py
pdoc --html --force --output-dir .\ .\src\rivtapi.py
pdoc --html --force --output-dir .\ .\src\units.py
pdoc --html --force --output-dir .\ .\src\folders.py
pdoc --html --force --output-dir .\ .\src\parse.py
pdoc --html --force --output-dir .\ .\src\tag_rst.py
pdoc --html --force --output-dir .\ .\src\tag_utf.py
pdoc --html --force --output-dir .\ .\src\cmd_rst.py
pdoc --html --force --output-dir .\ .\src\cmd_utf.py
pdoc --html --force --output-dir .\ .\src\write.py
pdoc --html --force --output-dir .\ .\src\checks.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll