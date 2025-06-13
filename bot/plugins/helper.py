from pyrogram import Client
import psutil
from .devtools import progress_for_pyrogram
from .torrent import downloader
from .anilist import user_anime, anime_duration, image_genre
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from bot import Config, bot, LOGS, collection, queue, channels
from pathlib import Path
from AnilistPython import Anilist
import sys,signal, anitopy, json, re, math, os, io, pyrogram, traceback, feedparser, asyncio, requests, time, subprocess, pymongo
from .doodstream import doodstream
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from .upload import upload
sudo_users = Config.AUTH_USERS
MAX_MESSAGE_LENGTH = 4096
FINISHED_PROGRESS_STR = "◾"
UN_FINISHED_PROGRESS_STR = "◽"

async def add_anime_channel(i):
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
 bc = await bot.send_message(chat_id=5703071595, text=rext)
 inp = await bot.ask(5703071595, "Want To Add As Monitor ?")
 if inp.text == "Yes" or inp.text == "yes":
    bibe = await bot.ask(5703071595, "Send Chat ID")
    boul = isinstance(str(bibe.text), str)
    if boul == True:
      bni = str(bibe.text)
      channels.insert_one({'anime_name' : anime_name, 'chat_id' : bni})
      await bot.send_message(chat_id=5703071595, text=f"Sucessfully Added {anime_name}")

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]

async def encode_480p(input_dir, output, message, total_time):
    joined = output
    b_lol = str(int(time.time()))
    ffmpeg_cmd = f'ffmpeg -hide_banner -loglevel error -progress {b_lol}.txt -i "{input_dir}" -map 0:v -map 0:a -map 0:s? -c:s copy -c:v libx265 -s 854x480 -crf 29 -preset medium -metadata title="{joined}" -metadata:s:v title="{joined} - 480p"  -metadata:s:a title="{joined} - JPN" -metadata:s:s title="{joined} - English" -c:a libfdk_aac -ab 46k -vbr 2 -ac 2 -profile:a aac_he_v2 "{output}" -y'
    process = await asyncio.create_subprocess_shell(
            ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
    )
    COMPRESSION_START_TIME = time.time()
    while process.returncode != 0:
     try:
      await asyncio.sleep(3)
      with open(f"/bot/{b_lol}.txt", 'r+') as file:
        text = file.read()
        frame = re.findall("frame=(\d+)", text)
        time_in_us=re.findall("out_time_ms=(\d+)", text)
        progress=re.findall("progress=(\w+)", text)
        speed=re.findall("speed=(\d+\.?\d*)", text)
        if len(frame):
          frame = int(frame[-1])
        else:
          frame = 1;
        if len(speed):
          speed = speed[-1]
        else:
          speed = 1;
        if len(time_in_us):
          time_in_us = time_in_us[-1]
        else:
          time_in_us = 1;
        if len(progress):
          if progress[-1] == "end":
            break
        execution_time = TimeFormatter((time.time() - COMPRESSION_START_TIME)*1000)
        ottt = hbs(int(Path(output).stat().st_size))
        elapsed_time = int(time_in_us)/1000000
        difference = math.floor((total_time - elapsed_time) / float(speed))
        ETA = "-"
        if difference > 0:
          ETA = TimeFormatter(difference*1000)
        percentage = math.floor(elapsed_time * 100 / total_time)
        perc_str = '{0}%'.format(round(percentage, 2))
        prog_bar_str = '{0}{1}'.format(''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]), ''.join([UN_FINISHED_PROGRESS_STR for i in range(10 - math.floor(percentage / 10))]))
        stats = f'➤ **{output}** 🎖\n' \
                f'➤ **Ꭲiʍᴇ Ꮮᴇfᴛ** ⏳ : {ETA}\n' \
                f'➤ **Ꮯurrᴇnᴛ Ꮪizᴇ** 🖥 : {ottt}\n' \
                f'➤ **Ꮲᴇrᴄᴇnᴛᴀgᴇ** 🗝 : {perc_str}\n' \
                f'➤ {prog_bar_str}\n' \
                f'➽───────────────❥'
        try:
          await message.edit(text=stats)
        except Exception as e:
          pass
     except Exception as e:
       LOGS.info(e)
    stdout, stderr = await process.communicate()
    os.remove(b_lol + '.txt')
    
async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = os.path.join(
        output_directory,
        str(time.time()) + ".jpg"
    )
    if video_file.upper().endswith(("MKV", "MP4", "WEBM")):
        cmd = f'ffmpeg -ss {str(ttl)} -i "{video_file}" -vframes 1 -s 1280x720 -vf "drawtext=fontfile=font.ttf:fontsize=30:fontcolor=white:bordercolor=black@0.50:x=w-tw-10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text=FIERCENETWORK" "{out_put_file_name}" -y'
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None
    
def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"
    

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

async def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720

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

def get_first_title():
    a = feedparser.parse("https://subsplease.org/rss/?r=1080")
    b = a["entries"]
    data = []
    for i in b:
        item = {}
        item['title'] = i['title']
        item['size'] = i['subsplease_size']
        item['link'] = i['link']
        data.append(item)
    title = data[0]['title']
    return str(title)
   
async def get_rss_list(bot, message):
 data = parse()
 stri = ''
 for x in range(0, len(data)):
  b = data[x]['title']
  size = data[x]['size']
  dic = anitopy.parse(b)
  anime_name = dic['anime_title']
  if "episode_number" in dic.keys():
    ep = dic["episode_number"]    
    joined = f'{dic["episode_number"]} - {anime_name} [@FIERCENETWORK].mkv'
  else:
    ep = "Special"
  b = f'{anime_name} - E{ep} Size : {size}'  
  stri = stri + f'{x}.) {b}\n'
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
 
async def napliya_vro(dicc):
 try:
   data = dicc
  # queue.insert_one({'queue' : str(data)}) 
   outputname = data['title']
   torrent_dir = data['link']
   total = data['size']
   bc = await bot.send_message(chat_id=5703071595, text=data['title'])
   if "[Batch]" in data['title']: 
    return await bot.send_document(chat_id=5703071595, document=torrent_dir, caption=f"Batch Detected {data['title']}")
   filepath = outputname
   try:
    await bc.edit(f"Downloading {outputname}")
    cmd = f'aria2c --seed-time=0 --out="{filepath}" "{torrent_dir}"'
    LOGS.info(cmd)
    process = await asyncio.create_subprocess_shell(cmd,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)  
    stdout, stderr = await process.communicate()
   except Exception as e:
    LOGS.info(e)
   dic = anitopy.parse(outputname)
   anime_name = dic['anime_title']
   bbcc = anime_name
   anilist = Anilist()
   diction = anilist.get_anime(anime_name)
   if diction['name_english'] != None:
    anime_name = str(diction['name_english'])
   genres, image= await image_genre(anime_name)
   if "episode_number" in dic.keys():
    ep = dic["episode_number"]    
    joined = f'{dic["episode_number"]} - {anime_name} [@FIERCENETWORK].mkv'
   else:
    ep = "Special"
    joined = f'Special - {anime_name} [@FIERCENETWORK].mkv'
   duration = get_duration(filepath) 
   await encode_480p(filepath, joined, bc, duration) 
   tt = f'**📌 {ep} - {anime_name} Was Released**\n**━━━━━━━━━━━━━━**\n**➜ 🎵 Audio : Japanese**\n**➜ 📂 Quality : 480p**\n**➜ 🎭 Genres : {genres}**\n**━━━━━━━━━━━━━━**'
   image , duration =  anime_duration(anime_name)
   response = requests.get(image)
   file = open("krsna.jpg", "wb")
   file.write(response.content)
   file.close()
   await bot.send_photo(chat_id=Config.LOG_CHANNEL, caption=tt, photo='krsna.jpg')
   if channels.find_one({'anime_name' : bbcc}):
    bick = channels.find_one({'anime_name' : bbcc})
    ch_chat_id = str(bick['chat_id'])
    d = upload(joined, 5703071595, ch_chat_id)
   vidid = await bot.send_document(document=joined,file_name=joined,caption="[@FIERCENETWORK]",force_document=True,chat_id=Config.LOG_CHANNEL)
   fileid = "CAACAgUAAxkBAAITv2MIhKkyqft1DpLHIARHOpZ37ATuAAINBwACTD0gVGGJxKfBkl0uHgQ"    
   await bot.send_sticker(chat_id=Config.LOG_CHANNEL, sticker=fileid)
   os.remove(joined)
   os.remove('krsna.jpg')
   os.remove(filepath)
   await bc.edit(f"SUCCESSFULLY ENCODED {outputname}")
 except Exception as e:
   LOGS.info(e)


async def download_torrent(i: int):
  try:
   data = parse()
   binn = data
   data = data[i]
   queue.insert_one({'queue' : str(data)}) 
   outputname = data['title']
   torrent_dir = data['link']
   total = data['size']
   bc = await bot.send_message(chat_id=5703071595, text=data['title'])
   if "[Batch]" in data['title']: 
    return await bot.send_document(chat_id=5703071595, document=torrent_dir, caption=f"Batch Detected {data['title']}")
   filepath = outputname
   try:
    await bc.edit(f"Downloading {outputname}")
    cmd = f'aria2c --seed-time=0 --out="{filepath}" "{torrent_dir}"'
    LOGS.info(cmd)
    process = await asyncio.create_subprocess_shell(cmd,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)  
    stdout, stderr = await process.communicate()
   except Exception as e:
    LOGS.info(e)
   dic = anitopy.parse(outputname)
   anime_name = dic['anime_title']
   bbcc = anime_name
   anilist = Anilist()
   diction = anilist.get_anime(anime_name)
   if diction['name_english'] != None:
    anime_name = str(diction['name_english'])
   genres, image= await image_genre(anime_name) 
   if "episode_number" in dic.keys():
    ep = dic["episode_number"]    
    joined = f'{dic["episode_number"]} - {anime_name} [@FIERCENETWORK].mkv'
   else:
    ep = "Special"
    joined = f'Special - {anime_name} [@FIERCENETWORK].mkv'
   duration = get_duration(filepath) 
   await encode_480p(filepath, joined, bc, duration) 
   tt = f'**📌 {ep} - {anime_name} Was Released**\n**━━━━━━━━━━━━━━**\n**➜ 🎵 Audio : Japanese**\n**➜ 📂 Quality : 480p**\n**➜ 🎭 Genres : {genres}**\n**━━━━━━━━━━━━━━**'
   image , duration =  anime_duration(anime_name)
   response = requests.get(image)
   file = open("krsna.jpg", "wb")
   file.write(response.content)
   file.close()
   await bot.send_photo(chat_id=Config.LOG_CHANNEL, caption=tt, photo='krsna.jpg')
   if channels.find_one({'anime_name' : bbcc}):
    bick = channels.find_one({'anime_name' : bbcc})
    ch_chat_id = str(bick['chat_id'])
    d = upload(joined, 5703071595, ch_chat_id)
   vidid = await bot.send_document(document=joined,file_name=joined,caption="[@FIERCENETWORK]",force_document=True,chat_id=Config.LOG_CHANNEL)
   fileid = "CAACAgUAAxkBAAITv2MIhKkyqft1DpLHIARHOpZ37ATuAAINBwACTD0gVGGJxKfBkl0uHgQ"    
   await bot.send_sticker(chat_id=Config.LOG_CHANNEL, sticker=fileid)
   os.remove(joined)
   os.remove('krsna.jpg')
   os.remove(filepath)
   queue.delete_one({'queue' : str(data)})
   await bc.edit(f"SUCCESSFULLY ENCODED {outputname}")
  except Exception as e:
   LOGS.info(e)

    
    
async def exec_message_f(client, message):
  if message.from_user.id in sudo_users:
    if True:
        DELAY_BETWEEN_EDITS = 0.3
        PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.id

        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "No Output"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > MAX_MESSAGE_LENGTH:
            with open("exec.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(OUTPUT))
            await client.send_document(
                chat_id=message.chat.id,
                document="exec.text",
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id
            )
            os.remove("exec.text")
            await message.delete()
        else:
            await message.reply_text(OUTPUT)
  else:
    return

async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def eval_message_f(client, message):
    if message.from_user.id in sudo_users:
        status_message = await message.reply_text("Processing ...")
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.id

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None

        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"

        final_output = (
            "**EVAL**: <code>{}</code>\n\n**OUTPUT**:\n<code>{}</code> \n".format(
                cmd, evaluation.strip()
            )
        )

        if len(final_output) > MAX_MESSAGE_LENGTH:
            with open("eval.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(final_output))
            await message.reply_document(
                document="eval.text",
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
            os.remove("eval.text")
            await status_message.delete()
        else:
            await status_message.edit(final_output)

    
async def upload_dir(client, message):
   cmd1 = message.text.split(" ", maxsplit=1)[1]
   replyid = message.id
   if message.reply_to_message:
      replyid = message.reply_to_message.id
   if os.path.exists(cmd1):
    xhamster = await message.reply_text('Uploading The File 📁')
    await client.send_document(
                chat_id=message.chat.id,
                document=cmd1,
                caption=cmd1,
                reply_to_message_id=replyid,
        )
    await xhamster.delete()
   else:
    await message.reply_text(f"Directory Not Found ```{cmd1}```", parse_mode="markdown")
    
async def batch(bot, message):
    magnet = await bot.download_media(message.reply_to_message)
    reply = message.reply_to_message
    try:
     cmd = f'aria2c --seed-time=0 --dir=torrent "{magnet}" '
     process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
     )
     stdout = await process.communicate()
     stderr = await process.communicate()
    except Exception as e:
     pass
     return "Nothing"
    tr = 'torrent/'
    dd = os.listdir(tr)
    filepaths = '/bot/torrent/'+ dd[0]
    data = os.listdir(f"{filepaths}/")
    data.sort(key=str.lower)
    x = len(data)
    a = Client('numb',session_string=Config.SESSION_STRING, api_id=Config.API_ID, api_hash=Config.API_HASH)
    await a.start()
    fn = data[0]
    diy = anitopy.parse(fn)
    an = diy["anime_title"]
    status, score, eps, hashtag, duration, genres, image, name, eng_name = await user_anime(an)
    mesa = f'Name - {name}\nEnglish Name - {eng_name}\nScore - {score}\nGenres - {genres}\nEpisodes - {eps}'
    ch = await a.create_channel(f'{eng_name} | {name}', f'{mesa}')
    anilist = Anilist()
    bind = anilist.get_anime(eng_name)
    img = bind['cover_image']
    await a.send_photo(chat_id=int(ch.id), caption=mesa, photo=image)
    response = requests.get(img)
    file = open("image.jpg", "wb")
    file.write(response.content)
    file.close()
    await a.set_chat_photo(chat_id=int(ch.id), photo='image.jpg')
    for i in range(0, x):
     try:   
       filepath = filepaths + '/' + data[i] 
       filename = data[i]
       duration = get_duration(filepath)
       width, height = await get_width_height(filepath)
       thumb = await take_screen_shot(
          filepath,
          os.path.dirname(os.path.abspath(filepath)),
          (duration / 2)
       )
       dic = anitopy.parse(filename)
       anime_name = dic["anime_title"]
       joined = anime_name
       if "anime_season" in dic.keys():
        season = dic["anime_season"]
        joined = anime_name + f" S{season}"
       else:
        season = 1
        joined = anime_name + f" S{season}"
       if "episode_number" in dic.keys():
        ep = dic["episode_number"]
        joined = joined + f"EP{ep}"
       else:
        ep = "OVA"
       if "video_resolution" in dic.keys():
        res = dic["video_resolution"]
        joined = joined + f" [{res}]"
       else:
        res = 'N/A'
       jon = joined
       joined = joined + ' @FIERCENETWORK'
       chatid = int(ch.id)
       vidid = await a.send_video(video=filepath,file_name=joined,caption=joined,thumb=thumb,width=width,height=height,duration=duration,supports_streaming=True,chat_id=chatid)
       status, score, eps, hashtag, duration, genres, image, name, eng_name = await user_anime(anime_name) 
       main_msg = f"⚜️ **{eng_name}**\n🇯🇵 **{name}**\n**Episode No : 1-{ep}**\n**Season : {season}**\n┏━━━━━━━━━━━━━━━━━\n┣**🎵 AUDIO : Japanese With English Subtitles**\n┣**🔖 Total Episodes : {eps}**\n**┣⭐️ Rating : {score}**\n**┣📂 QUALITY : {res}**\n**┣⌛️ STATUS : {status}**\n**┣🕔 Duration : {duration}**\n**┣🎭 Genres : {genres}**\n┗━━━━━━━━━━━━━━━━━\n\n#️⃣ {hashtag}"
     except Exception as e:
       await bot.send_message(message.from_user.id, e)
    url = await a.export_chat_invite_link(int(ch.id))
    await bot.send_photo(chat_id=Config.UPDATES_CHANNEL, photo=image, caption=main_msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download From Here" , url=url )]]))                              
    fileid = "CAACAgEAAxkBAAIMU2KozBhd-SPaszTPMr3EG-kG_k8vAAKXAgACJ_hhR9HcWzoditT7HgQ"    
    await a.send_sticker(chat_id=int(ch.id), sticker=fileid)
    os.system(f"rm -rf '{filepaths}'")
