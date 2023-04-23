"""import requests
import json

# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 843},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'menu_1',                             # 選單名稱
    'chatBarText': '功能選單',                        # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 794, 'height': 255},           # 選單位置與大小
          'action': {'type': 'message', 'text':'新聞'} 
        },
        {
          'bounds': {'x': 0, 'y': 255, 'width':794, 'height': 276},     # 選單位置與大小
          'action': {'type': 'richmenuswitch', 'richMenuAliasId':'menu_2','data':'richmenu=menu_2'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 0, 'y': 535, 'width':794, 'height': 307},     # 選單位置與大小
          'action': {'type': 'message', 'text':'地圖'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 794, 'y': 0, 'width': 905, 'height': 255},           # 選單位置與大小
          'action': {'type': 'message', 'text':'定位'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 794, 'y': 255, 'width': 905, 'height': 279},           # 選單位置與大小
          'action': {'type': 'richmenuswitch', 'richMenuAliasId':'menu_3','data':'richmenu=menu_3'} 
        },
        {
          'bounds': {'x': 794, 'y': 535, 'width': 905, 'height': 307},           # 選單位置與大小
          'action': {'type': 'message', 'text':'餐廳'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 1699, 'y': 9, 'width': 801, 'height': 252},           # 選單位置與大小
          'action': {'type': 'richmenuswitch', 'richMenuAliasId':'menu_4','data':'richmenu=menu_4'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 1699, 'y': 261, 'width': 801, 'height': 274},           # 選單位置與大小
          'action': {'type': 'message', 'text':'景點'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 1699, 'y': 535, 'width': 801, 'height': 307},           # 選單位置與大小
          'action': {'type': 'message', 'text':'住宿'}  # 點擊後開啟地圖定位，傳送位置資訊
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

with open("menu1.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-29136b645b8b8b86bf4e6f5109036f55", "image/jpeg", f)"""
    
"""import requests,json

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "richMenuAliasId":"menu_1",
    "richMenuId":"richmenu-29136b645b8b8b86bf4e6f5109036f55"
}
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)"""

import requests
headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-29136b645b8b8b86bf4e6f5109036f55', headers=headers)
print(req.text)

"""from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=')

rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
    
line_bot_api.delete_rich_menu('richmenu-9e38a19e8b18429071b22e758501402f')"""

"""import requests
import json

# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 843},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'menu_2',                             # 選單名稱
    'chatBarText': '功能選單',                        # 選單在 LINE 顯示的標題
    'areas':[ 
        {
          'bounds': {'x': 0, 'y': 3, 'width': 2500, 'height': 282},           # 選單位置與大小
          'action': {'type': 'richmenuswitch', 'richMenuAliasId':'menu_1','data':'richmenu=menu_1'} 
        },                                                                    # 選單內容
        {
          'bounds': {'x': 0, 'y': 290, 'width': 1250, 'height': 270},           # 選單位置與大小
          'action': {'type': 'message', 'text':'天氣'} 
        },
        {
          'bounds': {'x': 0, 'y': 560, 'width':1250, 'height': 280},     # 選單位置與大小
          'action': {'type': 'message', 'text':'地震'}                   # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1250, 'y': 290, 'width':1250, 'height': 270},     # 選單位置與大小
          'action': {'type': 'message', 'text':'空氣'}                    # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1250, 'y':567, 'width': 1250, 'height': 278},           # 選單位置與大小
          'action': {'type': 'message', 'text':'雷達'}                          # 點擊後傳送文字
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

with open("menu2.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-7b1c6a164f936703b4a011e2c9211e13", "image/jpeg", f)"""

"""import requests
import json
headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
body = {
    "richMenuAliasId":"menu_2",
    "richMenuId":"richmenu-7b1c6a164f936703b4a011e2c9211e13"
}
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)"""
    
"""import requests

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-7b1c6a164f936703b4a011e2c9211e13', 
                       headers=headers)

print(req.text)"""

"""import requests
import json

# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 843},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'menu_3',                             # 選單名稱
    'chatBarText': '功能選單',                        # 選單在 LINE 顯示的標題
    'areas':[ 
        {
          'bounds': {'x': 0, 'y': 0, 'width': 2500, 'height': 280},           # 選單位置與大小
          'action': {'type': 'richmenuswitch', 'richMenuAliasId':'menu_1','data':'richmenu=menu_1'} 
        },                                                                    # 選單內容
        {
          'bounds': {'x': 0, 'y': 285, 'width': 832, 'height': 275},           # 選單位置與大小
          'action': {'type': 'message', 'text':'高鐵'} 
        },
        {
          'bounds': {'x': 0, 'y': 564, 'width':832, 'height': 279},     # 選單位置與大小
          'action': {'type': 'message', 'text':'台鐵'}                   # 點擊後傳送文字
        },
        {
          'bounds': {'x': 836, 'y': 284, 'width':828, 'height': 275},     # 選單位置與大小
          'action': {'type': 'message', 'text':'火車'}                    # 點擊後傳送文字
        },
        {
          'bounds': {'x': 836, 'y':564, 'width': 828, 'height': 279},           # 選單位置與大小
          'action': {'type': 'message', 'text':'公車'}                          # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1668, 'y':284, 'width': 832, 'height': 284},           # 選單位置與大小
          'action': {'type': 'message', 'text':'停車位'}                          # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1668, 'y':564, 'width': 832, 'height': 279},           # 選單位置與大小
          'action': {'type': 'message', 'text':'公共自行車'}                          # 點擊後傳送文字
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

with open("menu3.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-9ddea1d322d2ae4889dce52ff462284e", "image/jpeg", f)"""

"""import requests
import json
headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
body = {
    "richMenuAliasId":"menu_3",
    "richMenuId":"richmenu-9ddea1d322d2ae4889dce52ff462284e"
}
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)"""
    
"""import requests

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-9ddea1d322d2ae4889dce52ff462284e', 
                       headers=headers)

print(req.text)"""


"""import requests
headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
req = requests.request('GET', 'https://api.line.me/v2/bot/richmenu/alias/list', headers=headers)
print(req.text)"""

"""from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=')

line_bot_api.delete_rich_menu_alias('menu_1')"""

"""import requests
import json

# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 843},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'menu_4',                             # 選單名稱
    'chatBarText': '功能選單',                        # 選單在 LINE 顯示的標題
    'areas':[ 
        {
          'bounds': {'x': 0, 'y': 0, 'width': 2500, 'height': 298},           # 選單位置與大小
          'action': {'type': 'richmenuswitch', 'richMenuAliasId':'menu_1','data':'richmenu=menu_1'} 
        },                                                                    # 選單內容
        {
          'bounds': {'x': 0, 'y': 298, 'width': 1250, 'height': 546},           # 選單位置與大小
          'action': {'type': 'message', 'text':'英漢字典'} 
        },
        {
          'bounds': {'x': 1250, 'y': 298, 'width':1250, 'height': 546},     # 選單位置與大小
          'action': {'type': 'message', 'text':'中油油價'}                   # 點擊後傳送文字
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

with open("menu4.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-c24e1cd58e01ceea3e496ba86987acea", "image/jpeg", f)"""

"""import requests
import json
headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
body = {
    "richMenuAliasId":"menu_4",
    "richMenuId":"richmenu-c24e1cd58e01ceea3e496ba86987acea"
}
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)"""
    
"""import requests

headers = {"Authorization":"Bearer 4kW19F7L5Yt+DKSvppThCuirviV8iyqGcEYrg8aM2NjaDNl4zyA5fsFebqJusjAEb5CLVAD/dC7eDl3m7E64ByD6qOoUB0h+jyFRZkfq5tZ+gBxdd/adTJri+vdiikYKn9J58RLux6L14oElp7BBRwdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-c24e1cd58e01ceea3e496ba86987acea', 
                       headers=headers)

print(req.text)"""