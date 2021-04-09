# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

box = QComboBox()
box.addItems(['a', 'b', 'c'])
box.show()
print('')
print(None)
print (box.itemText(3))
print (box.itemText(1))
box.removeItem(-1)
app.exec_()