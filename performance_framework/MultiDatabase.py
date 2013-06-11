import TweetStream, ConfigParser, Logger, datetime, Postgres

class MultiDatabase:
  
  def __init__(self, logger, inserts, selects, database, config, thread_count):
    self.inserts = inserts
    self.selects = selects
    self.database = database
    self.logger = logger
    self.config = config
    self.thread_count = thread_count
    self.file = open(self.get_file_name(), 'w')
  
  def get_file_name(self):
    return   './logs/'+str(datetime.datetime.now())+'-'+self.database.to_string()\
    +'-read-'+str(self.selects)+'-write-'+str(self.inserts)+'.log'
    
  def run(self):
    for x in xrange(self.thread_count):
      s = TweetStream.get_instance(self.logger, self.inserts, self.selects, self.database, self.config).start()
  
def initialize(url, port, gets, posts, logger, config, thread_count):
  return MultiWeb(url, port, gets, posts, logger, config, thread_count)
  
if __name__ == "__main__":
  config = ConfigParser.RawConfigParser()
  config.read('config.conf')
  m = MultiDatabase(Logger.initialize('test'), 10, 0, Postgres.initialize(config), config, 10)
  m.run()