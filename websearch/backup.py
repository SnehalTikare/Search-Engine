import scrapy
from ..items import WebsearchItem


class WebsearchSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
       'http://quotes.toscrape.com/'
    ]
    def parse(self,response):
        items = WebsearchItem()
        all_div_quotes = response.css("div.quote")
        for quotes in all_div_quotes:
            title = quotes.css("span.text::text").extract()
            author = quotes.css(".author::text").extract()
            tags = quotes.css(".tag::text").extract()
            items['title'] = title
            items['author'] = author
            items['tags'] = tags
            yield items


#### items.py

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebsearchItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    
###### pipelines.py
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class WebsearchPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("myquotes.db")
        self.curr =  self.conn.cursor()

    def create_table(self):
        self.curr.execute(""" DROP TABLE IF EXISTS quotes_db""")
        self.curr.execute("""create table quotes_db
        (title text, 
        author text,
        tag text
        )""")
 
    def process_item(self, item,spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute(""" insert into quotes_db values(?,?,?)""",(
        item['title'][0],
        item['author'][0],
        item['tags'][0]
        ))
        self.conn.commit()
