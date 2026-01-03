from bot.plugins.helper import download_torrent, batch, add_anime_channel, channels_list, get_rss_list, renew
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import bot, Config, LOGS
from .database import pgk, clear_queue
from .plugins.anilist import uploadanime
from datetime import datetime
import asyncio
from .plugins.devtools import exec_message_f , eval_message_f
from .plugins.dl import checkup , torrent_task

START_TIME = datetime.now()


 ## Check uptime of the BOT
@bot.on_message(filters.incoming & filters.command(["uptime"]))
async def help_message(bot, message):
   if message.from_user.id in Config.AUTH_USERS:
    await bot.send_message(chat_id=message.from_user.id,text=f"UPTIME: {str(datetime.now() - START_TIME).split('.')[0]}")
    return
   else:
    return await message.reply_sticker("CAACAgUAAxkBAAIah2LNhR_vCtyL-YCw8Sf3cO0BCFnqAAKDBgACmStpV778w4PJK2OkHgQ")

## START MESSAGE
    
@bot.on_message(filters.incoming & filters.command(["start"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    REXT = f"Hey {message.from_user.mention()} ✨\n\n" \
        "🚀 Your all-in-one automation bot:\n" \
        "• Fetches content via RSS\n" \
        "• Encodes videos flawlessly\n" \
        "• Uploads & posts directly to your channel\n" \
        "• Designs clean, eye-catching banners\n\n" \
        "⚙️ Smart. Fast. Reliable.\n" \
        "👨‍💻 Developed by @Nirusaki\n\n" \
        "Enjoy the automation 💙"

    await bot.send_message(
        chat_id=message.chat.id,
        text=REXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Join Fiercenetwork', url='https://t.me/Fiercenetwork')
                ]
            ]
        ),
        reply_to_message_id=message.id,
    )
    

@bot.on_message(filters.incoming & filters.command(["tor"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    try:
      await download_torrent(int((message.text).split(" ")[1]), message)
    except:
       await message.reply_text("Enter With a valid Number")

@bot.on_message(filters.incoming & filters.command(["clear"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    clear_queue()
    await bot.send_message(chat_id=message.from_user.id, text="**Queue Cleared Successfully**", reply_to_message_id=message.reply_to_message)


@bot.on_message(filters.incoming & filters.command(["channel"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    await add_anime_channel(int((message.text).split(" ")[1]), message)
    
@bot.on_message(filters.incoming & filters.command(["logs", "log"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    await bot.send_document(chat_id=message.chat.id, reply_to_message_id=message.id, force_document=True, document="BOT@Log.txt")
    await bot.send_document(chat_id=message.chat.id, reply_to_message_id=message.id, force_document=True, document="aria2.log")
    
@bot.on_message(filters.incoming & filters.command(["execute", "exec", "bash"])) #DONE
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await exec_message_f(bot, message)
 
@bot.on_message(filters.incoming & filters.command(["rss"])) #DONE
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await get_rss_list(message)
      
@bot.on_message(filters.incoming & filters.command(["list"])) #DONE
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await channels_list(bot, message)      
    
@bot.on_message(filters.incoming & filters.command(["find"])) #DONE
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await uploadanime(bot, message)   
    
@bot.on_message(filters.incoming & filters.command(["eval", "py", "evaluate"])) #DONE
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")    
    await eval_message_f(bot, message)        
    
@bot.on_message(filters.incoming & filters.command(["batch"]))
async def help_message(bot, message):   
    if message.chat.id not in Config.AUTH_USERS:
       return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    try:
      i = (message.text).split()[1]
    except:
       return await message.reply_text("Give Valid Input")
    try:
       i = int(i)
    except:
       pass
    await batch(i, message)

@bot.on_message(filters.incoming & filters.command(["renew"]))
async def help_message(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    clear_queue()
    await renew()
    await bot.send_message(chat_id=message.from_user.id, text="**BOT RENEWED SUCCESSFULLY**", reply_to_message_id=message.reply_to_message)


async def startup():
    await asyncio.create_subprocess_shell('aria2c --enable-rpc --console-log-level=error --log=aria2.log --log-level=error --summary-interval=0 >/dev/null 2>&1 &')
    await bot.start()
    me = await bot.get_me()
    LOGS.info(f"The Bot - {me.username} Has Started")
    asyncio.create_task(checkup())
    asyncio.create_task(torrent_task())
    x = len(Config.AUTH_USERS)
    for i in range(0, x):
      await bot.send_message(chat_id=Config.AUTH_USERS[i], text="Bot Has Restarted")
    await idle()
    await bot.stop()

pgk()      
bot.loop.run_until_complete(startup())
