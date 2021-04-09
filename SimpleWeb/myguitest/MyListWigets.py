# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class MyListWigets(QDialog):
    def __init__(self, parent=None):
        super(MyListWigets, self).__init__(parent)
        self.itemFamliy = ['Cell', 'Cellplmncfg', 'plmninfo', 'PLMN', 'cellPLMN']
        self.label = QLabel("Input")
        self.LWigets = QListWidget()
        # self.LWigets.addItems(self.itemFamliy)
        self.linedit = QLineEdit()
        self.linedit.setText('')
        # self.LWigets.hide()
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.label)
        splitter1.addWidget(self.linedit)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.linedit)
        splitter2.addWidget(self.LWigets)

        layout = QHBoxLayout()
        layout.addWidget(splitter1)
        layout.addWidget(splitter2)
        self.setLayout(layout)
        self.linedit.textEdited.connect(self.dynamicShow)
        self.LWigets.itemClicked.connect(self.chooseItem)

    def chooseItem(self, item):
        self.linedit.setText(item.text())

    def dynamicShow(self):
        curText = self.linedit.text()
        new_items = []
        if curText in self.itemFamliy:
            new_items.append(curText)
        elif curText == ' ' or curText == '':
            new_items = self.itemFamliy[:]
        else:
            for item in self.itemFamliy:
                if curText.upper() in item.upper():
                    new_items.append(item)

            if new_items == []:
                new_items = ['cannot match your input']

        self.updateitems(new_items)
        self.LWigets.showPopup()

    def printItems(self):
        index = 0
        while '' != self.LWigets.itemText(index):
            print("itemText(%d)" % index)
            print(self.LWigets.itemText(index))
            index = index + 1

    def updateitems(self, new_items):
        self.LWigets.show()
        self.LWigets.clear()
        self.LWigets.addItems(new_items)


app = QApplication(sys.argv)
comb = MyListWigets()
comb.show()
app.exec_()
