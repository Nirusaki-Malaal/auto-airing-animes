from pydrive.auth import GoogleAuth, AuthenticationError
from bot import collection as col 
from bot import bot, Config, LOGS
import json, pyrogram, time, datetime, asyncio, os
from pydrive.drive import GoogleDrive
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

async def if_user(message):
   if col.find_one({'id' : message.from_user.id}):
      return True
   else:
      return False   

async def authorise(bot, message):
    gauth = GoogleAuth()
    if col.find_one({'id' : message.from_user.id}):
     dictionary = col.find_one({'id' : message.from_user.id})
     credentials = str(dictionary['credentials']) ## credentials
     if not os.path.exists(str(message.from_user.id)):
      with open(f'{str(message.from_user.id)}' , 'w') as file1:
       p = file1.write(credentials)
       file1.close()
     gauth.LoadCredentialsFile(str(message.from_user.id))
     if gauth.access_token_expired:
        gauth.Refresh() ## Refresh Token If Expired ##
        await bot.send_message(chat_id=message.from_user.id, text="Refreshed Authorisation")
     else:
        gauth.Authorize() ## Authorising With Saved Credentials ##
        await bot.send_message(chat_id=message.from_user.id, text="Already Authorised")
    else:
     authurl = gauth.GetAuthUrl()
     input1 = await bot.ask(chat_id=message.from_user.id, reply_to_message_id=message.id, text="Open This Url And Send The Authorisation Code" ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Link', url=authurl)]])) ## Listening
     try:
      drive = gauth.Auth(str(input1.text))
      gauth.SaveCredentialsFile(str(message.from_user.id))
      with open(str(message.from_user.id) , 'r') as file2:
       b = file2.read()
       file2.close()
      col.insert_one({'id': message.from_user.id, 'credentials' : b})
      await bot.send_message(chat_id=message.from_user.id, text="Authorized")
     except AuthenticationError as e:
      await bot.send_message(message.from_user.id, "Wrong Token Entered")
  
def check_user(message):
   gauth = GoogleAuth()
   if col.find_one({'id' : message}):
     dictionary = col.find_one({'id' : message})
     credentials = str(dictionary['credentials']) ## Credentials ##
     if not os.path.exists(str(message)):
      with open(f'{str(message)}' , 'w') as file1:
       p = file1.write(credentials)
       file1.close()
     gauth.LoadCredentialsFile(str(message))
     if gauth.access_token_expired:
        gauth.Refresh() ## Refresh Token If Expired ##
     else:
        gauth.Authorize() ## Authorising With Saved Credentials ##



                      