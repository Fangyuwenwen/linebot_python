"""import requests
import json

# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 843},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': '選單',                             # 選單名稱
    'chatBarText': '功能選單',                        # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 625, 'height': 843},           # 選單位置與大小
          'action': {'type': 'message', 'text':'天氣'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 625, 'y': 0, 'width':625, 'height': 843},     # 選單位置與大小
          'action': {'type': 'message', 'text':'雷達'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1250, 'y': 0, 'width':625, 'height': 843},     # 選單位置與大小
          'action': {'type': 'message', 'text':'地震'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1875, 'y': 0, 'width': 625, 'height': 843},           # 選單位置與大小
          'action': {'type': 'message', 'text':'空氣'}  # 點擊後開啟地圖定位，傳送位置資訊
        }
    ]
  }
# 向指定網址發送 request
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))
# 印出得到的結果
print(req.text)"""

"""from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=')

with open("menu.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-f55bbd7524cd6ab120fa6519d17154e7", "image/jpeg", f)"""
    
import requests

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-f55bbd7524cd6ab120fa6519d17154e7', 
                       headers=headers)

print(req.text)

"""from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=')

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)"""
    
#line_bot_api.delete_rich_menu('richmenu-d431d553a1d0af71c5844940093e8e5f')"""