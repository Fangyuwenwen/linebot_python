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
    with open('thsr.json',"r",encoding="utf-8") as f:
        data = json.load(f)

    StationID=[]
    StationName=[]
    SIN={}
    a="雲林"
    b="嘉義"
    for i in data :
        StationID.append(i['StationName']['Zh_tw'])
        StationName.append(i['StationID'])
        s=zip(StationID,StationName)
        SIN=dict(s)
        
    tdx = TDX(client_id, client_secret)
    #url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/OD/1047/to/1070/2023-03-22?%24top=30&%24format=JSON' 
    # url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/LiveBoard/Station/1000?$filter=Direction eq 1&$format=JSON'
    base_url = "https://tdx.transportdata.tw/api"
    
    endpoint = "/basic/v2/Rail/THSR/DailyTimetable/"
    od="OD/"+ SIN[a]+"/"
    to="to/"+SIN[b]+"/"
    date="2023-03-22"
    filter = "?%24top=30&%24format=JSON"
    #filter = "Direction eq 1"  # 順逆行: [0:'順行', 1:'逆行']
    url = base_url+endpoint+od+to+date+filter

    response = tdx.get_response(url)
    #print(response)
    #t_no=[]
    OriginStop=[]
    DestinationStop=[]
    s_time={}
    for i in response :
        #t_no.append("車次:"+i["DailyTrainInfo"]["TrainNo"])
        OriginStop.append("車次:"+i["DailyTrainInfo"]["TrainNo"]+"起點站"+i['OriginStopTime']['StationName']['Zh_tw']+"為"+i['OriginStopTime']['ArrivalTime'])
        DestinationStop.append("終點站"+i['DestinationStopTime']['StationName']['Zh_tw']+"為"+i['DestinationStopTime']['ArrivalTime'])
        stop=zip(OriginStop,DestinationStop)
        s_time=dict(stop)
    print(s_time)
