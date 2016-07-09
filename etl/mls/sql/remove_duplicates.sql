-- remove duplciates from club_seasons table
delete
    club1
from
    club_seasons club1,
    club_seasons club2
where
    club1.batch > club1.batch and
    club1.club = club2.club and
    club1.year = club2.year and
    club1.type = club2.type and
    club1.gp = club2.gp and
    club1.goals = club2.goals and
    club1.shots = club2.shots and
    club1.sog = club2.sog and
    club1.fc = club2.fc and
    club1.fs = club2.fs and
    club1.offsides = club2.offsides and
    club1.corners = club2.corners and
    club1.pkg = club2.pkg and
    club1.pka = club2.pka;

-- remove duplciates from player_seasons table
delete
    player1
from
    player_seasons player1,
    player_seasons player2
where
    player1.batch > player1.batch and
    player1.player = player2.player and
    player1.year = player2.year and
    player1.type = player2.type and
    player1.position = player2.position and
    player1.gp = player2.gp and
    player1.gs = player2.gs and
    player1.mins = player2.mins and
    player1.goals = player2.goals and
    player1.assists = player2.assists and
    player1.shots = player2.shots and
    player1.sog = player2.sog and
    player1.pkg_a = player2.pkg_a and
    player1.home_goals = player2.home_goals and
    player1.away_goals = player2.away_goals and
    player1.gp_90 = player2.gp_90 and
    player1.scoring_pct = player2.scoring_pct;
