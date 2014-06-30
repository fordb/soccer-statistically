# DATA NEEDS TO BE UPDATED FOR GAMES PAST 6/30 2PM

library(plyr)

setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")
data <- read.csv("wc_2014_headtohead.csv", stringsAsFactors = FALSE)

temp <- as.data.frame(model.matrix(home_score ~ result, data))
temp$"(Intercept)" <- NULL
temp$resultd <- ifelse(temp$resultl == 1, 0, ifelse(temp$resultw == 1, 0, 1))
data$win <- temp$resultw
data$draw <- temp$resultd
data$loss <- temp$resultl

data$c1 <- apply(data[,c(2,5)], 1, min)
data$c2 <- apply(data[,c(2,5)], 1, max)
data <- subset(data, c1 != c2)

d1 <- subset(data, home_continent == c1)
d2 <- subset(data, away_continent == c1)
d2[c(3,6)] = d2[c(6,3)]
d2[c(8,10)] = d2[c(10,8)]
data <- rbind(d1,d2)

breakdown <- ddply(data, .(c1, c2), summarize, 
                   gp = length(home), gf = sum(home_score), ga = sum(away_score),
                   wins = sum(win), draws = sum(draw), losses = sum(loss))

breakdown$gf_game <- round(breakdown$gf / breakdown$gp,3)
breakdown$ga_game <- round(breakdown$ga / breakdown$gp,3)

