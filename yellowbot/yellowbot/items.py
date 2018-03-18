# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YellowbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    postal = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()

