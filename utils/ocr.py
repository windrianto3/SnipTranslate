from pytesseract import image_to_string
import cv2
from PIL import Image
import deepl
import os
from dotenv import load_dotenv

class TLHelper():
    def __init__(self):
        load_dotenv()
        self.token = os.environ.get("api-token")
        self.tler = deepl.Translator(self.token)

    def _get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def _preprocess(self, imgpath):
        # Currently only uses grayscaling for preprocessing
        return self._get_grayscale(cv2.imread(imgpath))
    
    def read_image(self, imgpath):
        processed_image = self._preprocess(imgpath)
        text = image_to_string(image = processed_image, lang='jpn')
        return text

    def translate_text(self, text):
        result_text = self.tler.translate_text(text, target_lang="EN-US")
        return result_text
    
    def translate_image(self,imgpath):
        text = self.read_image(imgpath)
        return self.translate_text(text)

tl = TLHelper()
text = tl.translate_image(imgpath=r"D:\Projects\translator\translator\screenshots\picture.png")
print(text)