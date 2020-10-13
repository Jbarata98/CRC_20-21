import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
import numpy as np

#we created a dictionary but not really necessary
def file_import(metadata,co_presence):
    dict = {}
    graph = nx.Graph()
    with open(metadata) as f:
        nodes = f.readlines()
    for node in nodes:
        dict[int(node[:4])] = [node[5:].rstrip(),0,[]] # list = [type,degree,adjacent nodes]
        graph.add_node(int(node[:4]))
    with open(co_presence) as f:
        edges = f.readlines()
    i = 0
    for edge in edges:
        i+=1
        u = int(edge.split(" ")[1])
        v = int(edge.split(" ")[2])
        graph.add_edge(u,v)
        if i ==1000:
            nx.draw(graph,pos=nx.spring_layout(graph),node_size= 5,width=1, node_color = "r")
            plt.show()
        if v not in dict[u][2]:
            dict[u][1]+=1
            dict[u][2].append(v)
        if u not in dict[v][2]:
            dict[v][1] += 1
            dict[v][2].append(u)
    print("Final dictionary:\n", dict)
    return graph

# call all functions for analysis
def main():
    graph = file_import('datasets/metadata/metadata_LH10.dat','datasets/co-presence/tij_pres_LH10.dat')
    #nx.draw(graph,pos=nx.spring_layout(graph),node_size= 1,width=1, node_color = "r")
    #plt.show()



if __name__ == '__main__':
    main()



