from typing import List

class ItemScraped:
    name:str
    price:float
    origin:str
    platforms: List[str]
    discount: str
    image: str
    link: str


    def __init__(self, name, price, origin, platforms, discount, image, link):
        self.name = name
        self.price = price
        self.origin = origin
        self.platforms = platforms
        self.discount = discount if discount is not None else ""
        self.image = image
        self.link = link

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "origin": self.origin,
            "platforms": self.platforms,
            "discount": self.discount,
            "image": self.image,
            "link": self.link
        }