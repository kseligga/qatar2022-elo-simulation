import random

from numpy.random.mtrand import poisson

f = open("stspaste.txt", "r")
g = open("model_res.txt", "w+")

def mecz(punkty, linie):
    wyniki = []
    kursy = []
    for dane in linie:
        x = dane.split('\t')
        for el in x:
            if float(el[3::])<250:
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

    print(wyniki)
    print(kursy)
    print(probabs)
    print(goaldiff)
    expectedptswynik = []

    probabs1=0
    probabs2=0
    drawprob=0
    gs_probab=0
    for i in range(len(wyniki)):
        if goaldiff[i]>0:
            probabs1+=probabs[i]
        if goaldiff[i]<0:
            probabs2+=probabs[i]
        if goaldiff[i]==0:
            drawprob+=probabs[i]
        if int(wyniki[i][0])==gs:
            gs_probab+=probabs[i]

    we=probabs1/(probabs1+probabs2)
    print(we)
    print(drawprob)
    g.write(str(we) + ';' + str(gs_probab) + '\n')
    # sortedwyniki = list(reversed([x for _, x in sorted(zip(expectedptswynik, wyniki))]))
    # sortedexp = sorted(expectedptswynik, reverse=True)
    # g.write(str(sortedwyniki[0]) + ' ' + str(round(sortedexp[0], 3)) + '\n')
    #
    # for i in range(len(wyniki) - 1, -1, -1):
    #     print(str(sortedwyniki[i]) + ' spodziewane punkty: ' + str(round(sortedexp[i], 3)))


# for i in range(48):
#     linie = []
#     j = 0
#     f = open("stspaste.txt", "r")
#     for line in f.readlines():
#         line = line.strip('\n')
#         if int(j - i * 20) in wheredane:
#             linie.append(line)
#         j += 1
#     f.close()
#     mecz(punkty, linie)

def draw_probability(team1_we):
    x = team1_we-0.5
    sque=x**2
    quadr=sque**2
    return - 1.3746 * quadr - 0.5436 * sque + 0.2976

# scoring 0:
# y = 1,6163x4 - 4,1663x3 + 3,7334x2 - 1,8312x + 0,713
# scoring 1:
# y = -1,6687x4 + 3,295x3 - 2,6629x2 + 0,9349x + 0,2587
# scoring 2:
# y= -1,0356x4 + 2,1526x3 - 1,6883x2 + 0,8078x + 0,0294
# scoring 3:
# y = 0,1685x4 - 0,0619x3 - 0,0036x2 + 0,1632x
# scoring 4:
# y = 0,8176x4 - 1,3061x3 + 0,8288x2 - 0,1631x + 0,0086
# scoring 5:
# y = 0,4762x4 - 0,7185x3 + 0,3817x2 - 0,0783x + 0,0048


def score_som_foking_goals(we):
    x=we
    squ=x*x
    tri=squ*x
    qua=tri*x

    #error_corrector=0.3743*qua - 0.8052*tri + 0.589*squ - 0.1667*x + 1.0145
    error_corrector=1
    goals_0=(1.6163*qua - 4.1663*tri + 3.7334*squ - 1.8312*x + 0.713)/error_corrector
    goals_1=(-1.6687*qua + 3.295*tri - 2.6629*squ + 0.9349*x + 0.2587)/error_corrector
    goals_2=(-1.0356*qua + 2.1526*tri - 1.6883*squ + 0.8078*x + 0.0294)/error_corrector
    goals_3=(0.1685*qua - 0.0619*tri - 0.0036*squ + 0.1632*x)/error_corrector
    goals_4=(0.8176*qua - 1.3061*tri + 0.8288*squ - 0.1631*x + 0.0086)/error_corrector
    goals_5=(0.4762*qua - 0.7185*tri + 0.3817*squ - 0.0783*x + 0.0048)/error_corrector
    print(goals_5, goals_4, goals_3, goals_2, goals_1, goals_0)
    result = random.random()

    if result<goals_0: return 0
    if result<goals_1: return 1
    if result<goals_2: return 2
    if result<goals_3: return 3
    if result<goals_4: return 4
    if result<goals_5: return 5
    else: return 6 #about 1 in 50000 chance




