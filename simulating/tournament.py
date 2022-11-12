import time

from qatar2022.simulation_handling import Team,knockout_rounds, Group

# getting elo ratings
f = open("copiedwebsite.txt", "r")
content = f.read()
teams=[]
ratings=[]
result = content.split(' team-cell ')
for i in range(1,33):
    result1 = result[i].split(' narrow-layout')
    result2 = result1[1].split('"')
    teams.append(result2[2])
    ratings.append(int(result1[2][2:6]))

# preparing data
ratings = [x for _, x in sorted(zip(teams, ratings))]
names=sorted(teams)
grouppies=['C', 'D', 'F', 'G', 'G', 'F', 'E', 'F', 'D', 'A', 'B', 'D', 'E', 'H', 'B', 'E', 'C', 'F', 'A', 'C', 'H', 'A', 'C', 'A', 'G', 'H', 'E', 'G', 'D', 'B', 'H', 'B']
locations=[1,2,1,1,4,2,2,4,3,2,1,1,3,2,2,4,3,3,4,4,1,1,2,3,2,4,1,3,4,3,3,4]


def create():  # creating setup for every tournament is faster than deep copying every time
    """can be better, takes 0.1s of 0.44s for every 1k sims"""
    teams = []
    for i in range(32):
        rating=ratings[i]
        name=names[i]
        if name == 'Qatar':
            rating += 100
        team_i = Team(name, rating, grouppies[i], locations[i])
        #teams[i] = team_i
        teams.append(team_i)
    groups_setup = []
    for i in range(65, 73):
        tmp = [team for team in teams if team.group == chr(i)]
        groups_setup.append(Group(chr(i), tmp))
    return groups_setup


def tournament(groups):
    # group matches
    for group in groups:
        group.group_matches()
        #print(group)
    # preparing knockouts bracket
    knockouts = []
    tmp = -1
    for i in range(8):
        knockouts.append(groups[i].teamsy[int((tmp + 1) / 2)])
        tmp *= -1
    tmp = 1
    for i in range(8):
        knockouts.append(groups[i].teamsy[int((tmp + 1) / 2)])
        tmp *= -1

    # knockouts
    knockout_rounds(knockouts)


howmanytimes=1000
start=time.time()
for i in range(howmanytimes):
    global idx
    idx=0
    tournament(create())
    if i%(0.05*howmanytimes)==0:
        print(str(i/howmanytimes*100)+'%')
stop=time.time()
print(stop-start)

