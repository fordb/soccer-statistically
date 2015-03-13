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
        name = response.xpath('//div[@class="overlay"]/h2[@class="noborder"]/text()').extract()
        played = response.xpath('//li[@name="played"]/div[@class="data"]/text()').extract()
        wins = response.xpath('//li[@name="won"]/div[@class="data"]/text()').extract()
        draws = response.xpath('//li[@name="drawn"]/div[@class="data"]/text()').extract()
        losses = response.xpath('//li[@name="lost"]/div[@class="data"]/text()').extract()
        gf = response.xpath('//li[@name="goalsFor"][1]/div[@class="data"]/text()').extract()
        ga = response.xpath('//li[@name="goalsAgainst"]/div[@class="data"]/text()').extract()
        pk_goals = response.xpath('//li[@name="goalsFor"][2]/div[@class="data"]/text()').extract()
        club["name"] = name
        club["gp"] = played
        club["wins"] = wins
        club["draws"] = draws
        club["losses"] = losses
        club["gf"] = gf
        club["ga"] = ga
        club["pk_goals"] = pk_goals

        yield club


