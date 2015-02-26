import MySQLdb
import sys
from unidecode import unidecode
import uuid
from bs4 import BeautifulSoup
import re
import urllib2
import datetime

db = MySQLdb.connect(host="localhost", user="root", db="soccer_stat")
cur = db.cursor()

proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)

player_dict = {}
club_dict = {}
league_dict = {}


def create_leagues():
    cur.execute('drop table if exists leagues;')
    create_table = """
        create table leagues (
            league_id char(36),
            short_name varchar(5),
            long_name varchar(30),
            country varchar(30),
            unique key league (short_name, long_name));
    """
    cur.execute(create_table)

    l_id = uuid.uuid4()
    insert_data = """
        insert ignore into leagues
            (league_id, short_name, long_name, country)
            values (
                '{id}',
                'MLS',
                'Major League Soccer',
                'USA')
    """.format(id=l_id)
    cur.execute(insert_data)
    league_dict['MLS'] = l_id


def create_clubs():
    cur.execute('drop table if exists clubs;')
    create_table = """
        create table clubs (
            club_id char(36),
            name varchar(30),
            city varchar(30),
            league_id char(36),
            unique key name (name));
    """
    cur.execute(create_table)


def create_club_seasons():
    cur.execute('drop table if exists club_seasons;')
    create_table = """
        create table club_seasons (
            team_id char(36),
            year int,
            type varchar(10),
            club_id char(36),
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
    print >>sys.stderr, '[{time}] Scraping regular season teams year {y}...'.format(time=datetime.datetime.now(), y=y)
    url = 'http://www.mlssoccer.com/stats/team?season_year={year}&season_type=REG&op=Search&form_id=mls_stats_team_form'.format(year=y)
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
        c_id = uuid.uuid4()

        club_dict[club.lower().replace(" ", "").replace(".", "")] = c_id

        insert_club_data = """
            insert ignore into clubs
                (club_id, name, city, league_id)
                values (
                    '{c_id}',
                    '{club}',
                    NULL,
                    '{l_id}')
        """.format(c_id=c_id, club=club, l_id=league_dict['MLS'])
        cur.execute(insert_club_data)

        insert_data = """
            insert ignore into club_seasons
                (club_id, year, type, gp, goals, assists, shots, sog, fc, fs, offsides, corners, pkg, pka)
                values (
                    '{id}',
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
        """.format(id=c_id, year=y, gp=gp, goals=goals, assists=assists, shots=shots, sog=sog, fc=fc, fs=fs, offsides=offsides, corners=corners, pkg=pkg, pka=pka)
        cur.execute(insert_data)


def club_post_seasons(y):
    print >>sys.stderr, '[{time}] Scraping postseason teams year {y}...'.format(time=datetime.datetime.now(), y=y)
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
                        '{c_id}',
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
        """.format(c_id=c_id, year=y, gp=gp, goals=goals, assists=assists, shots=shots, sog=sog, fc=fc, fs=fs, offsides=offsides, corners=corners, pkg=pkg, pka=pka)
        cur.execute(insert_data)


def active_players():
    print >>sys.stderr, '[{time}] Scraping Active players...'.format(time=datetime.datetime.now())
    # get player data
    cur.execute('drop table if exists players;')
    create_table = """
        create table players (
            player_id char(36) primary key,
            number smallint,
            position varchar(5),
            name varchar(30),
            club_id char(36),
            age smallint,
            height int,
            weight smallint,
            country varchar(50),
            active varchar(10),
            twitter varchar(30),
            unique key name (name));
    """
    cur.execute(create_table)

    # active players only
    for n in range(11):
        print >>sys.stderr, '[{time}] Running page {n}...'.format(time=datetime.datetime.now(), n=n)
        url = 'http://www.mlssoccer.com/players?page={num}&field_player_club_nid=All&tid_2=197&title='.format(num=n)

        page = opener.open(url).read()
        soup = BeautifulSoup(page)

        numbers = soup.findAll('td', {'class': 'views-field views-field-field-player-jersey-no-value'})
        positions = soup.findAll('td', {'class': 'views-field views-field-field-player-position-detail-value'})
        names = soup.findAll('td', {'class': 'views-field views-field-field-player-lname-value'})
        clubs = soup.findAll('td', {'class': 'views-field views-field-field-player-club-nid'})
        ages = soup.findAll('td', {'class': 'views-field views-field-field-player-birth-date-value-1'})
        heights = soup.findAll('td', {'class': 'views-field views-field-field-player-height-value'})
        weights = soup.findAll('td', {'class': 'views-field views-field-field-player-weight-value'})
        countries = soup.findAll('td', {'class': 'views-field views-field-field-player-birth-country-value'})
        actives = soup.findAll('td', {'class': 'views-field views-field-name'})
        twitters = soup.findAll('td', {'class': 'views-field views-field-field-player-twitter-username-value'})

        assert len(numbers) == len(positions) == len(names) == len(clubs) == len(ages) == len(heights) == len(weights) == len(countries) == len(actives) == len(twitters)

        for c in range(len(countries)):
            number = unidecode(unicode(str(numbers[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if number == '':
                number = 'NULL'
            position = unidecode(unicode(str(positions[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if position == '':
                position = 'NULL'
            name = unidecode(unicode(str(names[c]).split('</a>')[0].split('>')[-1].lstrip().rstrip(), "utf-8"))
            name = name.replace("'", "")
            if name == '':
                name = 'NULL'
            club = unidecode(unicode(str(clubs[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if club == '':
                club = 'NULL'
            age = unidecode(unicode(str(ages[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if age == '':
                age = 'NULL'
            height = unidecode(unicode(str(heights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if height == '':
                height = 'NULL'
            else:
                height = height.replace("'", "''")
                feet = int(height[0])
                try:
                    inches = int(re.findall('[\d+]', height)[1])
                except IndexError:
                    inches = 0
            weight = unidecode(unicode(str(weights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if weight == '':
                weight = 'NULL'
            country = unidecode(unicode(str(countries[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if country == '':
                country = 'NULL'
            active = unidecode(unicode(str(actives[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            try:
                twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
            except IndexError:
                twitter = 'NULL'
            p_id = uuid.uuid4()
            player_dict[name.lower().replace(" ", "")] = p_id

            try:
                c_id = club_dict[club.lower().replace(" ", "").replace(".", "")]
            except KeyError:
                c_id = uuid.uuid4()
                if club == 'NULL':
                    pass
                else:
                    insert_new_club = """
                        insert ignore into clubs
                            (club_id, name, city, league_id)
                            values (
                                '{id}',
                                '{club}',
                                NULL,
                                NULL
                                );
                    """.format(id=c_id, club=club)
                    cur.execute(insert_new_club)

            insert_data = """
                insert ignore into players
                    (player_id, number, position, name, club_id, age, height, weight, country, active, twitter)
                    values (
                        '{id}',
                        {num},
                        '{position}',
                        '{name}',
                        '{c_id}',
                        {age},
                        {height},
                        {weight},
                        '{country}',
                        '{active}',
                        '{twitter}'
                        );
            """.format(id=p_id, num=number, position=position, name=name, c_id=c_id, age=age, height=(feet*12)+inches, weight=weight, country=country, active=active, twitter=twitter)
            cur.execute(insert_data)


def inactive_players():
    print >>sys.stderr, '[{time}] Scraping Inactive players...'.format(time=datetime.datetime.now())
    for n in range(37):
        print >>sys.stderr, '[{time}] Running page {n}...'.format(time=datetime.datetime.now(), n=n)
        url = 'http://www.mlssoccer.com/players?page={num}&field_player_club_nid=All&tid_2=198&title='.format(num=n)

        page = opener.open(url).read()
        soup = BeautifulSoup(page)

        numbers = soup.findAll('td', {'class': 'views-field views-field-field-player-jersey-no-value'})
        positions = soup.findAll('td', {'class': 'views-field views-field-field-player-position-detail-value'})
        names = soup.findAll('td', {'class': 'views-field views-field-field-player-lname-value'})
        clubs = soup.findAll('td', {'class': 'views-field views-field-field-player-club-nid'})
        ages = soup.findAll('td', {'class': 'views-field views-field-field-player-birth-date-value-1'})
        heights = soup.findAll('td', {'class': 'views-field views-field-field-player-height-value'})
        weights = soup.findAll('td', {'class': 'views-field views-field-field-player-weight-value'})
        countries = soup.findAll('td', {'class': 'views-field views-field-field-player-birth-country-value'})
        actives = soup.findAll('td', {'class': 'views-field views-field-name'})
        twitters = soup.findAll('td', {'class': 'views-field views-field-field-player-twitter-username-value'})

        assert len(numbers) == len(positions) == len(names) == len(clubs) == len(ages) == len(heights) == len(weights) == len(countries) == len(actives) == len(twitters)

        for c in range(len(countries)):
            number = unidecode(unicode(str(numbers[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if number == '':
                number = 'NULL'
            position = unidecode(unicode(str(positions[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if position == '':
                position = 'NULL'
            name = unidecode(unicode(str(names[c]).split('</a>')[0].split('>')[-1].lstrip().rstrip(), "utf-8"))
            name = name.replace("'", "")
            if name == '':
                name = 'NULL'
            club = unidecode(unicode(str(clubs[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if club == '':
                club = 'NULL'
            age = unidecode(unicode(str(ages[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if age == '':
                age = 'NULL'
            height = unidecode(unicode(str(heights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if height == '':
                height = 'NULL'
            else:
                height = height.replace("'", "''")
                feet = int(height[0])
                try:
                    inches = int(re.findall('[\d+]', height)[1])
                except IndexError:
                    inches = 0
            weight = unidecode(unicode(str(weights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if weight == '':
                weight = 'NULL'
            country = unidecode(unicode(str(countries[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            if country == '':
                country = 'NULL'
            active = unidecode(unicode(str(actives[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
            try:
                twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
            except IndexError:
                twitter = 'NULL'

            try:
                c_id = club_dict[club.lower().replace(" ", "").replace(".", "")]
            except KeyError:
                c_id = uuid.uuid4()
                if club == 'NULL':
                    pass
                else:
                    insert_new_club = """
                        insert ignore into clubs
                            (club_id, name, city, league_id)
                            values (
                                '{id}',
                                '{club}',
                                NULL,
                                NULL
                                );
                    """.format(id=c_id, club=club)
                    cur.execute(insert_new_club)

            p_id = uuid.uuid4()
            player_dict[name.lower().replace(" ", "")] = p_id
            insert_data = """
                insert ignore into players
                    (player_id, number, position, name, club_id, age, height, weight, country, active, twitter)
                    values (
                        '{id}',
                        {num},
                        '{position}',
                        '{name}',
                        '{c_id}',
                        {age},
                        {height},
                        {weight},
                        '{country}',
                        '{active}',
                        '{twitter}'
                        );
            """.format(id=p_id, num=number, position=position, name=name, c_id=c_id, age=age, height=(feet*12)+inches, weight=weight, country=country, active=active, twitter=twitter)
            cur.execute(insert_data)


def create_player_seasons():
    cur.execute('drop table if exists player_seasons;')
    create_table = """
        create table player_seasons (
            player_id char(36),
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
            unique key id_year (player_id, year));
    """
    cur.execute(create_table)


def player_regular_seasons(y):
    print >>sys.stderr, '[{time}] Scraping regular season year {y}...'.format(time=datetime.datetime.now(), y=y)
    # regular season field players
    first_name = None
    for p in range(50):
        url = 'http://www.mlssoccer.com/stats/season?sort=desc&order=SC%25&page={num}&season_year={year}&season_type=REG&team=ALL&group=GOALS&op=Search&form_id=mls_stats_individual_form'.format(num=p, year=y)
        page = opener.open(url).read()
        soup = BeautifulSoup(page)
        temp_name = None
        print >>sys.stderr, '[{time}] Running page {n}...'.format(time=datetime.datetime.now(), n=p)
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
            try:
                p_id = player_dict[name.lower().replace(" ", "")]
            except KeyError:
                p_id = uuid.uuid4()
                insert_new_player = """
                    insert ignore into players
                        (player_id, number, position, name, club_id, age, height, weight, country, active, twitter)
                        values (
                            '{id}',
                            NULL,
                            NULL,
                            '{name}',
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            NULL
                            );
                """.format(id=p_id, name=name)
                cur.execute(insert_new_player)

            insert_data = """
                    insert ignore into player_seasons
                        (player_id, year, type, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct)
                        values (
                            '{id}',
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
            """.format(id=p_id, year=y, club=club, pos=pos, gp=gp, gs=gs, mins=mins, goals=goals, assists=assists, shots=shots, sog=sog, gwg=gwg, pkg_a=pkg_a, home_goals=home_goals, away_goals=away_goals, gp90=gp90, scoring_pct=scoring_pct)
            cur.execute(insert_data)
        if temp_name is None:
            break


def player_post_seasons(y):
    print >>sys.stderr, '[{time}] Scraping playoffs year {y}...'.format(time=datetime.datetime.now(), y=y)
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
        try:
            p_id = player_dict[name.lower().replace(" ", "")]
        except KeyError:
            p_id = uuid.uuid4()
            insert_new_player = """
                insert ignore into players
                    (player_id, number, position, name, club_id, age, height, weight, country, active, twitter)
                    values (
                        '{id}',
                        NULL,
                        NULL,
                        '{name}',
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL
                        );
            """.format(id=p_id, name=name)
            cur.execute(insert_new_player)

        insert_data = """
                insert ignore into player_seasons
                    (player_id, year, type, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct)
                    values (
                        '{id}',
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
        """.format(id=p_id, year=y, pos=pos, gp=gp, gs=gs, mins=mins, goals=goals, assists=assists, shots=shots, sog=sog, gwg=gwg, pkg_a=pkg_a, home_goals=home_goals, away_goals=away_goals, gp90=gp90, scoring_pct=scoring_pct)
        cur.execute(insert_data)


def main():

    create_leagues()

    create_clubs()

    create_club_seasons()
    club_regular_seasons(2014)
    club_post_seasons(2014)
    club_regular_seasons(2013)
    club_post_seasons(2013)
    club_regular_seasons(2012)
    club_post_seasons(2012)
    club_regular_seasons(2011)
    club_post_seasons(2011)
    club_regular_seasons(2010)
    club_post_seasons(2010)

    active_players()
    inactive_players()

    create_player_seasons()
    player_regular_seasons(2014)
    player_post_seasons(2014)
    player_regular_seasons(2013)
    player_post_seasons(2013)
    player_regular_seasons(2012)
    player_post_seasons(2012)
    player_regular_seasons(2011)
    player_post_seasons(2011)
    player_regular_seasons(2010)
    player_post_seasons(2010)

    db.commit()

    cur.close()


main()
