
import re
import pytesseract
from PIL import Image
from PIL import ImageGrab
if __name__ == '__main__':
    text = pytesseract.image_to_string(Image.open("cut.png"), lang="eng")
    print(text)