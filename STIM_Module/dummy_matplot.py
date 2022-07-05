import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# TODO: Turn these three functions into one with more arguments, Refactor application.py yay

def ret_graph(type="g"):
    xVar = "Minute"
    if (type == "g"):
        my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Total Gold"])
        yVar = "Total Gold"
        line_color = 'y'
        col_num = 1
    elif (type == "e"):
        my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Total Exp"])
        yVar = "Total Exp"
        line_color = '#33ccff'
        col_num = 2
    elif (type == "d"):
        my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Gold Diff"])
        yVar = "Gold Diff"
        line_color = 'g'
        col_num = 3
    else:
        print("Error Invalid graph grab")

    return my_DF, xVar, yVar, line_color, col_num