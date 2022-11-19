error_corrector <- function(x) {
  0.3345 * x^4 - 0.7207 * x^3 + 0.5316 * x^2 - 0.1541 * x + 1.0144}
g0 <- function(x) {
  (1.6163*x^4 - 4.1663*x^3 + 3.7334*x^2 - 1.8312*x + 0.713)/error_corrector(x)}
g1 <- function(x) {
  (-1.6687 *x^4 + 3.295 * x^3 - 2.6629 * x^2 + 0.9349 * x + 0.2587)/error_corrector(x)}
g2 <- function(x) {
  (-1.0356 * x^4 + 2.1526 * x^3 - 1.6883 * x^2 + 0.8078 * x + 0.0294)/error_corrector(x)}
g3 <- function(x) {
  (0.1685 * x^4 - 0.0619 * x^3 - 0.0036 * x^2 + 0.1632 * x)/error_corrector(x)}
g4 <- function(x) {
  res<-((0.8176 * x^4 - 1.3061 * x^3 + 0.8288 * x^2 - 0.1631 * x + 0.0086)/error_corrector(x))
  ifelse(res<0, 0, res)}
g5 <- function(x) {
  res<-((0.4762 * x^4 - 0.7185 * x^3 + 0.3817 * x^2 - 0.0783 * x + 0.0048)/error_corrector(x))
  ifelse(res<0, 0, res)}

library(dplyr)
library(ggplot2)
library(tidyr)

# bookmaker_we.csv and model_res generated in model_making.py
# elo_we.csv generated in python simulation files (not in repo)
bookmaker<-read.csv("model_res.csv", sep=";")
bookmaker_we<-read.csv("bookmaker_we.csv", sep=";")
elo_we<-read.csv("elo_we.csv", sep=";")

elo_we<-as.data.frame(elo_we %>% 
  filter(idx<=48) %>% 
  group_by(idx, team1) %>% 
  summarise(avg_elo_we=mean(we_team1)))

df<-elo_we[c(1,7,2,8,13,20,14,19,32,26,25,31,38,44,43,37,10,3,4,9,22,16,21,15,28,33,34,27,40,46,39,45,5,6,12,11,23,24,17,18,35,36,29,30,47,48,41,42),] %>% 
  mutate(idx=NULL) %>% 
  select(avg_elo_we, team1)

cbind(df, bookmaker_we) %>% 
  ggplot(aes(x=we, y=avg_elo_we))+
  geom_point()+
  labs(title = "ELO Win expectancy vs bookmakers' win expectancy",
       x = "ELO win expectancy",
       y = "Bookmakers' win expectancy")+
  scale_y_continuous(expand=c(0,0), limits = c(0,1))+
  scale_x_continuous(expand=c(0,0), limits = c(0,1), minor_breaks = seq(0,1,0.05))+
  geom_function(fun=abs)+
  theme_minimal()

cor(df$avg_elo_we, bookmaker_we$we, method='pearson')



bookmaker<-bookmaker %>%
  mutate(my_n_goals_prob=case_when(
    n_goals==0~g0(win_expectancy),
    n_goals==1~g1(win_expectancy),
    n_goals==2~g2(win_expectancy),
    n_goals==3~g3(win_expectancy),
    n_goals==4~g4(win_expectancy),
    n_goals==5~g5(win_expectancy)
  ))

cor(bookmaker$n_goals_probability, bookmaker$my_n_goals_prob, method = "pearson")

for (n in 0:5) {
  res<-cor(bookmaker[bookmaker$n_goals==n,"n_goals_probability"],
      bookmaker[bookmaker$n_goals==n,"my_n_goals_prob"])
  print(res)
}

tmp<-filter(bookmaker, n_goals==5, n_goals_probability>0) %>% 
  select(n_goals_probability, my_n_goals_prob)
cor(tmp$n_goals_probability, tmp$my_n_goals_prob)

bookmaker %>% 
  ggplot(aes(x=win_expectancy, y=n_goals_probability,color=factor(n_goals)))+
  geom_point()+
  geom_function(fun=g0,color='#F8766D')+
  geom_function(fun=g1,color='#C49A00')+
  geom_function(fun=g2,color='#53B400')+
  geom_function(fun=g3,color='#00C094')+
  geom_function(fun=g4,color='#00B6EB')+
  geom_function(fun=g5,color='#A58AFF')+
  labs(title = "My functions from Excel vs bookmaker probabilities",
       x = "Win expectancy",
       y = "Probability of scoring n goals")+
  guides(color=guide_legend(title="n goals:"))+
  scale_y_continuous(expand=c(0,0), limits = c(0,1))+
  scale_x_continuous(expand=c(0,0), limits = c(0,1), minor_breaks = seq(0,1,0.05))+
  theme_minimal()

x<-c(seq(0,1,0.001))

goals<-as.data.frame(x) %>% 
  mutate(g0=g0(x),
         g2=g2(x),
         g3=g3(x),
         g4=g4(x),
         g5=g5(x),
         g1=1-g0-g2-g3-g4-g5)

df <- gather(goals, key = n_goals, value = n_goals_prob, 
             c("g0","g1","g2","g3","g4","g5"))

df %>% 
  ggplot(aes(x=x, y=n_goals_prob, color=n_goals))+
  geom_line(size=1)+
  theme_minimal()+
  labs(title = "Win expectancy vs probabilty of scoring",
       x = "Win expectancy",
       y = "Probability of scoring n goals")+
  guides(color=guide_legend(title="n goals:"))+
  scale_y_continuous(expand=c(0,0), limits = c(0,1))+
  scale_x_continuous(expand=c(0,0), limits = c(0,1), minor_breaks = seq(0,1,0.05))+
  scale_color_discrete(labels=c("0","1","2","3","4","5"))

goals %>% 
  mutate(xG = g1+2*g2+3*g3+4*g4+5*g5) %>% 
  select(x, xG) %>% 
  ggplot(aes(x=x, y=xG))+
  geom_line(size=1)+
  scale_y_continuous(expand=c(0,0), limits = c(0,3), minor_breaks = seq(0,3,0.25))+
  scale_x_continuous(expand=c(0,0), limits = c(0,1), minor_breaks = seq(0,1,0.05))+
  theme_bw()+
  labs(title = "Expected number of goals for win expectancy",
       x = "Win expectancy",
       y = "Expected number of goals")

