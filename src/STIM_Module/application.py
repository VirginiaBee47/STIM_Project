import timeit
from time import sleep, time
import tkinter as tk
from tkinter import CENTER, E, N, S, TOP, W, Label, StringVar, ttk
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3 as sq
from pandas import DataFrame
from threading import Thread
from PIL import ImageTk, Image

from STIM_Module.dummy_matplot import ret_graph, ret_pro_graph
from STIM_Module.api_funcs import *
from STIM_Module.analysis import just_the_tips


def matplot_init(color="grey"):
    COLOR = color
    matplotlib.rcParams['text.color'] = COLOR
    matplotlib.rcParams['axes.labelcolor'] = COLOR
    matplotlib.rcParams['xtick.color'] = COLOR
    matplotlib.rcParams['ytick.color'] = COLOR
    matplotlib.rcParams['axes.edgecolor'] = "black"
    matplotlib.rcParams['axes.facecolor'] = "black"


def styles_init():
    # Frame Default Styles
    frame_style = ttk.Style()
    frame_style.configure('My.TFrame', background="#808c9f")
    # Labels Default Styles
    l_style = ttk.Style()
    l_style.configure("Text.TLabel", background="#808c9f", foreground="white", anchor="center",
                      font=("Californian FB", 12))
    t_l_style = ttk.Style()
    t_l_style.configure("Title.TLabel", background="#808c9f", foreground="white", anchor="center",
                        font=("Californian FB", 16, "bold"))
    # Buttons Default Styles
    b_style = ttk.Style()
    b_style.configure("My.TButton", background="#808c9f", font=("Californian FB", 10))
    # Entry Default Styles NOT WOKRING
    e_style = ttk.Style()
    e_style.configure("My.TEntry", background="#909cAf", font=("Californian FB", 10), foreground="dark blue")


def popUp(binst, master, invalid=False):
    binst.destroy()
    win = tk.Toplevel()
    win.config(bg="#808c9f")
    win.geometry("300x125")
    win.wm_title("Enter your Summoner Name")
    if invalid:
        l = ttk.Label(win, text="Invalid input! Enter Summoner Name:", style="Text.TLabel")
    else:
        l = ttk.Label(win, text="Enter Summoner Name:", style="Text.TLabel")
    l.place(relx=.5, rely=.3, anchor=CENTER)
    sum_name = StringVar()
    e = ttk.Entry(win, width=10, textvariable=sum_name, style="My.TEntry")
    e.place(relx=.5, rely=.5, anchor=CENTER)
    b = ttk.Button(win, text="Enter", style="My.TButton",
                   command=lambda win=win, sum_name=sum_name, master=master: custom_destroy(win, sum_name, master))
    b.place(relx=.5, rely=.7, anchor=CENTER)
    win.bind('<Return>', lambda event: custom_destroy(win, sum_name, master))
    e.focus()
    win.protocol("WM_DELETE_WINDOW", lambda: custom_destroy(win, sum_name, master))


def custom_destroy(win, sum_name, master):
    for ele in master.winfo_children():
        ele.destroy()
    if (check_summoner_exists(sum_name.get()) == False or sum_name.get() == ""):
        popUp(win, master, invalid=True)
        MainWindow(master, button=False)
    else:
        SecondaryWindow(master, sum_name)


class AsyncGraphDraw(Thread):
    def __init__(self, parent, sum_name=None, game_id=None, row_num=1, is_pro=False):
        super().__init__()
        self.parent = parent
        self.sum_name = sum_name
        self.game_id = game_id
        self.row_num = row_num
        self.is_pro = is_pro

    def run(self):
        if self.is_pro:
            draw_graph(self.parent, "g", self.sum_name[0], self.game_id, 1, self.row_num)
            draw_graph(self.parent, "e", self.sum_name[0], self.game_id, 2, self.row_num)
            draw_graph(self.parent, "d", self.sum_name[0], self.game_id, 3, self.row_num)
        else:
            draw_graph(self.parent, "g", self.sum_name.get(), self.game_id, 1, self.row_num)
            draw_graph(self.parent, "e", self.sum_name.get(), self.game_id, 2, self.row_num)
            draw_graph(self.parent, "d", self.sum_name.get(), self.game_id, 3, self.row_num)


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
    figure2 = plt.Figure(figsize=(4, 4), dpi=50, facecolor='#707c8f')
    ax2 = figure2.add_subplot(111)
    ax2.patch.set_facecolor('black')
    line2 = FigureCanvasTkAgg(figure2, parent)
    if filename is None:
        df_obj, xVar, yVar, line_color = ret_graph(type, sum_name, game_id)
    else:
        df_obj, xVar, yVar, line_color = ret_pro_graph(type, filename)
    df_obj = df_obj[[xVar, yVar]].groupby(xVar).sum()
    df_obj.plot(kind='line', legend=True, ax=ax2, color=line_color, marker='o', fontsize=10, ylabel=yVar)
    ax2.set_title("Time Vs. %s" % yVar)
    widget = line2.get_tk_widget()
    widget.grid(column=col_num, row=row_num)


def delete_user_csvs(root):
    dir_name = "./data"
    if os.path.exists(dir_name):
        files = os.listdir(dir_name)
        for file in files:
            if file.endswith(".csv") or file.endswith(".json"):
                os.remove(os.path.join(dir_name, file))
    root.destroy()


class MainWindow(ttk.Frame):
    def __init__(self, master, button=True):
        ttk.Frame.__init__(self, master, style="My.TFrame")
        self.pack()
        
        if button:
            self.login_button = ttk.Button(self, text="Log In", command=popUp, style="My.TButton")
            self.login_button['command'] = lambda inst=self, master=master: popUp(self.login_button, master)
            self.login_button.grid(column=1, row=3, sticky=N)
        
        
        title = "Welcome to The League of Legends \nStatistics Tracker and Improvement Manager \nor STIM for short!"
        
        what_is_STIM = [
            "STIM is a companion app for Riot Games' multiplayer online battle arena (MOBA) game League of Legends.",
            "What this companion app does is it pulls real match data from your most recent match and displays it in a friendly format.",
            "It displays the most recent 3 games and 3 random games from a pro player, and displays important statistics such as gold and",
            "experience gain and the gold differential versus your opponent. Our app displays this data and",
            "also formulates an analysis to provide you tips and advice on how to improve your gameplay."
        ]
        
        how_to_use = [
            "1. Login using your summoner username\n"
            "2. Scroll through your user games and pro games independently\n"
            "3. Comparison between the two displayed games will be displayed in the advice section below the graphs.\n"
            "4. Invalid summoner names will be rejected and you will be prompted again for a valid summoner name"
        ]
        
        credits = [
            "Project Leader and Backend: Benjamin Covert\n"
            "Front End and GUI: David Hutchins\n"
            "Game Analysis and Distribution: Jaxton Willman"
        ]
        
        ttk.Label(self, text=title, style="Title.TLabel", anchor="center", justify="center").grid(column=1, row=0, sticky=N)
        
        ttk.Label(self, text="What is STIM?", style="Title.TLabel", anchor="center", justify="center").grid(column=0, row=1, sticky=N)
        ttk.Label(self, text=' '.join(what_is_STIM), style="Text.TLabel", anchor="center", justify="left", wraplength=300).grid(column=0, row=2, sticky=N)
        
        ttk.Label(self, text="How to Use it?", style="Title.TLabel", anchor="center", justify="center").grid(column=1, row=1, sticky=N)
        ttk.Label(self, text=' '.join(how_to_use), style="Text.TLabel", anchor="center", justify="left", wraplength=300).grid(column=1, row=2, sticky=N)
        
        ttk.Label(self, text="Credits", style="Title.TLabel", anchor="center", justify="center").grid(column=2, row=1, sticky=N)
        ttk.Label(self, text=' '.join(credits), style="Title.TLabel", anchor="center", justify="left", wraplength=300).grid(column=2, row=2, sticky=N)
        
        # Load image
        img_path = "src/STIM_Module/assets/Images/lol_image.jpg"
        if os.path.exists(img_path):
            self.img = ImageTk.PhotoImage(Image.open(img_path).resize((500, 250)))
            ttk.Label(self, image=self.img, anchor="center", borderwidth=0, background="#808c9f").grid(column=0, row=4, columnspan=3)


class SecondaryWindow(ttk.Frame):  # Summoner Name Verification
    def __init__(self, master, sum_name, pro_name=None):
        ttk.Frame.__init__(self, master, style="My.TFrame")

        # time_var = timeit.timeit(lambda: collect_data_for_rank(), number=1)
        pro_name = []
        pro_games_thread = Thread(target=collect_data_for_rank, args=("RANKED_SOLO_5x5", "DIAMOND", "I",
                                                                      pro_name))
                                    # THIS TAKES 7 SECONDS THIS IS MULTITHREADABLE IF I REMOVE RETURN
        pro_games_thread.start()
        # print(time_var)
        # TODO: Label is not showing up before popUp is called, not a big deal just good for flare

        num_games = 3
        puuid, sum_level = get_summoner(sum_name.get())
        recent_game_ids = get_recent_game_ids(puuid, num_games)

        # ttk.Label(self, text="Summoner Name: %s\nSummoner Level: %s" % (sum_name.get(), str(sum_level)), style="Title.TLabel").grid(column=0, row=0, sticky=(W, N), padx= 5)
        # User Game Display
        create_sqlite_db(sum_name.get())
        csv_thread = Thread(target=add_data_to_db, args=(sum_name.get(), puuid, num_games, recent_game_ids))
        csv_thread.start()
        self.pack()
        dot = 0
        dots = [".", "..", "..."]
        while (csv_thread.is_alive() or pro_games_thread.is_alive()):
            l = ttk.Label(self, text="Loading%s" % dots[dot % 3], style="Title.TLabel")
            l.grid(column=0, row=0, sticky=W)
            self.update()
            master.update()
            dot += 1
            sleep(.3)
            l.destroy()

        connection = sq.connect("data/game_data.db")
        cursor = connection.cursor()

        query = f'SELECT ID FROM {"GAMEDATA_" + "".join(str(pro_name[0]).split())}'
        cursor.execute(query)
        numeric_ids = [ID[0] for ID in cursor.fetchall()]
        pro_game_ids = ['NA1_' + str(ID) for ID in numeric_ids]
        print("LOOK HERE:::::::", recent_game_ids)
        print("NUMERIC IDS::::::::", numeric_ids)
        GameDisplayWindow(master, self, sum_name, 0, 0, recent_game_ids, pro_name, pro_game_ids=pro_game_ids)


class GameDisplayWindow(ttk.Frame):
    def __init__(self, master, parent, sum_name, user_game_num, pro_game_num, game_ids, pro_name, pro_game_ids):
        number_user_games = len(game_ids)
        number_pro_games = len(pro_game_ids)
        parent.pack_forget()
        ttk.Frame.__init__(self, master, style="My.TFrame")
        self.pack()
        _, sum_level = get_summoner(sum_name.get())
        #recent_game_id = game_ids[user_game_num]
        ttk.Label(self, text="Summoner Name: %s\nSummoner Level: %s" % (sum_name.get(), str(sum_level)),
                  style="Title.TLabel").grid(column=0, row=0, sticky=(W, N), padx=5)
        
        # Drawing User Games
        ttk.Label(self, text="%s's Stats For \nGame %s" % (sum_name.get(), ((user_game_num % number_user_games) + 1)), style="Title.TLabel").grid(column=0, row=1, sticky=W)
        user_game_thread = AsyncGraphDraw(self, sum_name, game_ids[user_game_num], row_num=1)
        user_game_thread.start()
        self.switch_button = ttk.Button(self, text="Switch Accounts", style="My.TButton", command=lambda: popUp(self.switch_button, master))
        self.switch_button.grid(column=0, row=1, sticky=(N, W))
        ttk.Button(self, text="View Next User Game", style="My.TButton",
                   command=lambda: GameDisplayWindow(master, self, sum_name, ((user_game_num + 1) % number_user_games), pro_game_num,
                                                     game_ids, pro_name, pro_game_ids)).grid(column=0, row=1, sticky=(S, W), pady=25)
        ttk.Button(self, text="View Previous User Game", style="My.TButton",
                   command=lambda: GameDisplayWindow(master, self, sum_name, ((user_game_num - 1) % number_user_games), pro_game_num,
                                                     game_ids, pro_name, pro_game_ids)).grid(column=0, row=1, sticky=(S, W))
        
        # Drawing Pro Games
        ttk.Label(self, text="Pro's Stats For \nGame %d" % ((pro_game_num % number_pro_games) + 1), style="Title.TLabel").grid(column=0, row=2, sticky=W)
        print("IDS:", pro_game_ids)
        pro_game_thread = AsyncGraphDraw(self, pro_name, pro_game_ids[pro_game_num], row_num=2, is_pro=True)
        pro_game_thread.start()
        ttk.Button(self, text="View Next Pro Game", style="My.TButton",
                   command=lambda: GameDisplayWindow(master, self, sum_name, user_game_num, ((pro_game_num + 1) % number_pro_games),
                                                     game_ids, pro_name, pro_game_ids)).grid(column=0, row=2, sticky=(S, W), pady=25)
        ttk.Button(self, text="View Previous Pro Game", style="My.TButton",
                   command=lambda: GameDisplayWindow(master, self, sum_name, user_game_num, ((pro_game_num - 1) % number_pro_games),
                                                     game_ids, pro_name, pro_game_ids)).grid(column=0, row=2, sticky=(S, W))
        
        
        # Display advice and analysis
        ttk.Label(self, text="Advice For This Comparison:", style="Title.TLabel").grid(column=0, row=4, sticky=(W, N))
                
        tips = just_the_tips(sum_name, game_ids[user_game_num], pro_name, pro_game_ids[pro_game_num])
        tip_row_num = 5
        for tip in tips:
            ttk.Label(self, text=tip, style="Text.TLabel").grid(column=0, columnspan=4, row=tip_row_num, sticky=(W, N))
            tip_row_num += 1


def main():
    root = tk.Tk()
    root.geometry("1200x900")
    root.config(bg="#808c9f")
    root.title("Statistics Tracker and Improvement Manager")
    styles_init()
    main_window = MainWindow(root)
    root.protocol("WM_DELETE_WINDOW", lambda: delete_user_csvs(root))
    root.mainloop()


if __name__ == "__main__":
    main()
