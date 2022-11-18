import random

g = open("champs.csv", "w+")
g.write('champ' + '\n')
h = open("all_matches.csv", "w+")
h.write('team1;team2;goals1;goals2;pen1;pen2;idx' + '\n')
grp = open("groups.csv", "w+")
grp.write('group_name;1st;2nd;3rd;4th' + '\n')
idx = 0


def sim_match(team1, team2, is_knockout=False):
    global idx
    idx += 1
    # elo ratings vars
    dr = (team1.rating - team2.rating)
    we = 1 / (10 ** (-dr / 400) + 1)

    # drawing goals for each team
    goals1 = score_som_foking_goals(we)
    goals2 = score_som_foking_goals(1 - we)

    winner = None
    loser = None
    w = -1
    if goals1 == goals2:
        w = 0.5
        team1.pts += 1
        team2.pts += 1
        if is_knockout:
            pen = pens()
            if pen[0] < pen[1]:
                winner = team2
                loser = team1
            else:
                winner = team1
                loser = team2
            h.write(
                str(team1) + ';' + str(team2) + ';' + str(goals1) + ';' + str(goals2) + ';' + str(pen[0]) + ';' + str(
                    pen[1]) + ';' + str(idx) + '\n')
            return winner, (goals1, pen[0]), (goals2, pen[1]), loser
    if goals1 > goals2:
        winner = team1
        loser = team2
        w = 1
        team1.pts += 3
    if goals2 > goals1:
        winner = team2
        loser = team1
        w = 0
        team2.pts += 3

    k = 60
    gd = abs(goals1 - goals2)
    if gd == 2: k += 0.5
    if gd == 3: k += 0.75
    if gd > 3: k += (gd - 3) / 8
    delta = k * (w - we)
    team1.rating += delta
    team2.rating -= delta

    team1.mp += 1
    team2.mp += 1
    team1.gs += goals1
    team1.gc += goals2
    team2.gs += goals2
    team2.gc += goals1

    h.write(str(team1) + ';' + str(team2) + ';' + str(goals1) + ';' + str(goals2) + ';ND;ND;' + str(idx) + '\n')
    return winner, goals1, goals2, loser


def pens():
    scr1 = 0
    scr2 = 0
    for i in range(5):
        if random.random() < 0.76: scr1 += 1
        if random.random() < 0.76: scr2 += 1
        if abs(scr1 - scr2) > 4 - i: return scr1, scr2
    while scr1 == scr2:  # sudden death
        if random.random() < 0.75: scr1 += 1
        if random.random() < 0.75: scr2 += 1
    return scr1, scr2


def knockout_rounds(still_there):
    rnd = len(still_there)
    # all of this if statement just to play 3rd place game:
    if rnd == 4:
        final = [None, None]
        sf1 = sim_match(still_there[0], still_there[1], is_knockout=True)
        sf2 = sim_match(still_there[2], still_there[3], is_knockout=True)
        final[0], final[1] = sf1[0], sf2[0]
        third = sim_match(sf1[3], sf2[3], is_knockout=True)[0]
        knockout_rounds(final)
    else:
        if rnd == 1:
            g.write(str(still_there[0].name) + '\n')
            global idx
            idx = 0
            return still_there[0]  # world champ here
        next_round = [None] * int(rnd / 2)
        for i in range(0, rnd, 2):
            next_round[int(i / 2)] = sim_match(still_there[i], still_there[i + 1], is_knockout=True)[0]
        knockout_rounds(next_round)


class Team:
    __slots__ = ['name', 'rating', 'group', 'group_loc', 'pts', 'gs', 'gc', 'mp']

    def __init__(self, name: str, rating: int, group: chr, group_loc: int, pts: int = 0, gs: int = 0, gc: int = 0,
                 mp: int = 0):
        self.name = name
        self.rating = rating
        self.group = group
        self.group_loc = group_loc
        self.pts = pts
        self.gs = gs
        self.gc = gc
        self.mp = mp

    def __repr__(self) -> str:
        return self.name

    def __lt__(self, other):
        if self.mp == 0 and other.mp == 0:
            return self.group_loc < other.group_loc
        if self.pts == other.pts:
            if (self.gs - self.gc) == (other.gs - other.gc):
                if self.gs == other.gs:
                    return self.rating < other.rating
                return self.gs < other.gs
            return (self.gs - self.gc) < (other.gs - other.gc)
        return self.pts < other.pts


class Group:
    __slots__ = ['name', 'teamsy']

    def __init__(self, name, teamsy):
        self.name = name
        self.teamsy = sorted(teamsy)

    def __repr__(self) -> str:
        return self.name + ';' + str(self.teamsy[0]) + ';' + str(self.teamsy[1]) + ';' + str(
            self.teamsy[2]) + ';' + str(self.teamsy[3])

    def group_matches(self):
        sim_match(self.teamsy[0], self.teamsy[1])
        sim_match(self.teamsy[2], self.teamsy[3])
        sim_match(self.teamsy[0], self.teamsy[2])
        sim_match(self.teamsy[3], self.teamsy[1])
        sim_match(self.teamsy[3], self.teamsy[0])
        sim_match(self.teamsy[1], self.teamsy[2])

        self.teamsy = sorted(self.teamsy, reverse=True)
        grp.write(str(self) + '\n')


def score_som_foking_goals(we):
    x = we
    squ = x * x
    tri = squ * x
    qua = tri * x

    result = random.random()
    error_corrector = 0.3345 * qua - 0.7207 * tri + 0.5316 * squ - 0.1541 * x + 1.0144
    goals_0 = (1.6163 * qua - 4.1663 * tri + 3.7334 * squ - 1.8312 * x + 0.713) / error_corrector
    if result < goals_0: return 0
    goals_1 = (-1.6687 * qua + 3.295 * tri - 2.6629 * squ + 0.9349 * x + 0.2587) / error_corrector
    if result < (goals_0 + goals_1): return 1
    goals_2 = (-1.0356 * qua + 2.1526 * tri - 1.6883 * squ + 0.8078 * x + 0.0294) / error_corrector
    if result < (goals_0 + goals_1 + goals_2): return 2
    goals_3 = (0.1685 * qua - 0.0619 * tri - 0.0036 * squ + 0.1632 * x) / error_corrector
    if result < (goals_0 + goals_1 + goals_2 + goals_3): return 3
    goals_4 = max(0, (0.8176 * qua - 1.3061 * tri + 0.8288 * squ - 0.1631 * x + 0.0086)) / error_corrector
    if result < (goals_0 + goals_1 + goals_2 + goals_3 + goals_4): return 4
    goals_5 = max(0, (0.4762 * qua - 0.7185 * tri + 0.3817 * squ - 0.0783 * x + 0.0048)) / error_corrector
    if result < (goals_0 + goals_1 + goals_2 + goals_3 + goals_4 + goals_5):
        return 5
    else:
        return 0
