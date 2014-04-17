from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from crawler.items import CrawlerItem
import re
import codecs
from crawler.functions import getIdentifier
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from pymongo import MongoClient
from scrapy.exceptions import DropItem

class TagiCommentsSpider(Spider):
    name = "tagicomments"
    allowed_domains = [ "tagesanzeiger.ch"]
    client = MongoClient()
    db = client.ktidashboard
    items = db.crawler
    urls = items.distinct('url')
    y = [s +'?comments=1' for s in urls if 'tagesanzeiger' in s]
    stored = items.distinct('identifer')
    start_urls = y
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        hasdiscus = hxs.select('//div[@class="noTalkback"]')
        if not hasdiscus:   
            items = []
            text = hxs.select('//div[@class="komment"]/p/span').extract()
            user = hxs.select('//div[@class="kommentLeft"]/h4/text()').extract()
            time =hxs.select('//div[@class="kommentTime"]/text()').extract()
            if text:
                for i in range(0,len(text)):
                    dates = datetime.strptime(time[i][:-12], '%d.%m.%Y').strftime('%Y-%m-%d')
                    texts =''.join(BeautifulSoup(text[i]).findAll(text=True))
                    texts = texts.strip()
                    indeti =  getIdentifier(texts,dates)
                    item = CrawlerItem()
                    item['url'] = response.url
                    item['texts'] = text[i]
                    item['time'] = dates
                    item['author'] =  user[i]
                    item['source'] = 'Comments'
                    item['site'] = 'Tagesanzeiger'
                    item['location'] = 'Schweiz'
                    item['identifer'] =  indeti
                    item['crawltime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if (indeti not in self.stored):
                        self.stored.append(indeti)
                        items.append(item)
                return items
    