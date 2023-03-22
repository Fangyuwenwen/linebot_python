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

    url ='https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/OD/1047/to/1070/2023-03-21?%24top=30&%24format=JSON'
    #base_url = "https://tdx.transportdata.tw/api"
    # 取得指定[車站]列車即時到離站電子看板(動態前後30分鐘的車次)
    #endpoint = "/basic/v2/Rail/TRA/LiveBoard/Station/1000"
    #filter = "Direction eq 1"  # 順逆行: [0:'順行', 1:'逆行']
    #url = f"{base_url}{endpoint}?$filter={filter}&$format=JSON"

    response = tdx.get_response(url)
    print(response)
