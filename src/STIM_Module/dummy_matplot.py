import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# TODO: Turn these three functions into one with more arguments, Refactor application.py yay

def ret_graph(type="g", summoner_name=None, game_id=None):
    xVar = "Minute"
    if type == "g":
        my_DF = pd.read_csv(".\\data\\%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",",
                            usecols=["Minute", "Total Gold"])
        yVar = "Total Gold"
        line_color = 'y'
        col_num = 1
    elif type == "e":
        my_DF = pd.read_csv(".\\data\\%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",",
                            usecols=["Minute", "Total Exp"])
        yVar = "Total Exp"
        line_color = '#33ccff'
        col_num = 2
    elif type == "d":
        my_DF = pd.read_csv(".\\data\\%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",",
                            usecols=["Minute", "Gold Diff"])
        yVar = "Gold Diff"
        line_color = 'g'
        col_num = 3
    else:
        print("Error Invalid graph grab")

    return my_DF, xVar, yVar, line_color, col_num
