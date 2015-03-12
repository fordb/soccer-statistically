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
            club = ClubPageItem()
            club["title"] = url.split("/")[-1]
            club["link"] = url
            yield club

            yield scrapy.http.Request(url, callback=self.parse_club)


    def parse_club(self, response):
        
        club = ClubDetailItem()
        name = response.xpath('//div[@class="overlay"]/h2[@class="noborder"]/text()').extract()
        played = response.xpath('//li[@name="played"]/div[@class="data"]/text()').extract()

        club["url"] = response.url
        club["name"] = name
        club["gp"] = played

        yield club


