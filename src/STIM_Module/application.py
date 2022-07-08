import tkinter as tk
from tkinter import CENTER, E, N, TOP, W, Label, StringVar, ttk
import matplotlib

from pandas import DataFrame
from pip import main
from dummy_matplot import ret_graph
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from STIM_Module.api_funcs import *


def matplot_init(color="grey"):
    COLOR = color
    matplotlib.rcParams['text.color'] = COLOR
    matplotlib.rcParams['axes.labelcolor'] = COLOR
    matplotlib.rcParams['xtick.color'] = COLOR
    matplotlib.rcParams['ytick.color'] = COLOR
    matplotlib.rcParams['axes.edgecolor'] = "black"
    matplotlib.rcParams['axes.facecolor'] = "black"


def pop_up(inst, master):
    inst.pack_forget()  # Destroy the parent, (May not be necessary)
    win = tk.Toplevel()
    win.config(bg="#808c9f")
    win.geometry("300x125")
    win.wm_title("Enter your Summoner Name")
    main_style = ttk.Style()
    main_style.configure("Label_Style.TLabel", background="#808c9f", foreground="white")
    l = ttk.Label(win, text="Enter Summoner Name:", style="Label_Style.TLabel")
    l.place(relx=.5, rely=.3, anchor=CENTER)
    sum_name = StringVar()
    e = ttk.Entry(win, width=10, textvariable=sum_name)
    e.place(relx=.5, rely=.5, anchor=CENTER)
    b = ttk.Button(win, text="Enter",
                   command=lambda win=win, sum_name=sum_name, master=master: custom_destroy(win, sum_name, master))
    b.place(relx=.5, rely=.7, anchor=CENTER)
    # TODO: Add Enter key functionality


def custom_destroy(win, sum_name, master):
    win.destroy()
    SecondaryWindow(master, sum_name)


def load_game(master, game_idx):
    # TODO: Call API to get game data and call MATPLOT to graph it
    pass


def draw_graph(parent, type="g", sum_name=None, game_id=None):
    matplot_init("white")
    df_obj = DataFrame()
    figure2 = plt.Figure(figsize=(4, 4), dpi=50, facecolor='#707c8f')
    ax2 = figure2.add_subplot(111)
    ax2.patch.set_facecolor('black')
    line2 = FigureCanvasTkAgg(figure2, parent)
    df_obj, xVar, yVar, line_color, col_num = ret_graph(type, sum_name, game_id)
    df_obj = df_obj[[xVar, yVar]].groupby(xVar).sum()
    df_obj.plot(kind='line', legend=True, ax=ax2, color=line_color, marker='o', fontsize=10, ylabel=yVar)
    ax2.set_title("Time Vs. %s" % yVar)
    widget = line2.get_tk_widget()
    widget.grid(column=col_num, row=0)


class MainWindow(ttk.Frame):
    def __init__(self, master):
        main_style = ttk.Style()
        main_style.configure("Button_Style.TButton", background="#808c9f")
        ttk.Frame.__init__(self, master)
        self.pack()
        login_button = ttk.Button(self, text="Log In", command=pop_up, style="Button_Style.TButton")
        login_button['command'] = lambda inst=self, master=master: pop_up(inst, master)
        login_button.pack(side=TOP)


class SecondaryWindow(ttk.Frame):  # Summoner Name Verification
    def __init__(self, master, sum_name):
        ttk.Frame.__init__(self, master, style="My.TFrame")
        self.pack()
        l_style = ttk.Style()
        l_style.configure("Label_Style.TLabel", background="#808c9f", foreground="white")
        if check_summoner_exists(sum_name.get()) == False:
            print(sum_name.get())
            print("Why is no display")
            ttk.Label(self, text="Invalid Summoner Try Again!", style="Label_Style.TLabel").grid(column=0, row=0)
            pop_up(self, master)
            # TODO: Label is not showing up before pop_up is called, not a big deal just good for flare
        else:
            ttk.Label(self, text="Summoner Name: %s\nWelcome Summoner Gathering Stats!" % sum_name.get(),
                      style="Label_Style.TLabel").grid(column=0, row=0, sticky=(W, N), padx=5)
            puuid, _ = get_summoner(sum_name.get())
            recent_game_id = get_recent_game_ids(puuid, 1)
            print(recent_game_id[0])
            make_game_csv(sum_name.get(), puuid, 1, recent_game_id)
            draw_graph(self, "g", sum_name.get(), recent_game_id[0])
            draw_graph(self, "e", sum_name.get(), recent_game_id[0])
            draw_graph(self, "d", sum_name.get(), recent_game_id[0])


def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.config(bg="#808c9f")
    s = ttk.Style()
    s.configure('My.TFrame', background="#808c9f")
    main_window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
