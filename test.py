import json,requests
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']
print(cities)

token = 'CWB-F99C4A80-6BBC-4597-8238-CD2DF9C871E8'
url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=雲林縣'
Data = requests.get(url)
Data = (json.loads(Data.text))['records']['location'][0]['weatherElement']
print(Data)
res = [[] , [] , []]
for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
#print(res)