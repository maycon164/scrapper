# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GamesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    discount_percentage = scrapy.Field()
    platforms = scrapy.Field()
    link_to_page = scrapy.Field()
    origin = scrapy.Field()
    date = scrapy.Field()
