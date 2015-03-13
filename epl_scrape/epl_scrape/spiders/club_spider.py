import scrapy
import urlparse
from epl_scrape.items import ClubPageItem
from epl_scrape.items import ClubDetailItem


class EPLClubSpider(scrapy.spider.BaseSpider):
    name = "epl-club"
    allowed_domains = ["premierleague.com"]
    start_urls = [
        "http://www.premierleague.com/en-gb/clubs.html"
    ]
    
    def parse(self, response):
        clubs = response.xpath('//ul/li[re:test(@class, "logo[0-9]+$")]//@href').extract()
        for c in clubs:
            url = "http://www.premierleague.com" + c.replace("profile.overview.html", "profile.statistics.html")

            yield scrapy.http.Request(url, callback=self.parse_club)


    def parse_club(self, response):
        
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


