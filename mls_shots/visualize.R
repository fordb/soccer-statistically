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

match_tiles_shots <- function(x, y) {
  return(nrow(subset(d, x1>x & x1<x+diff & y1>y & y1<y+diff)))
}

match_tiles_goals <- function(x, y) {
  return(nrow(subset(d, x1>x & x1<x+diff & y1>y & y1<y+diff & outcome=="goal")))
}


tiles$shots <- mapply(match_tiles_shots, tiles$x_tile, tiles$y_tile)
tiles$goals <- mapply(match_tiles_goals, tiles$x_tile, tiles$y_tile)
tiles$pct <- tiles$goals/tiles$shots

tiles[which(tiles$shots<3),]$pct <- 0.0

ggplot(tiles, aes(x=x_tile, y=y_tile)) + geom_tile(aes(fill=pct)) +
  scale_fill_gradient(low="red", high="yellow") + 
  geom_segment(aes(x=21.1, y=33.4, xend=78.9, yend=33.4),colour="black") +
  geom_segment(aes(x=36.8, y=11.1, xend=63.2, yend=11.1),colour="black") + 
  geom_segment(aes(x=21.1, y=33.4, xend=21.1, yend=0),colour="black") + 
  geom_segment(aes(x=78.9, y=33.4, xend=78.9, yend=0),colour="black") +
  geom_segment(aes(x=36.8, y=11,1, xend=36.8, yend=0),colour="black") + 
  geom_segment(aes(x=63.2, y=11.1, xend=63.2, yend=0),colour="black")

