from bot import collection, queue, Config, LOGS
import pymongo, ast
from .plugins.helper import get_first_title
list_handler = []
db_data = []

def pgk():
  if collection.find_one({'_id' : Config.AUTH_USERS[0]}):
    LOGS.info("YES")
  else:
    title = get_first_title()
    collection.insert_one({'_id' : Config.AUTH_USERS[0], 'title' : title})
    
def get_latest_anime():
 b = collection.find_one({'_id' : Config.AUTH_USERS[0]})
 return b["title"]

def update_latest_anime(title):
   myquery = {'_id' : Config.AUTH_USERS[0]}
   newquery = {'$set': { 'title': title }}
   collection.update_one(myquery, newquery)

def napana():
  queries = queue.find({})
  for query in queries:
   que = str(query["queue"])
   b = ast.literal_eval(que)
   if not query["_id"] in list_handler: 
    list_handler.append(query["_id"])
   if not b in db_data:
    db_data.append(b)
