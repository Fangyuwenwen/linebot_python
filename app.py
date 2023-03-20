import requests
import statistics
import time
import datetime
import errno
import json
import os
import sys
import tempfile
import news.py
from urllib.request import urlopen
from argparse import ArgumentParser


from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

#thingspeak
READ_API_KEY='O0TENR74YMQ8ORIT'
CHANNEL_ID='1886703'

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

#取得溫度和濕度
TS = urlopen("https://api.thingspeak.com/channels/1886703/feeds.json?api_key=O0TENR74YMQ8ORIT&results=2")
response = TS.read()
data=json.loads(response.decode('utf-8'))
tem_value=str(data["channel"]["field1"]+data["feeds"][1]["field1"])
hum_value=str(data["channel"]["field2"]+data["feeds"][1]["field2"])

#取得天氣資料
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']

def get(city):
    token = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    Data = (json.loads(Data.text))['records']['location'][0]['weatherElement']
    res = [[] , [] , []]
    for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
    return res

    
# 取得空氣品質
def city_status(city):
    city_list, site_list ={}, {}
    msg = '找不到空氣品質資訊。'
    try:
        # 2022/12 時氣象局有修改了 API 內容，將部份大小寫混合全改成小寫，因此程式碼也跟著修正
        url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
        a_data = requests.get(url)             # 使用 get 方法透過空氣品質指標 API 取得內容
        a_data_json = a_data.json()            # json 格式化訊息內容
        for i in a_data_json['records']:       # 依序取出 records 內容的每個項目
            city = i['county']                 # 取出縣市名稱
            if city not in city_list:
                city_list[city]=[]             # 以縣市名稱為 key，準備存入串列資料
            site = i['sitename']               # 取出鄉鎮區域名稱
            aqi = int(i['aqi'])                # 取得 AQI 數值
            status = i['status']               # 取得空氣品質狀態
            site_list[site] = {'aqi':aqi, 'status':status}  # 記錄鄉鎮區域空氣品質
            city_list[city].append(aqi)        # 將各個縣市裡的鄉鎮區域空氣 aqi 數值，以串列方式放入縣市名稱的變數裡
        for i in city_list:
            if i in city: # 如果地址裡包含縣市名稱的 key，就直接使用對應的內容
                # https://airtw.epa.gov.tw/cht/Information/Standard/AirQualityIndicator.aspx
                aqi_val = round(statistics.mean(city_list[i]),0)  # 計算平均數值，如果找不到鄉鎮區域，就使用縣市的平均值
                aqi_status = ''  # 手動判斷對應的空氣品質說明文字
                if aqi_val<=50: aqi_status = '良好'
                elif aqi_val>50 and aqi_val<=100: aqi_status = '普通'
                elif aqi_val>100 and aqi_val<=150: aqi_status = '對敏感族群不健康'
                elif aqi_val>150 and aqi_val<=200: aqi_status = '對所有族群不健康'
                elif aqi_val>200 and aqi_val<=300: aqi_status = '非常不健康'
                else: aqi_status = '危害'
                msg = f'空氣品質{aqi_status} ( AQI {aqi_val} )。' # 定義回傳的訊息
                break
        for i in site_list:
            if i in city:  # 如果地址裡包含鄉鎮區域名稱的 key，就直接使用對應的內容
                msg = f'空氣品質{site_list[i]["status"]} ( AQI {site_list[i]["aqi"]} )。'
                break
        return msg    # 回傳 msg
    except:
        return msg    # 如果取資料有發生錯誤，直接回傳 msg
    
#取得地震資訊
def earth_quake():
    msg = ['找不到地震資訊','找不到地震資訊']            # 預設回傳的訊息
    code = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'  #https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8
    url ='https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization='+code
    e_data = requests.get(url)                                   # 爬取地震資訊網址
    e_data_json = e_data.json()                                  # json 格式化訊息內容
    eq = e_data_json['records']['Earthquake']                    # 取出地震資訊
    for i in eq:
        loc = i['EarthquakeInfo']['Epicenter']['Location']       # 地震地點
        val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] # 地震規模
        dep = i['EarthquakeInfo']['FocalDepth']              # 地震深度
        eq_time = i['EarthquakeInfo']['OriginTime']              # 地震時間
        img = i['ReportImageURI']                                # 地震圖
        msg = [f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}。', img]
        break     # 取出第一筆資料後就 break
    return msg    # 回傳 msg

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == '溫度':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=tem_value))
    elif message_text == '濕度':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=hum_value))
    elif message_text == '圖表':
        flexmessage= json.load(open('flex.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage('圖表',flexmessage)
        )
    elif message_text[:2] == '天氣':
        city = message_text[3:]
        city = city.replace('台','臺')
        if(not (city in cities)):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="查詢格式為: 天氣 縣市"))
        else:
            res = get(city)
            line_bot_api.reply_message(
                event.reply_token, TemplateSendMessage(
                alt_text = city + '未來天氣預測',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                            title = '{} ~ {}'.format(data[0]['startTime'][5:-3],data[0]['endTime'][5:-3]),
                            text = '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                            actions = [
                                URIAction(
                                    label = '詳細內容',
                                    uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                )
                            ]
                        )for data in res
                    ]
                )
            ))
    elif message_text[:2] == '空氣':
        city = message_text[3:]
        city = city.replace('台','臺')
        if(not (city in cities)):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="查詢格式為: 空氣 縣市"))
        else:
            msg = city_status(city)
            line_bot_api.reply_message(
                event.reply_token, TemplateSendMessage(
                alt_text = city + '目前空氣品質',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                            title = city+'目前空氣品質',
                            text = msg,
                            actions = [
                                URIAction(
                                    label = '詳細內容',
                                    uri = 'https://airtw.epa.gov.tw/'
                                )
                            ]
                        )
                    ]
                )
            ))
    elif message_text == '雷達':
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(original_content_url='https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?', preview_image_url='https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?')
                )
    elif message_text == '地震':
        msg=earth_quake()
        #line_bot_api.push_message('你的 User ID', TextSendMessage(text='Hello World!!!'))
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=msg[0])
        )
        line_bot_api.reply_message(
            event.reply_token, 
            ImageSendMessage(original_content_url=msg[1],preview_image_url=msg[1])
        )
    elif message_text == '新聞':
        now_news=news()
        line_bot_api.reply_message(
            event.reply_token, TemplateSendMessage(
            alt_text = '最新熱門新聞',
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                        title = '最新熱門新聞',
                        text = '新聞標題:'+now_news[['title']],
                        actions = [
                            URIAction(
                                label = '詳細內容',
                                uri = now_news[['title']]
                            )
                        ]
                    )
                ]
            )
        )
    )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請輸入正確關鍵字'))

@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    news.news()
    
    app.run(debug=options.debug, port=options.port)