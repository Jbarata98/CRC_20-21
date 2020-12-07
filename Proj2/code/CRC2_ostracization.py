import random as rand
import collections
import matplotlib.pyplot as plt

'''------------------------------------INIT VARIABLES---------------------------------------------------------------'''

ger = 1000
N = 100
rondas = 1
mut1, mut2, mut3, mut4, mut5, mut6 = 0.001, 0.002, 0.01, 0.02, 0.1, 0.2
mut = mut1
average_list = []   # lista dos average de cada geracao
ostr = 0.5          # value of ostracization

population = collections.defaultdict(list)

'''------------------------------------INIT VARIABLES---------------------------------------------------------------'''

'''Function to populate, returns a dictionary = {User:(p,q,payoff)}'''


def populate(popl):  # populates our sample
    i = 1
    while i <= N:
        popl['S' + str(i)] = [rand.uniform(0, 1), rand.uniform(0, 1), 0, 0, False] #difference now is that we have a boolean caracterizing if its being ostracized or not
        i += 1
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
    popl_new = collections.defaultdict(list)  # populacao da geracao seguinte
    for comb in combinations:  # o cada combination corresponde a um par de utlizadores (S1,S2) como no paper

        if popl[comb[1]][4]: # verifies if S2 is being ostracized
            r = rand.random()
            if r > ostr and popl[comb[0]][0] >= popl[comb[1]][1]:  #se o p do S1 for maior ou igual que o q do S2 and randomly gets selected that you wont be ostracized
                popl[comb[0]][2] += 1 - popl[comb[0]][0]   # o payoff do S1 sera igual a 1-p
                popl[comb[1]][2] += popl[comb[0]][0]   # o payoff do S2 ira aumentar em P
                payoff_total += 1
                popl[comb[0]][3] += 1
        else:
            if popl[comb[0]][0] >= popl[comb[1]][1]:
                popl[comb[0]][2] += 1 - popl[comb[0]][0]
                popl[comb[1]][2] += popl[comb[0]][0]
                payoff_total += 1
                popl[comb[0]][3] += 1

        if popl[comb[0]][4]: # verifies if S1 is being ostracized
            r = rand.random()
            if r > ostr and popl[comb[1]][0] >= popl[comb[0]][1]:
                popl[comb[1]][2] += 1 - popl[comb[1]][0]
                popl[comb[0]][2] += popl[comb[1]][0]
                payoff_total += 1
                popl[comb[1]][3] += 1
        else:
            if popl[comb[1]][0] >= popl[comb[0]][1]:
                popl[comb[1]][2] += 1 - popl[comb[1]][0]
                popl[comb[0]][2] += popl[comb[1]][0]
                payoff_total += 1
                popl[comb[1]][3] += 1


    '''calculate average q value (useful to display later)'''
    for person in popl.keys():
        popl[person][2] /= payoff_total
        if popl[person][3] < N / 2:
            popl[person][4] = True

        average_p += popl[person][0]
        average_q += popl[person][1]


    ''' calculates new population taking into account the predefined mutations '''

    l_popl = list(popl.keys())

    i = 0
    while i < N:
        comparing = 0
        r = rand.random()
        p = 0
        r_t = False
        var = i
        while p < N:
            comparing += popl[l_popl[var - p]][2]
            if r < comparing:
                r_t = True
                new_p = rand.uniform(popl[l_popl[var - p]][0] - popl[l_popl[var - p]][0] * mut,
                                     popl[l_popl[var - p]][0] + popl[l_popl[var - p]][0] * mut)
                new_q = rand.uniform(popl[l_popl[var - p]][1] - popl[l_popl[var - p]][1] * mut,
                                     popl[l_popl[var - p]][1] + popl[l_popl[var - p]][1] * mut)
                popl_new['S' + str(i + 1)] = [new_p, new_q, 0, 0, popl[l_popl[var - p]][4]]
                break
            p += 1
        if not r_t:
            new_p = rand.uniform(popl[l_popl[var - p]][0] - popl[l_popl[var - p]][0] * mut,
                                 popl[l_popl[var - p]][0] + popl[l_popl[var - p]][0] * mut)
            new_q = rand.uniform(popl[l_popl[var - p]][1] - popl[l_popl[var - p]][1] * mut,
                                 popl[l_popl[var - p]][1] + popl[l_popl[var - p]][1] * mut)
            popl_new['S' + str(i + 1)] = [new_p, new_q, 0, 0, popl[l_popl[var - p]][4]]
        i += 1


    print('--------RONDA:------------', ronda, '----Geracao:-----', geracao)


    average_p /= N
    average_q /= N
    if ronda == 0:
        average_list.append([[average_p, average_q]])
    else:
        average_list[geracao] += [[average_p, average_q]]

    num_rands = []  # hack to make sure we dont have more than 100 offpsrings, deletes randomly the overflow
    while len(num_rands) < j - N:
        r = rand.randint(1, j)
        if r not in num_rands:
            num_rands.append(r)
            del (popl_new['S' + str(r)])
    return popl_new, payoff_total

''' main function, calculates the new population for each generation '''


def main():
    ronda = 0
    for j in range(0, rondas):
        geracao = 0
        popl_sample = populate(population)
        for i in range(0, ger):
            popl_new, payoff_total = random_encounters(popl_sample, ronda, geracao)

            popl_sample = popl_new
            geracao += 1
        ronda += 1

    '''saves the average q and p value to plot'''

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

    '''-------------plot the figures----------------------- '''

    plt.subplots(figsize=(8, 6))
    plt.title('$\\bar{p}$ and $\\bar{q}$ variation over time'), plt.ylabel('Value', fontsize=16), plt.xlabel(
        '$log_{10}t$', fontsize=16)

    plt.plot(range(ger), p_list, color='blue', label="average_p", linestyle='--')
    plt.plot(range(ger), q_list, color='red', label="average_q", linestyle='--')
    plt.legend(['Average p', 'Average q'])

    plt.xscale("log")
    plt.ylim([0, 1])
    plt.show()

    return 0


if __name__ == '__main__':
    main()
