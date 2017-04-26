# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    subway = scrapy.Field()
    size = scrapy.Field()
    height = scrapy.Field()
    totalHeight = scrapy.Field()
    type = scrapy.Field()
    distance = scrapy.Field()
    price = scrapy.Field()
    pass
