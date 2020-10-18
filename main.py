import networkx as nx
import collections
import matplotlib.pyplot as plt
import operator
import powerlaw
import numpy as np
import random
import math

MANUAL_ALPHA = False

#function that receives a file and generates the graph
#current structure is .txt file with 3 columns, which we take the 2nd and 3rd (represent the nodes) to create the edges.
def graph_generator(file_path):
    graph = nx.Graph()
    with open(file_path) as f:
        edges = f.readlines()
    for edge in edges:
        u = int(edge.split(" ")[0])
        v = int(edge.split(" ")[1])
        if not graph.has_edge(u,v):
            graph.add_edge(u, v)
    return graph

def generate_random_graph():
    random_G = nx.gnm_random_graph(1574, 17215) #size of
    return random_G

def cum_degree_dist(deg,prob_deg):
    p_cum = []
    for i in range(len(deg)):
        p_cum+=[sum([d for d in prob_deg[i:]])]
    return p_cum

#degree analysis
#return an array with the analysis variables
def degree_dist(G,global_degree):
    print('nr of connected components?:', nx.number_connected_components(G))
    components = list(nx.connected_components(G))
    print("len connected components: ", [c for c in components[1:]])
    components  = components[1:]
    for component in components:
        print(component)
        for node in component:
            print(node)
            G.remove_node(node)
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    deg_hist = nx.degree_histogram(G)                                   # degrees histogram
    print("deg_hist:", deg_hist)
    prob_deg_hist=[d/num_nodes for d in deg_hist]
    n_node_degs=[deg for deg in range(len(deg_hist))]                   # nr of nodes that have the degree deg
    degrees = sorted([deg for node, deg in G.degree()], reverse=True)
    degreeCount = collections.Counter(degrees)
    cum_degree = cum_degree_dist(global_degree, prob_deg_hist)
    #bc = nx.betweenness_centrality(G, normalized=False)
    #closeness = nx.closeness_centrality(G)
    #degcentrality = nx.degree_centrality(G)
    print('number of nodes:', num_nodes)
    print('number of edges:', num_edges)
    print('clustering coefficient:', nx.average_clustering(G))

    print('avg shortest path length:', nx.average_shortest_path_length(G))
    #print('is connected?:', nx.is_connected(G))
    print("most common degree in the graph:", max(degreeCount, key=degreeCount.get))
    print("average degree of the graph is:", 2*(num_edges) / num_nodes)
    print("maximum degree of the graph:", degrees[0])
    print("cumulative degree: ", cum_degree)
    #print("node with max betweeness centrality: ", sorted(bc.items(), key=operator.itemgetter(1), reverse=True)[:5])
    #print("closeness centrality:", sorted(closeness.items(), key=operator.itemgetter(1), reverse=True)[:5])
    #print("degreee centrality:", sorted(degcentrality.items(), key=operator.itemgetter(1), reverse=True)[:5])
    return [num_nodes,num_edges,deg_hist,prob_deg_hist,n_node_degs,degreeCount,cum_degree] # bc missing

def plot_degree_maker(n_nodes_degs,n_nodes_degs_prefattach,p_cum,p_cum_rand):
    results = powerlaw.Fit(p_cum_rand)    # I had to manually change xmin to get decent plot
    print(" syntethic alpha:\n" , results.power_law.alpha)
    plt.subplots(figsize=(8, 6))
    plt.loglog(n_nodes_degs, p_cum, color='black',label = "airport_net",linestyle='--')
    plt.loglog(n_nodes_degs_prefattach, p_cum_rand, color='green',label = "pref_attach_net",linestyle='--')
    #plt.loglog(n_nodes_degs, [pow(k, -(results.power_law.alpha))for k in n_nodes_degs], color='red',label = "powerlaw")
    plt.title("Cumulative Degree Distribution in a log-log scale", fontsize=17)
    plt.ylabel("$P_{cum}k$", fontsize=20)
    plt.xlabel("k", fontsize=20)
    plt.legend()
    plt.show()

#main function that analyzes
#depends on the variables
def analyze_graph(graph,airport_degrees,degree_analysis = False, visualization=True):
    if degree_analysis:
        return degree_dist(graph,airport_degrees)
    if visualization:
        nx.draw(graph,pos=nx.spring_layout(graph),node_size= 1,width=1, node_color = "r")
        plt.show()
        plt.savefig("Graph.png",format="PNG")


def prefattach_simulator(n, m, m0, a):
    assert n >= m0 and m0 >= m and a > 0;
    G = nx.cycle_graph(m0);
    for i in range(m0, n):
        G.add_node(i);
        if len(G.edges) == 0:
            chosen = [0];
        else:
            total = sum([G.degree(k) ** a for k in G.nodes]);
            problist = [G.degree(k) ** a / total for k in G.nodes];
            chosen = np.random.choice(G.nodes, m, p=problist, replace=False);
        for j in chosen:
            G.add_edge(j, i);
    return G

def manual_alpha(p_k,node_degs):
    cum_deg = 0
    counter = 1
    for cum, node_deg in zip(p_k[2:], node_degs):
        try:
            cum = math.log(cum)
        except ValueError as e:
            counter += 1
            continue
        node_deg = math.log(node_deg)
        cum_deg += cum / node_deg
    print("manual alpha: \n", (cum_deg + math.log(p_k[1])) / (len(node_degs) - counter))

# call all functions for analysis #write the variables to get desired output
def main():
    graph = graph_generator('datasets/USairport_2010.txt')
    random_G = generate_random_graph()
    airport_degrees = nx.degree_histogram(graph)
    n_nodes_degrees = [deg for deg in range(len(airport_degrees))]
    print("US Airport Graph:\n")
    #variables array format  = num_nodes,num_edges,deg_hist,prob_deg_hist,n_node_degs,degreeCount,cum_degree
    analysis_array = analyze_graph(graph,airport_degrees,degree_analysis=True, visualization=False)  #analysis of graph
    print("\nRandom Graph:\n")
    #analysis_array_random= analyze_graph(random_G,airport_degrees,degree_analysis=True, visualization=False) #analysis of random graph

    # if you want to calculate alpha by math formula
    if MANUAL_ALPHA:
        manual_alpha(analysis_array[3],n_nodes_degrees[2:])

    print("\nPlotting Graph...\n")
    #plot_degree_maker(n_nodes_degrees,analysis_array[6],analysis_array_random[6])
    print("\nPreferential Attachment Simulations:\n")
    #run simulation
    prefattach = prefattach_simulator(1572, 21, 786, 1.5)
    prefattach_degrees = nx.degree_histogram(prefattach)
    n_nodes_degs_prefattach = [deg for deg in range(len(prefattach_degrees))]
    analysis_array_prefattach = analyze_graph(prefattach, prefattach_degrees, degree_analysis=True, visualization=False)
    plot_degree_maker(n_nodes_degrees,n_nodes_degs_prefattach,analysis_array[6],analysis_array_prefattach[6])

if __name__ == '__main__':
    main()
