echo Y | rmdir docs /S
echo Y | rmdir _autosummary /S
sphinx-apidoc  -o . rivtlib --separate
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
rem echo F | xcopy /y /i C:\python313\Lib\site-packages\rivtlib\*.py .\rivtlib\
