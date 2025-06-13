import os
import libtorrent as lt
import logging
import time
from pymongo import MongoClient
from pyromod import listen
import asyncio
from logging.handlers import RotatingFileHandler
from pyrogram import Client

class Config(object):
  BOT_TOKEN = str("")
  API_ID = int()
  API_HASH = str("")
  DOWNLOAD_LOCATION = str("bot/downloads/")
  LOG_CHANNEL = "Ongoing_Animes_480p"
  UPDATES_CHANNEL = "FIERCENETWORK"
  DOWNLOAD_DIR = "downloads/"
  AUTH_USERS = [5703071595]
  BOT_USERNAME = "LOL_BOT"
  SESSION_STRING = ""
  DATABASE_URL = ''
  
cluster = MongoClient(Config.DATABASE_URL)
db = cluster[Config.BOT_USERNAME]
collection = db["data"]
queue = db["queue"]
channels = db["channels"]
  
LOG_FILE_NAME = f"BOT@Log.txt"

if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=2097152000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
LOGS = logging.getLogger(__name__)  

bot = Client("Airing", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

if not Config.DOWNLOAD_DIR.endswith("/"):
  Config.DOWNLOAD_DIR = str() + "/"
if not os.path.isdir(Config.DOWNLOAD_DIR):
  os.makedirs(Config.DOWNLOAD_DIR)
  
os.makedirs('torrent/')  
ses = lt.session()
ses.listen_on(6881, 6891)
