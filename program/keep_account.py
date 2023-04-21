from google.oauth2.service_account import Credentials
import gspread
import pandas as pd

scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file("keep_account.json", scopes=scope)
gs = gspread.authorize(creds)
sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1203YlnhYjZ8hdVujCRbyAouVmQH8OWQ4M1YNk40GU6E/edit#gid=0')
wks_list = sheet.worksheets()
print(wks_list)