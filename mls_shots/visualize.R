library(ggplot2)

setwd("~/Desktop/Soccer-Stat/database_gen/mls_shots/")

d <- read.csv("data.csv", stringsAsFactors=FALSE)

d$outcome <- as.factor(d$outcome)

colorado <- subset(d, team=="Toronto FC")
ggplot(colorado, aes(x=x1, y=y1, color=outcome)) + geom_point() + xlim(0,100) + ylim(0,100) + 
  geom_segment(aes(x=21.1, y=33.4, xend=78.9, yend=33.4),colour="red") +
  geom_segment(aes(x=36.8, y=11.1, xend=63.2, yend=11.1),colour="red") + 
  geom_segment(aes(x=21.1, y=33.4, xend=21.1, yend=0),colour="red") + 
  geom_segment(aes(x=78.9, y=33.4, xend=78.9, yend=0),colour="red") +
  geom_segment(aes(x=36.8, y=11,1, xend=36.8, yend=0),colour="red") + 
  geom_segment(aes(x=63.2, y=11.1, xend=63.2, yend=0),colour="red") +
  geom_point(size=3, alpha=1)


diff <- 5
x_tile <- seq(0,100-diff/2,diff)
y_tile <- seq(diff/2,100-diff/2,diff)

tiles <- expand.grid(x_tile=x_tile, y_tile=y_tile)
tiles <- subset(tiles, x_tile!=50 | y_tile!=22.5)

match_tiles <- function(x, y) {
  return(nrow(subset(d, x1>x & x1<x+diff & y1>y & y1<y+diff)))
}


tiles$count <- mapply(match_tiles, tiles$x_tile, tiles$y_tile)
str(tiles)

ggplot(tiles, aes(x=x_tile, y=y_tile)) + geom_tile(aes(fill=count)) +
  scale_fill_gradient(low="red", high="yellow") + 
  geom_segment(aes(x=21.1, y=33.4, xend=78.9, yend=33.4),colour="white") +
  geom_segment(aes(x=36.8, y=11.1, xend=63.2, yend=11.1),colour="white") + 
  geom_segment(aes(x=21.1, y=33.4, xend=21.1, yend=0),colour="white") + 
  geom_segment(aes(x=78.9, y=33.4, xend=78.9, yend=0),colour="white") +
  geom_segment(aes(x=36.8, y=11,1, xend=36.8, yend=0),colour="white") + 
  geom_segment(aes(x=63.2, y=11.1, xend=63.2, yend=0),colour="white")

