import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


myarr = np.empty((0,2), int)
l = []
for i in range(1, 11):
    if (i % 3 == 2):
        l.append([i, (i-1*32)])
    else:
        l.append([i, i*32])
myarr = np.append(myarr, np.array(l), axis=0)

my_DF = pd.DataFrame()
my_DF = pd.read_csv(".\\test.csv", header=0, delimiter="\t", usecols=["Minute", "Diff"])

# print(myarr)
print(my_DF.head(10))


