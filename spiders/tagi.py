from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from crawler.items import CrawlerItem
import re
import codecs
from crawlercrawler.functions import getIdentifier
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from pymongo import MongoClient
from scrapy.exceptions import DropItem

class TagiSpider(Spider):
    client = MongoClient()
    name = "tagi"
    allowed_domains = [ "tagesanzeiger.ch"]
    keywords = getKeywords(location="")
    for i in keywords:
        start_urls = ['http://www.tagesanzeiger.ch/ajax/tags.html?action=searchArticles&keyword='+i+'&pageId=%s&itemsPerPage=20&order=date' % page for page in xrange(1,100,1)]
    db = client.ktidashboard
    items = db.crawler
    stored = items.distinct('identifer')
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//h3/a/@href')
        items = []
        items.extend([self.make_requests_from_url('http://www.tagesanzeiger.ch' + url.extract()).replace(callback=self.parse_advisor) for url in sites])
        return items
    
    def parse_advisor(self, response):
        hxs = HtmlXPathSelector(response)
        text = hxs.select('//div[@id="singleLeft"]/p').extract()
        date = hxs.select('//p[@class="publishedDate"]/text()').extract()
        dates = date[0].replace('Erstellt: ','')
        dates = datetime.strptime(dates[:-11], '%d.%m.%Y').strftime('%Y-%m-%d')
        s = ""
        items = []
        for i in range(0,len(text)):
            texts = ''.join( BeautifulSoup( text [i]).findAll( text = True ))
            texts =texts.replace('var badword = 0;', '')
            texts =texts.replace('var badwordserch = 1;', '')
            texts =texts.replace(date[0], '')
            texts = texts.strip()
            s +=texts
        if s:
            indeti =  getIdentifier(s,dates)
            if (indeti in self.stored):
                raise DropItem("Duplicate item found")
            else:
                item = CrawlerItem()
                item['url'] = response.url
                item['texts'] = s 
                item['time'] = dates
                item['author'] = 'Tagi'
                item['source'] = 'Zeitung'
                item['site'] = 'Tagesanzeiger'
                item['location'] = 'Schweiz'
                item['identifer'] =  indeti
                item['crawltime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.stored.append(indeti)
                return item