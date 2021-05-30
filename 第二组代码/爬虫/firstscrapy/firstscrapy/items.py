# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    museum= scrapy.Field()
    author= scrapy.Field()
    # description= scrapy.Field()
    detail_url= scrapy.Field()
    time= scrapy.Field()
    content = scrapy.Field()
    pass
