from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic, QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QBuffer
from PIL.ImageQt import ImageQt
from PIL import Image
import io

class CaptureScreen(QtWidgets.QSplashScreen):
    """QSplashScreen, that track mouse event for capturing screenshot."""
    def __init__(self):
        """"""
        super(CaptureScreen, self).__init__()
 
        # Points on screen marking the origin and end of regtangle area.
        self.origin = QtCore.QPoint(0,0)
        self.end = QtCore.QPoint(0,0)
 
        # A drawing widget for representing bounding area
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

        # Variable to store image
        self.storedImage = None

        self.ui = None
 
        self.createDimScreenEffect()
 
    def createDimScreenEffect(self):
        """Fill splashScreen with black color and reduce the widget opacity to create dim screen effect"""
 
        # Get the screen geometry of the main desktop screen for size ref
        primScreenGeo = QtGui.QGuiApplication.primaryScreen().geometry()
 
        screenPixMap = QtGui.QPixmap(primScreenGeo.width(), primScreenGeo.height())
        screenPixMap.fill(QtGui.QColor(0,0,0))
 
        self.setPixmap(screenPixMap)
 
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setWindowOpacity(0.4)
 
    def mousePressEvent(self, event):
        """Show rectangle at mouse position when left-clicked"""
        if event.button() == QtCore.Qt.LeftButton:
            self.origin = event.pos()
 
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rubberBand.show()
 
    def mouseMoveEvent(self, event):
        """Resize rectangle as we move mouse, after left-clicked."""
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
 
    def mouseReleaseEvent(self, event):
        """Upon mouse released, ask the main desktop's QScreen to capture screen on defined area."""
        if event.button() == QtCore.Qt.LeftButton:
            self.end = event.pos()
 
            self.rubberBand.hide()
            self.hide()
 
            primaryScreen = QtGui.QGuiApplication.primaryScreen()
            grabbedPixMap = primaryScreen.grabWindow(0, self.origin.x(), self.origin.y(), self.end.x()-self.origin.x(), self.end.y()-self.origin.y())
            grabbedPixMap.save('screenshot_windowed.jpg', 'jpg')

            self.storedImage = grabbedPixMap
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            self.storedImage.save(buffer, "PNG")

            self.ui.curr_image = Image.open(io.BytesIO(buffer.data()))
            self.ui.pix = self.storedImage
            
            self.ui.updateUI()