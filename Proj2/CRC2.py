import random as rand
import itertools as iter
import collections
import matplotlib.pyplot as plt

ger = 1000
N = 100
rondas = 1
mut1, mut2, mut3, mut4, mut5, mut6 = 0.001, 0.002, 0.01, 0.02, 0.1, 0.2
average_list = []                                       # lista dos average de cada geracao

population = collections.defaultdict(list)

'''Function to populate, returns a dictionary = {User:(p,q,payoff)}'''

def populate(popl):                                     # populates our sample
    i = 1
    while i <= N:
        popl['S' + str(i)] = [rand.random(), rand.random(), 0]
        i += 1
    # print("population:\n", popl)
    return popl

'''Function that calculates the random encounters'''
'''Args: Population (dictionary), Round number (integer), Generation number(integer)'''
'''Output: New population sample (dictionary)'''

def random_encounters(popl, ron, ger):
    ronda = ron
    geracao = ger
    combinations = [(x, y) for idx, x in enumerate(list(popl)) for y in list(popl)[idx + 1:]]
    payoff_total = 0
    average_p, average_q = 0, 0
    j = 0
    # payof_frac_tot = 0 #
    popl_new = collections.defaultdict(list)          # populacao da geracao seguinte
    top5, top5_p, top5_q = [0] * 5, [0] * 5, [0] * 5
    for comb in combinations:                         # o cada combination corresponde a um par de utlizadores (S1,S2) como no paper
        if popl[comb[0]][0] >= popl[comb[1]][1]:      # se o p do S1 for maior ou igual que o q do S2
            popl[comb[0]][2] += 1 - popl[comb[0]][0]  # o payoff do S1 sera igual a 1-p
            popl[comb[1]][2] += popl[comb[0]][0]      # o payoff do S2 ira aumentar em P
            payoff_total += 1


    for person in popl.keys():
        popl[person][2] /= payoff_total
        '''Experiencias do Ze Maluco'''
        # if popl[person][2] > min(top5):
        #     if top5[0] == min(top5):
        #         top5[0] = popl[person][2]
        #         top5_p[0] = popl[person][0]
        #         top5_q[0] = popl[person][1]
        #     elif top5[1] == min(top5):
        #         top5[1] = popl[person][2]
        #         top5_p[1] = popl[person][0]
        #         top5_q[1] = popl[person][1]
        #     elif top5[2] == min(top5):
        #         top5[2] = popl[person][2]
        #         top5_p[2] = popl[person][0]
        #         top5_q[2] = popl[person][1]
        #     elif top5[3] == min(top5):
        #         top5[3] = popl[person][2]
        #         top5_p[3] = popl[person][0]
        #         top5_q[3] = popl[person][1]
        #     else:
        #         top5[4] = popl[person][2]
        #         top5_p[4] = popl[person][0]
        #         top5_q[4] = popl[person][1]

        average_p += popl[person][0]
        average_q += popl[person][1]


        i = 0
        while i < N / 10 + 3 * N / 100:                   # calculates new population taking into account the mutations
            if rand.random() < popl[person][2] * 10:
                new_p = rand.uniform(popl[person][0] - popl[person][0] * mut5, popl[person][0] + popl[person][0] * mut5)
                new_q = rand.uniform(popl[person][1] - popl[person][1] * mut5, popl[person][1] + popl[person][1] * mut5)
                popl_new['S' + str(j + 1)] = [new_p, new_q, 0]
                '''print('old_p:',popl[person][0])
                print('new_p:',new_p)
                print('old_q:',popl[person][1])
                print('new_q:',new_q)'''
                j += 1
            i += 1
    print('--------RONDA:------------', ronda, '----Geracao:-----', geracao)
    '''print('top 5 payoff:', top5)
    print('top 5 pespes:', top5_p)
    print('top 5 quesques:', top5_q)'''

    average_p /= N
    average_q /= N
    if ronda == 0:
        average_list.append([[average_p, average_q]])
    else:
        average_list[geracao].append([average_p, average_q])
    '''print('average p:',average_p)
    print('average q:',average_q)'''
    num_rands = []                               #hack to make sure we dont have more than 100 offpsrings, deletes randomly the overflow
    while len(num_rands) < j - N:
        r = rand.randint(1, j)
        if r not in num_rands:
            num_rands.append(r)
            del (popl_new['S' + str(r)])
    # payof_frac_tot+= popl[person][2] # has to be 1 in the end
    return popl_new


def main():
    popl_sample = populate(population)
    ronda = 0
    for j in range(0, rondas):
        geracao = 0
        for i in range(0, ger):
            popl_new = random_encounters(popl_sample, ronda, geracao)
            # print(len(popl_new))
            # print(popl_sample)
            # print(popl_new)
            popl_sample = popl_new
            geracao += 1
        ronda += 1

    print(average_list)
    p_list, q_list = [], []
    for i in average_list:
        to_append_p, to_append_q = 0, 0
        for j in i:
            to_append_p += j[0]
            to_append_q += j[1]
        to_append_p /= rondas
        to_append_q /= rondas
        p_list.append(to_append_p)
        q_list.append(to_append_q)

    print(p_list)
    print(q_list)

    plt.subplots(figsize=(8, 6))
    plt.title('$\\bar{P}$ variation over time'),plt.ylabel('$\\bar{P}$',fontsize=16), plt.xlabel('$log_{10}t$', fontsize=16)

    plt.plot(range(ger), p_list, color='blue', label="average_p", linestyle='--')
    plt.plot(range(ger), q_list, color='red', label="average_q", linestyle='--')
    plt.xscale("log")
    plt.ylim([0, 1])
    plt.show()

    return 0


if __name__ == '__main__':
    main()
