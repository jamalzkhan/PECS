import tweetstream, threading, ConfigParser, random, time, datetime
import logging
import MongoDB
import Postgres

class TweetStream(threading.Thread):
  
  def __init__(self, logger, inserts, selects, database, config):
    
    self.twitter_username = config.get('twitter','username')
    self.twitter_password = config.get('twitter','password')
    self.selects = selects
    self.inserts = inserts
    self.probability_tracker = 0
    self.database = database
    self.response_data = []
    self.logger = logger
    threading.Thread.__init__(self)
  
  def get_file_name(self):
    return   './logs/'+str(datetime.datetime.now())+'-'+self.database.to_string()\
    +'-read-'+str(self.selects)+'-write-'+str(self.inserts)+'.log'
  
  def run(self):
    self.logger.log("Starting to stream tweets from Twitter")
    self.file = open(self.get_file_name(), 'w')
    self.stream  = tweetstream.SampleStream(self.twitter_username, self.twitter_password)
    
    max_queries = self.inserts + self.selects
    count = 0
    reads = 0
    writes = 0
    for tweet in self.stream:
      before = datetime.datetime.now()
      #if self.put_tweet_in_database():
      if count < self.inserts:
        writes += 1
        self.add_to_database(tweet)  
      else:
        reads += 1
        #self.query_database()
      after =  datetime.datetime.now()
      delta = after - before
      count += 1
      #logger.(str(delta.total_seconds()) + ", ")
      self.response_data.append(delta.total_seconds())
      if count == max_queries:
        break
    self.logger.log("Database queries complete")
    self.logger.log("Conducted " +str(reads) + " reads and " + str(writes) +" writes.")
    self.logger.log_to_file(self.file, str(self.response_data))
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