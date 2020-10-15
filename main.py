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
        if not graph.has_edge(u,v):
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
    random_G = nx.gnm_random_graph(10220, 49812)

    num_nodes = graph.number_of_nodes()
    num_nodes_rand = random_G.number_of_nodes()

    num_edges = graph.number_of_edges()
    num_edges_rand = graph.number_of_edges()

    deg = nx.degree_histogram(graph)
    deg_rand = nx.degree_histogram(random_G)

    max_value=max(deg)
    i=0
    while i<len(deg) :
        if deg[i] == max_value:
            common_degree = i
            break
        i+=1

    i=0
    max_value = max(deg_rand)
    while i<len(deg_rand) :
        if deg_rand[i] == max_value:
            common_degree_rand = i
            break
        i+=1

    print("Airport Graph:")
    print('')

    print('number of nodes:', num_nodes)
    print('number of edges:', num_edges)
    print('maximum degree of the graph:', len(deg)-1)
    print('average degree:', num_edges / num_nodes)
    print('most common degree :', common_degree)
    print('')
    print('')
    print('')

    #analyze(graph,degree_distribution=True, visualization=False)

    print('Random Graph')
    print('')

    print('number of nodes:', num_nodes_rand)
    print('number of edges:', num_edges_rand)
    print('maximum degree of the graph:', len(deg_rand) - 1)
    print('average degree:',num_edges_rand/num_nodes_rand)
    print('most common degree in the graph:', common_degree_rand)

    #analyze(random_G, degree_distribution=True, visualization=False)




if __name__ == '__main__':
    main()



