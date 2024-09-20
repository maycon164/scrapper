from datetime import datetime

import scrapy

from games.games.items import GamesItem


class NuveemcardSpider(scrapy.Spider):
    name = "nuveemcard"
    allowed_domains = ["www.nuuvem.com"]
    start_urls = ["https://www.nuuvem.com/br-en/catalog/platforms/pc"]

    def parse(self, response):
        items = response.xpath("//div[@class='products-items']/div/div/div[@class='product-card--grid']");

        for item in items:
            game = GamesItem()
            game["title"] = item.css("h3.product-title::text").get()
            game["price"] = f"R$ {item.css("span.integer::text").get()}{item.css("span.decimal::text").get()}"
            game["image"] = item.css("div.product-img > img::attr(src)").get()
            game["discount_percentage"] = item.css("span.product-discount::text").get()
            game["platform"] = item.css("i.icon + span::text").getall()
            game["link_to_page"] = item.css("a.product-card--wrapper::attr(href)").get()
            game["origin"] = "NUUVEM"
            game["date_discovered"] = datetime.today()
            yield game
