import matplotlib.pyplot as plt
import itertools as iter
import collections
import random as rand
import matplotlib.pyplot as plt

Ger = 100000
N = 100
Rondas = 1
mut, mut2, mut3, mut4, mut5, mut6 = 0.001, 0.002, 0.01, 0.02, 0.1, 0.2
mut = mut
average_list = []

checkpoints_dict = collections.defaultdict(list) #to plot checkpoints graph #0,100,10000,100000 generations

Neigh_n1, Neigh_n2, Neigh_n3= 1,3,5
Neigh_n = Neigh_n1

population = collections.defaultdict(list)

def populate(popl):
    i = 1
    while i <= N:
        popl['S'+ str(i)] = [rand.random(),rand.random(),0,[]]  #[p , q , payoff da ronda , payoff da vizinhança ]
        i+=1
    #print("population:\n", popl)
    return popl


def encounters_1D(popul, ger_nr, checkpoints):
    print(ger_nr)
    popl = popul
    l_popl = list(popl.keys())
    i = 0
    popl_new = 0
    while i < len(l_popl):
        if i == N-1:                                                    # calculo de payoffs nao precisa dos Neis
            if popl[l_popl[i]][0] >= popl[l_popl[-1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[-1]][2] += popl[l_popl[-1]][0]
            if popl[l_popl[i]][0] >= popl[l_popl[i - 1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[i - 1]][2] += popl[l_popl[i - 1]][0]

        else:
            if popl[l_popl[i]][0] >= popl[l_popl[i+1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[i+1]][2] += popl[l_popl[i+1]][0]
            if popl[l_popl[i]][0] >= popl[l_popl[i-1]][1]:
                popl[l_popl[i]][2] += 1 - popl[l_popl[i]][0]
                popl[l_popl[i-1]][2] += popl[l_popl[i-1]][0]
        i += 1

    i = 0
    #print(popl)
    while i < N:
        payoff_total = popl[l_popl[i]][2]

        j = 1
        while j < Neigh_n + 1:
            if i + j >= N: # passou do N
                payoff_total += popl[l_popl[i - j]][2]
                payoff_total += popl[l_popl[i+j-N]][2]
            else:
                payoff_total += popl[l_popl[i - j]][2]
                payoff_total += popl[l_popl[i + j]][2]
            j += 1

        if payoff_total == 0:
            payoff_list = [1/3,1/3,1/3]
        else:
            payoff_list = [popl[l_popl[i]][2]/payoff_total]
        j = 1

        while j < Neigh_n + 1:
            if payoff_total != 0:
                if i+j >= N:  # passou do N
                    payoff_list += [popl[l_popl[i - j]][2] / payoff_total]
                    payoff_list += [popl[l_popl[i+j-N]][2] / payoff_total]
                else:
                    payoff_list += [popl[l_popl[i - j]][2]/payoff_total]
                    payoff_list += [popl[l_popl[i + j]][2]/payoff_total]
            j += 1
        #print(payoff_list)
        popl[l_popl[i]][3] += payoff_list
        i += 1
    #print(popl)
    i=0
    popl_new = collections.defaultdict(list)
    comparing = 0
    average_q_ronda = 0
    average_p_ronda = 0
    while i < N:
        r = rand.random()
        k = 0
        r_t = False
        comparing += popl[l_popl[i]][3][k]
        while k < Neigh_n*2 :
            #print(i, k)
            if r < comparing:
                r_t = True
                if k == 0:
                    popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i]][0] + popl[l_popl[i]][0] * mut,popl[l_popl[i]][0] - popl[l_popl[i]][0] * mut),
                                           rand.uniform(popl[l_popl[i]][1] + popl[l_popl[i]][1] * mut,popl[l_popl[i]][1] - popl[l_popl[i]][1] * mut),
                                           0, []
                                           ]
                    if ger_nr in checkpoints:
                        checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))
                    average_p_ronda += popl_new[l_popl[i]][0]
                    average_q_ronda += popl_new[l_popl[i]][1]
                elif k%2 == 1:
                    l = int((k+1)/2)

                    popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i-l]][0] + popl[l_popl[i-l]][0] * mut,
                                                        popl[l_popl[i-l]][0] - popl[l_popl[i-l]][0] * mut),
                                           rand.uniform(popl[l_popl[i-l]][1] + popl[l_popl[i-l]][1] * mut,
                                                        popl[l_popl[i-l]][1] - popl[l_popl[i-l]][1] * mut),
                                           0, []
                                           ]
                    if ger_nr in checkpoints:
                        checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))
                    average_p_ronda += popl_new[l_popl[i]][0]
                    average_q_ronda += popl_new[l_popl[i]][1]
                else:
                    l = int(k/2)
                    if i+k>=N:
                        popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i + l - N]][0] + popl[l_popl[i + l - N]][0] * mut,
                                                            popl[l_popl[i + l - N]][0] - popl[l_popl[i + l - N]][0] * mut),
                                               rand.uniform(popl[l_popl[i + l - N]][1] + popl[l_popl[i + l - N]][1] * mut,
                                                            popl[l_popl[i + l - N]][1] - popl[l_popl[i + l - N]][1] * mut),
                                               0, []
                                               ]
                        if ger_nr in checkpoints:
                            checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))
                        average_p_ronda += popl_new[l_popl[i]][0]
                        average_q_ronda += popl_new[l_popl[i]][1]
                    else:
                        popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i + k]][0] + popl[l_popl[i + k]][0] * mut,
                                                        popl[l_popl[i + k]][0] - popl[l_popl[i + k]][0] * mut),
                                                rand.uniform(popl[l_popl[i + k]][1] + popl[l_popl[i + k]][1] * mut,
                                                        popl[l_popl[i + k]][1] - popl[l_popl[i + k]][1] * mut),
                                           0, []
                                           ]
                    if ger_nr in checkpoints:
                        checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

                    average_p_ronda += popl_new[l_popl[i]][0]
                    average_q_ronda += popl_new[l_popl[i]][1]
                break
            k += 1

        if not r_t:
            k = int(k / 2)
            if i + k >= N:
                popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i + k - N]][0] + popl[l_popl[i + k - N]][0] * mut,
                                                    popl[l_popl[i + k - N]][0] - popl[l_popl[i + k - N]][0] * mut),
                                       rand.uniform(popl[l_popl[i + k - N]][1] + popl[l_popl[i + k - N]][1] * mut,
                                                    popl[l_popl[i + k - N]][1] - popl[l_popl[i + k - N]][1] * mut),
                                       0, []
                                       ]
                if ger_nr in checkpoints:
                    checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))
                average_p_ronda += popl_new[l_popl[i]][0]
                average_q_ronda += popl_new[l_popl[i]][1]
            else:
                popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i + k]][0] + popl[l_popl[i + k]][0] * mut,
                                                    popl[l_popl[i + k]][0] - popl[l_popl[i + k]][0] * mut),
                                       rand.uniform(popl[l_popl[i + k]][1] + popl[l_popl[i + k]][1] * mut,
                                                    popl[l_popl[i + k]][1] - popl[l_popl[i + k]][1] * mut),
                                       0, []
                                       ]
            print(ger_nr)
            if ger_nr in checkpoints:

                checkpoints_dict[ger_nr].append((popl_new[l_popl[i]][0], popl_new[l_popl[i]][1]))

            average_p_ronda += popl_new[l_popl[i]][0]
            average_q_ronda += popl_new[l_popl[i]][1]
        i += 1

    '''r = rand.random()
    if r < popl[l_popl[i]][3][0]:
        popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i]][0] + popl[l_popl[i]][0]*mut,popl[l_popl[i]][0] - popl[l_popl[i]][0]*mut),
                               rand.uniform(popl[l_popl[i]][1] + popl[l_popl[i]][1]*mut,popl[l_popl[i]][1] - popl[l_popl[i]][1]*mut),
                               0, []
                               ]
        average_p_ronda += popl_new[l_popl[i]][0]
        average_q_ronda += popl_new[l_popl[i]][1]
    elif r < popl[l_popl[i]][3][0] + popl[l_popl[i]][3][1]:
        popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[i-1]][0] + popl[l_popl[i-1]][0] * mut,popl[l_popl[i-1]][0] - popl[l_popl[i-1]][0] * mut),
                               rand.uniform(popl[l_popl[i-1]][1] + popl[l_popl[i-1]][1] * mut,popl[l_popl[i-1]][1] - popl[l_popl[i-1]][1] * mut),
                               0, []
                               ]
        average_p_ronda += popl_new[l_popl[i]][0]
        average_q_ronda += popl_new[l_popl[i]][1]
    else:
        popl_new[l_popl[i]] = [rand.uniform(popl[l_popl[j-1]][0] + popl[l_popl[j-1]][0] * mut,popl[l_popl[j-1]][0] - popl[l_popl[j-1]][0] * mut),
                               rand.uniform(popl[l_popl[j-1]][1] + popl[l_popl[j-1]][1] * mut,popl[l_popl[j-1]][1] - popl[l_popl[j-1]][1] * mut),
                               0, []
                               ]
        average_p_ronda += popl_new[l_popl[i]][0]
        average_q_ronda += popl_new[l_popl[i]][1]'''
    average_list.append([average_p_ronda/N, average_q_ronda/N])

    #print(popl_new)
    return popl_new

def checkpoint_plot(p_q,population,ger):
    fig,ax = plt.subplots(figsize=(8, 6))
    plt.title('spatial distribution of acceptance and offer strategies'), plt.ylabel('Probability', fontsize=16), plt.xlabel(
         'population', fontsize=16)

    ax.scatter(range(population), [i[0] for i in p_q[ger]], color='blue', label="p")
    ax.scatter(range(population), [i[1] for i in p_q[ger]], color='red', label="q")
    plt.ylim([0, 1])
    ax.grid(True)
    ax.legend()
    plt.show()


def main():
    checkpoints = [1,100,10000,100000]
    popl_sample = populate(population)
    ronda=0
    for j in range(0,Rondas):
        geracao = 0
        for i in range(0,Ger):
            popl_new = encounters_1D(popl_sample, i+1, checkpoints)
            #print(len(popl_new))
            #print(popl_sample)
            #print(popl_new)
            popl_sample = popl_new
            # print(geracao)

            geracao+=1
        ronda+=1


    print(average_list)
    p_list = []
    q_list = []

    i=0
    while i<len(average_list) :
        to_append_p = 0
        to_append_q = 0
        j=0
        #while j<len(average_list[i]):
            #to_append_p += average_list[i][j][0]
            #to_append_q += average_list[i][j][1]
            #j+=1
        to_append_p = average_list[i][0]
        to_append_q = average_list[i][1]
        #to_append_p /= Rondas
        #to_append_q /= Rondas

        p_list.append(to_append_p)
        q_list.append(to_append_q)
        i+=1

    for ger in checkpoints_dict.keys():
        checkpoint_plot(checkpoints_dict,N,ger)
    print("checkpoints_dict\n",checkpoints_dict[1])
    # plt.subplots(figsize=(8, 6))
    # plt.title('$\\bar{p}$ and $\\bar{q}$ variation over time'), plt.ylabel('Probability', fontsize=16), plt.xlabel(
    #     '$log_{10}t$', fontsize=16)
    #
    # plt.plot(range(Ger), p_list, color='blue', label="average_p", linestyle='--')
    # plt.plot(range(Ger), q_list, color='red', label="average_q", linestyle='--')
    # plt.xscale("log")
    # plt.ylim([0, 1])
    # plt.legend(['$\\bar{p}$-value', '$\\bar{q}$-value'])
    # plt.show()
    return 0





if __name__ == '__main__':
    main()