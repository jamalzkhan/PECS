class ApacheLogReader:
  
  def __init__(self, file_name):
    self.file_name = file_name
    self.file = self.open_file(file_name)
    
  def open_file(self, file_name):
    return open(file_name)
  
  def parse_file(self):
    count = 0
    for line in self.file:
      print line
      count += 1
      if count == 10:
        break
    
    
if __name__ == "__main__":
  name = "access.log"
  a =  ApacheLogReader(name)
  a.parse_file()