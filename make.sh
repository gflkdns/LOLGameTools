rm -rf __pycache__
rm -rf build
rm -rf dist
rm -rf *.spec

pyinstaller -F --uac-admin  丝滑走A_通用_自动识别攻速.py -i icon.ico
rm -rf __pycache__
rm -rf build
rm -rf *.spec

cp -rf icon.ico dist
#cp -rf Tesseract-OCR dist
