import httplib, datetime, urllib

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
    self.post_data = self.get_post_data(config)
    
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
    self.http_connection.request("POST", '/'+request_url, urllib.urlencode(data))
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
        res = self.get_request(self.get_url).read()
      else:
        params = urllib.urlencode(self.post_data)
        res = self.post_request(self.post_url, self.post_data).read()
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
    res = s.get_request("/").read()
    #print res.status, res.reason
    after =  datetime.datetime.now()
    delta = after - before
    response_data.append(delta.total_seconds())
  
  print response_data
  s.disconnect()