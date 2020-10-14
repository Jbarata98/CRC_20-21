import networkx as nx
import collections
import matplotlib.pyplot as plt
import powerlaw
import numpy as np

#function that receives a file and generates the graph
#current structure is .txt file with 3 columns, which we take the 2nd and 3rd (represent the nodes) to create the edges.
def graph_generator(file_path):
    graph = nx.Graph()
    with open(file_path) as f:
        edges = f.readlines()
    for edge in edges:
        u = int(edge.split(" ")[1])
        v = int(edge.split(" ")[2])
        graph.add_edge(u, v)
    return graph

#degree analysis
def degree_dist(G):
    degrees = sorted([deg for node, deg in G.degree()], reverse=True)
    degreeCount = collections.Counter(degrees)
    print("most common degree in the graph:", max(degreeCount, key=degreeCount.get))
    print("average degree of the graph is:", sum(degrees)/len(G.degree()))
    print("maximum degree of the graph:", degrees[0])

#main function that analyzes
#depends on the variables
def analyze(graph,degree_distribution = False, visualization=False):
    if degree_distribution:
        degree_dist(graph)
    if visualization:
        nx.draw(graph,pos=nx.spring_layout(graph),node_size= 1,width=1, node_color = "r")
        plt.show()
        plt.savefig("Graph.png",format="PNG")






# call all functions for analysis #write the variables to get desired output
def main():
    graph = graph_generator('datasets/USairport_2010.txt')
    analyze(graph,degree_distribution=True, visualization=False)


if __name__ == '__main__':
    main()



