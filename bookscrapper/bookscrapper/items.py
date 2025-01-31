# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BookscrapperItem(Item):
    # define the fields for your item here like:
    name = Field()
    pass

class BookItem(Item):
    # define the fields for your item here like:
    url = Field()
    title = Field()
    category = Field()
    description = Field()
    price = Field()
    stock = Field()
    stars = Field()
    reviews = Field()
    tax = Field()
    product_type = Field()
    price_excl_tax = Field()
    price_incl_tax = Field()
