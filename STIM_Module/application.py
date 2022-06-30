import tkinter as tk
from tkinter import CENTER, E, N, W, Label, StringVar, ttk

from pandas import DataFrame
from dummy_matplot import diff_graph, gold_graph, exp_graph
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def popUp(inst): 
    inst.pack_forget() # Destroy the parent, (May not be necessary)
    win = tk.Toplevel()
    win.config(bg="#808c9f")
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


def load_game(master, game_idx):
    # TODO: Call API to get game data and call MATPLOT to graph it
    pass

def draw_graph(parent, type="gold", posy=0, posx=0):
    df_obj = DataFrame()
    figure2 = plt.Figure(figsize=(4,4), dpi=50)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, parent)
    if type == "gold":
        df_obj = gold_graph()
        df_obj = df_obj[['Minute','Total Gold']].groupby('Minute').sum()
        df_obj.plot(kind='line', legend=True, ax=ax2, color='y',marker='o', fontsize=10, ylabel="Total Gold")
        ax2.set_title('Time Vs. Gold')
        line2.get_tk_widget().grid(column=1, row=3)
    elif type == "exp":
        df_obj = exp_graph()
        df_obj = df_obj[['Minute','Total Exp']].groupby('Minute').sum()
        df_obj.plot(kind='line', legend=True, ax=ax2, color='b',marker='o', fontsize=10, ylabel="Total Exp")
        ax2.set_title('Time Vs. Experience')
        line2.get_tk_widget().grid(column=2, row=3)
    elif type == "diff":
        df_obj = diff_graph()
        df_obj = df_obj[['Minute','Gold Diff']].groupby('Minute').sum()
        df_obj.plot(kind='line', legend=True, ax=ax2, color='y',marker='o', fontsize=10, ylabel="Gold Diff")
        ax2.set_title('Experience Differential')
        line2.get_tk_widget().grid(column=3, row=3)
    else:
        df_obj = diff_graph()
        df_obj = df_obj[['Minute','Gold Diff']].groupby('Minute').sum()
        df_obj.plot(kind='line', legend=True, ax=ax2, color='y',marker='o', fontsize=10, ylabel="Gold Diff")
        ax2.set_title('Gold Differential')


    

class MainWindow(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()
        login_button = ttk.Button(self, text="Log In", command=popUp)
        login_button['command'] = lambda inst=self: popUp(inst)
        login_button.pack()
       

class SecondaryWindow(ttk.Frame): # Summoner Name Verification
    def __init__(self, master):
        ttk.Frame.__init__(self, master, style="My.TFrame")
        self.pack()
        if (sum_name.get() == ""):
            print("Why is no display")
            ttk.Label(self, text="Invalid Summoner Try Again!").place(relx=.5, rely=.5, anchor=CENTER)
            popUp(self)
            # TODO: Label is not showing up before popUp is called, not a big deal just good for flare
        else:
            ttk.Label(self, text="Summoner Name: ").grid(column=0, row=0, sticky=W)
            sum_label = ttk.Label(self, textvariable=sum_name)
            sum_label.grid(column=1, row=0, sticky=W)
            ttk.Label(self, text="Welcome Summoner Gathering Stats!").grid(column=0, row=1,sticky=(N, W))
            draw_graph(self, "gold")
            draw_graph(self, "exp")
            draw_graph(self, "diff")


            


#if (__name__ == "__main__"):
root = tk.Tk()
root.geometry("800x600")
root.config(bg="#808c9f")
s = ttk.Style()
s.configure('My.TFrame', background="#808c9f")
sum_name = StringVar()
main_window = MainWindow(root)
root.mainloop()
