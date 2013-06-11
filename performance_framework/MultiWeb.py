import ServerConnection, ConfigParser, Logger, datetime
from shared import shared

class MultiWeb:
  
  def __init__(self, url, port, gets, posts, logger, config, thread_count):
    self.url = url
    self.port = port
    self.gets = gets
    self.posts = posts
    self.logger = logger
    self.config = config
    self.thread_count = thread_count
    self.file = open(self.get_file_name(), 'w')
  
  def get_file_name(self):
    return './logs/'+str(datetime.datetime.now())+'-'+self.url \
    +'-gets-'+str(self.gets)+'-puts-'+str(self.posts)+'.log'
    
  def run(self):
    for x in xrange(self.thread_count):
      s = ServerConnection.initialize(self.url, self.port, self.gets, self.posts, self.logger, self.config, self.file).start()
  
def initialize(url, port, gets, posts, logger, config, thread_count):
  return MultiWeb(url, port, gets, posts, logger, config, thread_count)
  
