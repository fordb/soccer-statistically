use soccer_stat;

drop table goals;

create table goals
(
game_id			varchar(7),
player_id		varchar(7),
minute			tinyint,
second			tinyint,
assist			varchar(7)
);

insert into goals values
('0000001', '0000001', 65, 21, '0000002');

