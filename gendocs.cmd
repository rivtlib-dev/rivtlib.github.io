echo Y | rmdir docs /S
echo Y | rmdir src /S
echo F | xcopy /y /i C:\python313\Lib\site-packages\rivtlib\*.py .\src\
pdoc --html --force --output-dir .\ .\src\api.py
pdoc --html --force --output-dir .\ .\src\units.py
pdoc --html --force --output-dir .\ .\src\folders.py
pdoc --html --force --output-dir .\ .\src\parse.py
pdoc --html --force --output-dir .\ .\src\tags.py
pdoc --html --force --output-dir .\ .\src\cmds.py
pdoc --html --force --output-dir .\ .\src\write.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll