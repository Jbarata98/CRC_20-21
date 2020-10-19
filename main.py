from analysis_funcs import *


# call all functions for analysis #write the variables to get desired output
def main():

    #airport, random and powerlaw fit plots

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

    print("\nPlotting Graph Airport\Powerlaw\Random...\n")
    #plot_degree_maker(n_nodes_degrees,analysis_array[6],analysis_array_random[6],POWER_LAW = True)
    print("\nPreferential Attachment Simulations:\n")

    #run simulation

    prefattach = prefattach_simulator(1572, 11, 32, 1.2)
    prefattach_degrees = nx.degree_histogram(prefattach)
    n_nodes_degs_prefattach = [deg for deg in range(len(prefattach_degrees))]
    analysis_array_prefattach = analyze_graph(prefattach, prefattach_degrees, degree_analysis=True, visualization=False)
    print("\nPlotting Graph Airport\Simulation...\n")
    plot_degree_maker(n_nodes_degrees,n_nodes_degs_prefattach,analysis_array[6],analysis_array_prefattach[6], POWER_LAW=False)

if __name__ == '__main__':
    main()
