echo Y | rmdir docs /S
rem echo F | xcopy /y /i C:\python313\Lib\site-packages\rivtlib\*.py .\rivtlib\
sphinx-apidoc -o . c:\git\rivtlib
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll