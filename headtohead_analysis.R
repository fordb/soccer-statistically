setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")

# read in data, strings are read as characters not factors
d <- read.csv("raw.csv", stringsAsFactor=FALSE)

# drop cases where teams have not played
# not really sure why these are in here in the first place,
# most likely on the website's end
d <- d[complete.cases(d),]

