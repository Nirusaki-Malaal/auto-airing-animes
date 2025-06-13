from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from bot import LOGS, Config
from AnilistPython import Anilist
from .search import shorten, airing_query, fav_query, anime_query, character_query, manga_query, GRAPHQL
import requests, shutil, os

# Anime Command
def user_anime(query):
 try:  
  anilist = Anilist()
  genre = ""
  b = anilist.get_anime(query)
  name = b["name_romaji"]
  eng_name = b["name_english"]
  image = b["banner_image"]
  genr = b["genres"]
  x = len(genr)  
  for i in range(0, x):
   genre = genre + f"#{genr[i]} "
  duration = "UNKNOWN"
  hashtag = f"#{b['airing_status']}"
  eps = b['airing_episodes']
  status = b['airing_status']
  score = b['average_score']
  return status, score, eps, hashtag, duration, genre, image, name, eng_name
 except Exception as e:
  return "NOTHING"

def anime_duration(anime):
 search = anime
 variables = {"search": search}
 json = requests.post(GRAPHQL, json={"query": anime_query, "variables": variables}).json()
 if "errors" in json:
  return None
 if json:
  json = json["data"]["Media"]
  id = json.get('id')
  mid = json.get('idMal')
  source = json['source'].capitalize()
  if "_" in source:
   source = source.replace("_", " ")
  duration = f"{json.get('duration', 'N/A')} Per Ep."
  image = f"https://img.anili.st/media/{id}"
  return image , duration
 
async def image_genre(query):
 search = query
 variables = {"search": search}
 json = requests.post(GRAPHQL, json={"query": anime_query, "variables": variables}).json()
 if "errors" in json:
  return None
 id = json['data']['Media']['id'] ##ID
 image = f"https://img.anili.st/media/{id}"
 genr = json['data']['Media']['genres'] ## GENRES
 genre = ''
 for i in range(0, len(genr)):
  genis = str(genr[i])
  if genis == "Sci-Fi":
   genis = genis.replace("-" ,"_")
  elif genis == "Slice of Life":
   genis = genis.replace(" ", "_")
  genre = genre + f"#{genis}, "
 return genre, image


async def uploadanime(bot, message):
 a = message.text
 b = a.split(' ',1)
 query = b[1]
 search = query
 variables = {"search": search}
 json = requests.post(GRAPHQL, json={"query": anime_query, "variables": variables}).json()
 if "errors" in json:
  return await message.reply_text("ANIME NOT FOUND")
 id = json['data']['Media']['id'] ##ID
 mid = json['data']['Media']['idMal']
 image = f"https://img.anili.st/media/{id}" ## IMAGE
 LOGS.info(image)
 duration = f"{json.get('duration', 'N/A')} Per Ep." ## DURATION of ep
 genr = json['data']['Media']['genres'] ## GENRES
 genre = ''
 x = len(genr)  
 for i in range(0, x):
  genre = genre + f"#{genr[i]} "
 romaji = json['data']['Media']['title']['romaji'] ## JAPANESE IN ENGLISH
 japanese = json['data']['Media']['title']['native'] ## NATIVE JAPANESE
 english = json['data']['Media']['title']['english'] ## ENGLISH NAME
 score = json['data']['Media']['averageScore']
 quality = '480p'
 episodes = json['data']['Media']['episodes']
 seasons = json['data']['Media']['seasonInt']
 status = json['data']['Media']['status']
 lang = await bot.ask(message.from_user.id, f"**Audio**")
 lang = lang.text
 hashtags = genre
 msg = f'**⚜️ {english}**\n🖥 Total Episodes {episodes}\n┏━━━━━━━━━━━━━━━━━\n┣🎵 AUDIO : {lang}\n┣🔖 Total Episodes : {episodes}\n┣⭐️ Rating : {score}\n┣📂 QUALITY : 480p\n┣⌛️ STATUS : {status}\n┣🎭 Genres : {genre}\n┗━━━━━━━━━━━━━━━━━'
 res = requests.get(image, stream = True)
 if res.status_code == 200:
    with open('k.png','wb') as f:
        shutil.copyfileobj(res.raw, f)
 input1 = await bot.ask(message.from_user.id, f"**Send Download Link**")
 url = input1.text
 await bot.send_photo(chat_id=Config.UPDATES_CHANNEL, photo='k.png', caption=msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download From Here", url=url)]]))
 os.remove('k.png')
