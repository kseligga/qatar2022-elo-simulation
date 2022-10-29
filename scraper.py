import time

from qatar2022.team import Team, Group, knockout_rounds

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

ratings = [x for _, x in sorted(zip(teams, ratings))]
names=sorted(teams)
print(names)
grouppies=['C', 'D', 'F', 'G', 'G', 'F', 'E', 'F', 'D', 'A', 'B', 'D', 'E', 'H', 'B', 'E', 'C', 'F', 'A', 'C', 'H', 'A', 'C', 'A', 'G', 'H', 'E', 'G', 'D', 'B', 'H', 'B']
locations=[1,2,1,1,4,2,2,4,3,2,1,1,3,2,2,4,3,3,4,4,1,1,2,3,2,4,1,3,4,3,3,4]

teams=[]
for i in range(32):
    if names[i]=='Qatar':
        ratings[i]+=100
    Team_i = Team(names[i], ratings[i], grouppies[i], locations[i])
    teams.append(Team_i)


groups_def=[]

for i in range(65,73):
    #print(chr(i))
    tmp=[z for z in teams if z.group == chr(i)]
    groups_def.append(Group(chr(i), tmp))


def tournament(groups):
    for group in groups:
        group.group_matches()
        #print(group)

    #print(groups)
    knockouts = [None] * 16

    tmp = -1
    for i in range(8):
        knockouts[i] = (groups[i].teamsy[int((tmp + 1) / 2)])
        tmp *= -1
    tmp = 1
    for i in range(8):
        knockouts[i + 8] = (groups[i].teamsy[int((tmp + 1) / 2)])
        tmp *= -1

    #print(knockouts)
    knockout_rounds(knockouts)

howmanytimes=100000
start=time.time()
for i in range(howmanytimes):
    tournament(groups_def)
stop=time.time()
print(stop-start)


