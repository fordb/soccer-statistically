import MySQLdb
import sys
from unidecode import unidecode

db = MySQLdb.connect(host="localhost", user="root", db="soccer_stat")
cur = db.cursor()

# inactive players
url = 'http://www.mlssoccer.com/players?field_player_club_nid=All&tid_2=198&title='

# player season (regular and post, by year) stats
url = 'http://www.mlssoccer.com/stats/season?season_year=2014&season_type=REG&team=ALL&group=GOALS&op=Search&form_id=mls_stats_individual_form'

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
            number = 'Null'
        position = unidecode(unicode(str(positions[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if position == '':
            position = 'Null'
        name = unidecode(unicode(str(names[c]).split('</a>')[0].split('>')[-1].lstrip().rstrip(), "utf-8"))
        name = name.replace("'", "")
        if name == '':
            name = 'Null'
        club = unidecode(unicode(str(clubs[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if club == '':
            club = 'Null'
        age = unidecode(unicode(str(ages[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if age == '':
            age = 'Null'
        height = unidecode(unicode(str(heights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        height = height[:-3].replace("'", "''").replace("\\", "")
        if height == '':
            height = 'Null'
        weight = unidecode(unicode(str(weights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if weight == '':
            weight = 'Null'
        country = unidecode(unicode(str(countries[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if country == '':
            country = 'Null'
        active = unidecode(unicode(str(actives[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        try:
            twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
        except IndexError:
            twitter = 'No Twitter'

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
            number = 'Null'
        position = unidecode(unicode(str(positions[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if position == '':
            position = 'Null'
        name = unidecode(unicode(str(names[c]).split('</a>')[0].split('>')[-1].lstrip().rstrip(), "utf-8"))
        name = name.replace("'", "")
        if name == '':
            name = 'Null'
        club = unidecode(unicode(str(clubs[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if club == '':
            club = 'Null'
        age = unidecode(unicode(str(ages[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if age == '':
            age = 'Null'
        height = unidecode(unicode(str(heights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        height = height[:-3].replace("'", "''").replace("\\", "")
        if height == '':
            height = 'Null'
        weight = unidecode(unicode(str(weights[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if weight == '':
            weight = 'Null'
        country = unidecode(unicode(str(countries[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        if country == '':
            country = 'Null'
        active = unidecode(unicode(str(actives[c]).split('>')[1].split('<')[0].lstrip().rstrip(), "utf-8"))
        try:
            twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
        except IndexError:
            twitter = 'No Twitter'
        try:
            twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
        except IndexError:
            twitter = 'No Twitter'

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


db.commit()

cur.close()
