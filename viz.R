library(ggplot2)
library(reshape2)

setwd("~/Desktop/Soccer-Stat/wc-continent-headtohead")
data <- readRDS("breakdown.Rda")

# plotting Europe matchups
b <- subset(data, continent == "europe")
ggplot(data = b, aes(x=opposition_continent, y=gf_game)) + geom_bar(stat = "identity")
b <- melt(b)
b <- rbind(subset(b, variable=="gf_game"),subset(b, variable=="ga_game"))
ggplot(b, aes(x = opposition_continent)) + 
  geom_bar(data = subset(b, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(b, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Europe") + ylim(-2.5,2.5)
ggsave(file="europe.png")

# function to get the data in the correct format for graphing
subsetting <- function(cont) {
  t1 <- subset(data, continent == cont)
  t2 <- subset(data, opposition_continent == cont)
  t <- data.frame(continent = c(t1$continent, t2$opposition_continent), 
                  opposition_continent = c(t1$opposition_continent, t2$continent),
                  gf_game = c(t1$gf_game, t2$ga_game),
                  ga_game = c(t1$ga_game, t2$gf_game))
  t <- melt(t)
  return(t)
}

# do the same for CONCACAF
t <- subsetting("concacaf")
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("CONCACAF") + ylim(-3,3)
ggsave(file="concacaf.png")

# and africa
t <- subsetting("africa")
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Africa") + ylim(-3,3)
ggsave(file="africa.png")

# and asia
t <- subsetting("asia")
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Asia") + ylim(-3,3)
ggsave(file="asia.png")

# and oceania
t <- subsetting("oceania")
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("Oceania") + ylim(-3,3)
ggsave(file="oceania.png")

# and south america
t <- subsetting("southamerica")
ggplot(t, aes(x = opposition_continent)) + 
  geom_bar(data = subset(t, variable == "gf_game"), aes(y = value, fill = value), stat="identity") +
  geom_bar(data = subset(t, variable == "ga_game"), aes(y=-value, fill=-value), stat = "identity") +
  theme(legend.position = "none") + xlab("") + ylab("GA ---- GF") + 
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", midpoint = 0, space = "rgb") + 
  ggtitle("South America") + ylim(-3,3)
ggsave(file="southamerica.png")