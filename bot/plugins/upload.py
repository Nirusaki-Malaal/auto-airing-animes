import json, re, os, sys, pyrogram, subprocess, argparse
import os.path as path
from bot import  LOGS, Config
from pydrive.auth import GoogleAuth
from bot.plugins.authorise import check_user
from pydrive.drive import GoogleDrive

class Creds:
 TEAMDRIVE_FOLDER_ID = "13NoH_JY13XQ5IeQHH070ed-1jyMVn-kY"
 TEAMDRIVE_ID = "0AMThLjNHeDmiUk9PVA"

def upload(filename, message, folder_id): ## message is id
 parent_folder = "Gdrive_Bot"
 Creds.TEAMDRIVE_FOLDER_ID = folder_id
 drive: GoogleDrive
 FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
 http = None
 initial_folder = None
 gauth: drive.GoogleAuth = GoogleAuth()
 check_user(message)
 gauth.LoadCredentialsFile(str(message))
 if gauth.credentials is None:
   LOGS.info("NOT AUTH USERS")
 elif gauth.access_token_expired:
  gauth.Refresh() ## # Refresh Them If Expired ##
  gauth.SaveCredentialsFile(str(message))
 else:
  gauth.Authorize() ## Initialize The Saved Credentials ##
  drive = GoogleDrive(gauth)
  http = drive.auth.Get_Http_Object()
  if not path.exists(filename):
   LOGS.info(f"Specified filename {filename} does not exist!")
   return
  if not Creds.TEAMDRIVE_FOLDER_ID :
   if parent_folder:
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file_folder in file_list:
     if file_folder['title'] == parent_folder:
      folderid = file_folder['id'] ## Getting Matching Folder Id ##
      LOGS.info("Folder Already Exist  !!  Trying To Upload")
      break
    else:
     folder_metadata = {'title': parent_folder, 'mimeType': 'application/vnd.google-apps.folder'} ## Creating Folder ##
     folder = drive.CreateFile(folder_metadata)
     folder.Upload()
     folderid = folder['id']
     foldertitle = folder['title']  ## Get Folder Info And Print To Screen ##
     LOGS.info('title: %s, id: %s' % (foldertitle, folderid))
  file_params = {'title': filename.split('/')[-1]}   
  if Creds.TEAMDRIVE_FOLDER_ID :
        file_params['parents'] = [{"kind": "drive#fileLink", "teamDriveId": Creds.TEAMDRIVE_ID, "id": Creds.TEAMDRIVE_FOLDER_ID}]
  else:
   if parent_folder:
    file_params['parents'] = [{"kind": "drive#fileLink", "id": folderid}]
  file_to_upload = drive.CreateFile(file_params)
  file_to_upload.SetContentFile(filename)
  try:
      file_to_upload.Upload(param={"supportsTeamDrives" : True})
      return file_to_upload['webContentLink']
  except Exception as e:
      LOGS.info(e)
#  if not Creds.TEAMDRIVE_FOLDER_ID:
#    file_to_upload.FetchMetadata()
#   file_to_upload.InsertPermission({'type':  'anyone', 'value': 'anyone', 'role':  'reader', 'withLink': True})
