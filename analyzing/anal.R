all_matches<-read.csv("all_matches.csv", sep=";")
groups<-read.csv("groups.csv", sep=";")
champs<-read.csv("champs.csv", sep=";")


library(dplyr)

all_matches %>% 
  summarise(suma=sum(goals1)+sum(goals2))/64000

poland<-all_matches %>% 
  filter(team1=='Poland' | team2=='Poland')

champs<-champs %>% 
  mutate(champ=Iran, Iran=NULL)
champs

#wholl be champion
champs %>% 
  group_by(champ) %>% 
  summarise(wins=n()) %>% 
  mutate(winratio=wins/999) %>% 
  arrange(-winratio)

#wholl adavance
awanse<-c(groups$X1st,groups$X2nd)
awanse<-as.data.frame(awanse)
awanse %>% 
  group_by(awanse) %>% 
  summarise(adv=n()) %>% 
  mutate(advratio=adv/1000) %>% 
  arrange(-advratio)


#poland matches
poland %>% 
  filter(idx==14) %>% 
  mutate(result=case_when(
    goals1>goals2~'Mexico',
    goals1<goals2~'Poland',
    TRUE~'Draw'
  )) %>% 
  group_by(result) %>% 
  summarise(resratio=n()/1000)

poland %>% 
  filter(idx==16) %>% 
  mutate(result=case_when(
    goals2>goals1~'Saudi_Arabia',
    goals2<goals1~'Poland',
    TRUE~'Draw'
  )) %>% 
  group_by(result) %>% 
  summarise(resratio=n()/1000)

poland %>% 
  filter(idx==17) %>% 
  mutate(result=case_when(
    goals2>goals1~'Argentina',
    goals2<goals1~'Poland',
    TRUE~'Draw'
  )) %>% 
  group_by(result) %>% 
  summarise(resratio=n()/1000)

#poland position
groups %>% 
  filter(group_name=='C') %>% 
  mutate(polando=case_when(
    X1st=='Poland'~1,
    X2nd=='Poland'~2,
    X3rd=='Poland'~3,
    TRUE~4,
  )) %>% 
  group_by(polando) %>% 
  summarise(posrate=n()/1000)

#rivals of poland
all_matches %>% 
  filter(idx>48 & (team1=='Poland' | team2=='Poland')) %>% 
  mutate(phase=case_when(
    idx<57~'rof16',
    idx<61~'qf',
    idx<63~'sf',
    idx==63~'mo3rd',
    TRUE~'final'
  )) %>% 
  filter(phase=='final') %>% 
  mutate(rival=case_when(
    team1=='Poland'~team2,
    TRUE~team1
  )) %>% 
  group_by(rival) %>% 
  summarise(nriv=n()) %>% 
  mutate(ratriv=nriv/sum(nriv), nriv=NULL) %>% 
  arrange(-ratriv)

#most common final
all_matches %>% 
  filter(idx==64) %>% 
  group_by(team1, team2) %>% 
  summarise(ratfinals=n()/1000) %>% 
  arrange(-ratfinals)


