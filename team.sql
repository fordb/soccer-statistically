-- create team table

use soccer_stat;

show tables;

drop table team;

create table team
(
team_id			varchar(5)		primary key,
league_id		varchar(3),
short_name		varchar(4),
long_name		varchar(30),
city			varchar(30),
foreign key (league_id) references league(league_id));

insert into team values
('00001', '001', 'REV', 'New England Revolution', 'Boston');

insert into team values
('00002', '001', 'NYR', 'New York Red Bulls', 'New York');


select
	t.long_name,
    l.long_name
from team t, league l
where t.league_id = l.league_id;
