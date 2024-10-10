import re
from xml.sax import parse

import pymongo
from typing import List

from model.item import ItemScraped


class ItemsScrapedRepository:
    collection = None
    page_size = 20

    def __init__(self, uri, database):
        client = pymongo.MongoClient(uri)
        self.collection = client[database]['items']

    def get_all_by_params(self, name:str, min_price:float, max_price:float, platforms:List[str], origin:str, page:int):
        query:dict = {}

        self.handle_platforms(platforms, query)
        self.handle_min_max_price(min_price, max_price, query)
        self.handle_title(name, query)
        self.handle_origin(origin, query)

        print(query)

        skip = self.page_size * page if page is not 1 else 0

        return self.parse_mongo_response(self.collection.find(query)
                                         .skip(skip).limit(self.page_size))

    def handle_origin(self, origin: str, query:dict):
        if origin is not None:
            query["origin"] = {"$eq": origin}

    def handle_platforms(self, platforms:List[str], query:dict):
        if platforms:
            query["platforms"] = {"$in": platforms}

    def handle_title(self, title:str, query:dict):
        if title is not None:
            query["title"] ={ "$regex" : f"^{title}", "$options": "i"}

    def handle_min_max_price(self, min_price:float, max_price:float, query:dict) :
        if min_price is not None and max_price is not None:
            query["price"] = {"$gte": min_price, "$lte": max_price}
            return

        if min_price is not None:
            query["price"] = {"$gte": min_price}

        if max_price is not None:
            query["price"] = {"$lte": max_price}



    def get_all_by_title(self, name):
        query = {"title": { "$regex" : f"^{name}", "$options": "i"}} ### ^ -> search at the beginning of the string, i -> case-insensitive
        return self.parse_mongo_response(self.collection.find(query))

    def parse_mongo_response(self, response):
        return list(map(self.to_item_scrapped, response))

    def to_item_scrapped(self, mongo_result):
        return ItemScraped(
            mongo_result["title"],
            mongo_result["price"],
            mongo_result["origin"],
            mongo_result["platforms"],
            mongo_result["discount_percentage"],
            mongo_result["image"],
            mongo_result["link_to_page"])


