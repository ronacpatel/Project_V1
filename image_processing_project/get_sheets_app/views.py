


import os
import re
import json
import base64
from django.http import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_key_file_path():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    key_file_path = os.path.join(current_directory, 'key.json')
    return key_file_path


credentials = service_account.Credentials.from_service_account_file(
    get_key_file_path(),
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)


drive_service = build('drive', 'v3', credentials=credentials)


sheets_service = build('sheets', 'v4', credentials=credentials)


def get_folder_name(folder_id):
    folder_info = drive_service.files().get(fileId=folder_id, fields='name').execute()
    return folder_info.get('name')


def get_sheet_info(sheet_id):
    try:
        sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])

        sheet_info = []

        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={sheet['properties']['sheetId']}"

            
            sheet_content = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}').execute()
            values = sheet_content.get('values', [])

            
            sheet_data = []
            if values:
                for row in values:
                    sheet_data.append(row)

            sheet_info.append({
                "sheet_name": sheet_name,
                "sheet_url": sheet_url,
                "sheet_data": sheet_data  
            })

        return sheet_info
    except HttpError as err:
        if err.resp.status == 404:
            return None 
        else:
            raise

def get_google_drive_info(request):
    
    google_sheets_info = []

    
    results = drive_service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'", fields="files(id, name, parents)").execute()
    files = results.get('files', [])

    
    for file in files:
        sheet_name = file['name']
        sheet_id = file['id']
        folder_ids = file.get('parents', [])

        
        folder_names = [get_folder_name(folder_id) for folder_id in folder_ids]

        
        sheet_info = get_sheet_info(sheet_id)
        if sheet_info is not None:
            google_sheets_info.append({
                'Sheet Name': sheet_name,
                'Sheet ID': sheet_id,
                'Folder Names': folder_names,
                'Sheet Info': sheet_info
            })

    
    data_to_api = []
    for info in google_sheets_info:
        data_to_api.append({
            'Sheet Name': info['Sheet Name'],
            'Sheet ID': info['Sheet ID'],
            'Folder Names': info['Folder Names'],
            'Sheet Info': info['Sheet Info']
        })

    
    return JsonResponse({"sheet_info": data_to_api}, safe=False)
