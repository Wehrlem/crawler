# -*- coding: utf-8 -*-
from TwitterSearch import *
import MySQLdb as db
from pymongo import MongoClient
from functions import getIdentifier
from datetime import datetime
import re
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.setKeywords(['Tourismus']) # let's define all words we would like to have a look for
    tso.setLanguage('de') # we want to see German tweets only
    tso.setCount(2) # please dear Mr Twitter, only give us 7 results per page
    tso.setIncludeEntities(False) # and don't give us all those entity information
    #Set up the mysql connection
    conn = db.connect('localhost','don', 'marcello_1664', 'knowz')
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    #Set up the mongo connection
    client = MongoClient()
    db = client.ktidashboard
    items = db.crawler
    stored = items.distinct('identifer')


    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'Z3rU3WMQnvg5xUsox7Rfg',
        consumer_secret = 'yQGMdqA9M25V5g2tsmg6GPdZuR9dr73chErWBx94Jk',
        access_token = '216641262-67CaLeYKWOPz54qObHHe9UESTlncdMyEP4zhl0bI',
        access_token_secret = 'H827lhCwUQka9TiMG7IwSAJkHVBC3f9DG78sy8uNA'
     )

    for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
        url = ''
        try:
            url = re.search("(?P<url>https?://[^\s]+)", tweet['text']).group("url")
        except:
            pass
        time = tweet['created_at']
        time = tweet['created_at'][4:] 
        time = time[:15] + time[-5:]
        fmt = "%b %d %H:%M:%S %Y"
        time = datetime.strptime(time, fmt).strftime('%Y-%m-%d %H:%M:%S')
        crawltime= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        indeti =  getIdentifier(tweet['text'],time)
        if (indeti not in stored):
            cursor.execute("""INSERT INTO webcrawler (url,site,author,texts,time,crawltime,source,location) VALUES (%s, %s, %s, %s,%s, %s, %s,%s)""" , (url,'Twitter',tweet['user']['screen_name'].encode('utf-8'),tweet['text'].encode('utf-8'),time,crawltime,'tweet','world'))
            conn.commit()
            tweet = {"source": "tweet", "author":tweet['user'],"site":"Twitter","texts": tweet['text'],"location":"welt", "time": time, "crawltime":crawltime, "identifer":indeti }
            items.insert(tweet)
            stored.append(indeti)


except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)