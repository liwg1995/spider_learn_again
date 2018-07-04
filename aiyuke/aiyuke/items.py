# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AiyukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    datetime = scrapy.Field()
    content = scrapy.Field()
    cate = scrapy.Field()
    image_url = scrapy.Field()
