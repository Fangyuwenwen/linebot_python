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
now_news=news()
print(now_news[['title']])
#1.3.0, 1.4.1, 1.5.0, 1.5.1, 1.6.0, 1.6.1, 1.6.2, 1.7.0, 1.7.1, 1.7.2, 1.8.0, 1.8.1, 1.8.2, 1.9.0, 1.9.1, 1.9.2, 1.9.3, 1.10.0.post2, 
# 1.10.1, 1.10.2, 1.10.4, 1.11.0, 1.11.1, 1.11.2, 1.11.3, 1.12.0, 1.12.1, 1.13.0, 1.13.1, 1.13.3, 1.14.0, 1.14.1, 1.14.2, 1.14.3, 1.14.4, 
# 1.14.5, 1.14.6, 1.15.0, 1.15.1, 1.15.2, 1.15.3, 1.15.4, 1.16.0, 1.16.1, 1.16.2, 1.16.3, 1.16.4, 1.16.5, 1.16.6, 1.17.0, 1.17.1, 1.17.2, 1.17.3, 
# 1.17.4, 1.17.5, 1.18.0, 1.18.1, 1.18.2, 1.18.3, 1.18.4, 1.18.5, 1.19.0, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.19.5, 1.20.0, 1.20.1, 1.20.2, 1.20.3, 
# 1.21.0, 1.21.1, 1.21.2, 1.21.3, 1.21.4, 1.21.5, 1.21.6, 1.22.0, 1.22.1, 1.22.2, 1.22.3, 1.22.4, 1.23.0rc1, 1.23.0rc2, 1.23.0rc3, 1.23.0, 1.23.1, 
# 1.23.2, 1.23.3, 1.23.4, 1.23.5, 1.24.0rc1, 1.24.0rc2, 1.24.0, 1.24.1, 1.24.2