import requests
import json

# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 640},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'bbb',                             # 選單名稱
    'chatBarText': 'b',                        # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 1250, 'height': 640},           # 選單位置與大小
          'action': {'type': 'uri', 'uri': 'https://line.me/R/nv/location/'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 1251, 'y': 0, 'width':625, 'height': 640},     # 選單位置與大小
          'action': {'type': 'message', 'text':'雷達回波圖'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1879, 'y': 0, 'width':625, 'height': 640},     # 選單位置與大小
          'action': {'type': 'message', 'text':'地震資訊'}               # 點擊後傳送文字
        }
    ]
  }
# 向指定網址發送 request
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers,data=json.dumps(body).encode('utf-8'))

from linebot import (LineBotApi, WebhookHandler)

line_bot_api = LineBotApi('4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=')

with open("richmenu.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-d431d553a1d0af71c5844940093e8e5f", "image/jpeg", f)

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=", "Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-d431d553a1d0af71c5844940093e8e5f', 
                      headers=headers)

# 印出得到的結果
print(req.text)