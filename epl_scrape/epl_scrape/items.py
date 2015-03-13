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
    shots = scrapy.Field()
    crosses = scrapy.Field()
    offsides = scrapy.Field()
    saves = scrapy.Field()
    own_goals = scrapy.Field()
    shutouts = scrapy.Field()
    blocks = scrapy.Field()
    clearances = scrapy.Field()
    fouls = scrapy.Field()
    cards = scrapy.Field()
