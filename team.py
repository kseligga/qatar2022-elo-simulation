import random

def sim_match(team1, team2, is_knockout=False):

    dr = (team1.ranting - team2.ranting)
    we = 1 / (10 ** (-dr / 400) + 1)



    # TODO
    goals1 = score_som_foking_goals(we)
    goals2 = score_som_foking_goals(1-we)

    # goals1=random.randint(0,3)
    # goals2 = random.randint(0, 3)

    #print(str(team1)+' '+str(team2)+' wynik to '+str(goals1)+' : '+str(goals2))
    winner = None
    w = -1

    if goals1 == goals2:
        w = 0.5
        team1.pts+=1
        team2.pts+=1
        if is_knockout:
            pen=pens()
            if pen[0] > pen[1]:
                winner = team2
            else:
                winner = team1
            #print(goals1, goals2, winner)
            return [winner, [goals1, pen[0]], [goals2, pen[1]]]
    if goals1 > goals2:
        winner = team1
        w = 1
        team1.pts+=3
    if goals2 > goals1:
        winner = team2
        w = 0
        team2.pts+=3

    delta = 60 * (w - we)
    team1.ranting += delta
    team2.ranting -= delta

    team1.mp+=1
    team2.mp+=1
    team1.gs+=goals1
    team1.gc+=goals2
    team2.gs+=goals2
    team2.gc+=goals1

    #print(goals1, goals2, winner)
    return (winner, goals1, goals2)

def pens():
    scr1=0
    scr2=0
    for i in range(5):
        if random.random()<0.76: scr1+=1
        if random.random()<0.76: scr2+=1
        if abs(scr1-scr2)>4-i: return (scr1, scr2)
    while scr1==scr2:
        if random.random()<0.75: scr1+=1
        if random.random()<0.75: scr2+=1
    return scr1, scr2

def knockout_rounds(still_there):
    rnd=len(still_there)
    if rnd==1:
        return still_there[0]
    next_round=[None] * int(rnd/2)
    for i in range(0,rnd,2):
        #print(i)
        #print(still_there[i], still_there[i+1])
        winner = sim_match(still_there[i], still_there[i+1], is_knockout=True)[0]
        next_round[int(i/2)] = winner
    knockout_rounds(next_round)


class Team:
    __slots__ = ['name', 'ranting', 'group', 'group_loc', 'pts', 'gs', 'gc', 'mp']

    def __init__(self, name: str, ranting: int, group: chr, group_loc: int, pts: int=0, gs: int=0, gc:int=0, mp:int=0):
        self.name=name
        self.ranting=ranting
        self.group=group
        self.group_loc=group_loc
        self.pts=pts
        self.gs=gs
        self.gc=gc
        self.mp=mp

    def __repr__(self) -> str:
        return (self.name+' '+self.group+' '+str(self.group_loc)+' '+str(round(self.ranting))+' '+str(self.pts))

    def __lt__(self, other):
        if self.mp==0 and other.mp==0:
            return self.group_loc<other.group_loc
        if self.pts==other.pts:
            if (self.gs-self.gc)==(other.gs-other.gc):
                if (self.gs==other.gs):
                    return self.ranting<other.ranting
                return self.gs<other.gs
            return (self.gs-self.gc)<(other.gs-other.gc)
        return self.pts<other.pts

class Group:
    __slots__ = ['name', 'teamsy']

    def __init__(self, name, teamsy):
        self.name=name
        self.teamsy=sorted(teamsy)

    def __repr__(self) -> str:
        return (self.name+' '+str(self.teamsy))

    def group_matches(self):
        sim_match(self.teamsy[0], self.teamsy[1])
        sim_match(self.teamsy[2], self.teamsy[3])
        sim_match(self.teamsy[0], self.teamsy[2])
        sim_match(self.teamsy[1], self.teamsy[3])
        sim_match(self.teamsy[0], self.teamsy[3])
        sim_match(self.teamsy[1], self.teamsy[2])

        self.teamsy=sorted(self.teamsy, reverse=True)



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
    #print(goals_5, goals_4, goals_3, goals_2, goals_1, goals_0)
    result = random.random()

    if result<(goals_0): return 0
    if result<(goals_0+goals_1): return 1
    if result<(goals_0+goals_1+goals_2): return 2
    if result<(goals_0+goals_1+goals_2+goals_3): return 3
    if result<(goals_0+goals_1+goals_2+goals_3+goals_4): return 4
    if result<(goals_0+goals_1+goals_2+goals_3+goals_4+goals_5): return 5
    else: #time.sleep(2)
        #print('6 goals!!!')
        return 6 #about 1 in 50000 chance
