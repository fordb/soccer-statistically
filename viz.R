3


### comparisons to current world cup

# europe
m <- for_comparison("europe")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("Europe -- GF/Game")
ggsave(file="europe_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ggtitle("Europe -- GA/Game")
ggsave(file="europe_ga.png")

# concacaf
m <- for_comparison("concacaf")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("CONCACAF -- GF/Game")
ggsave(file="concacaf_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("CONCACAF -- GA/Game")
ggsave(file="concacaf_ga.png")

# africa
m <- for_comparison("africa")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("Africa -- GF/Game")
ggsave(file="africa_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("Africa -- GA/Game")
ggsave(file="africa_ga.png")

# asia
m <- for_comparison("asia")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("Asia -- GF/Game")
ggsave(file="asia_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("Asia -- GA/Game")
ggsave(file="asia_ga.png")


# south america
m <- for_comparison("southamerica")
# goals for
ggplot(subset(m, variable=="gf_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("South America -- GF/Game")
ggsave(file="southamerica_gf.png")
# goals against
ggplot(subset(m, variable=="ga_game"), aes(x = opposition_continent, y = value, fill = fill)) + 
  geom_bar(stat="identity",position="dodge") + ylim(0,3) + ylim(0,3) + ggtitle("South America -- GA/Game")
ggsave(file="asouthamerica_ga.png")
