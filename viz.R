library(ggplot2)
library(reshape2)

setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")
data <- readRDS("breakdown.Rda")
data2014 <- readRDS("wc2014_breakdown.Rda")

# reformat a little
data <- data[c("continent","opposition_continent","gf_game","ga_game")]
data2014 <- data2014[c("home_continent","away_continent","gf_game","ga_game")]
names(data2014) <- names(data)
data2014$continent <- as.character(lapply(data2014$continent, function(x) gsub(" ", "", tolower(x))))
data2014$opposition_continent <- as.character(lapply(data2014$opposition_continent, function(x) gsub(" ", "", tolower(x))))


# function to get the data in the correct format for graphing gf vs. ga
subsetting <- function(cont,d) {
  t1 <- subset(d, continent == cont)
  t2 <- subset(d, opposition_continent == cont)
  t <- data.frame(continent = c(t1$continent, t2$opposition_continent), 
                  opposition_continent = c(t1$opposition_continent, t2$continent),
                  gf_game = c(t1$gf_game, t2$ga_game),
                  ga_game = c(t1$ga_game, t2$gf_game))
  t <- melt(t)
  return(t)
}

# function to get the data in the correct format for graphs comparing 2014 to past data
for_comparison <- function(cont) {
  d1 <- subsetting(cont, data2014)
  d1$fill <- "2014"
  d1_opps <- unique(d1$opposition_continent)
  d2 <- subsetting(cont, data)
  d2 <- subset(d2, opposition_continent %in% d1_opps)
  d2$fill <- "Past"
  m <- rbind(d1, d2)
}


### get gf/ga graphs ###
# Europe
t <- subsetting("europe",data)
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Europe") + ylim(-3,3)
ggsave(file="europe.png")

# do the same for CONCACAF
t <- subsetting("concacaf",data)
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("CONCACAF") + ylim(-3,3)
ggsave(file="concacaf.png")

# and africa
t <- subsetting("africa",data)
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Africa") + ylim(-3,3)
ggsave(file="africa.png")

# and asia
t <- subsetting("asia",data)
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Asia") + ylim(-3,3)
ggsave(file="asia.png")

# and oceania
t <- subsetting("oceania",data)
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Oceania") + ylim(-3,3)
ggsave(file="oceania.png")

# and south america
t <- subsetting("southamerica",data)
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("South America") + ylim(-3,3)
ggsave(file="southamerica.png")


### comparisons to current world cup
# europe
m <- for_comparison("europe")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ggtitle("Europe -- GF/Game")
ggsave(file="europe_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ggtitle("Europe -- GA/Game")
ggsave(file="europe_ga.png")

# concacaf
m <- for_comparison("concacaf")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("CONCACAF -- GF/Game")
ggsave(file="concacaf_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("CONCACAF -- GA/Game")
ggsave(file="concacaf_ga.png")

# africa
m <- for_comparison("africa")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("Africa -- GF/Game")
ggsave(file="africa_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("Africa -- GA/Game")
ggsave(file="africa_ga.png")

# asia
m <- for_comparison("asia")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("Asia -- GF/Game")
ggsave(file="asia_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("Asia -- GA/Game")
ggsave(file="asia_ga.png")


# south america
m <- for_comparison("southamerica")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("South America -- GF/Game")
ggsave(file="southamerica_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("South America -- GA/Game")
ggsave(file="asouthamerica_ga.png")

