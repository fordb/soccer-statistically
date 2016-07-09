import MySQLdb
import sys
from bs4 import BeautifulSoup
import urllib2
import datetime

player_dict = {}
club_dict = {}
league_dict = {'MLS': 1}

player_counter = 1
club_counter = 1
league_counter = 1


def create_club_seasons(cur):
    cur.execute('drop table if exists club_seasons;')
    create_table = """
        create table club_seasons (
            club varchar(100),
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
            unique key team_year (club, year, type));
    """
    cur.execute(create_table)


def club_seasons(y, season, cur):
    proxy_support = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_support)
    print >>sys.stderr, '[{time}] Scraping {s} season teams year {y}...'.format(
        time=datetime.datetime.now(), s=season, y=y)
    url = 'http://www.mlssoccer.com/stats/team?year={year}&season_type={season}'.format(year=y, season=season)
    page = opener.open(url).read()
    soup = BeautifulSoup(page)
    length = len(soup.find('tbody').findAll('tr'))
    for row in range(0, length):
        club = soup.find('tbody').findAll('td', attrs={'data-title': 'club'})[row].contents[0]
        gp = soup.find('tbody').findAll('td', attrs={'data-title': 'gp'})[row].contents[0]
        goals = soup.find('tbody').findAll('td', attrs={'data-title': 'g'})[row].contents[0]
        assists = soup.find('tbody').findAll('td', attrs={'data-title': 'a'})[row].contents[0]
        shots = soup.find('tbody').findAll('td', attrs={'data-title': 'shts'})[row].contents[0]
        sog = soup.find('tbody').findAll('td', attrs={'data-title': 'sog'})[row].contents[0]
        fc = soup.find('tbody').findAll('td', attrs={'data-title': 'fc'})[row].contents[0]
        fs = soup.find('tbody').findAll('td', attrs={'data-title': 'fs'})[row].contents[0]
        offsides = soup.find('tbody').findAll('td', attrs={'data-title': 'off'})[row].contents[0]
        corners = soup.find('tbody').findAll('td', attrs={'data-title': 'ck'})[row].contents[0]
        pkg = soup.find('tbody').findAll('td', attrs={'data-title': 'pkg'})[row].contents[0]
        pka = soup.find('tbody').findAll('td', attrs={'data-title': 'pka'})[row].contents[0]


        insert_data = """
            insert ignore into club_seasons
                (club, year, type, gp, goals, assists, shots, sog, fc, fs, offsides, corners, pkg, pka)
                values (
                    '{club}',
                    {year},
                    '{type}',
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
        """.format(club=club, type=season, year=y, gp=gp, goals=goals, assists=assists, shots=shots,
                   sog=sog, fc=fc, fs=fs, offsides=offsides, corners=corners,
                   pkg=pkg, pka=pka)
        cur.execute(insert_data)


def create_player_seasons(cur):
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
            unique key player_year (player, year, type));
    """
    cur.execute(create_table)


def player_seasons(y, season, cur):
    print >>sys.stderr, '[{time}] Scraping {s} season year {y}...'.format(
        time=datetime.datetime.now(), s=season, y=y)
    # regular season field players
    proxy_support = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_support)
    for p in range(30):
        url = 'http://www.mlssoccer.com/stats/season?page={p}&franchise=select&year={year}&season_type={season}&group=goals'.format(
            p=p, year=y, season=season)
        page = opener.open(url).read()
        soup = BeautifulSoup(page)
        print >>sys.stderr, '[{time}] Running page {n}...'.format(
            time=datetime.datetime.now(), n=p)
        for row in range(25):
            try:
                name = soup.find('tbody').findAll('td', attrs={'data-title': 'Player'})[row].find('a').contents[0]
                club = soup.find('tbody').findAll('td', attrs={'data-title': 'Club'})[row].contents[0]
                pos = soup.find('tbody').findAll('td', attrs={'data-title': 'POS'})[row].contents[0]
                gp = soup.find('tbody').findAll('td', attrs={'data-title': 'GP'})[row].contents[0]
                gs = soup.find('tbody').findAll('td', attrs={'data-title': 'GS'})[row].contents[0]
                mins = soup.find('tbody').findAll('td', attrs={'data-title': 'MINS'})[row].contents[0]
                goals = soup.find('tbody').findAll('td', attrs={'data-title': 'G'})[row].contents[0]
                assists = soup.find('tbody').findAll('td', attrs={'data-title': 'A'})[row].contents[0]
                shots = soup.find('tbody').findAll('td', attrs={'data-title': 'SHTS'})[row].contents[0]
                sog = soup.find('tbody').findAll('td', attrs={'data-title': 'SOG'})[row].contents[0]
                gwg = soup.find('tbody').findAll('td', attrs={'data-title': 'GWG'})[row].contents[0]
                pkg_a = soup.find('tbody').findAll('td', attrs={'data-title': 'PKG/A'})[row].contents[0]
                home_goals = soup.find('tbody').findAll('td', attrs={'data-title': 'HmG'})[row].contents[0]
                away_goals = soup.find('tbody').findAll('td', attrs={'data-title': 'RdG'})[row].contents[0]
                gp90 = soup.find('tbody').findAll('td', attrs={'data-title': 'G/90min'})[row].contents[0]
                scoring_pct = soup.find('tbody').findAll('td', attrs={'data-title': 'SC%'})[row].contents[0]

                insert_data = """
                    insert ignore into player_seasons
                        (player, year, type, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct)
                        values (
                            '{player}',
                            {year},
                            '{season}',
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
                """.format(player=name, year=y, season=season, club=club, pos=pos, gp=gp, gs=gs,
                           mins=mins, goals=goals, assists=assists, shots=shots,
                           sog=sog, gwg=gwg, pkg_a=pkg_a, home_goals=home_goals,
                           away_goals=away_goals, gp90=gp90, scoring_pct=scoring_pct)
                cur.execute(insert_data)
            except:
                pass

def main():

    create_club_seasons()
    club_seasons(2014, 'REG')
    club_seasons(2014, 'PS')
    # club_seasons(2013, 'REG')
    # club_seasons(2013, 'PS')
    # club_seasons(2012, 'REG')
    # club_seasons(2012, 'PS')
    # club_seasons(2011, 'REG')
    # club_seasons(2011, 'PS')
    # club_seasons(2010, 'REG')
    # club_seasons(2010, 'PS')
    # club_seasons(2009, 'REG')
    # club_seasons(2009, 'PS')
    # club_seasons(2008, 'REG')
    # club_seasons(2008, 'PS')
    # club_seasons(2007, 'REG')
    # club_seasons(2007, 'PS')
    # club_seasons(2006, 'REG')
    # club_seasons(2006, 'PS')
    # club_seasons(2005, 'REG')
    # club_seasons(2005, 'PS')
    # club_seasons(2004, 'REG')
    # club_seasons(2004, 'PS')
    # club_seasons(2003, 'REG')
    # club_seasons(2003, 'PS')
    # club_seasons(2002, 'REG')
    # club_seasons(2002, 'PS')
    # club_seasons(2001, 'REG')
    # club_seasons(2001, 'PS')
    # club_seasons(2000, 'REG')
    # club_seasons(2000, 'PS')
    # club_seasons(1999, 'REG')
    # club_seasons(1999, 'PS')
    # club_seasons(1998, 'REG')
    # club_seasons(1998, 'PS')
    # club_seasons(1997, 'REG')
    # club_seasons(1997, 'PS')
    # club_seasons(1996, 'REG')
    # club_seasons(1996, 'PS')
    
    create_player_seasons()
    player_seasons(2014, 'REG')
    player_seasons(2014, 'POS')
    # player_regular_seasons(2013)
    # player_post_seasons(2013)
    # player_regular_seasons(2012)
    # player_post_seasons(2012)
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



if __name__ == '__main__':
    main()
