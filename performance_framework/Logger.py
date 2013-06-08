import logging

class Logger:
  
  def __init__(self, logging, name ,extention=".log"):
    self.extension=".log"
    self.format = '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
    self.config = logging.basicConfig(format=self.format, level=logging.INFO)
    self.logger = logging.getLogger(name)
    
  def log(self, message):
    """Logging a message to the console"""
    self.logger.info(message)

  def log_to_file(self, file, data):
    """Logging certain data to a file, the data should be a string"""
    file.write(data)

def initialize(name):
  return Logger(logging, name)
  
if __name__ == "__main__":
  l = initialize("test")
  l.log("this is soo cool")