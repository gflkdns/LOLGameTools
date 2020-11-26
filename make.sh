rm -rf __pycache__
rm -rf build
rm -rf dist
rm -rf *.spec
pyinstaller -F -w ZA_Max.py -i icon.ico
rm -rf __pycache__
rm -rf build
rm -rf *.spec

cp -rf icon.ico dist

get_char()
{
SAVEDSTTY=`stty -g`
stty -echo
stty raw
dd if=/dev/tty bs=1 count=1 2> /dev/null
stty -raw
stty echo
stty $SAVEDSTTY
}

echo "Press any key to exit..."
char=`get_char`
