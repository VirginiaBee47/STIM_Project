import tkinter as tk
from tkinter import CENTER, E, N, W, Label, StringVar, ttk

from pyparsing import col
def popUp(inst): 
    inst.pack_forget() # Destroy the parent, (May not be necessary)
    win = tk.Toplevel()
    win.geometry("300x125")
    win.wm_title("Enter your Summoner Name")
    l = ttk.Label(win, text="Enter Summoner Name:")
    l.place(relx=.5, rely=.3, anchor=CENTER)
    e = ttk.Entry(win, width=10, textvariable=sum_name)
    e.place(relx=.5, rely=.5, anchor=CENTER)
    b = ttk.Button(win ,text="Enter", command=lambda win=win : custom_destroy(win))
    b.place(relx=.5, rely=.7, anchor=CENTER)
    # TODO: Add Enter key functionality

def custom_destroy(win):
    win.destroy()
    SecondaryWindow(root)

class MainWindow(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()
        login_button = ttk.Button(self, text="Log In", command=popUp)
        login_button['command'] = lambda inst=self: popUp(inst)
        login_button.pack()
       

class SecondaryWindow(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()
        if (sum_name.get() == ""):
            print("Why is no display")
            ttk.Label(self, text="Invalid Summoner Try Again!").place(relx=.5, rely=.5, anchor=CENTER)
            popUp(self)
            # TODO: Label is not showing up before popUp is called, not a big deal just good for flare
        else:
            ttk.Label(self, text="Summoner Name: ").grid(column=0, row=0, sticky=(N, E))
            sum_label = ttk.Label(self, textvariable=sum_name)
            sum_label.grid(column=1, row=0, sticky=(N, W))
            ttk.Label(self, text="Welcome Summoner Gathering Stats!").grid(column=1, row=1)




#if (__name__ == "__main__"):
root = tk.Tk()
root.geometry("640x400")
sum_name = StringVar()
main_window = MainWindow(root)
root.mainloop()
