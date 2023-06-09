from pytesseract import image_to_string
import cv2
from PIL import Image
import deepl
import os
from dotenv import load_dotenv

class OCRHelper():
    def __init__(self):
        load_dotenv()
        self.token = os.environ.get("api-token")

    def _get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def _preprocess(self, imgpath):
        # Currently only uses grayscaling
        img = Image.open(image_path)
        return self._get_grayscale(cv2.imread(imgpath))
    
    def read_image(imgpath):
        processed_image = self._preprocess(self, imgpath)
        text = image_to_string(image = processed_image)
        return text