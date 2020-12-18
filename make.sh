rm -rf __pycache__
rm -rf build
rm -rf dist
rm -rf *.spec
pyinstaller -F -w 丝滑走A.py -i icon.ico
pyinstaller -F 卡牌大师切牌v2.py -i icon.ico
pyinstaller -F 武器光速摸眼v2.py -i icon.ico
pyinstaller -F 盲僧光速摸眼v2.py -i icon.ico
rm -rf __pycache__
rm -rf build
rm -rf *.spec

cp -rf icon.ico dist
