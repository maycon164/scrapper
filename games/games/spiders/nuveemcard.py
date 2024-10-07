from datetime import datetime

import scrapy

from games.items import GamesItem


class NuveemSpider(scrapy.Spider):
    name = "nuvem"
    allowed_domains = ["www.nuuvem.com"]
    start_urls = ["https://www.nuuvem.com/br-en/catalog/platforms/pc"]

    def parse(self, response):
        items = response.xpath("//div[@class='products-items']/div/div/div[@class='product-card--grid']")

        for item in items:
            register = GamesItem()
            register["title"] = item.css("h3.product-title::text").get().strip()
            register["price"] = f'R$ {item.css("span.integer::text").get()}{item.css("span.decimal::text").get()}'
            register["image"] = item.css("div.product-img > img::attr(src)").get()

            percentage = item.css("span.product-discount::text").get()
            
            register["discount_percentage"] = int(percentage.strip().replace('%', '')) if percentage else 0
            register["platforms"] = list(filter(None, map(str.strip, item.css("i.icon + span::text").getall())))
            register["link_to_page"] = item.css("a.product-card--wrapper::attr(href)").get()
            register["origin"] = "NUUVEM"
            register["date"] = datetime.today()
            yield register

        current_page = int(response.css("a.pagination--item-active::text").get())

        if current_page == 10:
            return
                
        next_page_url = response.urljoin(f"/br-en/catalog/platforms/pc/page/{str(current_page + 1)}")
        print(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)
