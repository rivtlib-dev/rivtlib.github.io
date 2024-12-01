echo Y | rmdir docs /S
mkdir docs
mkdir docs/src
echo F | xcopy /y E:\python313\Lib\site-packages\rivtlib\*.* .\docs\src\ 
cd pdocs
python -m pydoc -w .\src\cmd_rst.py
python -m pydoc -w .\src\cmd_utf.py
python -m pydoc -w .\src\rivtlib\parse.py
python -m pydoc -w .\src\rivtlib\rivtapi.py
python -m pydoc -w .\src\rivtlib\folders.py
python -m pydoc -w .\src\rivtlib\tag_rst.py
python -m pydoc -w .\src\rivtlib\tag_utf.py
python -m pydoc -w .\src\rivtlib\units.py
python -m pydoc -w .\src\rivtlib\write.py
python -m pydoc -w .\src\rivtlib\units.py
python -m pydoc -w .\src\rivtlib\__init__.py
python -m pydoc -w .\src\rivtlib\__main__.py
cd ..
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
