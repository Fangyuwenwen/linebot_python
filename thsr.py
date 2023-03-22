import json 
import requests

client_id = '11061108-00b12e58-30cf-432d'
client_secret = 'fac2feb7-d9a9-4389-be90-b71c4c69671f'


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


if __name__ == '__main__':
    tdx = TDX(client_id, client_secret)
    #url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/OD/1047/to/1070/2023-03-22?%24top=30&%24format=JSON' 
    # url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/LiveBoard/Station/1000?$filter=Direction eq 1&$format=JSON'
    base_url = "https://tdx.transportdata.tw/api"
    
    endpoint = "/basic/v2/Rail/TRA/LiveBoard/Station/1000"
    filter = "Direction eq 1"  # 順逆行: [0:'順行', 1:'逆行']
    url = f"{base_url}{endpoint}?$filter={filter}&$format=JSON"

    response = tdx.get_response(url)
    print(response)

with open('thsr.json',"r",encoding="utf-8") as f:
    data = json.load(f)

StationID=[]
StationName=[]
SIN={}
a="雲林"
for i in data :
    StationID.append(i['StationName']['Zh_tw'])
    StationName.append(i['StationID'])
    s=zip(StationID,StationName)
    SIN=dict(s)
print(SIN[a])
