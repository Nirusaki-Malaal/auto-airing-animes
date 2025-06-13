import pyrogram
from bot.database import get_latest_anime, update_latest_anime, list_handler, db_data, napana, queue
import asyncio
import hashlib
from .helper import get_first_title, download_torrent, napliya_vro
from pyrogram import idle
import threading
from urllib.request import urlopen, Request
import subprocess
import time
import  os
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os
from bot import Config, bot, LOGS
LIMIT_TORRENT_SIZE = 2040109465

async def checkup():
 LOGS.info("STARTING CHECKUP")
 napana()
 if len(db_data) >= 0:
   LOGS.info("SOMETHING DETECTED") 
   x = len(db_data)
   for i in range(0,x):
     await napliya_vro(db_data[i])
     queue.delete_one({"_id" : list_handler[i]})
   db_data.clear()
   list_handler.clear()
        
async def torrent_task():
    LOGS.info("Starting To Check Updates")
    current_title = get_latest_anime()
    while True:
     try:
        await asyncio.sleep(15)
        new_title = get_first_title()
        if new_title == current_title:
            continue
        else:
            current_title = new_title
            update_latest_anime(current_title)
            await bot.send_message(chat_id=5703071595, text="Changes Detected Downloading Torrent")
            LOGS.info("Changes Detected")
            asyncio.create_task(download_torrent(0))
            await asyncio.sleep(15)
            continue
     except Exception as e:
        LOGS.info(e)
        
           
async def startup():
    await bot.start()
    LOGS.info("The Bot Has Started")
    asyncio.create_task(checkup())
    asyncio.create_task(torrent_task())
    x = len(Config.AUTH_USERS)
    for i in range(0, x):
      await bot.send_message(chat_id=Config.AUTH_USERS[i], text="**Ᏼᴏᴛ Ꮋᴀs Ꮢᴇsᴛᴀrᴛᴇd**")
    await idle()
    await bot.stop()
    
