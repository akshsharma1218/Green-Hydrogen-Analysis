import feedparser
import time
import pandas as pd

url = "https://news.google.com/rss/search?q=green+hydrogen&hl=en-IN&gl=IN&ceid=IN:en"
start_date = time.strptime("2022-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")

def news_data():
    data = feedparser.parse(url)
    scraped_data = []
    for item in data['items']:
        context={}
        if(item['published_parsed']>start_date):
            context['date'] = time.strftime('%Y-%m-%d %H:%M:%S',item['published_parsed'])
            context['data'] = item['title']
            context['source'] = item['source']['title']
            scraped_data.append(context)
    df = pd.DataFrame(scraped_data,columns=['date','data','source'])
    return df

if __name__ == "__main__":
    news_data()