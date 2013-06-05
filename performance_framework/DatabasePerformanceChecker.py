import  pymongo
import datetime
import logging

class DatabasePerformanceChecker:
  
  def __init__(self, name=""):
    self.name = name
    
    self.connection = None
    self.db = None
    self.collection = None
    self.logger = logging
    self.logger.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    self.logger.info('Initialized '+ name + ' performance checker')

  def setup(self, database, collection):
    self.logger.info('Database connection initialized.')
    self.client = pymongo.MongoClient()
    self.db = self.client[database]
    self.collection = self.db[collection]
    self.logger.info('Connected to the database.')
    
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

if __name__ == "__main__":  
  d = DatabasePerformanceChecker("mongodb")
  d.setup(database='test', collection='system.profile')
  logs = d.get_logs()
  avg = d.get_average_for_attribute(data=logs)
  print "Average response time for queries: " + str(avg) + " mills"