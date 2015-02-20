import MySQLdb
import sys
from unidecode import unidecode

db = MySQLdb.connect(host="localhost", user="root", db="soccer_stat")
cur = db.cursor()


# team (regular and post, by year) stats
url = 'http://www.mlssoccer.com/stats/team?season_year=2014&season_type=REG&op=Search&form_id=mls_stats_team_form'

# boxscore
url = 'http://matchcenter.mlssoccer.com/matchcenter/2014-10-04-vancouver-whitecaps-fc-vs-fc-dallas/boxscore'


from bs4 import BeautifulSoup
import re
import urllib2
import datetime

proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)


def players():
        # get player data
        cur.execute('drop table if exists players;')
        create_table = """
            create table players (
                player_id int not null auto_increment primary key,
                number smallint,
                position varchar(5),
                name varchar(30),
                club varchar(25),
                age smallint,
                height varchar(5),
                weight smallint,
                country varchar(50),
                active varchar(10),
                twitter varchar(30));
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
                height = height[:-3].replace("'", "''").replace("\\", "")
                if height == '':
                    height = 'NULL'
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

                insert_data = """
                    insert into players
                        (number, position, name, club, age, height, weight, country, active, twitter)
                        values (
                            {num},
                            '{position}',
                            '{name}',
                            '{club}',
                            {age},
                            '{height}',
                            {weight},
                            '{country}',
                            '{active}',
                            '{twitter}'
                            );
                """.format(num=number, position=position, name=name, club=club, age=age, height=height, weight=weight, country=country, active=active, twitter=twitter)
                cur.execute(insert_data)

        # inactive players only
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
                height = height[:-3].replace("'", "''").replace("\\", "")
                if height == '':
                    height = 'NULL'
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

                insert_data = """
                    insert into players
                        (number, position, name, club, age, height, weight, country, active, twitter)
                        values (
                            {num},
                            '{position}',
                            '{name}',
                            '{club}',
                            {age},
                            '{height}',
                            {weight},
                            '{country}',
                            '{active}',
                            '{twitter}'
                            );
                """.format(num=number, position=position, name=name, club=club, age=age, height=height, weight=weight, country=country, active=active, twitter=twitter)
                cur.execute(insert_data)


def seasons():
    cur.execute('drop table if exists seasons;')
    create_table = """
        create table seasons (
            player_id int not null auto_increment primary key,
            year int,
            club varchar(30),
            position varchar(5),
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
            gp_90 decimal(3,2),
            scoring_pct decimal(4,1));
    """
    cur.execute(create_table)

    for y in range(2014, 1995, -1):
        print >>sys.stderr, '[{time}] Running year {y}...'.format(time=datetime.datetime.now(), y=y)
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
                        insert into seasons
                            (year, club, position, gp, gs, mins, goals, assists, shots, sog, gwg, pkg_a, home_goals, away_goals, gp_90, scoring_pct)
                            values (
                                {year},
                                '{club}',
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
                """.format(year=y, club=club, pos=pos, gp=gp, gs=gs, mins=mins, goals=goals, assists=assists, shots=shots, sog=sog, gwg=gwg, pkg_a=pkg_a, home_goals=home_goals, away_goals=away_goals, gp90=gp90, scoring_pct=scoring_pct)
                cur.execute(insert_data)
            if temp_name is None:
                break


def main():
    # players()
    seasons()
    db.commit()

    cur.close()


main()
