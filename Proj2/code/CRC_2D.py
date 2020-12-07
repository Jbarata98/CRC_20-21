import collections
import random as rand
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import PillowWriter

'''------------------------------------INIT VARIABLES---------------------------------------------------------------'''

GER = 150

GRID_SIZE = 20
MUTANT_GRID_SIZE = 2

N = 100
Rondas = 1

mut1, mut2, mut3, mut4, mut5, mut6 = 0.001, 0.002, 0.01, 0.02, 0.1, 0.2

mut = mut1

average_list = []

mutant_p, mutant_q = rand.uniform(0.3 / 2, 0.4 / 2), rand.uniform(0.2 / 2, 0.3 / 2)
resident_p, resident_q = rand.uniform(0.1 / 2, 0.2 / 2), rand.uniform(0 / 2, 0.1 / 2)

'''------------------------------------INIT VARIABLES---------------------------------------------------------------'''

'''Populate a 2D spatial setting with a 3x3 mutant cluster'''
'''each cell represents a user with attributes: [p , q , payoff, payoff neighboorhood, (row_index,column_index)]'''


def populate_2D():
    matrix = [[[resident_p, resident_q, 0, [], (column, row)] for row in range(GRID_SIZE)] for column in
              range(GRID_SIZE)]

    for i in range(-1, 2):
        matrix[int(GRID_SIZE / 2) - 1][int(GRID_SIZE / 2) + i - 1] = [mutant_p, mutant_q, 0, [], (
        int(GRID_SIZE / 2) - 1, int(GRID_SIZE / 2) + i - 1)]
        matrix[int(GRID_SIZE / 2) - 2][int(GRID_SIZE / 2) + i - 1] = [mutant_p, mutant_q, 0, [], (
        int(GRID_SIZE / 2) - 2, int(GRID_SIZE / 2) + i - 1)]
        matrix[int(GRID_SIZE / 2) + 0][int(GRID_SIZE / 2) + i - 1] = [mutant_p, mutant_q, 0, [], (
        int(GRID_SIZE / 2) + 0, int(GRID_SIZE / 2) + i - 1)]
    return matrix


'''Function to calculate von neumann neighbors : (adapted from online version)'''


def find_neighbours(arr):
    neighbors = collections.defaultdict(list)

    for i in range(len(arr)):
        for j, value in enumerate(arr[i]):

            if i == 0 or i == len(arr) - 1 or j == 0 or j == len(arr[i]) - 1:
                # corners
                new_neighbors = []
                if i != 0:
                    new_neighbors.append((arr[i - 1][j], (i - 1, j)))  # top neighbor
                if j != len(arr[i]) - 1:
                    new_neighbors.append((arr[i][j + 1], (i, j + 1)))  # right neighbor
                if i != len(arr) - 1:
                    new_neighbors.append((arr[i + 1][j], (i + 1, j)))  # bottom neighbor
                if j != 0:
                    new_neighbors.append((arr[i][j - 1], (i, j - 1)))  # left neighbor

            else:
                # add neighbors
                new_neighbors = [
                    (arr[i - 1][j], (i - 1, j)),  # top neighbor
                    (arr[i][j + 1], (i, j + 1)),  # right neighbor
                    (arr[i + 1][j], (i + 1, j)),  # bottom neighbor
                    (arr[i][j - 1], (i, j - 1))  # left neighbor
                ]

            neighbors[(i, j)].append({
                "neighbors": new_neighbors})

    return neighbors


'''Uncomment to print the matrix '''

''' PRINT MATRIX  
for row in matrix:
    print(row)
    print("\n")
'''
'--------------------------------------------------ENCOUNTERS 2D-------------------------------------------------------'


def encounters_2D(population):
    popl = population
    neis = find_neighbours(popl)  # dictionary {'index':[{'neighbors':[(neighbor1,(index)),.....]}]}
    for row_nr in range(len(popl)):
        for column_nr in range(len(popl)):

            for nei in neis[(row_nr, column_nr)][0]['neighbors']:
                if popl[row_nr][column_nr][0] >= nei[0][1]:
                    popl[row_nr][column_nr][2] += 1 - popl[row_nr][column_nr][0]
                    popl[nei[1][0]][nei[1][1]][2] += popl[row_nr][column_nr][0]

    for row_nr in range(len(popl)):
        for column_nr in range(len(popl)):
            payoff_total = popl[row_nr][column_nr][2]
            for nei in neis[(row_nr, column_nr)][0]['neighbors']:
                payoff_total += nei[0][2]

            popl[row_nr][column_nr][3].append(popl[row_nr][column_nr][2] / payoff_total)

            for nei in neis[(row_nr, column_nr)][0]['neighbors']:
                popl[row_nr][column_nr][3].append(nei[0][2] / payoff_total)

    '-------------------------------------Calculate new generation----------------------------------------------------'

    neis = find_neighbours(popl)

    popl_new = population
    for row_nr in range(len(popl)):
        for column_nr in range(len(popl)):
            comparing = 0
            r = rand.random()
            r_t = False
            i = 0
            nei = neis[(row_nr, column_nr)][0]['neighbors']
            # print(nei)
            while i < len(popl[row_nr][column_nr][3]):
                comparing += popl[row_nr][column_nr][3][i]
                if r < comparing:
                    if i == 0:
                        p_mut = popl[row_nr][column_nr][0] * mut
                        q_mut = popl[row_nr][column_nr][1] * mut
                        popl_new[row_nr][column_nr] = [
                            rand.uniform(popl[row_nr][column_nr][0] - p_mut, popl[row_nr][column_nr][0] + p_mut),
                            rand.uniform(popl[row_nr][column_nr][1] - q_mut, popl[row_nr][column_nr][1] + q_mut),
                            0, [], (row_nr, column_nr)]
                    else:
                        n = nei[i - 1]
                        p_mut = popl[n[1][0]][n[1][1]][0] * mut
                        q_mut = popl[n[1][0]][n[1][1]][1] * mut
                        popl_new[row_nr][column_nr] = [
                            rand.uniform(popl[n[1][0]][n[1][1]][0] - p_mut, popl[n[1][0]][n[1][1]][0] + p_mut),
                            rand.uniform(popl[n[1][0]][n[1][1]][1] - q_mut, popl[n[1][0]][n[1][1]][1] + q_mut),
                            0, [], (row_nr, column_nr)]
                    r_t = True
                i += 1

            if not r_t:
                n = nei[i - 1]
                p_mut = popl[n[1][0]][n[1][1]][0] * mut
                q_mut = popl[n[1][0]][n[1][1]][1] * mut
                popl_new[row_nr][column_nr] = [
                    rand.uniform(popl[n[1][0]][n[1][1]][0] - p_mut, popl[n[1][0]][n[1][1]][0] + p_mut),
                    rand.uniform(popl[n[1][0]][n[1][1]][1] - q_mut, popl[n[1][0]][n[1][1]][1] + q_mut),
                    0, [], (row_nr, column_nr)]

    return popl_new


'''---------------------------------------SIMULATION------------------------------------------------------------------'''


# sets up the lattice 2D
def set_up():
    xmin = 0
    xmax = GRID_SIZE
    ymin = 0
    ymax = GRID_SIZE
    fig1 = plt.figure(figsize=[10, 10])
    ax = fig1.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(xmin, xmax), ylim=(ymin, ymax))
    ax.axis(False)

    # setup da grelha - reticulado
    # linhas horizontais
    for i in range(ymin, ymax + 1):
        lines, = ax.plot([xmin, xmax], [i, i], '-', color='0.35')

    # linhas verticais
    for i in range(xmin, xmax + 1):
        lines, = ax.plot([i, i], [ymin, ymax], '-', color='0.35')
    # plt.show()
    return (ax, fig1)


'''Paint the lattice according to the last step'''
'''Note that this function can be altered to paint the lattice according to the first step'''


# paints it
def paint(lista):
    (ax, fig1) = set_up()
    patch = [[] for i in range(GRID_SIZE * GRID_SIZE)]
    # print(len(lista[0))
    for r in range(
            GRID_SIZE * GRID_SIZE):  # adicionar um parametro a nossa lista que era o index dessa posicao para esta parte
        x = lista[-1][r][4][0]

        y = lista[-1][r][4][1]
        patch[r] = ax.add_patch(patches.Rectangle([x, y], 1, 1, color=(
            1 - (lista[0][r][0] + lista[0][r][0]), 1 - (lista[0][r][0] + lista[0][r][0]),
            1 - (lista[0][r][0] + lista[0][r][0]))))  # a cor é calculada com 1 - (p+q)
    return (patch, fig1)


'''Animate the lattice with the changes to the sites at each step'''


class LoopingPillowWriter(PillowWriter):
    def finish(self):
        self._frames[0].save(
            self.outfile, save_all=True, append_images=self._frames[1:],
            duration=int(1000 / self.fps), loop=0)


population_updates = []


def main():
    # calculates the new popl sample
    popl_sample = populate_2D()
    for ger in range(0, GER):
        flat_popl = [item for sublist in popl_sample for item in sublist]
        population_updates.append(flat_popl)
        popl_new = encounters_2D(popl_sample)
        print(ger)
        popl_sample = popl_new

    # Funcao que da update a cada quadrado
    def animate(i):
        print(i)
        for j in range(GRID_SIZE * GRID_SIZE):
            tipo1 = population_updates[i][j][0]
            tipo2 = population_updates[i][j][1]
            patch[j].set_color((0.4 - (tipo1 + tipo2), 0.4 - (tipo1 + tipo2), 0.4 - (tipo1 + tipo2)))  # (1-p+q)
        return patch

    (patch, fig1) = paint(population_updates)

    '''saves the gif - uncomment to do so '''
    #
    # anim = animation.FuncAnimation(fig1, animate, frames=GER, interval=500, blit=True)
    #
    # anim.save('animacao_simulação.gif',
    #           writer=LoopingPillowWriter(fps=3))  # you can change the fps for easier understanding


#
if __name__ == '__main__':
    main()
