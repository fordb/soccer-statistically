use soccer_stat;

drop table player;

create table player
(
player_id			varchar(7)		primary key,
first_name			varchar(25),
last_name			varchar(25),
dob					date,
country				varchar(25),
position			varchar(4)
);

insert into player values
('0000001', 'Teal', 'Bunbury', '1990-02-27', 'Canada', 'FW');

insert into player values
('0000002', 'Lee', 'Nguyen', '1986-10-07', 'USA', 'MF');

