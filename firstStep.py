#this is the firt step in any desktop program using pyqt library
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys

FROM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FROM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinite loop


if __name__ == '__main__':
    main()