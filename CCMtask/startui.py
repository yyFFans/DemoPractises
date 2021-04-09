# -*- coding: utf-8 -*-
import sys

from ccm import *
from PyQt5.QtWidgets import QMainWindow, QApplication


class CCMWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CCMTask()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CCMWindow()

    mainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    mainWindow.setFixedSize(mainWindow.width(), mainWindow.height())
    mainWindow.show()
    sys.exit(app.exec_())