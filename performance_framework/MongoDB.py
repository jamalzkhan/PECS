import  pymongo, datetime, json, bson, hashlib, ConfigParser
import logging

class MongoDB:
  
  def __init__(self, logger):
    self.logger = logger
    
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    db = config.get('database', 'dbname')
    collection = config.get('database', 'testtable')
    
    self.setup(db, collection)

  def setup(self, database, collection):
    self.logger.log('Database connection initialized.')
    self.client = pymongo.MongoClient()
    self.db = self.client[database]
    self.collection = self.db[collection]
    self.logger.log('Connected to the database.')
    
  def to_string(self):
    return "mongo"
    
  def add_tweets(self, tweet):
    data = tweet
    self.collection.insert(data)
    
  def query_database(self):
    self.collection.find()
    
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

def initialize(config, logger):
  return MongoDB(logger)

if __name__ == "__main__":  
  d = MongoDB()
  d.setup(database='test', collection='system.profile')
  logs = d.get_logs()
  avg = d.get_average_for_attribute(data=logs)
  print "Average response time for queries: " + str(avg) + " mills"