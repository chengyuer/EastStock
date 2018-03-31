# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import pymongo

class ExamplePipeline(object):
    def __init__(self):
        myCon = pymongo.MongoClient(host='127.0.0.1',port=27017)
        db = myCon['stockRedis']
        self.col = db['data']
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        self.col.insert({'num': item['num'], 'name': item['name'], 'sentimentScore': item['sentimentScore'],
                         'confidenceScore': item['confidenceScore'], 'positiveScore': item['positiveScore'],
                         'negativeScore': item['negativeScore']})
        return item
