import tweetstream, threading, ConfigParser, random, time, datetime
import logging
import MongoDB
import Postgres

class TweetStream(threading.Thread):
  
  def __init__(self, log, probability, database):
    
    config = ConfigParser.RawConfigParser()
    config.read('config.conf')
    
    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')
    self.probability = probability
    self.probability_tracker = 0
    self.database = database
    self.response_data = []
  
  def run(self, time_limit):
    self.stream  = tweetstream.SampleStream(self.twitter_username, self.twitter_password)
    adding = 0
    not_adding = 0
    max_count = 1000
    count = 0
    for tweet in self.stream:
      count += 1
      #before = time.mktime(datetime.datetime.now().timetuple()) * 1000
      before = datetime.datetime.now()
      #print "%20f"%before
      if self.put_tweet_in_database():
        self.add_to_database(tweet)  
      else:
        self.query_database()
      after =  datetime.datetime.now()
      delta = after - before
      self.response_data.append(delta.total_seconds())
      if count == 1000:
        break
    print sum(self.response_data)/len(self.response_data)
        
  def put_tweet_in_database(self):
    r = random.random()
    return r <= self.probability
      
  def add_to_database(self, data):
    self.database.add_tweets(data)
  
  def query_database(self):
    self.database.query_database()

if __name__ == "__main__":
  m = MongoDB.initialize()
  p = Postgres.initialize()
  t = TweetStream(logging, 1.0 , m)
  t.run(None)