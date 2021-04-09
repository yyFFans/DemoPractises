# -*- coding: utf-8 -*-

from tkinter import *

root = Tk()
labelfont = ('times', 10, 'bold')  # family,size,style
widget = Label(root, text='Hello config world', padx=20, pady=20)
widget.config(bg='black', fg='yellow')  # also hexadecimal color identifier stringlike '#ff0000'
widget.config(font=labelfont)
widget.config(height=3, width=20)
widget.pack(expand=YES, fill=BOTH)

widget = Button(root, text='Spam', padx=0, pady=0)
widget.pack(padx=10, pady=10)
widget.config(cursor='gumby', bd=8, relief=RAISED, bg='dark green', fg='white')
widget.config(font=('helvetica', 20, 'underline italic'))
widget.pack(expand=YES, fill=BOTH)
root.mainloop()
