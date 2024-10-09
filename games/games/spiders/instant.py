import scrapy

from games.items import GamesItem
from datetime import datetime

class InstantSpider(scrapy.Spider):
    name = "instant"
    allowed_domains = ["www.instant-gaming.com"]
    start_urls = ["https://www.instant-gaming.com/en/search/?platform[0]=pc&type[0]=steam&sort_by=bestsellers_desc&version=2&h=1&d=bestsellers&page=1"]

    def parse(self, response):
        items = response.css('div.listing-items > div.item')
        
        for item in items:
            register = GamesItem()
            
            register['title'] = item.css('div.name > span::text').get()
            price = item.css('div.price::text').get()
            register['price'] = float(price.replace("R$", "").strip()) if price is not None else None
            register['image'] = item.css('img.picture::attr(data-src)').get()
            register['discount_percentage'] = item.css('div.discount::text').get()
            register['link_to_page'] = item.css('a::attr(href)').get()
            register['platforms'] = ['Steam']
            register['origin'] = "INSTANT GAMING"
            register["date"] = datetime.today()            
            yield register
            
            
        current_page = int(response.css('ul.pagination > li.selected::text').get())
        
        if current_page == 2:
            return
        
        page_number = current_page + 1
        next_page_url = f'https://www.instant-gaming.com/en/search/?platform[0]=pc&type[0]=steam&sort_by=bestsellers_desc&version=2&h=1&d=bestsellers&page={str(page_number)}'
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    
