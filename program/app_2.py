import requests
import statistics
import errno
import json
import os
import sys
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import re
import wsgiref.simple_server
from argparse import ArgumentParser

from urllib.request import urlopen
from argparse import ArgumentParser


from flask import Flask, request, abort

from builtins import bytes
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,MessageTemplateAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage,PostbackTemplateAction)

from linebot.utils import PY3

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

#thingspeak
READ_API_KEY='O0TENR74YMQ8ORIT'
CHANNEL_ID='1886703'

#tdx
client_id = '11061108-00b12e58-30cf-432d'
client_secret = 'fac2feb7-d9a9-4389-be90-b71c4c69671f'

#tdx會員登入
class TDX():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        token_url = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(token_url, headers=headers, data=data)
        # print(response.status_code)
        # print(response.json())
        return response.json()['access_token']

    def get_response(self, url):
        headers = {'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        return response.json()

#取得溫度和濕度
#TS = urlopen("https://api.thingspeak.com/channels/1886703/feeds.json?api_key=O0TENR74YMQ8ORIT&results=2")
#response = TS.read()
#data=json.loads(response.decode('utf-8'))
#tem_value=str(data["channel"]["field1"]+data["feeds"][1]["field1"])
#hum_value=str(data["channel"]["field2"]+data["feeds"][1]["field2"])

#取得天氣資料
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']

def get(city):
    token = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
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
    # 2022/12 時氣象局有修改了 API 內容，將部份大小寫混合全改成小寫，因此程式碼也跟著修正
    url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=ee00f31a-b8e7-42cf-bf73-71f383609760&limit=1000&sort=ImportDate%20desc&format=JSON'
    a_data = requests.get(url)             # 使用 get 方法透過空氣品質指標 API 取得內容
    a_data_json = a_data.json()            # json 格式化訊息內容
    for i in a_data_json['records']:       # 依序取出 records 內容的每個項目
        city = i['county']                 # 取出縣市名稱
        if city not in city_list:
            city_list[city]=[]             # 以縣市名稱為 key，準備存入串列資料
        site = i['sitename']               # 取出鄉鎮區域名稱
        if i['aqi']:
            aqi = int(i['aqi'])  
        else:
            aqi=0                          # 取得 AQI 數值
        status = i['status']               # 取得空氣品質狀態
        pm10 = i ['pm10']
        publishtime= i['publishtime']
        site_list[site] = {'aqi':aqi,'pm10':pm10 ,'status':status}  # 記錄鄉鎮區域空氣品質
        city_list[city].append(aqi)        # 將各個縣市裡的鄉鎮區域空氣 aqi 數值，以串列方式放入縣市名稱的變數裡
    for i in city_list:
        if i in city: # 如果地址裡包含縣市名稱的 key，就直接使用對應的內容
            # 參考 https://airtw.epa.gov.tw/cht/Information/Standard/AirQualityIndicator.aspx
            aqi_val = round(statistics.mean(city_list[i]),0)  # 計算平均數值，如果找不到鄉鎮區域，就使用縣市的平均值
            aqi_status = ''  # 手動判斷對應的空氣品質說明文字
            if aqi_val<=50: aqi_status = '良好'
            elif aqi_val>50 and aqi_val<=100: aqi_status = '普通'
            elif aqi_val>100 and aqi_val<=150: aqi_status = '對敏感族群不健康'
            elif aqi_val>150 and aqi_val<=200: aqi_status = '對所有族群不健康'
            elif aqi_val>200 and aqi_val<=300: aqi_status = '非常不健康'
            else: aqi_status = '危害'
            msg = f'空氣品質{aqi_status} \n AQI {aqi_val} \n pm10 {pm10} \n 資料發布時間 {publishtime}' # 定義回傳的訊息
            break
    for i in site_list:
        if i in city:  # 如果地址裡包含鄉鎮區域名稱的 key，就直接使用對應的內容
            msg = f'空氣品質{aqi_status} \n AQI {aqi_val} \n pm10 {pm10} \n 資料發布時間 {publishtime}'
            break
    return msg    # 回傳 msg
    
#取得地震資訊
def earth_quake():
    msg = ['找不到地震資訊','找不到地震資訊']            # 預設回傳的訊息
    code = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'  #https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8
    url ='https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization='+code
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

#取得最新新聞
def news(): 
    url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    r = requests.get(url)
    web_content = r.text
    soup = BeautifulSoup(web_content,'lxml')
    web_url = soup.find_all('div', class_='XlKvRb',limit=10)
    title = soup.find_all('a',class_='gPFEn',limit=10)
    titles = [t.text for t in title]
    newUrls = [requests.get(t.find('a')['href'].replace('.','https://news.google.com',1)).url for t in web_url]
    for i in range(len(titles)):
        #print(titles[i-1])
        if len(titles[i-1])>55:
            newUrls.pop(titles.index(titles[i-1]))
            titles.remove(titles[i-1])
    #print(newUrls)
    df = pd.DataFrame(
    {
        'title': titles,
        'links': newUrls
    })
    js = df.to_json(orient = 'records',force_ascii=False)
    return js

#取得高鐵時刻表
thsr_stations='{"南港": "0990", "臺北": "1000", "板橋": "1010", "桃園": "1020", "新竹": "1030", "苗栗": "1035", "台中": "1040", "彰化": "1043", "雲林": "1047", "嘉義": "1050", "台南": "1060", "左營": "1070"}'
thsr_city=['南港','臺北','板橋','桃園','新竹','苗栗','台中','彰化','雲林','嘉義','台南','左營']
def thsr_time(u_date,u_time,u_od,u_to):
    tdx = TDX(client_id, client_secret)
    y = json.loads(thsr_stations)
    #url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/OD/1047/to/1070/2023-03-22?%24top=30&%24format=JSON' 
    base_url = "https://tdx.transportdata.tw/api"
    endpoint = "/basic/v2/Rail/THSR/DailyTimetable/"
    od='OD/'+y[u_od]+'/'
    to='to/'+y[u_to]+'/'
    date=u_date
    filter = "?%24top=60&%24format=JSON"
    url = base_url+endpoint+od+to+date+filter
    response = tdx.get_response(url)
    #print(response)
    t_no=[]
    OriginStop=[]
    DestinationStop=[]
    #s_time={}
    for i in response :
        if i['OriginStopTime']['ArrivalTime'] >= u_time :
            t_no.append(i["DailyTrainInfo"]["TrainNo"]) #車次
            OriginStop.append(i['OriginStopTime']['StationName']['Zh_tw']+" "+i['OriginStopTime']['ArrivalTime']) #出發+出發時間
            DestinationStop.append(i['DestinationStopTime']['StationName']['Zh_tw']+" "+i['DestinationStopTime']['ArrivalTime']) #抵達+抵達時間
        #stop=zip(OriginStop,DestinationStop)
        #s_time=dict(stop)
    #print(s_time)
    df = pd.DataFrame(
    {
        't_no': t_no,
        'OriginStop': OriginStop,
        'DestinationStop':DestinationStop
    })
    js = df.to_json(orient = 'records',force_ascii=False)
    return(js)

#取得台鐵時刻表
tra_stations='{"基隆": "0900", "三坑": "0910", "八堵": "0920", "七堵": "0930", "百福": "0940", "五堵": "0950", "汐止": "0960", "汐科": "0970", "南港": "0980", "松山": "0990", "臺北": "1000", "臺北-環島": "1001", "萬華": "1010", "板橋": "1020", "浮洲": "1030", "樹林": "1040", "南樹林": "1050", "山佳": "1060", "鶯歌": "1070", "桃園": "1080", "內壢": "1090", "中壢": "1100", "埔心": "1110", "楊梅": "1120", "富岡": "1130", "新富": "1140", "北湖": "1150", "湖口": "1160", "新豐": "1170", "竹北": "1180", "北新竹": "1190", "千甲": "1191", "新莊": "1192", "竹中": "1193", "六家": "1194", "上員": "1201", "榮華": "1202", "竹東": "1203", "橫山": "1204", "九讚頭": "1205", "合興": "1206", "富貴": "1207", "內灣": "1208", "新竹": "1210", "三姓橋": "1220", "香山": "1230", "崎頂": "1240", "竹南": "1250", "談文": "2110", "大山": "2120", "後龍": "2130", "龍港": "2140", "白沙屯": "2150", "新埔": "2160", "通霄": "2170", "苑裡": "2180", "日南": "2190", "大甲": "2200", "臺中港": "2210", "清水": "2220", "沙鹿": "2230", "龍井": "2240", "大肚": "2250", "追分": "2260", "造橋": "3140", "豐富": "3150", "苗栗": "3160", "南勢": "3170", "銅鑼": "3180", "三義": "3190", "泰安": "3210", "后里": "3220", "豐原": "3230", "栗林": "3240", "潭子": "3250", "頭家厝": "3260", "松竹": "3270", "太原": "3280", "精武": "3290", "臺中": "3300", "五權": "3310", "大慶": "3320", "烏日": "3330", "新烏日": "3340", "成功": "3350", "彰化": "3360", "花壇": "3370", "大村": "3380", "員林": "3390", "永靖": "3400", "社頭": "3410", "田中": "3420", "二水": "3430", "源泉": "3431", "濁水": "3432", "龍泉": "3433", "集集": "3434", "水里": "3435", "車埕": "3436","林內": "3450", "石榴": "3460", "斗六": "3470", "斗南": "3480", "石龜": "3490", "大林": "4050", "民雄": "4060", "嘉北": "4070", "嘉義": "4080", "水上": "4090", "南靖": "4100","後壁": "4110", "新營": "4120", "柳營": "4130", "林鳳營": "4140", "隆田": "4150", "拔林": "4160", "善化": "4170", "南科": "4180", "新市": "4190", "永康": "4200", "大橋": "4210","臺南": "4220", "保安": "4250", "仁德": "4260", "中洲": "4270", "長榮大學": "4271", "沙崙": "4272", "大湖": "4290", "路竹": "4300", "岡山": "4310", "橋頭": "4320", "楠梓": "4330","新左營": "4340", "左營": "4350", "內惟": "4360", "美術館": "4370", "鼓山": "4380", "三塊厝": "4390", "高雄": "4400", "民族": "4410", "科工館": "4420", "正義": "4430", "鳳山": "4440","後庄": "4450", "九曲堂": "4460", "六塊厝": "4470", "屏東": "5000", "歸來": "5010", "麟洛": "5020", "西勢": "5030", "竹田": "5040", "潮州": "5050", "崁頂": "5060", "南州": "5070", "鎮安": "5080", "林邊": "5090", "佳冬": "5100", "東海": "5110", "枋寮": "5120", "加祿": "5130", "內獅": "5140", "枋山": "5160", "枋野": "5170", "大武": "5190", "瀧溪": "5200","金崙": "5210", "太麻里": "5220", "知本": "5230", "康樂": "5240", "潮州基地": "5999", "臺東": "6000", "山里": "6010", "鹿野": "6020", "瑞源": "6030", "瑞和": "6040", "關山": "6050", "海端": "6060", "池上": "6070", "富里": "6080", "東竹": "6090", "東里": "6100", "玉里": "6110", "三民": "6120", "瑞穗": "6130", "富源": "6140", "大富": "6150", "光復": "6160","萬榮": "6170", "鳳林": "6180", "南平": "6190", "林榮新光": "6200", "豐田": "6210", "壽豐": "6220", "平和": "6230", "志學": "6240", "吉安": "6250", "花蓮": "7000", "北埔": "7010","景美": "7020", "新城": "7030", "崇德": "7040", "和仁": "7050", "和平": "7060", "漢本": "7070", "武塔": "7080", "南澳": "7090", "東澳": "7100", "永樂": "7110", "蘇澳": "7120", "蘇澳新": "7130", "新馬": "7140", "冬山": "7150", "羅東": "7160", "中里": "7170", "二結": "7180", "宜蘭": "7190", "四城": "7200", "礁溪": "7210", "頂埔": "7220", "頭城": "7230","外澳": "7240", "龜山": "7250", "大溪": "7260", "大里": "7270", "石城": "7280", "福隆": "7290", "貢寮": "7300", "雙溪": "7310", "牡丹": "7320", "三貂嶺": "7330", "大華": "7331","十分": "7332", "望古": "7333", "嶺腳": "7334", "平溪": "7335", "菁桐": "7336", "猴硐": "7350", "瑞芳": "7360", "海科館": "7361", "八斗子": "7362", "四腳亭": "7380", "暖暖": "7390"}'
tra_city=['基隆', '三坑', '八堵', '七堵', '百福', '五堵', '汐止', '汐科', '南港', '松山', '臺北', '臺北-環島', '萬華', '板橋', '浮洲', '樹林', '南樹林', '山佳', '鶯歌', '桃園', '內壢', '中壢', '埔心', '楊梅', '富岡', '新富', '北湖', '湖口', '新豐', '竹北', '北新竹', '千甲', '新莊', '竹中', '六家', '上員', '榮華', '竹東', '橫山', '九讚頭', '合興', '富貴', '內灣', '新竹', '三姓橋', '香山', '崎頂', '竹南', '談文', '大山', '後龍', '龍港', '白沙屯', '新埔', '通霄', '苑裡', '日南', '大甲', '臺中港', '清水', '沙鹿', '龍井', '大肚', '追分', '造橋', '豐富', '苗栗', '南勢', '銅鑼', '三義', '泰安', '后里', '豐原', '栗林', '潭子', '頭家厝', '松竹', '太原', '精武', '臺中', '五權', '大慶', '烏日', '新烏日', '成功', '彰化', '花壇', '大村', '員林', '永靖', '社頭', '田中', '二水', '源泉', '濁水', '龍泉', '集集', '水里', '車埕', '林內', '石榴', '斗六', '斗南', '石龜', '大林', '民雄', '嘉北', '嘉義', '水上', '南靖', '後壁', '新營', '柳營', '林鳳營', '隆田', '拔林', '善化', '南科', '新市', '永康', '大橋', '臺南', '保安', '仁德', '中洲', '長榮大學', '沙崙', '大湖', '路竹', '岡山', '橋頭', '楠梓', '新左營', '左營', '內惟', '美術館', '鼓山', '三塊厝', '高雄', '民族', '科工館', '正義', '鳳山', '後庄', '九曲堂', '六塊厝', '屏東', '歸來', '麟洛', '西勢', '竹田', '潮州', '崁頂', '南州', '鎮安', '林邊', '佳冬', '東海', '枋寮', '加祿', '內獅', '枋山', '枋野', '大武', '瀧溪', '金崙', '太麻里', '知本', '康樂', '潮州基地', '臺東', '山里', '鹿野', '瑞源', '瑞和', '關山', '海端', '池上', '富里', '東竹', '東里', '玉里', '三民', '瑞穗', '富源', '大富', '光復', '萬榮', '鳳林', '南平', '林榮新光', '豐田', '壽豐', '平和', '志學', '吉安', '花蓮', '北埔', '景美', '新城', '崇德', '和仁', '和平', '漢本', '武塔', '南澳', '東澳', '永樂', '蘇澳', '蘇澳新', '新馬', '冬山', '羅東', '中里', '二結', '宜蘭', '四城', '礁溪', '頂埔', '頭城', '外澳', '龜山', '大溪', '大里', '石城', '福隆', '貢寮', '雙溪', '牡丹', '三貂嶺', '大華', '十分', '望古', '嶺腳', '平溪', '菁桐', '猴硐', '瑞芳', '海科館', '八斗子', '四腳亭', '暖暖']
def tra_time(u_date,u_time,u_od,u_to):
    tdx = TDX(client_id, client_secret)
    y = json.loads(tra_stations)
    #url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/DailyTimetable/OD/3470/to/4340/2023-03-24?%24top=30&%24format=JSON'
    base_url = "https://tdx.transportdata.tw/api"
    endpoint = "/basic/v2/Rail/TRA/DailyTimetable/"
    od="OD/"+ y[u_od]+"/"
    to="to/"+y[u_to]+"/"
    date=u_date
    filter = "?%24top=60&%24format=JSON"
    #filter = "Direction eq 1"  # 順逆行: [0:'順行', 1:'逆行']
    url = base_url+endpoint+od+to+date+filter
    response = tdx.get_response(url)
    #print(response)
    t_no=[]
    OriginStop=[]
    DestinationStop=[]
    #s_time={}
    for i in response :
        if i['OriginStopTime']['ArrivalTime'] >= u_time :
            t_no.append(i["DailyTrainInfo"]["TrainNo"]) #車次
            OriginStop.append(i['OriginStopTime']['StationName']['Zh_tw']+" "+i['OriginStopTime']['ArrivalTime']) #出發+出發時間
            DestinationStop.append(i['DestinationStopTime']['StationName']['Zh_tw']+" "+i['DestinationStopTime']['ArrivalTime']) #抵達+抵達時間
        #stop=zip(OriginStop,DestinationStop)
        #s_time=dict(stop)
    #print(s_time)
    df = pd.DataFrame(
    {
        't_no': t_no,
        'OriginStop': OriginStop,
        'DestinationStop':DestinationStop
    })
    js = df.to_json(orient = 'records',force_ascii=False)
    return(js)

#取得字典
def trans(word):
    url="https://tw.dictionary.search.yahoo.com/search?p="+word
    r = requests.get(url)
    web_content = r.text
    soup = BeautifulSoup(web_content,'lxml')
    w_mid = []
    w_trs = []
    #title = soup.find(class_="fz-24 fw-500 c-black lh-24")
    #print(title.text)
    for mid in soup.find_all(class_="pos_button fz-14 fl-l mr-12"):
        w_mid.append(mid.text)
        #print(mid.text)
    for trs in soup.find_all(class_ ="fz-16 fl-l dictionaryExplanation"):
        w_trs.append(trs.text)
        #print(trs.text)
    df = pd.DataFrame(
    {
        'w_mid': w_mid,
        'w_trs': w_trs
    })
    js = df.to_json(orient = 'records',force_ascii=False)
    return(js)

#讀取中油油價
def oil_price():
    url = "https://www.cpc.com.tw/historyprice.aspx?n=2890"
    resp = requests.get(url)
    m = re.search("var pieSeries = (.*);", resp.text)
    jsonstr = m.group(0).strip('var pieSeries = ').strip(";")
    j = json.loads(jsonstr)
    up_data = []
    oil92_data = []
    oil95_data = []
    oil98_data = []
    oilsuper_date = []
    msg=""
    for item in j[:7]:
        up_data.append(item['name'])
        for data in item['data']:
            oilsuper_date.append(data['name'] + ":" + str(data['y']))
    for item in j[7:14]:
        for data in item['data']:
            oil98_data.append(data['name'] + ":" + str(data['y']))
    for item in j[14:21]:
        for data in item['data']:
            oil95_data.append(data['name'] + ":" + str(data['y']))
    for item in j[21:28]:
        for data in item['data']:
            oil92_data.append(data['name'] + ":" + str(data['y']))
    for i,j,k,l,m in zip(up_data,oil92_data,oil95_data,oil98_data,oilsuper_date):
        msg += "更新時間:  "+i+"\n"+j+"\n"+k+"\n"+l+"\n"+m+"\n"
        #print(i+" "+j+" "+k+" "+l+" "+m)    
    return msg

#取得旅遊資訊
CarParkings = []
ScenicSpots = []
Hotels = []
Restaurants = []
RailStations = []
BusStations = []
BikeStations = []
       
def get_location(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        u_latitude = event.message.latitude
        u_longitude = event.message.longitude
        tdx = TDX(client_id, client_secret)
        #u_latitude = "23.70393"
        #u_longitude = "120.42887"
        #u_latitude = "24.10887"
        #u_longitude =  "120.62545"
        #url="https://tdx.transportdata.tw/api/advanced/V3/Map/GeoLocating/Tourism/Nearby/LocationX/120.62545/LocationY/24.10887/Distance/500?%24format=JSON"
        base_url = "https://tdx.transportdata.tw/api/advanced/V3/Map/GeoLocating/Tourism/Nearby/"
        endpoint = "/Distance/500?%24format=JSON"
        LocationX = "LocationX/"+str(u_longitude)+"/"
        LocationY = "LocationY/"+str(u_latitude)
        url = base_url+LocationX+LocationY+endpoint
        response = tdx.get_response(url)
        for i in response :
            CarParkings.append(i["CarParkings"]["CarParkingList"])
            ScenicSpots.append(i["ScenicSpots"]["ScenicSpotList"])
            Hotels.append(i["Hotels"]["HotelList"])
            Restaurants.append(i["Restaurants"]["RestaurantList"])
            RailStations.append(i["RailStations"]["RailStationList"])
            BusStations.append(i["BusStations"]["BusStationList"])
            BikeStations.append(i["BikeStations"]["BikeStationList"])
        line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                        alt_text = '附近交通及觀光資訊一覽',
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                                    title="附近交通及觀光資訊一覽",
                                    text="請選擇想要查詢的資訊",
                                    actions = [
                                        PostbackTemplateAction(
                                        label="停車位資訊",
                                        text="附近停車位資訊",
                                        data="停車位資訊"
                                        ),
                                        PostbackTemplateAction(
                                        label="觀光景點資訊",
                                        text="附近觀光景點資訊",
                                        data="觀光景點資訊"
                                    ),
                                    PostbackTemplateAction(
                                        label="住宿資訊",
                                        text="附近住宿資訊",
                                        data="住宿資訊"
                                    )
                                ]
                            ),
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                                    title="附近交通及觀光資訊一覽",
                                    text="請選擇想要查詢的資訊",
                                    actions=[
                                        PostbackTemplateAction(
                                            label="鐵路資訊",
                                            text="附近鐵路資訊",
                                            data="鐵路資訊"
                                        ),
                                        PostbackTemplateAction(
                                            label="公車資訊",
                                            text="附近公車資訊",
                                            data="公車資訊"
                                        ),
                                        PostbackTemplateAction(
                                            label="公共腳踏車資訊",
                                            text="附近公共腳踏車資訊",
                                            data="腳踏車資訊"
                                    )
                                ]
                            ),
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                                    title="附近交通及觀光資訊一覽",
                                    text="請選擇想要查詢的資訊",
                                    actions=[
                                        PostbackTemplateAction(
                                            label="餐廳資訊",
                                            text="附近餐廳資訊",
                                            data="餐廳資訊"
                                        ),
                                        URIAction(
                                            label = '開啟地圖',
                                            uri = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
                                        ),
                                        MessageTemplateAction(
                                            label='結束使用',
                                            text='查詢結束'
                                    )
                                ]
                            )            
                        ]
                    )
                )
            )

def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.type == 'text':
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
                    msg = city_status(city)
                    line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                        alt_text = city + '未來天氣預測',
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/VzKGQlk.jpg',
                                    title = '{} ~ {}'.format(data[0]['startTime'][5:-3],data[0]['endTime'][5:-3]),
                                    text = '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {} %'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                                    actions = [
                                        URIAction(
                                            label = '詳細內容',
                                            uri = 'https://www.cwa.gov.tw/V8/C/W/OBS_Map.html'
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
                        alt_text = city,
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/KBWYCgp.jpg',
                                    title = city,
                                    text = msg,
                                    actions = [
                                        URIAction(
                                            label = '詳細內容',
                                            uri = 'https://airtw.moenv.gov.tw/'
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
                item = json.loads(now_news)
                line_bot_api.reply_message(
                    event.reply_token, TemplateSendMessage(
                    alt_text = '最新熱門新聞',
                    template = CarouselTemplate(
                        columns = [
                            CarouselColumn(
                                thumbnail_image_url = 'https://i.imgur.com/vcLfL9y.jpg',
                                title = '最新熱門新聞',
                                text = '新聞標題:'+i['title'],
                                actions = [
                                    URIAction(
                                        label = '詳細內容',
                                        uri = i['links']
                                    )
                                ]
                            )for i in item
                        ]
                    )
                )
            )
            elif message_text[:2] == "高鐵":
                station = message_text[21:]
                if(not (station in thsr_city)):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入日期、時間、上車站、下車站 (ex.高鐵2023-03-23 14:00雲林到左營)"))
                else:
                    date = message_text[2:12]
                    time = message_text[13:18]
                    od = message_text[18:20]
                    to = message_text[21:]
                    thsr_t = thsr_time(date,time,od,to)
                    item = json.loads(thsr_t)
                    mes=" "
                    for i in item:
                        mes+="\n"+i["t_no"]+" "+i["OriginStop"]+" "+i["DestinationStop"]+"\n"
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="車次 "+" 上車時間 "+" 下車時間 "+mes)
                )
            elif message_text[:2] == "台鐵":
                if(message_text[2:6]!="2023"):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入日期、上車站、下車站 (ex.台鐵2023-03-23 08:00斗六到新左營)"))
                else:
                    date = message_text[2:12]
                    time = message_text[13:18]
                    if(message_text[18:20] in tra_city):
                        od = message_text[18:20]
                        to = message_text[21:]
                    elif(message_text[18:21] in tra_city):
                        od = message_text[18:21]
                        to = message_text[22:]
                    elif(message_text[18:22] in tra_city):
                        od = message_text[18:22]
                        to = message_text[23:]
                    thsr_t = tra_time(date,time,od,to)
                    item = json.loads(thsr_t)
                    mes=" "
                    for i in item:
                        mes+="\n"+i["t_no"]+" "+i["OriginStop"]+" "+i["DestinationStop"]+"\n"
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="車次 "+" 上車時間 "+" 下車時間 "+mes)
            )
                    
            elif message_text == "停車位" or message_text == "景點" or message_text == "住宿" or message_text == "餐廳" or message_text == "火車" or message_text == "公車" or message_text == "公共自行車" or message_text == "定位":
                line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                        alt_text = '請傳送目前位置',
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/XPOPLJS.jpg',
                                    text = "請傳送目前位置",
                                    actions = [
                                        URIAction(
                                            label = '傳送位置',
                                            uri = 'https://line.me/R/nv/location/'
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            elif message_text == "地圖" :
                line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                        alt_text = '打開google地圖',
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/bUdxsRx.jpg',
                                    text = "打開google地圖",
                                    actions = [
                                        URIAction(
                                            label = '傳送',
                                            uri = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            elif message_text == "附近停車位資訊" :
                mes=""
                mes_url = []
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in CarParkings:
                    for j in i :
                        mes_url.append("https://www.google.com.tw/maps/search/"+j['CarParkName'])
                        mes+=j['CarParkName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到停車場資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近停車場資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/7OOX4Sp.jpg',
                                                title = '停車場資料',
                                                text = '停車場名稱:'+j['CarParkName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                )
                            )
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近停車場資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/7OOX4Sp.jpg',
                                                title = '停車場資料',
                                                text = '停車場名稱:'+j['CarParkName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                )
            )
            elif message_text == "附近觀光景點資訊" :
                mes=""
                mes_url = []
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in ScenicSpots:
                    for j in i : 
                        mes_url.append("https://www.google.com.tw/maps/search/"+j['ScenicSpotName'])
                        mes+=j['ScenicSpotName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到觀光景點資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近觀光景點資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/n7dCKV6.jpg',
                                                title = '觀光景點資料',
                                                text = '觀光景點名稱:'+j['ScenicSpotName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                ))
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近觀光景點資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/n7dCKV6.jpg',
                                                title = '觀光景點資料',
                                                text = '觀光景點名稱:'+j['ScenicSpotName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                ))
            elif message_text == "附近住宿資訊" :
                mes=""
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in Hotels:
                    for j in i :
                        mes+=j['HotelName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到住宿資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近住宿資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/Ingra3v.jpg',
                                                title = '住宿資料',
                                                text = '住宿名稱:'+j['HotelName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                ))
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近住宿資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/Ingra3v.jpg',
                                                title = '住宿資料',
                                                text = '住宿名稱:'+j['HotelName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                ))
            elif message_text == "附近餐廳資訊" :
                mes=""
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in Restaurants:
                    for j in i :
                        mes+=j['RestaurantName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到餐廳資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近餐廳資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/uzrCrAA.jpg',
                                                title = '餐廳資料',
                                                text = '餐廳名稱:'+j['RestaurantName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                ))
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近餐廳資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/uzrCrAA.jpg',
                                                title = '餐廳資料',
                                                text = '餐廳名稱:'+j['RestaurantName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                ))
            elif message_text == "附近鐵路資訊" :
                mes=""
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in RailStations:
                    for j in i :
                        mes+=j['StationName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到鐵路資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近鐵路資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/J5QPbM8.jpg',
                                                title = '鐵路資料',
                                                text = '車站編號'+j['StationUID']+"\n"+'車站名稱:'+j['StationName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                ))
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近鐵路資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/J5QPbM8.jpg',
                                                title = '鐵路資料',
                                                text = '車站編號'+j['StationUID']+"\n"+'車站名稱:'+j['StationName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                ))
            elif message_text == "附近公車資訊" :
                mes=""
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in BusStations:
                    for j in i :
                        mes+=j['StopName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到公車資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近公車資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/Ri8x6hH.jpg',
                                                title = '公車資料',
                                                text = '公車名稱:'+j['RouteName']+"\n"+"停靠站名:"+j['StopName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                ))
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近公車資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/Ri8x6hH.jpg',
                                                title = '公車資料',
                                                text = "停靠站名:"+j['StopName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                ))
            elif message_text == "附近公共腳踏車資訊" :
                mes=""
                #car,scen,hote,rest,rail,bus,bike=location_message()
                for i in BikeStations:
                    for j in i :
                        mes+=j['StationName']+"\n"
                    if len(mes) == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="附近沒有查到公共腳踏車資料"))
                    elif len(mes) > 10 :
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近公共腳踏車資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/2lze1Ll.jpg',
                                                title = '公共腳踏車資料',
                                                text = '公共腳踏車名稱:'+j['StationName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i[:10]
                                        ]
                                    )
                                ))
                    else:
                        line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text = '附近公共腳踏車資料',
                                    template = CarouselTemplate(
                                        columns = [
                                            CarouselColumn(
                                                thumbnail_image_url = 'https://i.imgur.com/2lze1Ll.jpg',
                                                title = '公共腳踏車資料',
                                                text = '公共腳踏車名稱:'+j['StationName'],
                                                actions = [
                                                    URIAction(
                                                        label = '詳細內容',
                                                        uri = "https://www.google.com.tw/maps/search/"
                                                    )
                                                ]
                                            )for j in i
                                        ]
                                    )
                                ))
            elif message_text[:4] == "英漢字典":
                msg = ""
                if not str(message_text[6:]).isalpha() :
                    line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="查詢格式為:英漢字典 apple"))
                else:
                    word = message_text[5:]
                    msg = trans(word)
                    item = json.loads(msg)
                    line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                        alt_text = '英漢字典',
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/3qq5Glz.jpg',
                                    title = '查詢單字:  '+word,
                                    text = i['w_mid']+i['w_trs']+"\n",
                                    actions = [
                                        URIAction(
                                            label = '詳細內容',
                                            uri = 'https://tw.dictionary.search.yahoo.com/'
                                        )
                                    ]
                                )for i in item
                            ]
                        )
                    ))
            elif message_text == "中油油價" or message_text == "中油" or message_text == "油價":
                msg = oil_price()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = msg))
            elif message_text == "巡檢測試設備":
                msg = ""
                line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                        alt_text = '巡檢測試設備一覽',
                        template = CarouselTemplate(
                            columns = [
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                                    title="俯仰油壓缸",
                                    text="請查詢測試點",
                                    actions = [
                                        PostbackTemplateAction(
                                        label="動力站油箱",
                                        text="動力站油箱",
                                        data="停車位資訊"
                                        ),
                                        PostbackTemplateAction(
                                        label="泵浦",
                                        text="泵浦",
                                        data="觀光景點資訊"
                                    ),
                                    PostbackTemplateAction(
                                        label="閥塊檢查",
                                        text="閥塊檢查",
                                        data="住宿資訊"
                                    )
                                ]
                            ),
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                                    title="附近交通及觀光資訊一覽",
                                    text="請選擇想要查詢的資訊",
                                    actions=[
                                        PostbackTemplateAction(
                                            label="鐵路資訊",
                                            text="附近鐵路資訊",
                                            data="鐵路資訊"
                                        ),
                                        PostbackTemplateAction(
                                            label="公車資訊",
                                            text="附近公車資訊",
                                            data="公車資訊"
                                        ),
                                        PostbackTemplateAction(
                                            label="公共腳踏車資訊",
                                            text="附近公共腳踏車資訊",
                                            data="腳踏車資訊"
                                    )
                                ]
                            ),
                                CarouselColumn(
                                    thumbnail_image_url = 'https://i.imgur.com/Ukpmoeh.jpg',
                                    title="附近交通及觀光資訊一覽",
                                    text="請選擇想要查詢的資訊",
                                    actions=[
                                        PostbackTemplateAction(
                                            label="餐廳資訊",
                                            text="附近餐廳資訊",
                                            data="餐廳資訊"
                                        ),
                                        URIAction(
                                            label = '開啟地圖',
                                            uri = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
                                        ),
                                        MessageTemplateAction(
                                            label='結束使用',
                                            text='查詢結束'
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

def application(environ, start_response):
    # check request path
    if environ['PATH_INFO'] != '/callback':
        start_response('404 Not Found', [])
        return create_body('Not Found')

    # check request method
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [])
        return create_body('Method Not Allowed')

    # get X-Line-Signature header value
    signature = environ['HTTP_X_LINE_SIGNATURE']

    # get request body as text
    wsgi_input = environ['wsgi.input']
    content_length = int(environ['CONTENT_LENGTH'])
    body = wsgi_input.read(content_length).decode('utf-8')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        start_response('400 Bad Request', [])
        return create_body('Bad Request')

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if isinstance(event, MessageEvent):
            if  isinstance(event.message, LocationMessage):
                get_location(event)            
            if  isinstance(event.message, TextMessage):
                handle_message(event)

    start_response('200 OK', [])
    return create_body('OK')


def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text

if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    options = arg_parser.parse_args()

    httpd = wsgiref.simple_server.make_server('', options.port, application)
    httpd.serve_forever()
