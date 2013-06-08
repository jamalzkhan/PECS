import tweetstream, threading, ConfigParser, random, time, datetime
import logging
import MongoDB
import Postgres

class TweetStream(threading.Thread):
  
  def __init__(self, logger, inserts, selects, database):
    
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    
    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')
    self.selects = selects
    self.inserts = inserts
    self.probability_tracker = 0
    self.database = database
    self.response_data = []
    self.logger = logger
  
  
  def get_file_name(self):
    return   './logs/'+str(datetime.datetime.now())+'-'+self.database.to_string()+'-read-'+str(self.selects)+'-write-'+str(self.inserts)+'.log'
  
  def run(self, time_limit):
    self.logger.log("Starting to stream tweets from Twitter")
    self.file = f = open(self.get_file_name(), 'w')
    self.stream  = tweetstream.SampleStream(self.twitter_username, self.twitter_password)
    
    max_queries = self.inserts + self.selects
    count = 0
    for tweet in self.stream:
      count += 1
      before = datetime.datetime.now()
      #if self.put_tweet_in_database():
      if count < self.inserts:
        self.add_to_database(tweet)  
      else:
        self.query_database()
      after =  datetime.datetime.now()
      delta = after - before
      #logger.(str(delta.total_seconds()) + ", ")
      self.response_data.append(delta.total_seconds())
      if count == max_queries:
        break
    self.logger.log("Database queries complete")
    self.logger.log("Average response time: "+str(sum(self.response_data)/len(self.response_data)))
        
  def put_tweet_in_database(self):
    r = random.random()
    return r <= self.probability
      
  def add_to_database(self, data):
    self.database.add_tweets(data)
  
  def query_database(self):
    self.database.query_database()
  
def get_instance(logger, inserts, selects, database):
  return TweetStream(logger, inserts, selects, database)

if __name__ == "__main__":
  m = MongoDB.initialize()
  #p = Postgres.initialize()
  t = TweetStream(logging, 100, 100 , m)
  t.run(None)