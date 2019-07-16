import pytesseract
from PIL import Image

image = Image.open('C:\\Users\\Administrator\\Desktop\\微信截图_20190605104456.png')
code = pytesseract.image_to_string(image)
print(code)