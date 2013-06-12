import threading, ConfigParser, random, time, datetime
from twython import TwythonStreamer
import logging
import MongoDB
import Postgres

class MyStreamer(TwythonStreamer):
    
    def init_variables(self, tweetstream):
      self.tweetstream = tweetstream
      self.max_count = tweetstream.inserts + tweetstream.selects
      self.count = 0
      self.reads = 0
      self.writes = 0
  
    def on_success(self, data):
      
      before = datetime.datetime.now()
      
      if self.count < self.tweetstream.inserts:
        self.writes += 1
        self.tweetstream.add_to_database(data)
      else:
        self.reads += 1
        self.tweetstream.query_database()
      after =  datetime.datetime.now()
      delta = after - before
      self.tweetstream.response_data.append(delta.total_seconds())
      
      self.count += 1
      
      if self.count == self.max_count:
        self.disconnect()

    def on_error(self, status_code, data):
        self.tweetstream.logger.log(status_code, data)

class TweetStream(threading.Thread):
  
  def __init__(self, logger, inserts, selects, database, config):
    
    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')
    
    self.app_key = config.get('twitter','app_key')
    self.app_secret = config.get('twitter', 'app_secret')
    self.oauth_token = config.get('twitter', 'oauth_token')
    self.oauth_token_secret = config.get('twitter', 'oauth_token_secret')
    
    self.selects = selects
    self.inserts = inserts
    self.probability_tracker = 0
    self.database = database
    self.response_data = []
    self.logger = logger
    self.streamer = MyStreamer(self.app_key, self.app_secret, self.oauth_token, self.oauth_token_secret)
    threading.Thread.__init__(self)
  
  def get_file_name(self):
    return   './logs/'+str(datetime.datetime.now())+'-'+self.database.to_string()\
    +'-read-'+str(self.selects)+'-write-'+str(self.inserts)+'.log'
  
  def run(self):
    self.streamer.init_variables(self)
    self.logger.log("Starting to stream tweets from Twitter")
    self.streamer.statuses.sample()
    
    self.file = open(self.get_file_name(), 'w')
    self.logger.log("Database queries complete")
    self.logger.log("Conducted " +str(self.streamer.reads) + " reads and " + str(self.streamer.writes) +" writes.")
    self.logger.log_to_file(self.file, str(self.response_data).replace('[', '').replace(']', '').replace(' ', '').replace(',','\n'))
    self.logger.log("Average response time: "+str(sum(self.response_data)/len(self.response_data)))
        
  def put_tweet_in_database(self):
    r = random.random()
    return r <= self.probability
      
  def add_to_database(self, data):
    self.database.add_tweets(data)
  
  def query_database(self):
    self.database.query_database()
  
def get_instance(logger, inserts, selects, database, config):
  return TweetStream(logger, inserts, selects, database, config)

if __name__ == "__main__":
  m = MongoDB.initialize()
  p = Postgres.initialize()
  t = TweetStream(logging, 100, 100 , m)
  t.run()