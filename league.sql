use soccer_stat;

show tables;

drop table league;

create table league
(
league_id		varchar(3)		not null		primary key,
short_name		varchar(5)		not null,
long_name		varchar(30)		not null,
country			varchar(30)		not null,
points_for_win	integer(1)		not null,
points_for_draw	integer(1)		not null
);

show tables;

insert into league values
('001', 'MLS', 'Major League Soccer', 'USA', 3, 1);

insert into league values
('002', 'EPL', 'Barclays Premier League', 'England', 3, 1);

select * from league;