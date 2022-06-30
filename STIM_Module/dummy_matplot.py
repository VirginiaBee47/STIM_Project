import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
# TODO: Turn these three functions into one with more arguments, Refactor application.py

def gold_graph():
    my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Total Gold"])
    return my_DF

def exp_graph():
    my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Total Exp"])
    return my_DF


def diff_graph():
    my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Gold Diff"])

    return my_DF