import requests
import asyncio
import traceback
import time
from bot.plugins.helper import download_torrent, upload_dir, exec_message_f , eval_message_f, batch, napliya_vro, add_anime_channel, channels_list, get_rss_list
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from bot import bot, Config, LOGS
from bot.plugins.dl import startup
from .database import pgk
from .plugins.anilist import uploadanime
from .plugins.authorise import authorise
sudo_users = Config.AUTH_USERS
app = bot
from datetime import datetime

START_TIME = datetime.now()

@bot.on_message(filters.incoming & filters.command(["uptime"]))
async def help_message(bot, message):
   if message.from_user.id in Config.AUTH_USERS:
    await bot.send_message(chat_id=message.from_user.id,text=f"**Uᴩᴛiʍᴇ: {str(datetime.now() - START_TIME).split('.')[0]}**")
    return
   else:
    return await message.reply_sticker("CAACAgUAAxkBAAIah2LNhR_vCtyL-YCw8Sf3cO0BCFnqAAKDBgACmStpV778w4PJK2OkHgQ")


    
@bot.on_message(filters.incoming & filters.command(["start"]))
async def help_message(app, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    REXT = f"Hi {message.from_user.mention()}\n**•I can Encode Telegram files And Send Sample (Especially Movies,Animes), just send me a video.**\n**•This Bot is Developed by @NIRUSAKI_AYEDAEMON**\n**•Simple, Easy and Convenient to use**\n**Thanks**"
    await bot.send_message(
        chat_id=message.chat.id,
        text=REXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Join Anixpo', url='https://t.me/AniXpo')
                ]
            ]
        ),
        reply_to_message_id=message.id,
    )
    
@bot.on_message(filters.incoming & filters.command(["tor"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    b = message.text
    c = int(b.split(" ")[1])
    await download_torrent(c)


@bot.on_message(filters.incoming & filters.command(["channel"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    b = message.text
    c = int(b.split(" ")[1])
    await add_anime_channel(c)
    
@bot.on_message(filters.incoming & filters.command(["logs", "log"]))
async def help_message(app, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    await bot.send_document(chat_id=message.chat.id, reply_to_message_id=message.id, force_document=True, document="BOT@Log.txt")
    
@app.on_message(filters.incoming & filters.command(["execute", "exec", "bash"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await exec_message_f(app, message)
 
@app.on_message(filters.incoming & filters.command(["rss"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await get_rss_list(app, message)

@app.on_message(filters.incoming & filters.command(["auth"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await authorise(app, message)
      
@app.on_message(filters.incoming & filters.command(["list"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await channels_list(app, message)      
      
@app.on_message(filters.incoming & filters.command(["ul"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await (app, message)      
    
@app.on_message(filters.incoming & filters.command(["find"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await uploadanime(app, message)   
    
@app.on_message(filters.incoming & filters.command(["eval", "py", "evaluate"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await eval_message_f(app, message)        
    
@bot.on_message(filters.incoming & filters.command(["batch"]))
async def help_message(app, message):    
    await batch(app, message)

pgk()      
bot.loop.run_until_complete(startup())
