# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AzscoreItem(scrapy.Item):
    dataSourceCode = scrapy.Field()
    regionName = scrapy.Field()
    tournament = scrapy.Field()
    home = scrapy.Field()
    # homeScore = scrapy.Field()
    away = scrapy.Field()
    # awayScore = scrapy.Field()
    beginTime = scrapy.Field()
    sportName = scrapy.Field()
