"""from GoogleNews import GoogleNews
from datetime import datetime

#設定時間
now_date = datetime.now()
start_date = (str((now_date.month))+"/"+str((now_date.day))+"/"+str((now_date.year)))
end_date = (str((now_date.month))+"/"+str((now_date.day-7))+"/"+str((now_date.year)))
print(start_date)
print(end_date)
start_date = datetime.strptime(start_date,'%m/%d/%Y')
end_date = datetime.strptime(end_date,'%m/%d/%Y')
#爬取新聞
now_date = datetime.now()
googlenews = GoogleNews()
googlenews.setlang('cn')
#googlenews = GoogleNews(lang='cn')
googlenews.clear()
#googlenews.setTimeRange(end_date,start_date)
googlenews = GoogleNews(period='7d')
googlenews.setencode('utf-8')
#googlenews = GoogleNews(encode='utf-8')
#googlenews.search('重機')
googlenews.get_news('重機')
times =int (googlenews.get_page(1))


for i in range():
    googlenews.clear()
    googlenews.getpage(i)
    result = googlenews.result()
    Ur_list =[]
    for n in range(len(result)):
        print(n)
        print(result[n])
        temp = result[n]
        print(temp['link'])
        Ur_list.append(temp['link'])
        googlenews.gettext()"""

import requests 
from bs4 import BeautifulSoup
import pandas as pd
 
#爬取最新新聞
def news(): 
    url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    r = requests.get(url)
    web_content = r.text
    soup = BeautifulSoup(web_content,'lxml')
    title = soup.find_all('div', class_='XlKvRb',limit=5)
    #print(title)
    titles = [t.find('a')['aria-label'] for t in title]
    #print(titles)
    newUrls = [requests.get(t.find('a')['href'].replace('.','https://news.google.com',1)).url for t in title]
    #print(newUrls)
    df = pd.DataFrame(
    {
        'title': titles,
        'links': newUrls
    })
    return df
sprint(news())