-- run "source create_draft_stats.sql"

-- calculate how many picks per round in each year
create view picks
as
select
    year,
    max(pick) as picks
from
    draft
group by 1;


-- clean up positions in draft table
update draft set position = 'D' where position = 'Defender';
update draft set position = 'F' where position = 'Forward';
update draft set position = 'GK' where position in ('G', 'Goalkeeper');
update draft set position = 'M' where position = 'Midfielder';

-- manually fix positions some positions
-- use their most common position
update draft set position = 'M' where name = 'Chris Pontius';
update draft set position = 'M' where name = 'Ely Allen';
update draft set position = 'F' where name = 'Ryan Johnson';
update draft set position = 'M' where name = 'Greg Dalby';
update draft set position = 'D' where name = 'George John';
update draft set position = 'M' where name = 'Jeff Carroll';
update draft set position = 'F' where name = 'George Josten';
update draft set position = 'M' where name = 'Ryan Cordeiro';
update draft set position = 'M' where name = 'Danny Cruz';
update draft set position = 'M' where name = 'Dayton OBrien';
update draft set position = 'M' where name = 'Peter Lowry';

-- clean up club names
update draft set club = 'Chivas USA' where club = 'C.D. Chivas USA';
update draft set club = 'Columbus Crew' where club = 'Columbus Crew SC';
update draft set club = 'F.C. Dallas' where club = 'FC Dallas';










-- create draft stats table
drop view if exists draft_stats;
create view draft_stats
as
select
    d.*,
    (d.round-1) * picks.picks + d.pick as overall, 
    coalesce(sum(p.gp),0) as gp,
    coalesce(sum(p.gs),0) as gs,
    coalesce(sum(p.mins),0) as mins,
    coalesce(sum(goals),0) as goals,
    coalesce(sum(assists),0) as assists,
    coalesce(sum(shots),0) as shots,
    coalesce(sum(sog),0) as sog,
    coalesce(sum(gwg),0) as gwg,
    count(distinct p.mins) as years
from
    draft d
left join
    player_seasons p
on d.name=p.player
left join
    picks picks
on d.year=picks.year
group by 1,2,3,4,5,6,7,8;
