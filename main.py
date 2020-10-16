import networkx as nx
import collections
import matplotlib.pyplot as plt
import operator
import powerlaw
import numpy as np
import random


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
def degree_dist(G,global_degree):
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
    print('number of nodes:', num_nodes)
    print('number of edges:', num_edges)
    #print("node with max betweeness centrality: ", max(bc, key=bc.get))
    print("most common degree in the graph:", max(degreeCount, key=degreeCount.get))
    print("average degree of the graph is:", num_edges / num_nodes)
    print("maximum degree of the graph:", degrees[0])
    print("cumulative degree: ", cum_degree)
    return num_nodes,num_edges,deg_hist,prob_deg_hist,n_node_degs,degreeCount,cum_degree # bc missing

def plot_degree_maker(n_nodes_degs,p_cum,p_cum_rand):
    results = powerlaw.Fit(p_cum)
    fig2, axs2 = plt.subplots(figsize=(8, 6))
    plt.loglog(n_nodes_degs, p_cum, color='black')
    plt.loglog(n_nodes_degs, p_cum_rand, color='blue')
    plt.loglog(n_nodes_degs, [pow(k, -results.power_law.alpha) for k in n_nodes_degs], color='red')
    plt.title("Cumulative Degree Distribution in a log-log scale", fontsize=17)
    plt.ylabel("$P_{cum}k$", fontsize=20)
    plt.xlabel("k", fontsize=20)
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



def preferential(N, m0, m, alpha, seed=None):
    if m < 1 or  m >=N or alpha<0: 
            raise nx.NetworkXError(" network must have m >= 1"
                                   ", alpha > 0 "
                               " and m < n, m = %d, n = %d, alpha=%d" % (m, N, alpha)) 
    if seed is not None: 
            random.seed(seed) 
    G= nx.Graph()
    m00 = range(m0)
    G.add_nodes_from(m00)
    G.add_edge(0, 1)
    #print(G.edges)
    for j in range(m0, N):
        G.add_node(j)
        #print("nodes:"+str(G.nodes))
        probs = []
        for i in G.nodes:
            probs.append(G.degree(i)**alpha)
        #print('probs:' +str(probs))
        sumprobs = sum(probs)
        listprobs = [x / sumprobs for x in probs]
        #print('listprobs:'+str(listprobs))
        links = np.random.choice(G.nodes, m, p=listprobs, replace=False) 
        #print('link:'+str(links))
        for l in links:
            G.add_edge(l,i)
        #print('edges:'+str(G.edges))
    return G

#preferential(5, 2, 2, 1)


# call all functions for analysis #write the variables to get desired output
def main():
    graph = graph_generator('datasets/USairport_2010.txt')
    random_G = generate_random_graph()
    airport_degrees = nx.degree_histogram(graph)
    n_nodes_degrees = [deg for deg in range(len(airport_degrees))]
    print("US Airport Graph:\n")
    num_nodes,num_edges,deg_hist,prob_deg_hist,n_node_degs,degreeCount,cum_degree = analyze_graph(graph,airport_degrees,degree_analysis=True, visualization=False)  #analysis of graph
    print("\nRandom Graph:\n")
    num_nodes_rand,num_edges_rand,deg_hist_rand,prob_deg_hist_rand,n_node_degs_rand,degreeCount_rand,cum_degree_rand = analyze_graph(random_G,airport_degrees,degree_analysis=True, visualization=False) #analysis of random graph
    print("\n Plotting Graph...\n")
    plot_degree_maker(n_nodes_degrees,cum_degree,cum_degree_rand)

if __name__ == '__main__':
    main()
