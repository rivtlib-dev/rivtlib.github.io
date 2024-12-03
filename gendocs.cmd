echo Y | rmdir docs /S
echo F | xcopy /y E:\python313\Lib\site-packages\rivtlib\*.* .\src
pdoc --html --force --output-dir .\ .\src\parse.py
pdoc --html --force --output-dir .\ .\src\cmd_rst.py
pdoc --html --force --output-dir .\ .\src\cmd_utf.py
pdoc --html --force --output-dir .\ .\src\tag_rst.py
pdoc --html --force --output-dir .\ .\src\tag_utf.py
pdoc --html --force --output-dir .\ .\src\rivtapi.py
pdoc --html --force --output-dir .\ .\src\folders.py
pdoc --html --force --output-dir .\ .\src\__init__.py
pdoc --html --force --output-dir .\ .\src\__main__.py
pdoc --html --force --output-dir .\ .\src\check.pyy
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll