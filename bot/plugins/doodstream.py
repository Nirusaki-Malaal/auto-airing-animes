import requests
import sys
import os
import asyncio

def req(url):
 try:
  r = requests.get(url)
  response = r.json()
  if response['msg'] == "Wrong Auth":
   sys.exit("Invalid API key, please check your API key")
  else:
   return response
 except ConnectionError as e:
   sys.exit(f"ERROR : {e}")
  
async def doodstream(file):
 try:
  filename = file
  api_id = "139452vj0p3ouvpbgxggjn"
  url = f"https://doodapi.com/api/upload/server?key={api_id}"
  url_for_upload = req(url)['result']
  post_data = {"api_key": api_id}
  path = filename
  post_files = {"file": (filename, open(path, "rb"))}
  up = requests.post(url_for_upload, data=post_data, files=post_files)
  final = up.json()
  result = final['result']
  download = result[0]
  download_url = download['download_url']
  return download_url.replace("dood.la", "doodstream.com")
 except:
  return "google.com"

  
