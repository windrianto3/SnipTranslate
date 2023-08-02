from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import utils.uisnip as uisnip
import utils.ocr as ocr
import utils.screencap as screencap
from PIL.ImageQt import ImageQt
import deepl
#import windowdropdownbox

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle("Screen Translator")
        self.show()

        self.ocrHelper = ocr.TLHelper()
        self.screencapHelper = screencap.ScreenCapHelper()
        self.snipHelper = uisnip.CaptureScreen()
        self.snipHelper.ui = self

        self.errordialog = QtWidgets.QMessageBox()
        self.errordialog.setWindowTitle("Error")

        self.imagelabel.setScaledContents(False)

        self.snipbutton.clicked.connect(self.snipCapture)
        self.capmonitorbutton.clicked.connect(self.desktopScreenshot)
        self.capwindowbutton.clicked.connect(self.windowScreenshot)
        self.windowbox.popupSignal.connect(self.updateDropdown)
        
        # Declare app variables
        self.winlist = None
        self.wintitles = None
        self.curr_image = None
        self.pix = None
    
    def updateUI(self):
        # Update displayed image to the most recent capture
        self.imagelabel.setPixmap(self.pix.scaled(771, 341, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))

        # Run OCR and translator
        detected_text, translated_text = self.ocrHelper.read_image(self.ocrHelper.convertPILtoCV(self.curr_image))
        self.detectedtextbox.setPlainText(detected_text)
        self.translatedtextbox.setPlainText(translated_text)

    def desktopScreenshot(self):
        self.curr_image = self.screencapHelper.saveDesktopScreenScreenshot()
        qim = ImageQt(self.curr_image).copy()
        qim_pix = QtGui.QPixmap.fromImage(qim)
        self.pix = qim_pix
        self.updateUI()

    def snipCapture(self):
        self.snipHelper.show()

    def updateDropdown(self):
        self.winlist = self.screencapHelper.list_window_names()
        self.wintitles = [x[1] for x in self.winlist]
        self.windowbox.clear()
        self.windowbox.addItems(self.wintitles)
        
    def windowScreenshot(self):
        try:
            self.curr_image = self.screencapHelper.saveWindow(self.windowbox.currentText().lower(), "pic.png")
            #print("successfully grabbed window")
            self.pix = QtGui.QPixmap.fromImage(ImageQt(self.curr_image).copy())
            self.updateUI()
        except deepl.exceptions.ConnectionException as ce:
            self.errordialog.setText("Unable to connect to translation API. Please try again.")
            self.errordialog.exec()
        except IndexError as ie:
            self.errordialog.setText("Selected window no longer exists.")
            self.errordialog.exec()
        except ValueError as ve:
            if str(ve) == "text must not be empty":
                self.errordialog.setText("No text detected.")
                self.errordialog.exec()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Ui()
    app.exec_()
