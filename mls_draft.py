from bs4 import BeautifulSoup
import urllib2
import csv
import io
import MySQLdb


db = MySQLdb.connect(host="localhost", user="root", db="soccer_stat")
cur = db.cursor()


header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia

data = []

cur.execute('drop table if exists draft')
create_table = """
    create table draft (
        year int,
        club varchar(50),
        name varchar(50),
        position varchar(10),
        affiliation varchar(50));
"""
cur.execute(create_table)

for year in range(2000,2016):
    wiki = "http://en.wikipedia.org/wiki/{year}_MLS_SuperDraft".format(year=year)
    req = urllib2.Request(wiki,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    table = soup.find("table", { "class" : "wikitable sortable" })
    if not table:
        table = soup.find("table", { "class" : "wikitable sortable sortable" })

    for row in table.findAll("tr"):
        cells = row.findAll("td")
        #For each "tr", assign each "td" to a variable.
        if len(cells) == 4:
            team = cells[0].find(text=True).encode('ascii', 'ignore')
            player = max(cells[1].findAll(text=True), key=len).encode('ascii', 'ignore')
            print player
            position = cells[2].find(text=True).encode('ascii', 'ignore')
            affiliation = cells[3].find(text=True).encode('ascii', 'ignore')
            affiliation = affiliation.replace("'", "")
            insert_data = """
                insert ignore into draft
                  (year, club, name, position, affiliation)
                  values ({y}, '{c}', '{n}', '{p}', '{a}');
            """.format(y=year, c=team, n=player, p=position, a=affiliation)
            cur.execute(insert_data)
            
            data.append([year, team, player, position, affiliation])
    print year
           
db.commit()
cur.close()

with open('draft.csv', 'wb') as draft:
    a = csv.writer(draft, delimiter=',')
    a.writerows(data)

