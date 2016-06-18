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
  summarize(gp = round(sum(gp)/sum(years),2),
            mins = round(sum(mins)/sum(years),2),
            goals = round(sum(goals)/sum(years),2),
            years = round(sum(years)/length(name),2),
            picks = length(name))
clubs <- clubs[order(-clubs$mins),]
write.csv(clubs, 'graphs/table1.csv', row.names=FALSE)

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
ggplot(d, aes(x=mins_year)) + geom_density() + geom_vline(xintercept=150, color="red") + 
  xlab("Minutes Per Year") + ylab("Density") + ggtitle("Density Plot of Minutes Per Year") + 
  annotate("text", x = 1000, y = .0010, label = "Median = 150 minutes")
ggsave('graphs/plot1.png', last_plot())

# threshold 2
# use the visual kink in the graph at 400
ggplot(d, aes(x=mins_year)) + geom_density() + geom_vline(xintercept=400, color="red") +
  xlab("Minutes Per Year") + ylab("Density") + ggtitle("Density Plot of Minutes Per Year") + 
  annotate("text", x = 1200, y = .0010, label = "Threshold = 400 minutes")
ggsave('graphs/plot2.png', last_plot())


rounds <- 1:6
threshold <- 150
ggplot(subset(d, round==1), aes(x=mins_year)) + geom_density()
r1 <- nrow(subset(subset(d, round==1), mins_year>=threshold)) / nrow(subset(d, round==1))
ggplot(subset(d, round==2), aes(x=mins_year)) + geom_density()
r2 <- nrow(subset(subset(d, round==2), mins_year>=threshold)) / nrow(subset(d, round==2))
ggplot(subset(d, round==3), aes(x=mins_year)) + geom_density()
r3 <- nrow(subset(subset(d, round==3), mins_year>=threshold)) / nrow(subset(d, round==3))
ggplot(subset(d, round==4), aes(x=mins_year)) + geom_density()
r4 <- nrow(subset(subset(d, round==4), mins_year>=threshold)) / nrow(subset(d, round==4))
ggplot(subset(d, round==5), aes(x=mins_year)) + geom_density()
r5 <- nrow(subset(subset(d, round==5), mins_year>=threshold)) / nrow(subset(d, round==5))
ggplot(subset(d, round==6), aes(x=mins_year)) + geom_density()
r6 <- nrow(subset(subset(d, round==6), mins_year>=threshold)) / nrow(subset(d, round==6))
thresh150 <- data.frame(rounds=rounds, success_proportion=c(r1, r2, r3, r4, r5, r6))
thresh150$success_proportion <- round(thresh150$success_proportion,3)
write.csv(thresh150, 'graphs/table2.csv', row.names=FALSE)

threshold <- 400
ggplot(subset(d, round==1), aes(x=mins_year)) + geom_density()
r1 <- nrow(subset(subset(d, round==1), mins_year>=threshold)) / nrow(subset(d, round==1))
ggplot(subset(d, round==2), aes(x=mins_year)) + geom_density()
r2 <- nrow(subset(subset(d, round==2), mins_year>=threshold)) / nrow(subset(d, round==2))
ggplot(subset(d, round==3), aes(x=mins_year)) + geom_density()
r3 <- nrow(subset(subset(d, round==3), mins_year>=threshold)) / nrow(subset(d, round==3))
ggplot(subset(d, round==4), aes(x=mins_year)) + geom_density()
r4 <- nrow(subset(subset(d, round==4), mins_year>=threshold)) / nrow(subset(d, round==4))
ggplot(subset(d, round==5), aes(x=mins_year)) + geom_density()
r5 <- nrow(subset(subset(d, round==5), mins_year>=threshold)) / nrow(subset(d, round==5))
ggplot(subset(d, round==6), aes(x=mins_year)) + geom_density()
r6 <- nrow(subset(subset(d, round==6), mins_year>=threshold)) / nrow(subset(d, round==6))
thresh400 <- data.frame(rounds=rounds, success_proportion=c(r1, r2, r3, r4, r5, r6))
thresh400$success_proportion <- round(thresh400$success_proportion,3)
write.csv(thresh400, 'graphs/table3.csv', row.names=FALSE)

###
### model statistics by pick #
###

# minutes vs pick
ggplot(d, aes(x=overall, y=mins)) + geom_point() + geom_smooth(method="loess", se=FALSE) +
  xlab("Pick Number") + ylab("Minutes") + ggtitle("Pick Number vs. Minutes")
ggsave('graphs/plot3.png', last_plot())
lo_mins_picks <- loess(d$mins ~ d$overall)
predict(lo_mins_picks, 12)
minutes_picks <- data.frame(overall=1:75)
minutes_picks$expected_minutes <- predict(lo_mins_picks, minutes_picks$overall)
write.csv(minutes_picks, 'graphs/csv1.csv', row.names=FALSE)
ggplot(subset(d, round<4), aes(x=mins, color=as.factor(round))) + geom_density() + xlim(0,20000) + ylim(0, .0005)

# goals vs pick (midfielders and forwards only)
ggplot(subset(d, position %in% c("M", "F")), aes(x=overall, y=goals)) +
  geom_point() + geom_smooth(method="loess", se=FALSE) + xlab("Pick Number") +
  ylab("Goals") + ggtitle("Pick Number vs. Goals (MF and F only)")
ggsave('graphs/plot4.png', last_plot())

mf <- subset(d, position %in% c("M", "F"))
lo_goals <- loess(mf$goals ~ mf$overall)
goals <- data.frame(overall=1:75)
goals$expected_goals <- predict(lo_goals, goals$overall)
write.csv(goals, 'graphs/csv2.csv', row.names=FALSE)

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
minutes_picks$pred[15]
# 5th overall offensive player for 13th and 25th overall offensive player
goals$pred[5]
goals$pred[13]
goals$pred[25]


