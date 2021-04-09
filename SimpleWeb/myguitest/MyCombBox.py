# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *


class Mycomb(QDialog):
    def __init__(self, parent=None):
        super(Mycomb, self).__init__(parent)
        self.itemFamliy = ['Cell', 'Cellplmncfg', 'plmninfo', 'PLMN', 'cellPLMN']
        self.showitems = ['Cell', 'Cellplmncfg', 'plmninfo', 'PLMN', 'cellPLMN']
        self.label = QLabel("combbox")
        self.comb = QComboBox()
        self.comb.setEditable(True)
        self.comb.setCompleter(QCompleter())  # disable auto completion
        self.comb.addItems(self.itemFamliy)
        self.linedit = QLineEdit()
        self.comb.setLineEdit(self.linedit)
        self.linedit.setText('')
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comb)
        self.setLayout(layout)
        self.linedit.textEdited.connect(self.dynamicShow)

    def dynamicShow(self):
        curText = self.comb.currentText()
        if curText in self.itemFamliy:
            return
        if curText == ' ' or curText == '':
            return
        new_items = []

        for item in self.showitems:
            if curText.upper() in item.upper():
                new_items.append(item)

        del_items = list(set(self.showitems) ^ set(new_items))
        old_showitems = self.showitems
        if del_items != []:
            self.showitems = list(set(self.itemFamliy) - set(del_items))

        self.updateitems(old_showitems, self.showitems)
        self.LWigets.setEditText(curText)
        self.comb.showPopup()
        self.linedit.setFocus()

    def printItems(self):
        index = 0
        while '' != self.comb.itemText(index):
            print ("itemText(%d)" % index)
            print(self.comb.itemText(index))
            index = index + 1

    def updateitems(self, old_items, new_items):
        old_index_count = len(old_items)
        new_index_count = len(new_items)

        if old_index_count <= new_index_count:
            for index in range(old_index_count):
                self.comb.setItemText(index, new_items[index])
                new_items[index] = None
                print (58)
                self.printItems()
            for item in new_items:
                if item != None:
                    self.comb.addItem(item)
                print (62)
                self.printItems()
        else:
            for index in range(new_index_count):
                self.comb.setItemText(index, new_items[index])
                old_items[index] = None
                print(67)
                self.printItems()
            for item in old_items:
                if item != None:
                    index = self.comb.findText(item)
                    self.comb.removeItem(index)
                print(71)
                self.printItems()


app = QApplication(sys.argv)
comb = Mycomb()
comb.show()
app.exec_()
