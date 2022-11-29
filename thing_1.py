import urequests
import time

host='http://api.thingspeak.com'
read_api_key='1KD7G3JFAE0L6Q4O'
channel_id='1680573'

url='%s/channels/%s/feeds/last.json?api_key=%s' \
     %(host, channel_id, read_api_key)

while True:
    try:
        r=urequests.get(url)
        print(r.text)
        print(r.json())
    except:
        print('urequests.get() exception occurred!')
    time.sleep(3)