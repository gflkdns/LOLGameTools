rm -rf __pycache__
rm -rf build
rm -rf *.spec
rm -rf dist/ZouA/走*
rm -rf dist/ZouA/卡牌*

pyinstaller -D --uac-admin -w 卡牌大师秒切助手.py -i icon.ico
pyinstaller -D --uac-admin -w 走A.py -i icon.ico
pyinstaller -D --uac-admin -w 走A-E.py -i icon.ico
pyinstaller -D --uac-admin -w 走A-Q.py -i icon.ico
pyinstaller -D --uac-admin -w 走A-W.py -i icon.ico
pyinstaller -D --uac-admin -w 武器光速摸眼.py -i icon.ico
pyinstaller -D --uac-admin -w 盲僧光速摸眼.py -i icon.ico

#cp -rf ZouA dist
cp -rf dist/卡牌大师秒切助手/卡牌大师秒切助手.exe dist/ZouA
cp -rf dist/走A/走A.exe dist/ZouA
cp -rf dist/走A-E/走A-E.exe dist/ZouA
cp -rf dist/走A-Q/走A-Q.exe dist/ZouA
cp -rf dist/走A-W/走A-W.exe dist/ZouA
cp -rf dist/武器光速摸眼/武器光速摸眼.exe dist/ZouA
cp -rf dist/盲僧光速摸眼/盲僧光速摸眼.exe dist/ZouA

cp -rf dist/卡牌大师秒切助手/卡牌大师秒切助手.exe.manifest dist/ZouA
cp -rf dist/走A/走A.exe.manifest dist/ZouA
cp -rf dist/走A-E/走A-E.exe.manifest dist/ZouA
cp -rf dist/走A-Q/走A-Q.exe.manifest dist/ZouA
cp -rf dist/走A-W/走A-W.exe.manifest dist/ZouA
cp -rf dist/武器光速摸眼/武器光速摸眼.exe.manifest dist/ZouA
cp -rf dist/盲僧光速摸眼/盲僧光速摸眼.exe.manifest dist/ZouA

rm -rf dist/卡牌大师秒切助手
rm -rf dist/走A
rm -rf dist/走A-E
rm -rf dist/走A-Q
rm -rf dist/走A-W
rm -rf dist/武器光速摸眼
rm -rf dist/盲僧光速摸眼

rm -rf __pycache__
rm -rf build
rm -rf *.spec

