# -*- coding: utf-8 -*-

from tkinter import *

entry_list = ['Name', 'Age']


class App(Tk):
    def __init__(self):
        super().__init__()
        self.createWigets()

    def make_entries(self, root):
        entry_list = ['name', 'age', 'addr']

        for ent_name in entry_list:
            frm = Frame(root)
            label = Label(frm, text=ent_name)
            label.config(height=2, width=4)
            ent = Entry(frm)
            label.pack(side=LEFT, ipadx=4, ipady=4, padx=4, pady=4)
            ent.pack(side=RIGHT)
            frm.pack(side=TOP)

    def createWigets(self):
        # top buton frame
        topButtonFrame = Frame(self)
        genOutputButton = Button(topButtonFrame, text="Run to get output")
        genOutputButton.pack(side=LEFT, padx=4, pady=10)
        fileSelectButton = Button(topButtonFrame, text="Select File Dir")
        fileSelectButton.pack(side=RIGHT, padx=4, pady=10)

        topButtonFrame.pack(side=TOP)

        # cfg input frame
        cfgInputFrame = Frame(self)
        self.make_entries(cfgInputFrame)
        cfgInputFrame.pack(side=TOP)


if __name__ == '__main__':
    display = App()
    display.mainloop()
