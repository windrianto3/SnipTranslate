from pytesseract import image_to_string, get_languages
import cv2
from PIL import Image
import deepl
import os
from dotenv import load_dotenv
import numpy

class TLHelper():
    def __init__(self):
        load_dotenv()
        self.token = os.environ.get("api-token")
        self.tler = deepl.Translator(self.token)
        self.availableSRClangs = get_languages()
    
    def convertPILtoCV(self, pil_image):
        return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)

    def _get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def _preprocess(self, image):
        # Currently only uses grayscaling for preprocessing
        return self._get_grayscale(image)
    
    def read_image(self, image):
        processed_image = self._preprocess(image)
        detected_text = image_to_string(image = processed_image, lang='eng')
        translated_text = self.translate_text(detected_text)
        return detected_text, translated_text.text

    def translate_text(self, text):
        result_text = self.tler.translate_text(text, target_lang="EN-US")
        return result_text