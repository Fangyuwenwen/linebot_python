from urllib.request import urlopen

import json
import time


READ_API_KEY='O0TENR74YMQ8ORIT'
CHANNEL_ID='1886703'


#while True:#qZ4*G6*hDuDbj4p
TS = urlopen("https://api.thingspeak.com/channels/1886703/feeds.json?api_key=O0TENR74YMQ8ORIT&results=2")

response = TS.read()

data=json.loads(response.decode('utf-8'))

print(data)

print (data["channel"]["field1"]+data["feeds"][1]["field1"])
print (data["channel"]["field2"]+data["feeds"][1]["field2"])

""" 
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

TS.close() """