from fastapi import FastAPI
from fastapi_models import *
from utils.google_news import news_data
from utils.tweet_data import tweets
from transformers import pipeline


analysis_model = pipeline("sentiment-analysis")

app = FastAPI()

def getScore(x):
    result = analysis_model(x)[0]
    if result['label'] == "POSITIVE":
        return result['score']
    return -(result['score'])

@app.get("/home",response_model=List[Item])
async def all_data(min_count:Optional[int]=100):
    combined_data = tweets(min_count).append(news_data(),ignore_index=True) 
    combined_data['score'] = combined_data['data'].apply(lambda x:getScore(x))
    return combined_data.to_dict('records')

@app.get("/news_data",response_model=List[Item])
async def google_news_data():
    google_news_data = news_data()
    google_news_data['score'] = google_news_data['data'].apply(lambda x:getScore(x))
    return google_news_data.to_dict('records')

@app.get("/tweet_data",response_model=List[Item])
async def tweet_data(min_count:Optional[int]=100):
    tweet_data = tweets(min_count)
    tweet_data['score'] = tweet_data['data'].apply(lambda x:getScore(x))
    return tweet_data.to_dict('records')