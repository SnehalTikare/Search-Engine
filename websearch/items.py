# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebsearchItem(scrapy.Item):
    # define the fields for your item here like:
    origin_link = scrapy.Field()
    title = scrapy.Field()
    contents = scrapy.Field()
    outlinks = scrapy.Field()
    #contents_vt= scrapy.Field()
    #content= scrapy.Field()
    
    
