import httplib, datetime, urllib, threading
import Logger, ConfigParser
from shared import shared

class ServerConnection(threading.Thread):
  
  def __init__(self, url, port, gets, puts, logger, config, file):
    self.url = url
    self.port = port
    self.http_connection = httplib.HTTPConnection(url, port)
    self.gets = gets
    self.puts = puts
    self.logger = logger
    self.get_url = config.get('http','get')
    self.post_url = config.get('http','post')
    self.post_data = self.get_post_data(config)
    self.shared = shared
    self.file = file
    threading.Thread.__init__(self)
    
  def get_post_data(self, config):
    items = config.items('post')
    post_data = {}
    for (option, value) in items:
      post_data[option] = value
    return post_data
    
  def connect(self):
    self.http_connection.connect()

  def disconnect(self):
    self.http_connection.close()
  
  def get_request(self, request_url):
    self.http_connection.request("GET", '/'+request_url)
    return self.http_connection.getresponse()
    
  def post_request(self, request_url, data):
    headers = {"Content-type":"application/json", "Accept": "text/plain"}
    self.http_connection.request("POST", '/'+request_url, urllib.urlencode(data), headers)
    return self.http_connection.getresponse()
  
  def get_file_name(self):
     return './logs/'+str(datetime.datetime.now())+'-'+self.url \
      +'-gets-'+str(self.gets)+'-puts-'+str(self.puts)+'.log'

  def run(self):
    #self.file = open(self.get_file_name(), 'w')
    self.connect()
    response_data = []
    gets = 0
    post = 0
    for i in range(0, self.gets+self.puts):
      before = datetime.datetime.now()
      if i < self.gets:
        gets += 1
        res = self.get_request(self.get_url).read()
      else:
        post += 1
        params = urllib.urlencode(self.post_data)
        res = self.post_request(self.post_url, self.post_data).read()
      #print res.status, res.reason
      after =  datetime.datetime.now()
      delta = after - before
      response_data.append(delta.total_seconds())
    #self.shared += response_data
    print len(response_data)
    self.logger.log_to_file(self.file, str(response_data).replace('[', '').replace(']', '')+",")
    self.logger.log("Conducted " + str(gets) + " get requests and " + str(post) + " post requests.")

def initialize(url, port, gets, posts, logger, config, file):
  s = ServerConnection(url, port, gets, posts, logger, config, file)
  return s

if __name__ == "__main__":
  c = ConfigParser.RawConfigParser()
  c.read('config.conf')
  s = initialize("localhost", 3000, 10, 0, Logger.initialize("test"), c)
  s.run()
  s.disconnect()