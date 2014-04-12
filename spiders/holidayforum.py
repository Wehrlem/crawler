from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import CrawlerItem
import re
import codecs
from datetime import datetime
from crawler.functions import getIdentifier
from BeautifulSoup import BeautifulSoup
from pymongo import MongoClient
from scrapy.exceptions import DropItem

class HolidayForumSpider(BaseSpider):
    name = "holidayforum"
    allowed_domains = [ "holidaycheck.ch"]
    start_urls = ["http://www.holidaycheck.ch/forum-Schweiz-id_95.html"]
    client = MongoClient()
    db = client.ktidashboard
    items = db.crawler
    stored = items.distinct('identifer')
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="topicTitle floatLeft"]/a/@href')
        items = []
        items.extend([self.make_requests_from_url('http://www.holidaycheck.ch' + url.extract()).replace(callback=self.parse_forum) for url in sites])
        page_links=hxs.select('//span[@class="paginationNext"]/a')
        for link in page_links:
            url = 'http://www.holidaycheck.ch' + link.select('@href').extract()[0]
            items.append(self.make_requests_from_url(url))        
        return items
    def parse_forum(self, response):   
        hxs = HtmlXPathSelector(response)
        text = hxs.select('//div[@class="forumPostText"]').extract()
        
        time =  hxs.select('//div[@class="forumPostTitle"]/div[@class="floatRight"]/text()').extract()
        author = hxs.select('//div[@class="forumUsername"]/a/text()').extract()
        items = []
        for i in range(0,len(text)):
            texts =''.join(BeautifulSoup(text[i]).findAll(text=True))
            if time[i]: 
                thetime = time[i].strip()
                thetime = datetime.strptime(thetime, '%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            else:
                thetime= '2012-10-14 20:24:02'
            if getIdentifier(texts,thetime) in self.stored:
                raise DropItem("Duplicate item found")
            else:
                item = WebcrawlerItem()
                item['url'] = response.url
                item['texts'] =texts
                item['time'] = thetime
                item['author'] = author[i]
                item['source'] = 'forum'
                item['site'] = 'Holiday Check'
                item['location'] = 'Schweiz'
                item['crawltime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['identifer'] =  getIdentifier(texts, thetime)
                self.stored.append(getIdentifier(texts,thetime))
                items.append(item)
            return items
                
