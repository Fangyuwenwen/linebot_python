"""import json,requests
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']
print(cities)

token = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'
url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=雲林縣'
#https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8&format=JSON&locationName=雲林縣
Data = requests.get(url)
Data = (json.loads(Data.text))['records']['location'][0]['weatherElement']
print(Data)
res = [[] , [] , []]
for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])"""
#print(res)"""

import requests,statistics
def current_weather(address):
    city_list, area_list, area_list2 = {}, {}, {} # 定義好待會要用的變數    
    msg = '找不到氣象資訊。'                         # 預設回傳訊息

    # 定義取得資料的函式
    def get_data(url):
        w_data = requests.get(url)   # 爬取目前天氣網址的資料
        w_data_json = w_data.json()  # json 格式化訊息內容
        location = w_data_json['cwbopendata']['location']  # 取出對應地點的內容
        for i in location:
            #name = i['locationName']                    # 測站地點
            city = i['parameter'][0]['parameterValue']  # 城市
            area = i['parameter'][2]['parameterValue']  # 行政區
            temp = check_data(i['weatherElement'][3]['elementValue']['value'])                       # 氣溫
            humd = check_data(round(float(i['weatherElement'][4]['elementValue']['value'] )*100 ,1)) # 相對濕度
            r24 = check_data(i['weatherElement'][6]['elementValue']['value'])                        # 累積雨量
            if area not in area_list:
                area_list[area] = {'temp':temp, 'humd':humd, 'r24':r24}  # 以鄉鎮區域為 key，儲存需要的資訊
            if city not in city_list:
                city_list[city] = {'temp':[], 'humd':[], 'r24':[]}       # 以主要縣市名稱為 key，準備紀錄裡面所有鄉鎮的數值
            city_list[city]['temp'].append(temp)   # 記錄主要縣市裡鄉鎮區域的溫度 ( 串列格式 )
            city_list[city]['humd'].append(humd)   # 記錄主要縣市裡鄉鎮區域的濕度 ( 串列格式 )
            city_list[city]['r24'].append(r24)     # 記錄主要縣市裡鄉鎮區域的雨量 ( 串列格式 )

    # 定義如果數值小於 0，回傳 False 的函式
    def check_data(e):
        return False if float(e)<0 else float(e)

    # 定義產生回傳訊息的函式
    def msg_content(loc, msg):
        a = msg
        for i in loc:  
            if i in address: # 如果地址裡存在 key 的名稱
                temp = f"氣溫 {loc[i]['temp']} 度/n" if loc[i]['temp'] != False else ''
                humd = f"相對濕度 {loc[i]['humd']}%/n" if loc[i]['humd'] != False else ''
                r24 = f"累積雨量 {loc[i]['r24']}mm" if loc[i]['r24'] != False else ''
                description = f'{temp}{humd}{r24}'
                a = f'{description}。' # 取出 key 的內容作為回傳訊息使用
                break
        return a

    try:
        # 因為目前天氣有兩組網址，兩組都爬取
        code = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'
        get_data(f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization={code}&downloadType=WEB&format=JSON')
        #https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8&downloadType=WEB&format=JSON
        get_data(f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0003-001?Authorization={code}&downloadType=WEB&format=JSON')

        for i in city_list:
            if i not in area_list2: # 將主要縣市裡的數值平均後，以主要縣市名稱為 key，再度儲存一次，如果找不到鄉鎮區域，就使用平均數值
                area_list2[i] = {'temp':round(statistics.mean(city_list[i]['temp']),1), 
                                'humd':round(statistics.mean(city_list[i]['humd']),1), 
                                'r24':round(statistics.mean(city_list[i]['r24']),1)
                                }
        msg = msg_content(area_list2, msg)  # 將訊息改為「大縣市」 
        msg = msg_content(area_list, msg)   # 將訊息改為「鄉鎮區域」 
        return msg    # 回傳 msg
    except:
        return msg    # 如果取資料有發生錯誤，直接回傳 msg

"""import json,requests,statistics
city_list, site_list ={}, {}
address="雲林縣"
msg = '找不到空氣品質資訊。'
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
    city_list[city].append(aqi) # 將各個縣市裡的鄉鎮區域空氣 aqi 數值，以串列方式放入縣市名稱的變數裡
#print(city_list)
#print(site_list)
for i in city_list:
    if i in address: # 如果地址裡包含縣市名稱的 key，就直接使用對應的內容
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
        print(msg)
        break
for i in site_list:
    if i in address:  # 如果地址裡包含鄉鎮區域名稱的 key，就直接使用對應的內容
        msg = f'空氣品質{site_list[i]["status"]} ( AQI {site_list[i]["aqi"]} )。'
        break"""

"""import requests
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
a=earth_quake()
print(a[0])"""