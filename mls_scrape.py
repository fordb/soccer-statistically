

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
import sys

# get player data
f = open('players.csv', 'w')
f.write('number,position,name,club,age,height,weight,country,active,twitter\n')

# active players only
for n in range(11):
    print >>sys.stderr, '[{time}] Running page {n}...'.format(time=datetime.datetime.now(), n=n)
    url = 'http://www.mlssoccer.com/players?page={num}&field_player_club_nid=All&tid_2=197&title='.format(num=n)

    page = urllib2.urlopen(url)
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
        number = str(numbers[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        position = str(positions[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        name = str(names[c]).split('</a>')[0].split('>')[-1].lstrip().rstrip()
        club = str(clubs[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        age = str(ages[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        height = str(heights[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        weight = str(weights[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        country = str(countries[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        active = str(actives[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        try:
            twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
        except IndexError:
            twitter = 'No Twitter'

        f.write(number + ',' + position + ',' + name + ',' + club + ',' + age + ',' + height + ',' + weight + ',' + country + ',' + active + ',' + twitter + '\n')


# active players only
for n in range(37):
    print >>sys.stderr, '[{time}] Running page {n}...'.format(time=datetime.datetime.now(), n=n)
    url = 'http://www.mlssoccer.com/players?page={num}&field_player_club_nid=All&tid_2=198&title='.format(num=n)

    page = urllib2.urlopen(url)
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
        number = str(numbers[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        position = str(positions[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        name = str(names[c]).split('</a>')[0].split('>')[-1].lstrip().rstrip()
        club = str(clubs[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        age = str(ages[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        height = str(heights[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        weight = str(weights[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        country = str(countries[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        active = str(actives[c]).split('>')[1].split('<')[0].lstrip().rstrip()
        try:
            twitter = str(twitters[c]).split('twitter.com/')[1].split('" target')[0].lstrip().rstrip()
        except IndexError:
            twitter = 'No Twitter'

        f.write(number + ',' + position + ',' + name + ',' + club + ',' + age + ',' + height + ',' + weight + ',' + country + ',' + active + ',' + twitter + '\n')

f.close()
