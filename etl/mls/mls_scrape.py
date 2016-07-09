import MySQLdb
import sys
from bs4 import BeautifulSoup
import urllib2
import datetime
import time

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
            batch char(12),
            unique key team_year_batch (club, year, type, batch));
    """
    cur.execute(create_table)


def club_seasons(y, season, batch, cur):
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
                (club, year, type, gp, goals, assists, shots, sog, fc, fs, offsides, corners, pkg, pka, batch)
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
                    {pka},
                    '{b}'
                    );
        """.format(club=club, type=season, year=y, gp=gp, goals=goals, assists=assists, shots=shots,
                   sog=sog, fc=fc, fs=fs, offsides=offsides, corners=corners,
                   pkg=pkg, pka=pka, b=batch)
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
            batch char(12),
            unique key player_year_batch (player, year, type, batch));
    """
    cur.execute(create_table)


def player_seasons(y, season, batch, cur):
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
                        (player, year, type, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct, batch)
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
                            {scoring_pct},
                            '{b}'
                            );
                """.format(player=name, year=y, season=season, club=club, pos=pos, gp=gp, gs=gs,
                           mins=mins, goals=goals, assists=assists, shots=shots,
                           sog=sog, gwg=gwg, pkg_a=pkg_a, home_goals=home_goals,
                           away_goals=away_goals, gp90=gp90, scoring_pct=scoring_pct, b=batch)
                cur.execute(insert_data)
            except:
                pass

def main():
    batch = time.strftime("%Y%m%d%H%M")
    create_club_seasons()
    club_seasons(2014, 'REG', batch)
    club_seasons(2014, 'PS', batch)
    
    create_player_seasons()
    player_seasons(2014, 'REG', batch)
    player_seasons(2014, 'POS', batch)



if __name__ == '__main__':
    main()
