library(plyr)

setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")

# read in data, strings are read as characters not factors
d <- read.csv("raw.csv", stringsAsFactor=FALSE)

# drop cases where teams have not played
# not really sure why these are in here in the first place,
# most likely on the website's end
d <- d[complete.cases(d),]

countries <- unique(d$country)
d <- subset(d, opposition %in% countries)

# remove intra-continent games
d <- subset(d, continent != opposition_continent)
subset(subset(d, country == "algeria"), opposition == "bulgaria")
subset(subset(d, country == "bulgaria"), opposition == "algeria")

# remove duplicate games
# first make unique key for matchups
d$key1 <- paste(d$country, d$opposition, sep="_")
d$key2 <- paste(d$opposition, d$country, sep="_")
d$key <- apply(cbind(d$key1, d$key2),1,min)
d$key2 <- NULL

# remove non-duplicate games
id.table <- table(d$key)
d <- subset(d, key %in% names(id.table[id.table > 1]))
d <- d[duplicated(d$key),]


# clean up variables to make the key
d$key <- d$key1 <- NULL

# analyze
breakdown <- ddply(d, .(continent, opposition_continent), summarize, 
                   gp = sum(played), wins = sum(wins), draws = sum(draws),
                   losses = sum(losses), gf = sum(gf), ga = sum(ga))
