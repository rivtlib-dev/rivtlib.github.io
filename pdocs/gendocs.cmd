echo Y | rmdir docs /S
cd pdocs
python -m pydoc -w ..\..\rivtlib\cmd_rst.py
python -m pydoc -w ..\..\rivtlib\cmd_utf.py
python -m pydoc -w ..\..\rivtlib\parse.py
python -m pydoc -w ..\..\rivtlib\rivtapi.py
python -m pydoc -w ..\..\rivtlib\folders.py
python -m pydoc -w ..\..\rivtlib\tag_rst.py
python -m pydoc -w ..\..\rivtlib\tag_utf.py
python -m pydoc -w ..\..\rivtlib\units.py
python -m pydoc -w ..\..\rivtlib\write.py
python -m pydoc -w ..\..\rivtlib\units.py
python -m pydoc -w ..\..\rivtlib\__init__.py
python -m pydoc -w ..\..\rivtlib\__main__.py
copy *.html ..\docs
cd ..
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll
