import  pymongo, datetime, json, bson, hashlib, psycopg2, ConfigParser
import math, random

class Postgres:
  
  def __init__(self,user, password, db, table, logger):
    self.logger = logger
    self.setup(db, table)
    self.db = db
    self.table = table
    self.user = user
    self.password = password

  def connect_to_database(self):
    self.connection = psycopg2.connect("dbname="+self.db+" user="+self.user+" password="+self.password)
    self.cur = self.connection.cursor()
    
  def to_string(self):
    return "postgresql"
    
  def disconnect(self):
    self.cur.close()
    self.connection.close()
    
  def create_table(self):
    query = "create table "+self.table+" (id bigserial primary key,json text)"
    self.cur.execute(query)
    self.connection.commit()
    
  def query_database(self):
    """Gets a random number between 0 and 100 and selects tweets from the database"""
    n = math.ceil(random.random() * 100)
    query = "select * from " + self.table + " limit " + str(int(n))
    self.cur.execute(query)
    s = self.cur.fetchone()
    
  def add_tweets(self, tweet):
    tweet_data = json.dumps(tweet)
    tweet_data = tweet_data.replace("'","")
    query = "insert into "+self.table+"(json) values (" +"'" + tweet_data + "')"
    self.cur.execute(query)
    self.connection.commit()
  
  def drop_table(self):
    query = "drop table tweets"
    self.cur.execute(query)
    self.connection.commit()

  def setup(self, database, collection):
    self.logger.log('Database connection initialized.')
    self.logger.log('Connected to the database.')
    
def initialize(config, logger):
  db = config.get('database', 'dbname')
  table = config.get('database', 'testtable')
  user = config.get('postgres', 'user')
  password = config.get('postgres', 'password')
  p = Postgres(user, password, db, table, logger)
  p.connect_to_database()
  #p.create_table()
  return p
    
if __name__ == "__main__":
  p = Postgres("test", "tweets", logging)
  p.connect_to_database()
  #p.create_table()
  p.disconnect()
