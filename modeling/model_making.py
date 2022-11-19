f = open("stspaste.txt", "r")
g = open("model_res.csv", "w+")
h = open("bookmaker_we.csv", "w+")
g.write("n_goals;win_expectancy;n_goals_probability\n")
h.write("we\n")
wheredane = [1, 3, 5, 8, 10, 12, 15, 17, 19]


def mecz(linie):
    wyniki = []
    kursy = []
    for dane in linie:
        x = dane.split('\t')
        for el in x:
            if float(el[3::]) < 250:
                wyniki.append(el[0:3])
                kursy.append(float(el[3::]))

    falseprobabs = []
    for x in kursy:
        def res(x): return 1 / x

        falseprobabs.append(res(x))
    probabs = []
    for x in falseprobabs:
        def res(x): return x / sum(falseprobabs)

        probabs.append(res(x))

    goaldiff = []

    for x in wyniki:
        def res(x): return int(x[0]) - int(x[2])

        goaldiff.append(res(x))

    probabs1 = 0
    probabs2 = 0
    drawprob = 0
    gs_probab_host = 0
    gs_probab_away = 0
    we=0
    gs = 0
    while gs < 6:
        for i in range(len(wyniki)):
            if goaldiff[i] > 0:
                probabs1 += probabs[i]
            if goaldiff[i] < 0:
                probabs2 += probabs[i]
            if goaldiff[i] == 0:
                drawprob += probabs[i]
            if int(wyniki[i][2]) == gs:
                gs_probab_away += probabs[i]
            if int(wyniki[i][0]) == gs:
                gs_probab_host += probabs[i]

        we = probabs1 / (probabs1 + probabs2)
        g.write(str(gs) + ';' + str(1 - we) + ';' + str(gs_probab_away) + '\n')
        g.write(str(gs) + ';' + str(we) + ';' + str(gs_probab_host) + '\n')
        gs += 1
        gs_probab_away = 0
        gs_probab_host = 0
    h.write(str(we) + '\n')


for i in range(48):
    linie = []
    j = 0
    f = open("stspaste.txt", "r")
    for line in f.readlines():
        line = line.strip('\n')
        if int(j - i * 20) in wheredane:
            linie.append(line)
        j += 1
    f.close()
    mecz(linie)
f.close()
g.close()
h.close()