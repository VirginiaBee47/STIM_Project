import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# TODO: Turn these two functions into one just using filename now that it is returned to us

def ret_graph(type="g", summoner_name=None, game_id=None):

    xVar = "Minute"
    if (type == "g"):
        my_DF = pd.read_csv("./data/%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",", usecols=["Minute", "Total Gold"])
        yVar = "Total Gold"
        line_color = 'y'
    elif (type == "e"):
        my_DF = pd.read_csv("./data/%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",", usecols=["Minute", "Total Exp"])
        yVar = "Total Exp"
        line_color = '#33ccff'
    elif (type == "d"):
        my_DF = pd.read_csv("./data/%s_%s.csv" % (summoner_name, game_id), header=0, delimiter=",", usecols=["Minute", "Gold Diff"])
        yVar = "Gold Diff"
        line_color = 'g'
    else:
        print("Error Invalid graph grab")

    return my_DF, xVar, yVar, line_color

def ret_pro_graph(type="g", fileName=None):

    xVar = "Minute"
    if (type == "g"):
        my_DF = pd.read_csv(fileName, header=0, delimiter=",", usecols=["Minute", "Total Gold"])
        yVar = "Total Gold"
        line_color = 'y'
    elif (type == "e"):
        my_DF = pd.read_csv(fileName, header=0, delimiter=",", usecols=["Minute", "Total Exp"])
        yVar = "Total Exp"
        line_color = '#33ccff'
    elif (type == "d"):
        my_DF = pd.read_csv(fileName, header=0, delimiter=",", usecols=["Minute", "Gold Diff"])
        yVar = "Gold Diff"
        line_color = 'g'
    else:
        print("Error Invalid graph grab")

    return my_DF, xVar, yVar, line_color