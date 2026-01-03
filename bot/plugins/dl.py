from bot.database import get_latest_anime, update_latest_anime, list_handler, db_data, fetch, queue
import asyncio
from .helper import parse, download_torrent
from bot import bot, Config, LOGS

async def checkup():
 LOGS.info("STARTING CHECKUP")
 fetch() ### it will fetch from the database and update the queue
 if len(db_data) >= 0:
   for i in range(0,len(db_data)):
     LOGS.info(f"Downloading {db_data[i]['title']}") 
     await download_torrent(i=db_data[i],message='',mode='')
     queue.delete_one({"_id" : list_handler[i]})
   db_data.clear()
   list_handler.clear()
        
async def torrent_task():
    LOGS.info("Starting To Check Updates")
    current_title = get_latest_anime() ## database fetch
    while True:
     try:
        await asyncio.sleep(15)
        data = parse()
        new_title = data[0]['title']
        i=1
        while(new_title != current_title):
            asyncio.create_task(download_torrent(i=data[i], mode="automatic", message=''))
            new_title = data[i]['title']
            i+=1
        current_title = data[0]['title']
        update_latest_anime(current_title)
        await asyncio.sleep(15)
     except Exception as e:
        LOGS.exception(e)
        
           

    
