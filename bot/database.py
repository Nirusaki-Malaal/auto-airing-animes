from bot import collection, queue, Config, LOGS
import ast
from .plugins.helper import parse
list_handler = []
db_data = []

def pgk():
  if collection.find_one({'_id' : Config.AUTH_USERS[0]}):
    LOGS.info("YES")
  else:
    title = parse()[0]['title']
    collection.insert_one({'_id' : Config.AUTH_USERS[0], 'title' : title})
    
def get_latest_anime():
 b = collection.find_one({'_id' : Config.AUTH_USERS[0]})
 return b["title"]

def update_latest_anime(title):
   myquery = {'_id' : Config.AUTH_USERS[0]}
   newquery = {'$set': { 'title': title }}
   collection.update_one(myquery, newquery)

def clear_queue():
    queue.delete_many({})

def fetch():
  queries = queue.find({})
  for query in queries: 
   if not query["_id"] in list_handler: ## fetches ID of the object
    list_handler.append(query["_id"])
   if not ast.literal_eval(str(query["queue"])) in db_data: ## fetches the dictionary and appends it 
    db_data.append(ast.literal_eval(str(query["queue"])))

