# here are all the functions for the crawlers
from pymongo import MongoClient

def getIdentifier(input,date):
        if type(input).__name__=='list':
            input = ''.join(input)
        input = input.strip()
        identifier = input[:10] + date 
        return identifier.replace(" ", "")
    
    
def getKeywords(location):
    client = MongoClient()
    db = client.ktidashboard
    items = db.keywords
    if location == "":
        print 'all you need is loveall'
    return  ['tourism']