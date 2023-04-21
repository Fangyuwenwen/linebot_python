import json 
import requests
import pandas as pd

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
    with open('tra.json',"r",encoding="utf-8") as f:
        data = json.load(f)
    StationID=[]
    StationName=[]
    SIN={}
    a="斗六"
    b="新左營"
    for i in data :
        StationID.append(i['StationName']['Zh_tw'])
        StationName.append(i['StationID'])
        s=zip(StationID,StationName)
        SIN=dict(s)
    """with open("tra_station.json","w",encoding="utf-8") as th_st_file:
        json.dump(SIN,th_st_file,ensure_ascii = False)"""
        
    tdx = TDX(client_id, client_secret)
    #url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/DailyTimetable/OD/3470/to/4340/2023-03-24?%24top=30&%24format=JSON' 
    
    base_url = "https://tdx.transportdata.tw/api"
    
    endpoint = "/basic/v2/Rail/TRA/DailyTimetable/"
    od="OD/"+ SIN[a]+"/"
    to="to/"+SIN[b]+"/"
    date="2023-03-24"
    filter = "?%24top=30&%24format=JSON"
    #filter = "Direction eq 1"  # 順逆行: [0:'順行', 1:'逆行']
    url = base_url+endpoint+od+to+date+filter

    response = tdx.get_response(url)
    #print(response)
    t_no=[]
    OriginStop=[]
    DestinationStop=[]
    #s_time={}
    for i in response :
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
    print(js)