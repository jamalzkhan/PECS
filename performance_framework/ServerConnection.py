import httplib, datetime

class ServerConnection:
  
  def __init__(self, url, port, gets, puts, logger, config):
    self.url = url
    self.port = port
    self.http_connection = httplib.HTTPConnection(url, port)
    self.gets = gets
    self.puts = puts
    self.logger = logger
    self.get_url = config.get('http','get')
    self.post_url = config.get('http','post')
    
  def connect(self):
    self.http_connection.connect()

  def disconnect(self):
    self.http_connection.close()
  
  def request(self, method, request_url):
    self.http_connection.request(method, request_url)
    return self.http_connection.getresponse()
  
  def get_file_name(self):
     return './logs/'+str(datetime.datetime.now())+'-'+self.url \
      +'-gets-'+str(self.gets)+'-puts-'+str(self.puts)+'.log'

  def run(self, time_limit):
    self.file = open(self.get_file_name(), 'w')
    self.connect()
    response_data = []
    for i in range(0, self.gets+self.puts):
      before = datetime.datetime.now()
      if i < self.gets:
        res = self.request("GET", self.get_url).read()
      else:
        res = self.request("POST", self.post_url).read()
      #print res.status, res.reason
      after =  datetime.datetime.now()
      delta = after - before
      response_data.append(delta.total_seconds())
    self.logger.log_to_file(self.file, str(response_data))

def initialize(url, port, gets, posts, logger, config):
  s = ServerConnection(url, port, gets, posts, logger, config)
  return s

if __name__ == "__main__":
  s = initialize('localhost', 1337, 100, 200, logger)
  response_data = []
  
  for i in range(0, s.gets):
    before = datetime.datetime.now()
    res = s.request("GET", "/").read()
    #print res.status, res.reason
    after =  datetime.datetime.now()
    delta = after - before
    response_data.append(delta.total_seconds())
  
  print response_data
  s.disconnect()