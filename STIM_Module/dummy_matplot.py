from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def gold_graph():
    gold_nums = []
    min_markers = []
    for i in range(0,16):
        temp = i*23
        if (i % 3 == 0):
            temp = (i-1) * 23
        gold_nums.append(temp)
        min_markers.append(i)
    my_graph = plt.plot(min_markers, gold_nums)
    #plt.show()
    return my_graph

def exp_graph():
    exp_nums = []
    min_markers = []
    for i in range(0,16):
        temp = i*23
        if (i % 3 == 0):
            temp = (i-1) * 242
        exp_nums.append(temp)
        min_markers.append(i)


