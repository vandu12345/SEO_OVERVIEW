import matplotlib.pyplot as plt
import base64
from io import BytesIO
# import itertools
import random



def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format = 'png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
def get_plot(x,y):
    # plt.switch_backend("AGG")
    # plt.figure(figsize(10,5))
    plt.title("Image Graph Representation")
    colors = ["red", "blue", "green","c","m","y"]
    
    # print(n)
    n = 0
    for x,y in zip(x,y):
        n = random.randint(0,1000)
        plt.scatter(x,y,color=colors[n%6])
    plt.xticks(rotation=45)
    plt.ylabel('Scale in 0-1')
    plt.xlabel('Image Size')
    plt.tight_layout()
    graph = get_graph()
    return graph