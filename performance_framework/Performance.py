import TweetStream, MongoDB, Postgres, Logger, ConfigParser
from optparse import OptionParser

class Performance:
  
  def __init__(self, streamer, database, inserts, selects):
    self.streamer = streamer
    self.database = database
    self.inserts = inserts
    self.selects = selects
  
def setup_parser(parser):
  # Parser for the database options
  parser.add_option("-d", "--database", help="choose the database type")
  parser.add_option("-i", type="int", dest="inserts", help="number of inserts to do in the database")
  parser.add_option("-s", type="int", dest="selects", help="number of select queries to execute")
  
  # Parser for the HTTP server options
  parser.add_option("-u", "--url", help="path of the webserver")
  parser.add_option("-p", "--port", help="please give the port of the webserver, default 80")
  return parser

def get_database(database_string, config):
  database = None
  if database_string=="mongo":
    database = MongoDB.initialize(config)
  elif database_string=="postgres":
    database = Postgres.initialize(config)
  return database
  
def check_int_field(field):
  if field == None:
    return 0
  return field

def main():
  parser = setup_parser(OptionParser())
  (options, args) = parser.parse_args()
  
  # Parsing all the options (for the database and webserver)
  database_string = options.database
  inserts = options.inserts
  selects = options.selects
  
  url = options.url
  port = options.port
  
  # Configuration, which is derived from a specificc file
  config = ConfigParser.RawConfigParser()
  config.read('config.conf')
  
  database = get_database(database_string, config)
  if database == None:
    print "Something went wrong"
    
  inserts = check_int_field(inserts)
  selects = check_int_field(selects)
  
  logger = Logger.initialize('performance')
  streamer = TweetStream.get_instance(logger, inserts, selects, database, config)
  
  logger.log("Initalized tool, connecting to " + database.to_string() + " and performing " +str(inserts)+" writes and " + \
  str(selects) + " reads.")
  
  # Running the streamer
  streamer.run(None)

if __name__ == "__main__":
  main()