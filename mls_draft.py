from bs4 import BeautifulSoup
import urllib2
import csv
import io

header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia

data = []

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
            position = cells[2].find(text=True).encode('ascii', 'ignore')
            affiliation = cells[3].find(text=True).encode('ascii', 'ignore')
            try:
                name = cells[1].findAll("a", href=True)[0]["href"]
                print name
                wiki = "http://en.wikipedia.org{name}".format(name=name)
                req = urllib2.Request(wiki,headers=header)
                page = urllib2.urlopen(req)
                soup = BeautifulSoup(page)
                text = unicode.join(u'\n',map(unicode,soup))
                excerpt = text.split("Senior career")[1].split("text-align:center; background-color: #b0c4de; line-height: 1.5em")[0]
                soup = BeautifulSoup(excerpt)
                print [str(n.contents[0]) for n in soup.findAll("td", { "style" : "white-space: nowrap; vertical-align: baseline;text-align: right" }, text=True) if not "b" in str(n.contents[0])]
                x = [str(n.contents[0]) for n in soup.findAll("td", { "style" : "white-space: nowrap; vertical-align: baseline" }, text=True) if not "b" in str(n.contents[0])]
                print x
                
            except IndexError:
                games = 0
                goals = 0
            #data.append([year, team, player, position, affiliation, games, goals])
    print year
           

with open('draft.csv', 'wb') as draft:
    a = csv.writer(draft, delimiter=',')
    a.writerows(data)
