from datetime import datetime

import scrapy

from games.items import GamesItem

class AmazonSwitchSpider(scrapy.Spider):
    name = "switch"
    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/s?k=jogos+de+switch"]

    def parse(self, response):
        
        items = response.css('div.s-result-item')

        for item in items:
            register = GamesItem()
            
            register['title'] = item.css('span.a-text-normal::text').get()
            register['price'] = item.css('span.a-price-whole::text').get()
            register['platforms'] = ['Switch']
            register["origin"] = "AMAZON"
            register["date"] = datetime.today()
        
        yield register;
