
import itertools as iter
import collections
import random as rand
import matplotlib.pyplot as plt
import numpy as np

Ger = 100000

GRID_SIZE = 10
N = 100
Rondas = 1

mut1, mut2, mut3, mut4, mut5, mut6 = 0.001, 0.002, 0.01, 0.02, 0.1, 0.2

mut = mut1

average_list = []

checkpoints_dict = collections.defaultdict(list) #to plot checkpoints graph #0,100,10000,100000 generations



population = collections.defaultdict(list)

def populate(popl):
    i = 1
    while i <= N:
        popl['S'+ str(i)] = [rand.uniform(0,1),rand.uniform(0,1),0,[]]  #[p , q , payoff da ronda , payoff da vizinhança ]
        i+=1
    #print("population:\n", popl)
    return popl


def get_neighbourhood(matrix, coordinates, distance=1):
    dimensions = len(coordinates)
    neigh = []
    app = neigh.append

    def recc_von_neumann(arr, curr_dim=0, remaining_distance=distance, isCenter=True):
        # the breaking statement of the recursion
        if curr_dim == dimensions:
            if not isCenter:
                app(arr)
            return

        dimensions_coordinate = coordinates[curr_dim]
        if not (0 <= dimensions_coordinate < len(arr)):
            return

        dimesion_span = range(dimensions_coordinate - remaining_distance,
                              dimensions_coordinate + remaining_distance + 1)
        for c in dimesion_span:
            if 0 <= c < len(arr):
                recc_von_neumann(arr[c],
                                 curr_dim + 1,
                                 remaining_distance - abs(dimensions_coordinate - c),
                                 isCenter and dimensions_coordinate == c)
        return

    recc_von_neumann(matrix)
    return neigh

matrix = np.random.randint(2, size=(4,4))
print(matrix)
for row in range(len(matrix)):
    for column in range(len(matrix[0])):
        print(row,column)
        neighbours = get_neighbourhood(matrix,(row,column))
        print(neighbours)

