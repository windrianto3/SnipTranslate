from PyQt5 import uic, QtWidgets, QtGui, QtCore


class WindowDropdownBox(QtWidgets.QComboBox):
    popupSignal = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupSignal.emit()
        super(WindowDropdownBox, self).showPopup()