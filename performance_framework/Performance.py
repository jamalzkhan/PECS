import TweetStream, MongoDB, Postgres, logging
from optparse import OptionParser

class Performance:
  
  def __init__(self, streamer, database, inserts, selects):
    self.streamer = streamer
    self.database = database
    self.inserts = inserts
    self.selects = selects
  
def setup_parser(parser):
  parser.add_option("-d", "--database", help="choose the database type")
  parser.add_option("-i", type="int", dest="inserts", help="number of inserts to do in the database")
  parser.add_option("-s", type="int", dest="selects", help="number of select queries to execute")
  # parser.add_option("-l" "--limit", help="limit the number of records being inser")
  return parser

def get_database(database_string):
  database = None
  if database_string=="mongo":
    database = MongoDB.initialize()
  elif database_string=="postgres":
    database = Postgres.initialize()
  return database
  
def check_int_field(field):
  if field == None:
    return 0
  return field

def main():
  parser = setup_parser(OptionParser())
  (options, args) = parser.parse_args()
  
  # Parsing all the options
  database_string = options.database
  inserts = options.inserts
  selects = options.selects
  
  database = get_database(database_string)
  if database == None:
    print "Something went wrong"
    
  inserts = check_int_field(inserts)
  selects = check_int_field(selects)

  streamer = TweetStream.get_instance(logging, inserts, selects, database)
  streamer.run(None)

if __name__ == "__main__":
  main()