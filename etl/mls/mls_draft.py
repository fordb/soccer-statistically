# a lot of the code based off of the blog post below:
# https://adesquared.wordpress.com/2013/06/16/using-python-beautifulsoup-to-scrape-a-wikipedia-table/

from bs4 import BeautifulSoup
import urllib2
import MySQLdb
from unidecode import unidecode

db = MySQLdb.connect(host="localhost", user="ford", db="ss",
                     passwd="ss")
cur = db.cursor()

header = {'User-Agent': 'Mozilla/5.0'}

data = []

cur.execute('drop table if exists draft')
create_table = """
    create table mls_draft (
        year int,
        round int,
        pick int,
        club varchar(50),
        name varchar(50),
        position varchar(20),
        affiliation varchar(50));
"""
cur.execute(create_table)


for year in range(2000, 2016):
    wiki = "http://en.wikipedia.org/wiki/{year}_MLS_SuperDraft".format(year=year)
    req = urllib2.Request(wiki, headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    table = soup.findAll("table", { "class" : "wikitable sortable sortable" })
    table += soup.findAll("table", { "class" : "wikitable sortable" })

    rounds = len(table)
    if year in [2010, 2011]:
        rounds = len(table)-1
        
    for r in range(0, rounds):
        pick = 0
        for row in table[r].findAll("tr"):
            cells = row.findAll("td")
            # For each "tr", assign each "td" to a variable.
            length = len(cells)
            num = length - 4
            player = ""
            try:
                player = max(cells[num+1].findAll(text=True), key=len)
            except:
                IndexError
            if player == "PASS":
                team = cells[num].find(text=True).encode('ascii', 'ignore')
                player = unidecode(max(cells[num+1].findAll(text=True), key=len))
                insert_data = """
                    insert ignore into mls_draft
                      (year, round, pick, club, name, position, affiliation)
                      values ({y}, {r}, {pick}, '{c}', NULL, NULL, NULL);
                """.format(y=year, r=r+1, pick=pick+1, c=team, n=player)
                cur.execute(insert_data)
                data.append([year, pick+1, r+1, team, player, None, None])
                pick += 1
            elif len(cells) in [4, 5]:
                team = cells[num].find(text=True).encode('ascii', 'ignore')
                player = unidecode(max(cells[num+1].findAll(text=True), key=len))
                player = player.replace("'", "")
                position = cells[num+2].find(text=True).encode('ascii', 'ignore')
                affiliation = cells[num+3].find(text=True).encode('ascii', 'ignore')
                affiliation = affiliation.replace("'", "")
                insert_data = """
                    insert ignore into mls_draft
                      (year, round, pick, club, name, position, affiliation)
                      values ({y}, {r}, {pick}, '{c}', '{n}', '{p}', '{a}');
                """.format(y=year, r=r+1, pick=pick+1, c=team, n=player,
                           p=position, a=affiliation)
                cur.execute(insert_data)
                data.append([year, pick+1, r+1, team, player, position, affiliation])
                pick += 1
    print year
           
db.commit()
cur.close()

