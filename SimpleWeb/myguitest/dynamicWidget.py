# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget


class MyWidget(QFrame):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.label = QLabel("Input")
        self.lineEdit = QLineEdit()
        self.label.setFixedHeight(10)
        self.listWidget = QListWidget()
        self.lineEdit.setFixedHeight(30)
        self.lineEdit.setFixedWidth(100)
        self.listWidget.setFixedWidth(100)
        self.listWidget.setFixedHeight(200)
        self.itemFamily = ['Cell', 'CellPlmn', 'cellId', 'PLMN', 'PlmnInfo']

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        #layout.setRowStretch(0,1)
        #layout.setColumnStretch(0,1)
        layout.addWidget(self.lineEdit, 0, 1)
        layout.addWidget(self.listWidget, 1, 1)
        #layout.setRowStretch(1, 4)
        #layout.setColumnStretch(1,1)
        layout.setVerticalSpacing(0)
        rect = QRect(9, 10, 100, 1000)
        layout.setGeometry(rect)
        self.setLayout(layout)


app = QApplication(sys.argv)
dyWiget = MyWidget()
dyWiget.show()
app.exec_()
