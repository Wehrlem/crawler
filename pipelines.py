# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import nltk
import MySQLdb as db
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
import cPickle
import pymongo
from pymongo import MongoClient

class CrawlerPipeline(object):
    def __init__(self):
        self.conn = db.connect('localhost','don', 'Marcello_1664', 'knowz')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
    def process_item(self, item, spider):
        #if item['description']:
        #item['description'] = ' '.join(item['description']).lstrip()
        #tokens = nltk.word_tokenize(item['description'])
        #tokens =cPickle.dumps(tokens)
        try: 
            self.cursor.execute("""INSERT INTO webcrawler (url,site,author,texts,time,crawltime,source,location) VALUES (%s, %s, %s, %s,%s, %s, %s,%s)""" , (item['url'].encode('utf-8'),item['site'].encode('utf-8'),item['author'].encode('utf-8'),item['texts'].encode('utf-8'),item['time'],item['crawltime'],item['source'].encode('utf-8'),item['location'].encode('utf-8')))
            self.conn.commit()
        except db.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item
