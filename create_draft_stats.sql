-- run "source create_draft_stats.sql"

create view picks
as
select
    year,
    max(pick) as picks
from
    draft
group by 1;



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
