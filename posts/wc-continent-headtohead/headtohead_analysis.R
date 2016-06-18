# data includes all world cup matches INCLUDING qualifying games
# hence the high number of games between oceania and asia

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

# remove intra-continent games
d <- subset(d, continent != opposition_continent)

# clean up variables that made the key
d$key <- d$key1 <- NULL
# switch rows with continent = oceania to opposition_continent = oceania
temp1 <- subset(d, continent == "oceania")
temp1$tcontinent <- temp1$opposition_continent
temp1$topposition_continent <- temp1$continent
temp1$continent <- temp1$tcontinent
temp1$opposition_continent <- temp1$topposition_continent
temp1$topposition_continent <- temp1$tcontinent <- NULL
d <- subset(d, continent != "oceania")
d <- rbind(d, temp1)

# analysis
breakdown <- ddply(d, .(continent, opposition_continent), summarize, 
                   gp = sum(played), wins = sum(wins), draws = sum(draws),
                   losses = sum(losses), gf = sum(gf), ga = sum(ga))
# clean up extraneous dataframes
rm(id.table, sort_d, temp1)

# create some new variables
breakdown <- breakdown[order(-breakdown$gp),]
breakdown$gf_game <- round(breakdown$gf / breakdown$gp,3)
breakdown$ga_game <- round(breakdown$ga / breakdown$gp,3)
breakdown$win_pct <- round((breakdown$wins / breakdown$gp) + (1/3)*(breakdown$draws / breakdown$gp),3)
breakdown$matchup <- paste(breakdown$continent, breakdown$opposition_continent, sep = " v ")
# save data
saveRDS(breakdown, file = "breakdown.Rda")
