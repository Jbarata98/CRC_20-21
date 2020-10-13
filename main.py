import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
import numpy as np

def file_import(path):
    graph = nx.Graph()
    with open(path) as f:
        edges = f.readlines()
        print(edges)
    for edge in edges:
        u = int(edge.split(" ")[1])
        v = int(edge.split(" ")[2])
        graph.add_edge(u, v)
    return graph

# call all functions for analysis
def main():
    graph = file_import('datasets/USairport_2010.txt')
    nx.draw(graph,pos=nx.spring_layout(graph),node_size= 1,width=1, node_color = "r")
    #plt.show()
    plt.savefig("Graph.png",format="PNG")

if __name__ == '__main__':
    main()



