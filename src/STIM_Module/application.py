import tkinter as tk
from tkinter import CENTER, E, N, S, TOP, W, Label, StringVar, ttk
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from pandas import DataFrame

from STIM_Module.dummy_matplot import ret_graph, ret_pro_graph
from STIM_Module.api_funcs import *


def matplot_init(color="grey"):
    COLOR = color
    matplotlib.rcParams['text.color'] = COLOR
    matplotlib.rcParams['axes.labelcolor'] = COLOR
    matplotlib.rcParams['xtick.color'] = COLOR
    matplotlib.rcParams['ytick.color'] = COLOR
    matplotlib.rcParams['axes.edgecolor'] = "black"
    matplotlib.rcParams['axes.facecolor'] = "black"



def popUp(inst, master): 
    inst.pack_forget()
    win = tk.Toplevel()
    win.config(bg="#808c9f")
    win.geometry("300x125")
    win.wm_title("Enter your Summoner Name")
    main_style = ttk.Style()
    main_style.configure("Label_Style.TLabel", background= "#808c9f", foreground="white")
    l = ttk.Label(win, text="Enter Summoner Name:", style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold"))
    l.place(relx=.5, rely=.3, anchor=CENTER)
    sum_name = StringVar()
    e = ttk.Entry(win, width=10, textvariable=sum_name)
    e.place(relx=.5, rely=.5, anchor=CENTER)
    b = ttk.Button(win ,text="Enter", command=lambda win=win, sum_name=sum_name, master=master: custom_destroy(win, sum_name, master))
    b.place(relx=.5, rely=.7, anchor=CENTER)
    win.bind('<Return>', lambda event:custom_destroy(win, sum_name, master))
    e.focus()

def custom_destroy(win, sum_name, master):
    win.destroy()
    pro_games = collect_data_for_rank()
    SecondaryWindow(master, sum_name, pro_games)


def draw_all_graphs(parent, sum_name=None, game_id=None, row_num=1, filename=None):
    if filename is not None:
        draw_graph(parent, "g", col_num=1, row_num=row_num, filename=filename)
        draw_graph(parent, "e", col_num=2, row_num=row_num, filename=filename)
        draw_graph(parent, "d", col_num=3, row_num=row_num, filename=filename)
    else:
        draw_graph(parent, "g", sum_name.get(), game_id, 1, row_num)
        draw_graph(parent, "e", sum_name.get(), game_id, 2, row_num)
        draw_graph(parent, "d", sum_name.get(), game_id, 3, row_num)

        
def draw_graph(parent, type="g", sum_name=None, game_id=None, col_num=0, row_num=0, filename=None):
    matplot_init("white")
    df_obj = DataFrame()
    figure2 = plt.Figure(figsize=(4,4), dpi=50, facecolor='#707c8f')
    ax2 = figure2.add_subplot(111)
    ax2.patch.set_facecolor('black')
    line2 = FigureCanvasTkAgg(figure2, parent)
    if filename is None:
        df_obj, xVar, yVar, line_color = ret_graph(type, sum_name, game_id)
    else:
        df_obj, xVar, yVar, line_color = ret_pro_graph(type, filename)
    df_obj = df_obj[[xVar,yVar]].groupby(xVar).sum()
    df_obj.plot(kind='line', legend=True, ax=ax2, color=line_color ,marker='o', fontsize=10, ylabel=yVar)
    ax2.set_title("Time Vs. %s" % yVar)
    widget = line2.get_tk_widget()
    widget.grid(column=col_num, row=row_num)


def delete_user_csvs(root):
    #print("This got called???")
    dir_name = "./data"
    if os.path.exists(dir_name):
        files = os.listdir(dir_name)
        for file in files:
            if file.endswith(".csv") or file.endswith(".json"):
                os.remove(os.path.join(dir_name, file))
    root.destroy()

class MainWindow(ttk.Frame):
    def __init__(self, master):
        main_style = ttk.Style()
        main_style.configure("Button_Style.TButton", background= "#808c9f" )
        ttk.Frame.__init__(self, master)
        self.pack()
        login_button = ttk.Button(self, text="Log In", command=popUp, style="Button_Style.TButton")
        login_button['command'] = lambda inst=self, master=master : popUp(inst, master)
        login_button.pack(side=TOP)
       

class SecondaryWindow(ttk.Frame): # Summoner Name Verification
    def __init__(self, master, sum_name, pro_games):
        ttk.Frame.__init__(self, master, style="My.TFrame")
        self.pack()
        l_style = ttk.Style()
        l_style.configure("Label_Style.TLabel", background= "#808c9f", foreground="white")
        if (check_summoner_exists(sum_name.get()) == False or sum_name.get() == ""):
            ttk.Label(self, text="Invalid Summoner Try Again!", style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold")).grid(column=0, row=0)
            popUp(self, master)
            # TODO: Label is not showing up before popUp is called, not a big deal just good for flare
        else:
            num_games = 3
            puuid, sum_level = get_summoner(sum_name.get())
            recent_game_ids = get_recent_game_ids(puuid, num_games)
            ttk.Label(self, text="Summoner Name: %s\nSummoner Level: %s" % (sum_name.get(), str(sum_level)), style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold")).grid(column=0, row=0, sticky=(W, N), padx= 5)
            # User Game Display
            make_game_csv(sum_name.get(), puuid, num_games, recent_game_ids)
            GameDisplayWindow(master, self, sum_name, 0, 0, recent_game_ids, pro_games)

class GameDisplayWindow(ttk.Frame):
    def __init__(self, master, parent,sum_name, user_game_num, pro_game_num, game_ids, pro_games):
        parent.pack_forget()
        ttk.Frame.__init__(self, master, style="My.TFrame")
        self.pack()
        l_style = ttk.Style()
        l_style.configure("Label_Style.TLabel", background= "#808c9f", foreground="white")
        _, sum_level = get_summoner(sum_name.get())
        recent_game_id = game_ids[user_game_num]
        ttk.Label(self, text="Summoner Name: %s\nSummoner Level: %s" % (sum_name.get(), str(sum_level)), style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold")).grid(column=0, row=0, sticky=(W, N), padx= 5)
        ttk.Label(self, text="%s's Stats For \nGame %s" %(sum_name.get(), ((user_game_num % 3) + 1)), style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold")).grid(column=0, row=1, sticky=W)
        draw_all_graphs(self, sum_name, game_ids[user_game_num], row_num=1)
        ttk.Button(self, text="View Next User Game", command=lambda : GameDisplayWindow(master, self, sum_name, ((user_game_num+1) % 3), pro_game_num, game_ids, pro_games)).grid(column=0, row=1, sticky=(S, W))
        # Drawing Pro Games
        ttk.Label(self, text="Pro's Stats For \nGame %d" %((pro_game_num % 3) + 1), style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold")).grid(column=0, row=2, sticky=W)
        draw_all_graphs(self, row_num=2, filename=pro_games[pro_game_num])
        ttk.Button(self, text="View Next Pro Game", command=lambda : GameDisplayWindow(master, self, sum_name, user_game_num, ((pro_game_num + 1) % 3), game_ids, pro_games)).grid(column=0, row=2, sticky=(S, W))
        # Place Holder Advice Label
        advice_string = "Do better forehead."
        ttk.Label(self, text="Advice For This Comparison:", style="Label_Style.TLabel", font=("Friz Quadrata", 16, "bold")).grid(column=0, row=3, sticky=(W, N))
        ttk.Label(self, text="Tip 1: %s" % advice_string, style="Label_Style.TLabel", font=("Friz Quadrata", 10)).grid(column=0, row=4, sticky=(W, N))


def main():
    root = tk.Tk()
    root.geometry("1080x720")
    root.config(bg="#808c9f")
    s = ttk.Style()
    s.configure('My.TFrame', background="#808c9f")
    main_window = MainWindow(root)
    root.protocol("WM_DELETE_WINDOW", lambda : delete_user_csvs(root))
    root.mainloop()


if (__name__ == "__main__"):
    main()