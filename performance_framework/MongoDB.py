import  pymongo, datetime, json, bson, hashlib
from dateutil import parser
import logging

class MongoDB:
  
  def __init__(self, db, collection, logger):
    self.logger = logging
    self.logger.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    self.setup(db, collection)

  def setup(self, database, collection):
    self.logger.info('Database connection initialized.')
    self.client = pymongo.MongoClient()
    self.db = self.client[database]
    self.collection = self.db[collection]
    self.logger.info('Connected to the database.')
    
  def add_tweets(self, tweet):
    data = tweet
    self.db["tweets"].insert(data)
    
  def query_database(self):
    self.db["tweets"].find()
    
  def get_logs(self):
    logs = self.collection.find()
    return logs
      
  def get_average_for_attribute(self, data, field='millis'):
    count = 0.0
    avg_sum = 0.0
    for log in data:
      count += 1
      avg_sum += log[field]  
    return avg_sum / count

def initialize():
  return MongoDB("test", 'tweets', logging)

if __name__ == "__main__":  
  d = MongoDB()
  d.setup(database='test', collection='system.profile')
  logs = d.get_logs()
  avg = d.get_average_for_attribute(data=logs)
  print "Average response time for queries: " + str(avg) + " mills"