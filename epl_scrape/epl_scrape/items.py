# -*- coding: utf-8 -*-
import scrapy


class ClubPageItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()


class ClubDetailItem(scrapy.Item):
    name = scrapy.Field()
    gp = scrapy.Field()
    wins = scrapy.Field()
    draws = scrapy.Field()
    losses = scrapy.Field()
    gf = scrapy.Field()
    ga = scrapy.Field()
    pk_goals = scrapy.Field()
