echo Y | rmdir docs /S
mkdir docs
mkdir docs\code
echo F | xcopy /y E:\python313\Lib\site-packages\rivtlib\*.* .\docs\code
cd .\docs\code
python -m pydoc -w .\cmd_rst.py
python -m pydoc -w .\cmd_utf.py
python -m pydoc -w .\parse.py
python -m pydoc -w .\rivtapi.py
python -m pydoc -w .\folders.py
python -m pydoc -w .\tag_rst.py
python -m pydoc -w .\tag_utf.py
python -m pydoc -w .\units.py
python -m pydoc -w .\write.py
python -m pydoc -w .\units.py
python -m pydoc -w .\__init__.py
python -m pydoc -w .\__main__.py
cd ..
cd ..
sphinx-build . docs
echo F | xcopy /y CNAME .\docs\CNAME
echo F | xcopy /y .nojekyll .\docs\.nojekyll