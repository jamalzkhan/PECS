import tweetstream, threading, ConfigParser, random, time, datetime
import logging
import MongoDB
import Postgres

class TweetStream(threading.Thread):
  
  def __init__(self, log, inserts, selects, database):
    
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    
    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')
    self.selects = selects
    self.inserts = inserts
    self.probability_tracker = 0
    self.database = database
    self.response_data = []
  
  def run(self, time_limit):
    self.file = f = open('./logs/'+str(datetime.datetime.now())+'.log', 'w')
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
      self.file.write(str(delta.total_seconds()) + ", ")
      self.response_data.append(delta.total_seconds())
      if count == max_queries:
        break
    print sum(self.response_data)/len(self.response_data)
        
  def put_tweet_in_database(self):
    r = random.random()
    return r <= self.probability
      
  def add_to_database(self, data):
    self.database.add_tweets(data)
  
  def query_database(self):
    self.database.query_database()
  
def get_instance(logging, inserts, selects, database):
  return TweetStream(logging, inserts, selects, database)

if __name__ == "__main__":
  m = MongoDB.initialize()
  #p = Postgres.initialize()
  t = TweetStream(logging, 100, 100 , m)
  t.run(None)