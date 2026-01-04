import os , logging
from pymongo import MongoClient
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from pyromod import listen
from dotenv import load_dotenv

## LOADING SECRETS IN THE ENVIRONMENT

if os.path.exists('config.env'):
  load_dotenv('config.env')

## STORING THOSE SECRETS INTO VARIABLES
class Config(object):
  BOT_TOKEN = str(os.environ.get("BOT_TOKEN"))
  API_ID = int(os.environ.get("API_ID"))
  API_HASH = str(os.environ.get("API_HASH"))
  LOG_CHANNEL = str(os.environ.get("LOG_CHANNEL"))
  UPDATES_CHANNEL = str(os.environ.get("UPDATES_CHANNEL"))
  DOWNLOAD_DIR = str(os.environ.get("DOWNLOAD_DIR"))
  DETAIL_CHANNEL = int(os.environ.get("DETAIL_CHANNEL"))
  AUTH_USERS = list(set(int(x) for x in os.environ.get("AUTH_USERS").split()))
  BOT_USERNAME = str(os.environ.get("BOT_USERNAME"))
  SESSION_STRING = str(os.environ.get("SESSION_STRING"))
  DATABASE_URL = str(os.environ.get("DATABASE_URL"))
  ROOT_DIRECTORY = os.getcwd()
  if not DOWNLOAD_DIR.endswith("/"):
      DOWNLOAD_DIR = str() + "/"


## CREATING DATABASE , Cluster , Collections , Queue Channels

cluster = MongoClient(Config.DATABASE_URL)
db = cluster[Config.BOT_USERNAME]
collection = db["data"]
queue = db["queue"]
channels = db["channels"]
  

## CREATING A LOGGER FILE And A LOGGER TO REPORT DATA

LOG_FILE_NAME = "BOT@Log.txt"

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


bot = Client(f"{Config.BOT_USERNAME}", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, workers=4)

if not os.path.isdir(f'{Config.ROOT_DIRECTORY}/{Config.DOWNLOAD_DIR}'):
      os.makedirs(f'{Config.ROOT_DIRECTORY}/{Config.DOWNLOAD_DIR}')  

if not os.path.isdir(f'{Config.ROOT_DIRECTORY}/torrent/'):
      os.makedirs(f'{Config.ROOT_DIRECTORY}/torrent/')  

if not os.path.isdir(f'{Config.ROOT_DIRECTORY}/encodes/'):
      os.makedirs(f'{Config.ROOT_DIRECTORY}/encodes/') 

if not os.path.isdir(f'{Config.ROOT_DIRECTORY}/temp/'):
      os.makedirs(f'{Config.ROOT_DIRECTORY}/temp/')   
