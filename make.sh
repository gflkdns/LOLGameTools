rm -rf __pycache__
rm -rf build
rm -rf dist
rm -rf *.spec
pyinstaller -F --uac-admin -w 丝滑走A_通用.py -i icon.ico
pyinstaller -F --uac-admin 卡牌大师秒切助手.py -i icon.ico
pyinstaller -F --uac-admin 武器光速摸眼.py -i icon.ico
pyinstaller -F --uac-admin 盲僧光速摸眼.py -i icon.ico
pyinstaller -F --uac-admin -w 丝滑走A_寒冰自动Q.py -i icon.ico
pyinstaller -F --uac-admin -w 丝滑走A_大嘴自动W.py -i icon.ico
pyinstaller -F --uac-admin -w 丝滑走A_天使自动E.py -i icon.ico
pyinstaller -F --uac-admin -w 丝滑走A_老鼠自动R.py -i icon.ico
pyinstaller -F --uac-admin -w 丝滑走A_通用_自动识别攻速.py -i icon.ico
rm -rf __pycache__
rm -rf build
rm -rf *.spec

cp -rf icon.ico dist
