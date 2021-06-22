import cv2 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

from PIL import Image
import pytesseract as pyt
     
image_file = r'C:\Users\pichain\Desktop\work\sample\Pune\captcha.jpg'
im = Image.open(image_file)
text = pyt.image_to_string(image_file)
print(text)