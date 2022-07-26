import pandas as pd
import sqlite3 as sq
import ast
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# TODO: Turn these two functions into one just using filename now that it is returned to us


def ret_graph(type="g", summoner_name=None, game_id=None):
    xVar = "Minute"

    game_id_digits = int(game_id[4:])
    connection = sq.connect("data/game_data.db")
    cursor = connection.cursor()

    if type == "g":
        query = f'SELECT GOLDTL FROM {"GAMEDATA_" + "".join(summoner_name.split())} WHERE ID={game_id_digits}'
        cursor.execute(query)

        pre_list_str = str(cursor.fetchone())
        pre_list_str = pre_list_str[2:-3]
        list_of_vals = ast.literal_eval(pre_list_str)
        list_of_mins = [i for i in range(len(list_of_vals))]

        my_DF = pd.DataFrame(list(zip(list_of_mins, list_of_vals)), columns=["Minute", "Total Gold"])
        #my_DF = pd.read_csv("./data/%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",", usecols=["Minute", "Total Gold"])
        yVar = "Total Gold"
        line_color = 'y'
    elif type == "e":
        query = f'SELECT XPTL FROM {"GAMEDATA_" + "".join(summoner_name.split())} WHERE ID={game_id_digits}'
        cursor.execute(query)

        pre_list_str = str(cursor.fetchone())
        pre_list_str = pre_list_str[2:-3]
        list_of_vals = ast.literal_eval(pre_list_str)
        list_of_mins = [i for i in range(len(list_of_vals))]

        my_DF = pd.DataFrame(list(zip(list_of_mins, list_of_vals)), columns=["Minute", "Total Exp"])
        #my_DF = pd.read_csv("./data/%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",", usecols=["Minute", "Total Exp"])
        yVar = "Total Exp"
        line_color = '#33ccff'
    elif type == "d":
        query = f'SELECT GLDDIFTL FROM {"GAMEDATA_" + "".join(summoner_name.split())} WHERE ID={game_id_digits}'
        cursor.execute(query)

        pre_list_str = str(cursor.fetchone())
        pre_list_str = pre_list_str[2:-3]
        list_of_vals = ast.literal_eval(pre_list_str)
        list_of_mins = [i for i in range(len(list_of_vals))]

        my_DF = pd.DataFrame(list(zip(list_of_mins, list_of_vals)), columns=["Minute", "Gold Diff"])
        #my_DF = pd.read_csv("./data/%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",", usecols=["Minute", "Gold Diff"])
        yVar = "Gold Diff"
        line_color = 'g'
    else:
        print("Error Invalid graph grab")

    return my_DF, xVar, yVar, line_color


def ret_pro_graph(type="g", fileName=None):
    xVar = "Minute"
    if type == "g":
        my_DF = pd.read_csv(fileName, header=0, delimiter=",", usecols=["Minute", "Total Gold"])
        yVar = "Total Gold"
        line_color = 'y'
    elif type == "e":
        my_DF = pd.read_csv(fileName, header=0, delimiter=",", usecols=["Minute", "Total Exp"])
        yVar = "Total Exp"
        line_color = '#33ccff'
    elif type == "d":
        my_DF = pd.read_csv(fileName, header=0, delimiter=",", usecols=["Minute", "Gold Diff"])
        yVar = "Gold Diff"
        line_color = 'g'
    else:
        print("Error Invalid graph grab")

    return my_DF, xVar, yVar, line_color