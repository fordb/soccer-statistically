library(plyr)

setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")

# read in data, strings are read as characters not factors
d <- read.csv("raw.csv", stringsAsFactor=FALSE)

# drop cases where teams have not played
# not really sure why these are in here in the first place,
# most likely on the website's end
d <- d[complete.cases(d),]

# fix some faulty continent labels
fix_continents <- function(c, cont) {
  t1 <- subset(d, country == c)
  t1$continent <- cont
  t2 <- subset(d, opposition == c)
  if(nrow(t2) > 0) {
    t2$opposition_continent <- cont
    t <- rbind(t1, t2)
  } else {
    t <- t1
  }
  d1 <- subset(subset(d, country != c), opposition != c)
  d1 <- rbind(d1, t)
  return(d1)
}

# countries with faulty continent labels
# do this by hand
sort_d <- d[order(d$country),]
# australia, saudi-arabia, kazakhstan
d <- fix_continents("saudi-arabia", "asia")
d <- fix_continents("australia", "oceania")
d <- fix_continents("kazakhstan", "asia")

# remove intra-continent games
d <- subset(d, continent != opposition_continent)

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

