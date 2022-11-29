from urllib.request import urlopen

import json
import time


READ_API_KEY='O0TENR74YMQ8ORIT'
CHANNEL_ID='1886703'


while True:
    TS = urlopen("https://api.thingspeak.com/channels/1886703/fields/1.json?api_key=O0TENR74YMQ8ORIT&results=2")

    response = TS.read()

    data=json.loads(response.decode('utf-8'))

    print(data)

    print (data["feeds"][1]["field1"])

    a=data["feeds"][1]["field1"]

    if a=='1' :
        print("wood")
        break

    elif a=='2' :
        print("metal")
        break

    else:
        print("plastic")
        break

TS.close()