use soccer_stat;

create table game_stats
(
game_id			varchar(7)		primary key,
home_team_id	varchar(5),
away_team_id	varchar(5),
date			date,
local_time		time,
season_year		int(4),
home_score		smallint,
away_score		smallint,
attendance		int(6),
home_possession	decimal(2,2)
);

insert into game_stats values
('0000001', '001', '002', '2014-01-01', '13:00:00', 2014, 1, 0, 10000, .54);

select * from game_stats;