library(ggplot2)

setwd("~/Desktop/underdogs-and-inefficiencies")

d <- read.csv("upsets_data.csv", stringsAsFactor = FALSE)
str(d)

# overall
# under 15%
homeUnderdogs <- subset(d, homeWinProb < .15)
nrow(homeUnderdogs)
nrow(subset(homeUnderdogs, result == "H")) / nrow(homeUnderdogs)

awayUnderdogs <- subset(d, awayWinProb < .15)
nrow(awayUnderdogs)
nrow(subset(awayUnderdogs, result == "A")) / nrow(awayUnderdogs)

drawUnderdogs <- subset(d, drawProb < .15)
nrow(drawUnderdogs)
nrow(subset(drawUnderdogs, result == "D")) / nrow(drawUnderdogs)

home <- c()
away <- c()
draw <- c()
# by year
# 2014
h2014 <- subset(homeUnderdogs, year == 2014)
home <- c(home, nrow(subset(h2014, result == "H")) / nrow(h2014))
a2014 <- subset(awayUnderdogs, year == 2014)
away <- c(away, nrow(subset(a2014, result == "A")) / nrow(a2014))
d2014 <- subset(drawUnderdogs, year == 2014)
draw <- c(draw, nrow(subset(d2014, result == "D")) / nrow(d2014))

# 2013
h2013 <- subset(homeUnderdogs, year == 2013)
home <- c(home,nrow(subset(h2013, result == "H")) / nrow(h2013))
a2013 <- subset(awayUnderdogs, year == 2013)
away <- c(away,nrow(subset(a2013, result == "A")) / nrow(a2013))
d2013 <- subset(drawUnderdogs, year == 2013)
draw <- c(draw, nrow(subset(d2013, result == "D")) / nrow(d2013))

# 2012
h2012 <- subset(homeUnderdogs, year == 2012)
home <- c(home, nrow(subset(h2012, result == "H")) / nrow(h2012))
a2012 <- subset(awayUnderdogs, year == 2012)
away <- c(away, nrow(subset(a2012, result == "A")) / nrow(a2012))
d2012 <- subset(drawUnderdogs, year == 2012)
draw <- c(draw, nrow(subset(d2012, result == "D")) / nrow(d2012))

# 2011
h2011 <- subset(homeUnderdogs, year == 2011)
home <- c(home, nrow(subset(h2011, result == "H")) / nrow(h2011))
a2011 <- subset(awayUnderdogs, year == 2011)
away <- c(away, nrow(subset(a2011, result == "A")) / nrow(a2011))
d2011 <- subset(drawUnderdogs, year == 2011)
draw <- c(draw, nrow(subset(d2011, result == "D")) / nrow(d2011))

# 2010
h2010 <- subset(homeUnderdogs, year == 2010)
home <- c(home,nrow(subset(h2010, result == "H")) / nrow(h2010))
a2010 <- subset(awayUnderdogs, year == 2010)
away <- c(away, nrow(subset(a2010, result == "A")) / nrow(a2010))
d2010 <- subset(drawUnderdogs, year == 2010)
draw <- c(draw, nrow(subset(d2010, result == "D")) / nrow(d2010))

year <- c(2014, 2013, 2012, 2011, 2010)
year <- c(year, year, year)
prob <- c(home, away, draw)
underdog <- c(rep("home", 5), rep("away", 5), rep("draw", 5))
final <- as.data.frame(cbind(year, underdog, prob))
final$prob <- as.numeric(as.character(final$prob))

ggplot(data=final, aes(x=year, y=prob, group=underdog, colour=underdog)) + geom_line() + geom_point() + 
  ylab("% of underdog outcome occuring") + ggtitle("Significant Underdogs") + 
  geom_hline(aes(yintercept=.15), colour="#990000", linetype="dashed")

nrow(homeUnderdogs)
nrow(awayUnderdogs)
nrow(drawUnderdogs)
nrow(d)

