echo Y | rmdir docs /S
del *.html
mkdir docs
mkdir docs\code
echo F | xcopy /y E:\python313\Lib\site-packages\rivtlib\*.* .\docs\code
pdoc --html --output-dir .\ units.py
pdoc --html --output-dir .\ parse.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll