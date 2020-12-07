
import networkx as nx
import collections
import matplotlib.pyplot as plt
import operator
import powerlaw
import numpy as np
import random
import math
from scipy import stats

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

# generates random graph
def generate_random_graph():
    random_G = nx.gnm_random_graph(1574, 17215) #size of
    return random_G

#calculates cumulate probability
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
    degrees = sorted([deg for node, deg in G.degree()], reverse=False)
    print("degrees", degrees)
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
    print("maximum degree of the graph:", degrees[-1])
    print("cumulative degree: ", cum_degree)
    #print("node with max betweeness centrality: ", sorted(bc.items(), key=operator.itemgetter(1), reverse=True)[:5])
    #print("closeness centrality:", sorted(closeness.items(), key=operator.itemgetter(1), reverse=True)[:5])
    #print("degreee centrality:", sorted(degcentrality.items(), key=operator.itemgetter(1), reverse=True)[:5])
    return [num_nodes,num_edges,deg_hist,prob_deg_hist,n_node_degs,degreeCount,cum_degree,degrees] # bc missing

def plot_degree_maker(n_nodes_degs,n_nodes_degs_prefattach,p_cum,p_cum_rand,POWER_LAW = False,PREF_ATTACH = False, RANDOM_NET =False): #plot for pref attach and cum degree
    results = powerlaw.Fit(p_cum)
    print(" syntethic alpha:\n" , results.power_law.alpha)
    plt.subplots(figsize=(8, 6))
    plt.loglog(n_nodes_degs, p_cum, color='black',label = "airport_net",linestyle='--')
    if RANDOM_NET:
        plt.loglog(n_nodes_degs, p_cum_rand, color='green', label="random_net", linestyle='--')
    if PREF_ATTACH:
        plt.loglog(n_nodes_degs_prefattach, p_cum_rand, color='green',label = "pref_attach_net",linestyle='--')
    if POWER_LAW:
        plt.loglog(n_nodes_degs, [pow(k, -(results.power_law.alpha))for k in n_nodes_degs], color='red',label = "powerlaw")
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

#preferential attachment simulator
def prefattach_simulator(N, m, m0, alpha):
    if m < 1 or m >= N or alpha < 0:
        raise nx.NetworkXError(" network must have m >= 1"
                               ", alpha > 0 "
                               " and m < n, m = %d, n = %d, alpha=%d" % (m, N, alpha))
    G = nx.cycle_graph(m0)
    for i in range(m0, N):
        G.add_node(i)
        if len(G.edges) == 0:
            G.add_edge(0, i)
        else:
            total = sum([pow(G.degree(k), alpha) for k in G.nodes()])
            probs = [pow(G.degree(k),alpha) / total for k in G.nodes]
            random_choice = np.random.choice(G.nodes, m, p=probs, replace=False)
            for j in random_choice:
                G.add_edge(j, i)
    return G

#calculates alpha with logarithmic formula
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

#attempt to calculate lin_reg
def linear_regression(k,p_k):
    p_k =list(filter(lambda x : x != 0,p_k))
    for deg,prob_deg in zip(k,p_k):
        deg = math.log(deg)
        prob_deg = math.log(prob_deg)
    linreg = stats.linregress(k,p_k)
    print("linear regression:", linreg)
