library(dplyr)
library(ggplot2)
library(reshape2)

###
### get data and clean it
###

setwd("~/Desktop/Soccer-Stat/database_gen/mls_draft/")
d <- read.csv("draft_stats.csv", stringsAsFactors=FALSE, header=FALSE)

names(d) <- c("year", "round", "pick", "club", "name", "position", "affiliation",
              "overall", "gp", "gs", "mins", "goals", "assists", "shots",
              "sog", "gwg", "years")
# only look at draft performance since 2011
d <- subset(d, year < 2012)

# create per year metrics
d$mins_year <- d$mins / d$years
d[which(is.na(d$mins_year)), ]$mins_year <- 0
d$goals_year <- d$goals / d$years
d[which(is.na(d$goals_year)), ]$goals_year <- 0

str(d)
ordered <- d[order(d$overall),]


###
### performance by club and by round
###

clubs <- d %>%
  group_by(club) %>%
  summarize(gp = sum(gp)/sum(years),
            mins = sum(mins)/sum(years),
            goals = sum(goals)/sum(years),
            years = sum(years)/length(name),
            picks = length(name))
clubs <- clubs[order(-clubs$years),]

rounds <- d %>%
  group_by(round, position) %>%
  summarize(gp = sum(gp)/sum(years),
            mins = sum(mins)/sum(years),
            goals = sum(goals)/sum(years),
            picks = length(name))


###
### "success" threshold
###

# threshold 1
summary(d$mins_year) # below the median of 150 minutes per year
# i.e. playing about 5 minutes per game on average
ggplot(d, aes(x=mins_year)) + geom_density() + geom_vline(xintercept=150, color="red")

# threshold 2
# use the visual kink in the graph at 400
ggplot(d, aes(x=mins_year)) + geom_density() + geom_vline(xintercept=400, color="red")

threshold <- 150
threshold <- 400
ggplot(subset(d, round==1), aes(x=mins_year)) + geom_density()
nrow(subset(subset(d, round==1), mins_year>=threshold)) / nrow(subset(d, round==1))
ggplot(subset(d, round==2), aes(x=mins_year)) + geom_density()
nrow(subset(subset(d, round==2), mins_year>=threshold)) / nrow(subset(d, round==2))
ggplot(subset(d, round==3), aes(x=mins_year)) + geom_density()
nrow(subset(subset(d, round==3), mins_year>=threshold)) / nrow(subset(d, round==3))
ggplot(subset(d, round==4), aes(x=mins_year)) + geom_density()
nrow(subset(subset(d, round==4), mins_year>=threshold)) / nrow(subset(d, round==4))
ggplot(subset(d, round==5), aes(x=mins_year)) + geom_density()
nrow(subset(subset(d, round==5), mins_year>=threshold)) / nrow(subset(d, round==5))
ggplot(subset(d, round==6), aes(x=mins_year)) + geom_density()
nrow(subset(subset(d, round==6), mins_year>=threshold)) / nrow(subset(d, round==6))


###
### model statistics by pick #
###

# minutes vs pick
ggplot(d, aes(x=overall, y=mins)) + geom_point() + geom_smooth()
lo_mins_picks <- loess(d$mins ~ d$overall)
predict(lo_mins_picks, 12)
minutes_picks <- data.frame(overall=1:75)
minutes_picks$pred <- predict(lo_mins_picks, minutes_picks$overall)
lo_mins_picks <- loess(d$mins ~ d$overall)
predict(lo_mins_picks, 12)
minutes_picks <- data.frame(overall=1:75)
minutes_picks$pred <- predict(lo_mins_picks, minutes_picks$overall)
ggplot(subset(d, round<4), aes(x=mins, color=as.factor(round))) + geom_density() + xlim(0,20000) + ylim(0, .0005)

# goals vs pick (midfielders and forwards only)
ggplot(subset(d, position %in% c("M", "F")), aes(x=overall, y=goals)) +
  geom_point() + geom_smooth(method="loess")
mf <- subset(d, position %in% c("M", "F"))
lo_goals <- loess(mf$goals ~ mf$overall)
goals <- data.frame(overall=1:75)
goals$pred <- predict(lo_goals, goals$overall)

# minutes vs pick # (keepers only)
ggplot(subset(d, position=="GK"), aes(x=overall, y=mins)) +
  geom_point() + geom_smooth(method="loess") + ylim(0,4000)
ggplot(subset(d, position=="GK"), aes(x=overall, y=mins_year)) +
  geom_point() + geom_smooth(method="loess") + ylim(0,4000) +
  geom_abline(intercept=1000, slope=0, color="red")


###
### trade examples
###

# 1st overall for 11th and 18th overall
minutes_picks$pred[1]
minutes_picks$pred[11] + minutes_picks$pred[18]
# 5th overall offensive player for 13th and 25th overall offensive player
goals$pred[5]
goals$pred[13] + goals$pred[25]


