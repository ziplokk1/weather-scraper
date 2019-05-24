# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    time = scrapy.Field()
    weather = scrapy.Field()
    imgurl = scrapy.Field()
    county = scrapy.Field()
    state = scrapy.Field()
    matchtext = scrapy.Field()
    date = scrapy.Field()
