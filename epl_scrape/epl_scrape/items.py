# -*- coding: utf-8 -*-
import scrapy


class ClubPageItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()


class ClubDetailItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    gp = scrapy.Field()
    
