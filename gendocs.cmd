echo Y | rmdir docs /S
del *.html
mkdir docs
mkdir docs\code
echo F | xcopy /y E:\python313\Lib\site-packages\rivtlib\*.* .\docs\code
python -m pydoc -w .\docs\code\cmd_rst.py
python -m pydoc -w .\docs\code\cmd_utf.py
python -m pydoc -w .\docs\code\parse.py
python -m pydoc -w .\docs\code\rivtapi.py
python -m pydoc -w .\docs\code\folders.py
python -m pydoc -w .\docs\code\tag_rst.py
python -m pydoc -w .\docs\code\tag_utf.py
python -m pydoc -w .\docs\code\units.py
python -m pydoc -w .\docs\code\write.py
python -m pydoc -w .\docs\code\units.py
python -m pydoc -w .\docs\code\__init__.py
python -m pydoc -w .\docs\code\__main__.py
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll