import MySQLdb
import sys
from bs4 import BeautifulSoup
import urllib2
import datetime

db = MySQLdb.connect(host="localhost", user="root", db="soccer_stat")
cur = db.cursor()

proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)

player_dict = {}
club_dict = {}
league_dict = {}

player_counter = 1
club_counter = 1
league_counter = 1


def create_club_seasons():
    cur.execute('drop table if exists club_seasons;')
    create_table = """
        create table club_seasons (
            club_id int,
            year int,
            type varchar(10),
            gp int,
            goals int,
            assists int,
            shots int,
            sog int,
            fc int,
            fs int,
            offsides int,
            corners int,
            pkg int,
            pka int,
            unique key team_year (club_id, year, type));
    """
    cur.execute(create_table)


def club_regular_seasons(y):
    print >>sys.stderr, '[{time}] Scraping regular season teams year {y}...'.format(
        time=datetime.datetime.now(), y=y)
    url = 'http://www.mlssoccer.com/stats/team?season_year={year}&season_type=REG&op=Search&form_id=mls_stats_team_form'.format(year=y)
    page = opener.open(url).read()
    soup = BeautifulSoup(page)
    length = len(soup.find('tbody').findAll('td'))
    for row in range(0, length, 12):
        club = soup.find('tbody').findAll(
            'td', attrs={'class': 'club-col'})[row/12].contents[0]
        gp = soup.find('tbody').findAll('td')[row+1].contents[0]
        goals = soup.find('tbody').findAll('td')[row+2].contents[0]
        assists = soup.find('tbody').findAll('td')[row+3].contents[0]
        shots = soup.find('tbody').findAll('td')[row+4].contents[0]
        sog = soup.find('tbody').findAll('td')[row+5].contents[0]
        fc = soup.find('tbody').findAll('td')[row+6].contents[0]
        fs = soup.find('tbody').findAll('td')[row+7].contents[0]
        offsides = soup.find('tbody').findAll('td')[row+8].contents[0]
        corners = soup.find('tbody').findAll('td')[row+9].contents[0]
        pkg = soup.find('tbody').findAll('td')[row+10].contents[0]
        pka = soup.find('tbody').findAll('td')[row+11].contents[0]
        global club_counter
        c_id = club_counter
        club_counter += 1

        club_dict[club.lower().replace(" ", "").replace(".", "")] = c_id

        insert_club_data = """
            insert ignore into clubs
                (club_id, name, city, league_id)
                values (
                    {c_id},
                    '{club}',
                    NULL,
                    {l_id})
        """.format(c_id=c_id, club=club, l_id=league_dict['MLS'])
        cur.execute(insert_club_data)

        insert_data = """
            insert ignore into club_seasons
                (club_id, year, type, gp, goals, assists, shots, sog, fc, fs, offsides, corners, pkg, pka)
                values (
                    {id},
                    {year},
                    'regular',
                    {gp},
                    {goals},
                    {assists},
                    {shots},
                    {sog},
                    {fc},
                    {fs},
                    {offsides},
                    {corners},
                    {pkg},
                    {pka}
                    );
        """.format(id=c_id, year=y, gp=gp, goals=goals, assists=assists, shots=shots,
                   sog=sog, fc=fc, fs=fs, offsides=offsides, corners=corners,
                   pkg=pkg, pka=pka)
        cur.execute(insert_data)


def club_post_seasons(y):
    print >>sys.stderr, '[{time}] Scraping postseason teams year {y}...'.format(
        time=datetime.datetime.now(), y=y)
    url = 'http://www.mlssoccer.com/stats/team?season_year={year}&season_type=PS&op=Search&form_id=mls_stats_team_form'.format(year=y)
    page = opener.open(url).read()
    soup = BeautifulSoup(page)
    length = len(soup.find('tbody').findAll('td'))
    for row in range(0, length, 12):
        club = soup.find('tbody').findAll('td', attrs={'class': 'club-col'})[row/12].contents[0]
        gp = soup.find('tbody').findAll('td')[row+1].contents[0]
        goals = soup.find('tbody').findAll('td')[row+2].contents[0]
        assists = soup.find('tbody').findAll('td')[row+3].contents[0]
        shots = soup.find('tbody').findAll('td')[row+4].contents[0]
        sog = soup.find('tbody').findAll('td')[row+5].contents[0]
        fc = soup.find('tbody').findAll('td')[row+6].contents[0]
        fs = soup.find('tbody').findAll('td')[row+7].contents[0]
        offsides = soup.find('tbody').findAll('td')[row+8].contents[0]
        corners = soup.find('tbody').findAll('td')[row+9].contents[0]
        pkg = soup.find('tbody').findAll('td')[row+10].contents[0]
        pka = soup.find('tbody').findAll('td')[row+11].contents[0]
        c_id = club_dict[club.lower().replace(" ", "").replace(".", "")]

        insert_data = """
                insert ignore into club_seasons
                    (club_id, year, type, gp, goals, assists, shots, sog, fc, fs, offsides, corners, pkg, pka)
                    values (
                        {c_id},
                        {year},
                        'post',
                        {gp},
                        {goals},
                        {assists},
                        {shots},
                        {sog},
                        {fc},
                        {fs},
                        {offsides},
                        {corners},
                        {pkg},
                        {pka}
                        );
        """.format(c_id=c_id, year=y, gp=gp, goals=goals, assists=assists, shots=shots,
                   sog=sog, fc=fc, fs=fs, offsides=offsides, corners=corners, pkg=pkg,
                   pka=pka)
        cur.execute(insert_data)


def create_player_seasons():
    cur.execute('drop table if exists player_seasons;')
    create_table = """
        create table player_seasons (
            player varchar(30),
            year int,
            type varchar(10),
            position varchar(10),
            gp int,
            gs int,
            mins int,
            goals int,
            assists int,
            shots int,
            sog int,
            gwg int,
            pkg_a varchar(10),
            home_goals int,
            away_goals int,
            gp_90 decimal(4,2),
            scoring_pct decimal(4,1),
            unique key player_year (player, year));
    """
    cur.execute(create_table)


def player_regular_seasons(y):
    print >>sys.stderr, '[{time}] Scraping regular season year {y}...'.format(
        time=datetime.datetime.now(), y=y)
    # regular season field players
    first_name = None
    for p in range(50):
        url = 'http://www.mlssoccer.com/stats/season?sort=desc&order=SC%25&page={num}&season_year={year}&season_type=REG&team=ALL&group=GOALS&op=Search&form_id=mls_stats_individual_form'.format(num=p, year=y)
        page = opener.open(url).read()
        soup = BeautifulSoup(page)
        temp_name = None
        print >>sys.stderr, '[{time}] Running page {n}...'.format(
            time=datetime.datetime.now(), n=p)
        for row in range(0, 400, 16):
            name = soup.find('tbody').findAll('a')[(row/15)-1].contents[0]
            name = name.replace("'", "")
            if first_name == name:
                break
            if row == 0:
                first_name = name
            club = soup.find('tbody').findAll('td')[row+1].contents[0]
            pos = soup.find('tbody').findAll('td')[row+2].contents[0]
            gp = soup.find('tbody').findAll('td')[row+3].contents[0]
            gs = soup.find('tbody').findAll('td')[row+4].contents[0]
            mins = soup.find('tbody').findAll('td')[row+5].contents[0]
            goals = soup.find('tbody').findAll('td')[row+6].contents[0]
            assists = soup.find('tbody').findAll('td')[row+7].contents[0]
            shots = soup.find('tbody').findAll('td')[row+8].contents[0]
            sog = soup.find('tbody').findAll('td')[row+9].contents[0]
            gwg = soup.find('tbody').findAll('td')[row+10].contents[0]
            pkg_a = soup.find('tbody').findAll('td')[row+11].contents[0]
            home_goals = soup.find('tbody').findAll('td')[row+12].contents[0]
            away_goals = soup.find('tbody').findAll('td')[row+13].contents[0]
            gp90 = soup.find('tbody').findAll('td')[row+14].contents[0]
            scoring_pct = soup.find('tbody').findAll('td')[row+15].contents[0]
            temp_name = name

            insert_data = """
                    insert ignore into player_seasons
                        (player, year, type, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct)
                        values (
                            '{player}',
                            {year},
                            'regular',
                            '{pos}',
                            {gp},
                            {gs},
                            {mins},
                            {goals},
                            {assists},
                            {shots},
                            {sog},
                            {gwg},
                            '{pkg_a}',
                            {home_goals},
                            {away_goals},
                            {gp90},
                            {scoring_pct}
                            );
            """.format(player=name, year=y, club=club, pos=pos, gp=gp, gs=gs, mins=mins,
                       goals=goals, assists=assists, shots=shots, sog=sog, gwg=gwg,
                       pkg_a=pkg_a, home_goals=home_goals, away_goals=away_goals,
                       gp90=gp90, scoring_pct=scoring_pct)
            cur.execute(insert_data)
        if temp_name is None:
            break


def player_post_seasons(y):
    print >>sys.stderr, '[{time}] Scraping playoffs year {y}...'.format(
        time=datetime.datetime.now(), y=y)
    # playoff field players
    url = 'http://www.mlssoccer.com/stats/season?season_year={year}&season_type=PS&team=ALL&group=GOALS&op=Search&form_id=mls_stats_individual_form'.format(year=y)
    page = opener.open(url).read()
    soup = BeautifulSoup(page)
    length = len(soup.find('tbody').findAll('td'))
    for row in range(0, length, 15):
        name = soup.find('tbody').findAll('a')[row/15].contents[0]
        name = name.replace("'", "")
        pos = soup.find('tbody').findAll('td')[row+1].contents[0]
        gp = soup.find('tbody').findAll('td')[row+2].contents[0]
        gs = soup.find('tbody').findAll('td')[row+3].contents[0]
        mins = soup.find('tbody').findAll('td')[row+4].contents[0]
        goals = soup.find('tbody').findAll('td')[row+5].contents[0]
        assists = soup.find('tbody').findAll('td')[row+6].contents[0]
        shots = soup.find('tbody').findAll('td')[row+7].contents[0]
        sog = soup.find('tbody').findAll('td')[row+8].contents[0]
        gwg = soup.find('tbody').findAll('td')[row+9].contents[0]
        pkg_a = soup.find('tbody').findAll('td')[row+10].contents[0]
        home_goals = soup.find('tbody').findAll('td')[row+11].contents[0]
        away_goals = soup.find('tbody').findAll('td')[row+12].contents[0]
        gp90 = soup.find('tbody').findAll('td')[row+13].contents[0]
        scoring_pct = soup.find('tbody').findAll('td')[row+14].contents[0]

        insert_data = """
                insert ignore into player_seasons
                    (player, year, type, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct)
                    values (
                        '{player}',
                        {year},
                        'post',
                        '{pos}',
                        {gp},
                        {gs},
                        {mins},
                        {goals},
                        {assists},
                        {shots},
                        {sog},
                        {gwg},
                        '{pkg_a}',
                        {home_goals},
                        {away_goals},
                        {gp90},
                        {scoring_pct}
                        );
        """.format(player=name, year=y, pos=pos, gp=gp, gs=gs, mins=mins,
                   goals=goals, assists=assists, shots=shots, sog=sog, gwg=gwg,
                   pkg_a=pkg_a, home_goals=home_goals, away_goals=away_goals,
                   gp90=gp90, scoring_pct=scoring_pct)
        cur.execute(insert_data)


def main():

    create_club_seasons()
    #club_regular_seasons(2014)
    #club_post_seasons(2014)
    #club_regular_seasons(2013)
    #club_post_seasons(2013)
    #club_regular_seasons(2012)
    #club_post_seasons(2012)
    #club_regular_seasons(2011)
    #club_post_seasons(2011)
    #club_regular_seasons(2010)
    #club_post_seasons(2010)
    #club_regular_seasons(2009)
    #club_post_seasons(2009)
    #club_regular_seasons(2008)
    #club_post_seasons(2008)
    #club_regular_seasons(2007)
    #club_post_seasons(2007)
    #club_regular_seasons(2006)
    #club_post_seasons(2006)
    #club_regular_seasons(2005)
    #club_post_seasons(2005)
    #club_regular_seasons(2004)
    #club_post_seasons(2004)
    #club_regular_seasons(2003)
    #club_post_seasons(2003)
    #club_regular_seasons(2002)
    #club_post_seasons(2002)
    #club_regular_seasons(2001)
    #club_post_seasons(2001)
    #club_regular_seasons(2000)
    #club_post_seasons(2000)
    
    #active_players()
    #inactive_players()

    create_player_seasons()
    player_regular_seasons(2014)
    player_post_seasons(2014)
    player_regular_seasons(2013)
    player_post_seasons(2013)
    player_regular_seasons(2012)
    player_post_seasons(2012)
    # player_regular_seasons(2011)
    # player_post_seasons(2011)
    # player_regular_seasons(2010)
    # player_post_seasons(2010)
    # player_regular_seasons(2009)
    # player_post_seasons(2009)
    # player_regular_seasons(2008)
    # player_post_seasons(2008)
    # player_regular_seasons(2007)
    # player_post_seasons(2007)
    # player_regular_seasons(2006)
    # player_post_seasons(2006)
    # player_regular_seasons(2005)
    # player_post_seasons(2005)
    # player_regular_seasons(2004)
    # player_post_seasons(2004)
    # player_regular_seasons(2003)
    # player_post_seasons(2003)
    # player_regular_seasons(2002)
    # player_post_seasons(2002)
    # player_regular_seasons(2001)
    # player_post_seasons(2001)
    # player_regular_seasons(2000)
    # player_post_seasons(2000)

    db.commit()

    cur.close()


main()
