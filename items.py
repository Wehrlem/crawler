# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlerItem(Item):
    url = Field()
    site = Field()
    author = Field()
    texts = Field()
    time = Field()
    crawltime = Field()
    source = Field()
    location = Field()
    identifer = Field()
    key = Field()