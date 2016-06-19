import scrapy
from epl_scrape.items import ClubDetailItem


class EPLClubSpider(scrapy.Spider):
    name = "epl-club"
    allowed_domains = ["premierleague.com"]
    start_urls = [
        "http://www.premierleague.com/en-gb/clubs.html"
    ]
    
    def parse(self, response):
        clubs = response.xpath('//ul/li[re:test(@clubid, "[0-9]+")]//@href').extract()
        
        for c in clubs:
            for y in ['2015-2016', '2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
                      '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006', '2004-2005',
                      '2003-2004', '2002-2003', '2001-2002', '2000-2001']:
                url = "http://www.premierleague.com" + c.replace("profile.overview.html", "profile.statistics.html") + "?playedAt=BOTH&timelineView=BY_SEASON&toSeason={y}".format(y=y)
                yield scrapy.http.Request(url, callback=self.parse_club)


    def parse_club(self, response):

        year = response.url[-9:]
        club = ClubDetailItem()
        # overall
        name = response.xpath('//div[@class="overlay"]/h2[@class="noborder"]/text()').extract()
        played = response.xpath('//li[@name="played"]/div[@class="data"]/text()').extract()
        wins = response.xpath('//li[@name="won"]/div[@class="data"]/text()').extract()
        draws = response.xpath('//li[@name="drawn"]/div[@class="data"]/text()').extract()
        losses = response.xpath('//li[@name="lost"]/div[@class="data"]/text()').extract()
        # goals
        gf = response.xpath('//li[@name="goalsFor"][1]/div[@class="data"]/text()').extract()
        ga = response.xpath('//li[@name="goalsAgainst"]/div[@class="data"]/text()').extract()
        pk_goals = response.xpath('//li[@name="goalsFor"][2]/div[@class="data"]/text()').extract()
        # attacking
        shots = response.xpath('//li[@name="shots"]/div[@class="data"]/text()').extract()
        crosses = response.xpath('//li[@name="crosses"]/div[@class="data"]/text()').extract()
        offsides = response.xpath('//li[@name="offsides"]/div[@class="data"]/text()').extract()
        # defending
        saves = response.xpath('//li[@name="savesMade"]/div[@class="data"]/text()').extract()
        own_goals = response.xpath('//li[@name="ownGoals"]/div[@class="data"]/text()').extract()
        shutouts = response.xpath('//li[@name="cleanSheets"]/div[@class="data"]/text()').extract()
        blocks = response.xpath('//li[@name="blocks"]/div[@class="data"]/text()').extract()
        clearances = response.xpath('//li[@name="clearances"]/div[@class="data"]/text()').extract()
        # disciplinary
        fouls = response.xpath('//li[@name="fouls"]/div[@class="data"]/text()').extract()
        cards = response.xpath('//li[@name="cards"]/div[@class="data"]/text()').extract()

        club["name"] = name
        club["year"] = year
        club["gp"] = played
        club["wins"] = wins
        club["draws"] = draws
        club["losses"] = losses
        club["gf"] = gf
        club["ga"] = ga
        club["pk_goals"] = pk_goals
        club["shots"] = shots
        club["crosses"] = crosses
        club["offsides"] = offsides
        club["saves"] = saves
        club["own_goals"] = own_goals
        club["shutouts"] = shutouts
        club["blocks"] = blocks
        club["clearances"] = clearances
        club["fouls"] = fouls
        club["cards"] = cards

        yield club


