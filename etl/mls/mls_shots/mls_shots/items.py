# -*- coding: utf-8 -*-
import scrapy


class GameShotsItem(scrapy.Item):
    x1 = scrapy.Field()
    x2 = scrapy.Field()
    y1 = scrapy.Field()
    y2 = scrapy.Field()
    outcome = scrapy.Field()
    team = scrapy.Field()
    shot_id = scrapy.Field()
    game_id = scrapy.Field()
