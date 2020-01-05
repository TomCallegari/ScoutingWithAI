
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from Prospects.items import MetaItem, RegularSeasonItem

class MetaDataPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_METADATA_COLLECTION']]

    def process_item(self, item, spider):
        if not isinstance(item, MetaItem):
            return item
        self.collection.insert(dict(item))

class RegularSeasonPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_PLAYERSTATS_COLLECTION']]

    def process_item(self, item, spider):
        if not isinstance(item, RegularSeasonItem):
            return item
        self.collection.insert(dict(item))