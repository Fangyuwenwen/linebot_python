"""import requests
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
          'action': {'type': 'message', 'text':'請輸入天氣 +縣市'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 1251, 'y': 0, 'width':625, 'height': 640},     # 選單位置與大小
          'action': {'type': 'message', 'text':'雷達'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1879, 'y': 0, 'width':625, 'height': 640},     # 選單位置與大小
          'action': {'type': 'message', 'text':'地震'}               # 點擊後傳送文字
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

with open("richmenu.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-2e312eeeba3bd139bea7c3de9438002f", "image/jpeg", f)"""
    
import requests

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-2e312eeeba3bd139bea7c3de9438002f', 
                       headers=headers)

print(req.text)

"""from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=')

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
    
#line_bot_api.delete_rich_menu('richmenu-d431d553a1d0af71c5844940093e8e5f')"""