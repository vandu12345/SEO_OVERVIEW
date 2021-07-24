import matplotlib.pyplot as plt
import base64
from io import BytesIO
# import itertools
import random

def get_graph2():
    buffer = BytesIO()
    plt.savefig(buffer,format = 'png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
def get_plot2(x,y,str1):
    # plt.switch_backend("AGG")
    # plt.figure(figsize(10,5))
    plt.title(f"{str1} counts Graph Representation")
    # fig = plt.figure(figsize =(10, 7))
    plt.pie(x, labels = y)
    graph = get_graph2()
    return graph