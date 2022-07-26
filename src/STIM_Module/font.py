import tkinter as tk
from tkinter import *
from tkinter import Label, font

win = tk.Tk()
fonts = list(font.families())
rowcount = 0
columncount = 0

for i in fonts:
    if rowcount % 30 == 0:
        columncount += 1
        rowcount = 0
    Label(win, text=i, font=(i, 10, 'bold')).grid(row=rowcount, column=columncount)
    rowcount += 1

win.mainloop()
