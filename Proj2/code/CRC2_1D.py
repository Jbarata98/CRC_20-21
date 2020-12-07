import collections
import random as rand
import matplotlib.pyplot as plt
import imageio
import numpy as np

'''------------------------------------INIT VARIABLES---------------------------------------------------------------'''

Ger = 1000
N = 100
Rondas = 1
mut, mut2, mut3, mut4, mut5, mut6 = 0.001, 0.002, 0.01, 0.02, 0.1, 0.2
mut = mut3
average_list = []

checkpoints_dict = collections.defaultdict(list)  # to plot checkpoints graph #0,100,10000,100000 generations

Neigh_n1, Neigh_n2, Neigh_n3 = 1, 3, 5
Neigh_n = Neigh_n1

population = collections.defaultdict(list)

'''------------------------------------INIT VARIABLES---------------------------------------------------------------'''

'''Function to populate, returns a dictionary = {User:(p,q,payoff,[payoffs neighborhood])}'''


def populate(popl):
    i = 1
    while i <= N:
        if (i == N / 2) or (i == N / 4) or (i == 3 * N / 4):
            print(i)
            popl['S' + str(i)] = [0.2, 0.15, 0, []]
        else:
            popl['S' + str(i)] = [0.5, 0.05, 0, []]  # [p , q , payoff da ronda , payoff da vizinhança ]
        i += 1
    # print("population:\n", popl)
    return popl


''' calculate new population taking into account a 1D spatial setting'''


def encounters_1D(popul, ger_nr, checkpoints):
    popl = popul
    l_popl = list(popl.keys())
    i = 0
    while i < len(l_popl):
        if (i == N - 1):  # last one
            if popl[l_popl[i]][0] >= popl[l_popl[1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[0]][2] += popl[l_popl[i]][0]
            if popl[l_popl[i]][0] >= popl[l_popl[i - 1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[i - 1]][2] += popl[l_popl[i]][0]

        else:
            if popl[l_popl[i]][0] >= popl[l_popl[i + 1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[i + 1]][2] += popl[l_popl[i]][0]
            if popl[l_popl[i]][0] >= popl[l_popl[i - 1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[i - 1]][2] += popl[l_popl[i]][0]

        i += 1

    i = 0
    while i < N:
        payoff_total = popl[l_popl[i]][2]

        j = 1
        while j < Neigh_n + 1:
            if i + j >= N:  # passed the len (basically do a circle)
                payoff_total += popl[l_popl[i - j]][2]
                payoff_total += popl[l_popl[i + j - N]][2]
            else:
                payoff_total += popl[l_popl[i - j]][2]
                payoff_total += popl[l_popl[i + j]][2]
            j += 1

        if payoff_total == 0:  # rare occasion, just attribute a uniform payoff to all...
            payoff_list = [1 / 3, 1 / 3, 1 / 3]
        else:
            payoff_list = [popl[l_popl[i]][2] / payoff_total]
        j = 1

        while j < Neigh_n + 1:
            if payoff_total != 0:
                if i + j >= N:  # passou do N
                    payoff_list += [popl[l_popl[i - j]][2] / payoff_total]
                    payoff_list += [popl[l_popl[i + j - N]][2] / payoff_total]
                else:
                    payoff_list += [popl[l_popl[i - j]][2] / payoff_total]
                    payoff_list += [popl[l_popl[i + j]][2] / payoff_total]
            j += 1
        popl[l_popl[i]][3] += payoff_list
        i += 1

    '''calculates new generation'''

    i = 0
    popl_new = collections.defaultdict(list)
    average_q_ronda = 0
    average_p_ronda = 0
    while i < N:
        comparing = 0
        r = rand.random()
        k = 0
        r_t = False
        while k < Neigh_n * 2:
            comparing += popl[l_popl[i]][3][k]
            if r < comparing:
                r_t = True
                if k == 0:
                    popl_new[l_popl[i]] = [popl[l_popl[i]][0],
                                           popl[l_popl[i]][1],
                                           0, []]

                    '''Check if its a checkpoint to plot later on a cluster'''
                    if ger_nr in checkpoints:
                        checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                    average_p_ronda += popl_new[l_popl[i]][0]
                    average_q_ronda += popl_new[l_popl[i]][1]

                elif k % 2 == 1:
                    l = int((k + 1) / 2)

                    popl_new[l_popl[i]] = [popl[l_popl[i - k]][0],
                                           popl[l_popl[i - k]][1],
                                           0, []]

                    '''Check if its a checkpoint to plot later on a cluster'''
                    if ger_nr in checkpoints:
                        checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                    average_p_ronda += popl_new[l_popl[i]][0]
                    average_q_ronda += popl_new[l_popl[i]][1]

                else:
                    l = int(k / 2)
                    # print(l)
                    if i + k >= N:
                        popl_new[l_popl[i]] = [popl[l_popl[i + l - N]][0],
                                               popl[l_popl[i + l - N]][1],
                                               0, []]

                        '''Check if its a checkpoint to plot later on a cluster'''
                        if ger_nr in checkpoints:
                            checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                        average_p_ronda += popl_new[l_popl[i]][0]
                        average_q_ronda += popl_new[l_popl[i]][1]
                    else:
                        popl_new[l_popl[i]] = [popl[l_popl[i + l]][0],
                                               popl[l_popl[i + l]][1],
                                               0, []]

                    '''Check if its a checkpoint to plot later on a cluster'''
                    if ger_nr in checkpoints:
                        checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                    average_p_ronda += popl_new[l_popl[i]][0]
                    average_q_ronda += popl_new[l_popl[i]][1]
                break
            k += 1

        if not r_t:
            k = int(k / 2)
            if i + k >= N:
                popl_new[l_popl[i]] = [popl[l_popl[i + k - N]][0],
                                       popl[l_popl[i + k - N]][1],
                                       0, []]

                if ger_nr in checkpoints:
                    checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                average_p_ronda += popl_new[l_popl[i]][0]
                average_q_ronda += popl_new[l_popl[i]][1]
            else:
                popl_new[l_popl[i]] = [popl[l_popl[i + k - N]][0],
                                       popl[l_popl[i + k - N]][1],
                                       0, []]
                if ger_nr in checkpoints:
                    checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                average_p_ronda += popl_new[l_popl[i]][0]
                average_q_ronda += popl_new[l_popl[i]][1]

        i += 1
    average_list.append([average_p_ronda / N, average_q_ronda / N])
    return popl_new


'''scatter plot for each checkpoint'''


def checkpoint_plot(p_q, population, ger):
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.title('spatial distribution of acceptance and offer strategies'), plt.ylabel('Probability',
                                                                                     fontsize=16), plt.xlabel(
        'population', fontsize=16)
    ax.scatter(range(population), [i[0] for i in p_q[ger]], color='blue', label="p")
    ax.scatter(range(population), [i[1] for i in p_q[ger]], color='red', label="q")
    plt.ylim([0, 1])
    ax.grid(True)
    ax.legend()
    plt.show()
    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image


def main():
    checkpoints = [1, 10, 100, 1000, 10000, 100000]
    popl_sample = populate(population)
    ronda = 0
    for j in range(0, Rondas):
        geracao = 0
        for i in range(0, Ger):
            popl_new = encounters_1D(popl_sample, i + 1, checkpoints)

            popl_sample = popl_new
            print(geracao)
            geracao += 1
        ronda += 1

    p_list = []
    q_list = []

    i = 0
    while i < len(average_list):
        to_append_p = average_list[i][0]
        to_append_q = average_list[i][1]

        p_list.append(to_append_p)
        q_list.append(to_append_q)
        i += 1
    #
    '''save gif animation'''
    for ger in checkpoints_dict.keys():
        checkpoint_plot(checkpoints_dict, N, ger)


    '''Uncomment to save the gif'''
    # plt.show()
    # imageio.mimsave('demo.gif', [checkpoint_plot(checkpoints_dict, N, ger) for ger in checkpoints_dict.keys()], fps=1)

    '''Uncomment to plot the figures aswell'''

    plt.subplots(figsize=(8, 6))
    plt.title('$\\bar{p}$ and $\\bar{q}$ variation over time'), plt.ylabel('Probability', fontsize=16), plt.xlabel(
        '$log_{10}t$', fontsize=16)

    plt.plot(range(Ger), p_list, color='blue', label="average_p", linestyle='--')
    plt.plot(range(Ger), q_list, color='red', label="average_q", linestyle='--')
    plt.xscale("log")
    plt.ylim([0, 1])
    plt.legend(['$\\bar{p}$-value', '$\\bar{q}$-value'])
    plt.show()

    return 0


if __name__ == '__main__':
    main()
