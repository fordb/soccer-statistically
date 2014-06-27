library(plyr)

setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")
data <- read.csv("wc_2014_headtohead.csv", stringsAsFactors = FALSE)

data$c1 <- apply(data[,c(2,5)], 1, min)
data$c2 <- apply(data[,c(2,5)], 1, max)
data <- subset(data, c1 != c2)
breakdown <- ddply(data, .(c1, c2), summarize, 
                   gp = length(home), gf = sum(home_score), ga = sum(away_score))

breakdown$gf_game <- round(breakdown$gf / breakdown$gp,3)
breakdown$ga_game <- round(breakdown$ga / breakdown$gp,3)
