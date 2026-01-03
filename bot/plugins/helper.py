from pyrogram import Client
from .devtools import hbs , TimeFormatter
from .anilist import user_anime, anime_duration, image_genre
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import Config, bot, LOGS, queue, channels
from pathlib import Path
from AnilistPython import Anilist
import anitopy, re, math, os, feedparser, asyncio, requests, time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from .aria import Aria2py
FINISHED_PROGRESS_STR = "▣"
UN_FINISHED_PROGRESS_STR = "□"

async def renew():
  os.system(f"rm -rf {Config.ROOT_DIRECTORY}/torrent/*")
  os.system(f"rm -rf {Config.ROOT_DIRECTORY}/temp/*")
  os.system(f"rm -rf {Config.ROOT_DIRECTORY}/encodes/*")
  for i in os.listdir(Config.ROOT_DIRECTORY):
    if i.endswith('.txt') and "Log" not in i:
      os.remove(i)
  try:    
    os.system('pkill -9 ffmpeg')
  except:
    pass
  os.system('pkill -9 aria2c')
  await asyncio.create_subprocess_shell('aria2c --enable-rpc --console-log-level=error --log=aria2.log --log-level=error --summary-interval=0 >/dev/null 2>&1 &')



async def add_anime_channel(i, message):
 data = parse()   
 outputname = data[i]['title']
 total = data[i]['size']
 dic = anitopy.parse(outputname)
 anime_name = dic['anime_title']
 if "episode_number" in dic.keys():
    ep = dic["episode_number"]   
 else:
  ep = 'N/A'
 rext = f'Anime : {anime_name}\nEpisode : {ep}\nSize : {total}'
 await bot.send_message(chat_id=message.from_user.id, text=rext)
 inp = await bot.ask(message.from_user.id, "Want To Add As Monitor ?")
 if inp.text == "Yes" or inp.text == "yes":
    bibe = await bot.ask(message.from_user.id, "Send Chat ID")
    boul = isinstance(str(bibe.text), str)
    if boul == True:
      bni = str(bibe.text)
      channels.insert_one({'anime_name' : anime_name, 'chat_id' : bni})
      await bot.send_message(chat_id=message.from_user.id, text=f"Sucessfully Added {anime_name}")


async def encode_480p(input_dir, output, message, total_time, filename):
    b_lol = str(int(time.time()))
    ffmpeg_cmd = f'ffmpeg -hide_banner -loglevel error -progress {b_lol}.txt -i "{input_dir}" -map 0:v -map 0:a? -map 0:s? -c:s copy -c:v libx265 -pix_fmt yuv420p -crf 30 -preset fast -metadata title="{filename}" -metadata:s:v title="{filename} - 480p"  -metadata:s:a title="{filename} - JPN" -metadata:s:s title="{filename} - English" -c:a libopus -ab 50k -vbr 2 -ac 2 "{output}" -y'
    process = await asyncio.create_subprocess_shell(
            ffmpeg_cmd,
            stderr=asyncio.subprocess.PIPE
    )
    while process.returncode != 0:
     try:
      await asyncio.sleep(3)
      with open(f"{Config.ROOT_DIRECTORY}/{b_lol}.txt", 'r+') as file:
        text = file.read()
        frame = re.findall(r"frame=(\d+)", text)
        time_in_us=re.findall(r"out_time_ms=(\d+)", text)
        progress=re.findall(r"progress=(\w+)", text)
        speed=re.findall(r"speed=(\d+\.?\d*)", text)
        if len(frame):
          frame = int(frame[-1])
        else:
          frame = 1
        if len(speed):
          speed = speed[-1]
        else:
          speed = 1
        if len(time_in_us):
          time_in_us = time_in_us[-1]
        else:
          time_in_us = 1
        if len(progress):
          if progress[-1] == "end":
            break
        ottt = hbs(int(Path(output).stat().st_size))
        elapsed_time = int(time_in_us)/1000000
        difference = math.floor((total_time - elapsed_time) / float(speed))
        ETA = "-"
        if difference > 0:
          ETA = TimeFormatter(difference*1000)
        percentage = math.floor(elapsed_time * 100 / total_time)
        perc_str = '{0}%'.format(round(percentage, 2))
        prog_bar_str = '{0}{1}'.format(''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]), ''.join([UN_FINISHED_PROGRESS_STR for i in range(10 - math.floor(percentage / 10))]))
        stats = f'➤ **{filename}** 🎖\n' \
                f'➤ **Time Left** ⏳ : {ETA}\n' \
                f'➤ **Current Size** 🖥 : {ottt}\n' \
                f'➤ **Percentage** 🗝 : {perc_str}\n' \
                f'➤ {prog_bar_str}\n' \
                f'➽───────────────❥'
        try:
          await message.edit(text=stats)
        except Exception as e:
          pass
     except Exception as e:
       LOGS.exception(e)
    stderr = await process.communicate()
    if stderr:
      LOGS.error(stderr)
    os.remove(f"{Config.ROOT_DIRECTORY}/{b_lol}.txt")
    

    

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

def parse():
    a = feedparser.parse("https://subsplease.org/rss/?r=1080")
    b = a["entries"]
    data = []
    for i in b:
        item = {}
        item['title'] = i['title']
        item['size'] = i['subsplease_size']
        item['link'] = i['link']
        data.append(item)
    return data
   
## FIXED WITH NUMBERING
async def get_rss_list(message):
 data = parse()
 stri = '**RSS List -:** :\n\n'
 for x in range(0, len(data)):
  b = data[x]['title']
  size = data[x]['size']
  dic = anitopy.parse(b)
  anime_name = dic['anime_title']
  if "episode_number" in dic.keys():
    ep = dic["episode_number"]    
  else:
    ep = "Special"
  b = f'{anime_name} - E{ep} Size : {size}'  
  stri = stri + f'`{x+1}`.) {b}\n\n'
 stri = stri + r"**Use** /tor number **To 💻⬇️ Fetch The Torrent**" + "\n\n**━─━────༺༻────━─━**"
 await message.reply_text(stri)
 
async def channels_list(bot, message):
 b = channels.find({})
 stri = ''
 bn = 1
 for bc in b:
  anime_name = bc['anime_name']
  chat_id = str(bc['chat_id']).replace('-100', '')
  bc = f'Anime - {anime_name} [Channel](t.me/c/{chat_id}/1)'
  stri = stri + f'{bn}.) {bc}\n'
  bn = bn + 1
 await message.reply_text(stri) 
 


async def download_torrent(i, message="", mode=""):
  if i==0:
    return await bot.send_message(chat_id=message.chat.id,reply_to_message_id=message.id,text="**Invalid Value Please Enter Again**")
  try:
    if isinstance(i, int): 
      data = parse()[i-1]
    elif isinstance(i,dict):
      data = i # dic
    if isinstance(i ,dict):
      reply = await bot.send_message(chat_id=Config.DETAIL_CHANNEL, text=f"**Detected** , `{data['title']}`")
    if isinstance(i,int):
      reply = await bot.send_message(chat_id=message.from_user.id, text=f"**Detected** , `{data['title']}`")
    
    ## BATCH TREATMENT LATER.....
    if "[Batch]" in data['title']: 
        return await reply.edit(f"**Batch**\n ⚠️ Detected Skipping `{data['title']}`")
    if isinstance(i, int) or mode == "automatic":
      queue.insert_one({'queue' : str(data)})

    ## inserting it to the queue data structure
    filepath = Config.ROOT_DIRECTORY + '/torrent/' + data['title']
   ## DOWNLOADING THE MAGNET LINK
    try:
        await reply.edit(f"Downloading `{data['title']}`")
        aria = Aria2py()
        gid = await aria.add_magnet(data['link'], Config.ROOT_DIRECTORY + '/torrent' ,data['title'])
        data1 = aria.tell_status(gid) ## meta_gid
        while aria.tell_status(gid)['status'] == "active":
           await asyncio.sleep(0.1)
        ## META DOWNLOADING FINISHES
        gid = aria.real_gid(gid)
        data1 = aria.tell_status(gid)
        while data1['status'].lower() == "active":
          try:
           data1 = aria.tell_status(gid)
           prog_bar_txt = FINISHED_PROGRESS_STR*round(int(data1["completedLength"])/int(data1["totalLength"])*10) + UN_FINISHED_PROGRESS_STR*(10-round(int(data1["completedLength"])/int(data1["totalLength"])*10))
           text = f"**Filename** : `{data['title']}` \n**Total Size** : `{hbs(int(data1["totalLength"]))}`\n**Current Size**: {hbs(int(data1["completedLength"]))}\n**Percentage** : {round(int(data1["completedLength"])/int(data1["totalLength"]) * 100, 2)}\n{prog_bar_txt}"
           await reply.edit(text)
           await asyncio.sleep(5)
          except Exception as e:
             pass
        await reply.edit(f"✅ Download completed!\n `{data['title']}`")    
    except Exception as e:
      LOGS.exception(e)

    anime_name , joined, ep, genres = await rename(str(data['title'])) 
    output_directory = Config.ROOT_DIRECTORY + '/encodes/' + joined

    await encode_480p(filepath, output_directory, reply, get_duration(filepath), joined)

    ## PREPARING FOR THE TEXT
    caption = f'**📌 {ep} - {anime_name} Was Released**\n**━━━━━━━━━━━━━━**\n**➜ 🎵 Audio : Japanese**\n**➜ 📂 Quality : 480p**\n**➜ 🎭 Genres : {genres}**\n**━━━━━━━━━━━━━━**'
    image , duration =  anime_duration(anime_name)
    response = requests.get(image)
    with open(f"{Config.ROOT_DIRECTORY}/temp/{anime_name}.jpg", "wb") as file:
        file.write(response.content)

    await bot.send_photo(chat_id=Config.LOG_CHANNEL, caption=caption, photo=f"{Config.ROOT_DIRECTORY}/temp/{anime_name}.jpg")
    
    ## UPLOADING

    await bot.send_document(document=output_directory,file_name=joined,caption="[@FIERCENETWORK]",force_document=True,chat_id=Config.LOG_CHANNEL)

    ## SENDING STICKER  
    await bot.send_sticker(chat_id=Config.LOG_CHANNEL, sticker="CAACAgUAAxkBAAITv2MIhKkyqft1DpLHIARHOpZ37ATuAAINBwACTD0gVGGJxKfBkl0uHgQ")

    ## REMOVING temp FILES
    os.remove(output_directory)
    os.remove(f'{Config.ROOT_DIRECTORY}/temp/{anime_name}.jpg')
    os.remove(filepath)

    # UPDATING 
    if isinstance(i, int) or mode == "automatic":
        queue.delete_one({'queue' : str(data)})
    await reply.edit(f"**SUCCESSFULLY ENCODED** \n\n `{joined}`")
  except Exception as e:
    await reply.edit(f"**Error Occured Try Again**\n , `{e}`")
    if isinstance(i, int) or mode == "automatic":
      queue.delete_one({'queue' : str(data)})
    LOGS.exception(e)
    
async def batch(i,message): # i = integer or a string 
    aria = Aria2py()
    if isinstance(i, int): 
      magnet_link = parse()[i-1]['link'] ## title , magnet_link
    elif isinstance(i,str):
      magnet_link = i ## magnet_link
    else:
      return message.reply_text("Give A Correct Message")
    try:
        gid =  await aria.add_batch(magnet_link, Config.ROOT_DIRECTORY + '/torrent/')
        data1 = aria.tell_status(gid) ## meta_gid
        while aria.tell_status(gid)['status'] == "active":
              await asyncio.sleep(0.1)
        ## META DOWNLOADING FINISHES
        gid = aria.real_gid(gid)
        data1 = aria.tell_status(gid)
        reply = await bot.send_message(chat_id=message.from_user.id , reply_to_message_id=message.id , text=f"Downloading BATCH\n`{data1['bittorrent']['info']['name']}`")
        download_directory = Config.ROOT_DIRECTORY + '/torrent/' + data1['bittorrent']['info']['name']
        while data1['status'].lower() == "active":
          try:
           data1 = aria.tell_status(gid)
           prog_bar_txt = FINISHED_PROGRESS_STR*round(int(data1["completedLength"])/int(data1["totalLength"])*10) + UN_FINISHED_PROGRESS_STR*(10-round(int(data1["completedLength"])/int(data1["totalLength"])*10))
           text = f"**Filename** : `{data1['bittorrent']['info']['name']}` \n**Total Size** : `{hbs(int(data1["totalLength"]))}`\n**Current Size**: {hbs(int(data1["completedLength"]))}\n**Percentage** : {round(int(data1["completedLength"])/int(data1["totalLength"]) * 100, 2)}\n{prog_bar_txt}"
           await reply.edit(text)
           await asyncio.sleep(5)
          except Exception as e:
             pass
        await reply.edit(f"✅ Download Batch completed!\n `{data1['bittorrent']['info']['name']}`")    
        ## DOWNLOAD COMPLETED
        dir  = sorted(os.listdir(download_directory))
        for x in dir:
            filepath = download_directory + '/' + x
            anime_name , joined, ep, genres = await rename(str(x)) 
            output_directory = Config.ROOT_DIRECTORY + '/encodes/' + joined
            await encode_480p(filepath, output_directory, reply, get_duration(filepath), joined)    
            ## UPLOADING
            await bot.send_document(document=output_directory,file_name=joined,caption="[@FIERCENETWORK]",force_document=True,chat_id=Config.DETAIL_CHANNEL)
            ## REMOVING temp FILES
            os.remove(output_directory)
            os.remove(filepath)
        os.rmdir(download_directory)
    except Exception as e:
      LOGS.exception(e)


async def rename(outputname):
   anilist = Anilist()
   parsed = anitopy.parse(outputname)
   anime_name = parsed['anime_title']
   diction = anilist.get_anime(anime_name)
   if diction['name_english'] != None:
    anime_name = str(diction['name_english'])
   genres, image= await image_genre(anime_name) 
   if "episode_number" in parsed.keys():
    ep = parsed["episode_number"]    
    joined = f'{parsed["episode_number"]} - {anime_name} [@FIERCENETWORK].mkv'
   else:
    ep = "Special"
    joined = f'Special - {anime_name} [@FIERCENETWORK].mkv'
   return anime_name , joined, ep, genres