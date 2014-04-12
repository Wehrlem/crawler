from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from testspiders.spiders.followall import FollowAllSpider
from scrapy.utils.project import get_project_settings

def setup_crawler():
    spider = HolidayForumSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

setup_crawler()
log.start()
reactor.run()