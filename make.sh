rm -rf __pycache__
rm -rf build
rm -rf *.spec


pyinstaller -F --uac-admin -w 走A.py -i icon.ico

rm -rf __pycache__
rm -rf build
rm -rf *.spec



