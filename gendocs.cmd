echo Y | rmdir docs /S
echo F | xcopy /y E:\python313\Lib\site-packages\rivtlib\*.* .\source
pdoc --html --force --output-dir .\ .\source\parse.py
pdoc --html --force --output-dir .\ .\source\cmd_rst.py
pdoc --html --force --output-dir .\ .\source\cmd_utf.py
pdoc --html --force --output-dir .\ .\source\tag_rst.py
pdoc --html --force --output-dir .\ .\source\tag_utf.py
pdoc --html --force --output-dir .\ .\source\rivtapi.py
pdoc --html --force --output-dir .\ .\source\folders.py
pdoc --html --force --output-dir .\ .\source\__init__.py
pdoc --html --force --output-dir .\ .\source\__main__.py
pdoc --html --force --output-dir .\ .\source\check.pyy
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll