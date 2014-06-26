# import
from bs4 import BeautifulSoup
import urllib2

# open file to write to
f = open('raw.csv', 'w')
# write header line
f.write("country,continent,opposition,opposition_continent,played,wins,draws,losses,gf,ga\n")

### get all the countries by confederations ###
# asia
url = "http://www.11v11.com/afc/"
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
teams = soup.find_all('a')
asia = []
asia_dict = dict()
for i in range(32,76):
    asia.append(teams[i].encode_contents().replace(' ','-').lower())
    asia_dict[teams[i].encode_contents().replace(' ','-').lower()] = 'asia'
# remove countries that do not have pages
asia.remove("maldives")
asia.remove("macau")
asia.remove("vietnam")

# africa
url = "http://www.11v11.com/caf/"
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
teams = soup.find_all('a')
africa = []
africa_dict = dict()
for i in range(32,88):
    africa.append(teams[i].encode_contents().replace(' ','-').lower())
    africa_dict[teams[i].encode_contents().replace(' ','-').lower()] = 'africa'
# remove countries that do not have pages
africa.remove("gambia")
africa.remove("reunion")

# concacaf
url = "http://www.11v11.com/concacaf/"
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
teams = soup.find_all('a')
concacaf = []
concacaf_dict = dict()
for i in range(32,70):
    concacaf.append(teams[i].encode_contents().replace(' ','-').lower())
    concacaf_dict[teams[i].encode_contents().replace(' ','-').lower()] = 'concacaf'
# remove countries that do not have pages
concacaf.remove("sint-maarten")
concacaf.remove("st.-kitts-and-nevis")
concacaf.remove("st.-lucia")
concacaf.remove("st.-vincent-and-the-grenadines")
concacaf.remove("suriname")

# south america
url = "http://www.11v11.com/conmebol/"
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
teams = soup.find_all('a')
southamerica = []
southamerica_dict = dict()
for i in range(32,42):
    southamerica.append(teams[i].encode_contents().replace(' ','-').lower())
    southamerica_dict[teams[i].encode_contents().replace(' ','-').lower()] = 'southamerica'

# oceania
url = "http://www.11v11.com/ofc/"
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
teams = soup.find_all('a')
oceania = []
oceania_dict = dict()
for i in range(32,44):
    oceania.append(teams[i].encode_contents().replace(' ','-').lower())
    oceania_dict[teams[i].encode_contents().replace(' ','-').lower()] = 'oceania'

# europe
url = "http://www.11v11.com/uefa/"
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
teams = soup.find_all('a')
europe = []
europe_dict = dict()
for i in range(32,87):
    europe.append(teams[i].encode_contents().replace(' ','-').lower())
    europe_dict[teams[i].encode_contents().replace(' ','-').lower()] = 'europe'

# merge individual dictionaries in to one
full_dictionary = dict(asia_dict.items() + africa_dict.items() + concacaf_dict.items() + southamerica_dict.items() + oceania_dict.items() + europe_dict.items())


### loop through all countries head to head, by confederation ###
# asia
for a in asia:
    url = "http://www.11v11.com/teams/" + str(a) + "/tab/stats/comp/978"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    games = soup.find_all('tr')
    for g in range(1,len(games)):
        temp = games[g].find_all('td')
        # try looking in the dictionary for the country
        # if it doesn't exist, just continue
        # if it does write relevant info to csv file
        try:
            f.write(str(a) + "," + asia_dict[a] + "," + temp[0].encode_contents().replace(' ','-').replace('*','').lower() + "," + full_dictionary[temp[0].encode_contents().replace(' ','-').replace('*','').lower()] + "," + temp[1].encode_contents() + "," + temp[2].encode_contents() + "," + temp[3].encode_contents() + "," + temp[4].encode_contents() + "," + temp[5].encode_contents() + "," + temp[6].encode_contents() + "\n")
        except KeyError:
            pass
    print a

# africa
for a in africa:
    url = "http://www.11v11.com/teams/" + str(a) + "/tab/stats/comp/978"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    games = soup.find_all('tr')
    for g in range(1,len(games)):
        # try looking in the dictionary for the country
        # if it doesn't exist, just continue
        # if it does write relevant info to csv file
        temp = games[g].find_all('td')
        try:
            f.write(str(a) + "," + africa_dict[a] + "," + temp[0].encode_contents().replace(' ','-').replace('*','').lower() + "," + full_dictionary[temp[0].encode_contents().replace(' ','-').replace('*','').lower()] + "," + temp[1].encode_contents() + "," + temp[2].encode_contents() + "," + temp[3].encode_contents() + "," + temp[4].encode_contents() + "," + temp[5].encode_contents() + "," + temp[6].encode_contents() + "\n")
        except KeyError:
            pass
    print a

# concacaf
for a in concacaf:
    url = "http://www.11v11.com/teams/" + str(a) + "/tab/stats/comp/978"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    games = soup.find_all('tr')
    for g in range(1,len(games)):
        # try looking in the dictionary for the country
        # if it doesn't exist, just continue
        # if it does write relevant info to csv file
        temp = games[g].find_all('td')
        try:
            f.write(str(a) + "," + concacaf_dict[a] + "," + temp[0].encode_contents().replace(' ','-').replace('*','').lower() + "," + full_dictionary[temp[0].encode_contents().replace(' ','-').replace('*','').lower()] + "," + temp[1].encode_contents() + "," + temp[2].encode_contents() + "," + temp[3].encode_contents() + "," + temp[4].encode_contents() + "," + temp[5].encode_contents() + "," + temp[6].encode_contents() + "\n")
        except KeyError:
            pass
    print a

# south america
for a in southamerica:
    url = "http://www.11v11.com/teams/" + str(a) + "/tab/stats/comp/978"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    games = soup.find_all('tr')
    for g in range(1,len(games)):
        # try looking in the dictionary for the country
        # if it doesn't exist, just continue
        # if it does write relevant info to csv file
        temp = games[g].find_all('td')
        try:
            f.write(str(a) + "," + southamerica_dict[a] + "," + temp[0].encode_contents().replace(' ','-').replace('*','').lower() + "," + full_dictionary[temp[0].encode_contents().replace(' ','-').replace('*','').lower()] + "," + temp[1].encode_contents() + "," + temp[2].encode_contents() + "," + temp[3].encode_contents() + "," + temp[4].encode_contents() + "," + temp[5].encode_contents() + "," + temp[6].encode_contents() + "\n")
        except KeyError:
            pass
    print a

# oceania
for a in oceania:
    url = "http://www.11v11.com/teams/" + str(a) + "/tab/stats/comp/978"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    games = soup.find_all('tr')
    for g in range(1,len(games)):
        # try looking in the dictionary for the country
        # if it doesn't exist, just continue
        # if it does write relevant info to csv file
        temp = games[g].find_all('td')
        try:
            f.write(str(a) + "," + oceania_dict[a] + "," + temp[0].encode_contents().replace(' ','-').replace('*','').lower() + "," + full_dictionary[temp[0].encode_contents().replace(' ','-').replace('*','').lower()] + "," + temp[1].encode_contents() + "," + temp[2].encode_contents() + "," + temp[3].encode_contents() + "," + temp[4].encode_contents() + "," + temp[5].encode_contents() + "," + temp[6].encode_contents() + "\n")
        except KeyError:
            pass
    print a

# europe
for a in europe:
    url = "http://www.11v11.com/teams/" + str(a) + "/tab/stats/comp/978"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    games = soup.find_all('tr')
    for g in range(1,len(games)):
        # try looking in the dictionary for the country
        # if it doesn't exist, just continue
        # if it does write relevant info to csv file
        temp = games[g].find_all('td')
        try:
            f.write(str(a) + "," + europe_dict[a] + "," + temp[0].encode_contents().replace(' ','-').replace('*','').lower() + "," + full_dictionary[temp[0].encode_contents().replace(' ','-').replace('*','').lower()] + "," + temp[1].encode_contents() + "," + temp[2].encode_contents() + "," + temp[3].encode_contents() + "," + temp[4].encode_contents() + "," + temp[5].encode_contents() + "," + temp[6].encode_contents() + "\n")
        except KeyError:
            pass
    print a
    
# close the file
f.close()