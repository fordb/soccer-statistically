library(ggplot2)
library(grid)
library(jpeg)
library(RCurl)
library(hexbin)
library(dplyr)

setwd("~/git/soccer-statistically/etl/mls/mls_shots/")

d_2013 <- read.csv("shot_data_2013.csv", stringsAsFactors=FALSE)
d_2013$year <- 2013
d_2014 <- read.csv("shot_data_2014.csv", stringsAsFactors=FALSE)
d_2014$year <- 2014
d_2015 <- read.csv("shot_data_2015.csv", stringsAsFactors=FALSE)
d_2015$year <- 2015
d_2016 <- read.csv("shot_data_2016.csv", stringsAsFactors=FALSE)
d_2016$year <- 2016

d <- rbind(d_2013, d_2014, d_2015, d_2016)

d$outcome <- as.factor(d$outcome)

# full area: <rect x="2" y="2" width="74" height="58"/>
# percentages are based on these!

d$x_yd <- (d$x1 / 100) * 74
d$y_yd <- (d$y1 / 100) * 58

summary(d$x_yd)
summary(d$y_yd)

# simple plot using outcome to colour the dots
ggplot(d, aes(x=x_yd, y=y_yd)) +
  geom_point(aes(colour = outcome)) + 
  geom_hline(yintercept=58) + geom_hline(yintercept=0) +
  geom_vline(xintercept=0) + geom_vline(xintercept=74)

# some issues with y values for goals, all aove 90 and seem to be flipped...
# own goals?
# flip them
d[which(d$y_yd > 90), ]$y_yd <- 120 - d[which(d$y_yd > 90), ]$y_yd

# remove pks
pks <- subset(d, x_yd == 37 & y_yd == 13.340)
d <- subset(d, x_yd != 37 | y_yd != 13.340)

# remove shots from behind half
d <- subset(d, y_yd <= 58)


# that looks better!
ggplot(d, aes(x=x_yd, y=y_yd)) +
  geom_point(aes(colour = outcome)) + 
  geom_hline(yintercept=58) + geom_hline(yintercept=0) +
  geom_vline(xintercept=0) + geom_vline(xintercept=74)


# find a better diagram
field_url <- "https://s-media-cache-ak0.pinimg.com/736x/83/9b/95/839b958e458bf7c8623356d6d953fd08.jpg"
field <- rasterGrob(readJPEG(getURLContent(field_url)),
                    width=unit(1,"npc"), height=unit(1,"npc"))

plot_shots <- function(d) {
  p <- ggplot(d, aes(x=x_yd, y=y_yd)) + 
    annotation_custom(field, 0, 74, 0, 116) +
    #stat_binhex(bins = 80, colour = "gray", aes(alpha=..count..)) +
    stat_binhex(binwidth = c(2, 2), colour = "gray", aes(fill=..count.., alpha=..density..)) + # 2 yard by 2 yard hex
    scale_fill_gradientn(colours = c("yellow", "orange", "red")) +
    xlim(10, 66) +
    ylim(0, 58) +
    coord_fixed() +
    theme(line = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          axis.text.x = element_blank(),
          axis.text.y = element_blank(),
          legend.title = element_blank(),
          plot.title = element_blank())
  
  return(p)
}

plot_shots(d)

d$goal <- ifelse(d$outcome == 'goal', 1, 0)
shot_info <- d %>%
  group_by(team, year) %>%
  summarize(x1 = mean(x1), y1 = mean(y1),
            shots = length(game_id),
            goal_pct = sum(goal) / shots)

# best shooting pct
la_2016 <- subset(d, team=='LA' & year==2016)
# worst shooting pct
dc_2013  <- subset(d, team=='DC' & year==2013)

plot_shots(la_2016)
plot_shots(dc_2013)


# best 2016 team (regular season)
dal_2016 <- subset(d, team=='DAL' & year==2016)
# worst 2016 team (regular season)
chi_2016 <- subset(d, team=='CHI' & year==2016)

plot_shots(dal_2016)
plot_shots(chi_2016)

sum(dal_2016$goal)
sum(chi_2016$goal)


