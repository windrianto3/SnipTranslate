from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100,100,500,300)
    window.setWindowTitle("Screencap Translator")

    layout = QVBoxLayout() #or Hbox

    label = QLabel("Press the Button Below to take a Screenshot")

    scbutton = QPushButton("Press me!")
    scbutton.clicked.connect(on_clicked)

    layout.addWidget(label)
    layout.addWidget(scbutton)

    window.setLayout(layout)

    window.show()
    app.exec_()

def on_clicked():
    msg = QMessageBox()
    msg.setText("Hello World")
    msg.exec()

if __name__ == '__main__':
    main()