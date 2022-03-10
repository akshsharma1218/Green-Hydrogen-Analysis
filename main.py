from turtle import position
from fastapi import FastAPI
from fastapi_models import *
from utils.google_news import news_data
from utils.tweet_data import tweets
from transformers import pipeline
from fastapi.responses import StreamingResponse
import io
import pandas as pd

analysis_model = pipeline("sentiment-analysis")

app = FastAPI()


def getScore(x,y):
    if x == "POSITIVE":
        return y
    return -1*y
    


@app.get("/")
async def download_csv(min_count:Optional[int]=200):
    df = tweets(min_count).append(news_data(),ignore_index=True) 
    print("data recieve")
    sentiment_data = analysis_model(list(df['data']))
    print("analysis complete")
    score = pd.DataFrame(sentiment_data,columns=['label','score'])
    df['score'] = score.apply(lambda x:getScore(x['label'],x['score']),axis=1)
    stream = io.StringIO()
    df.to_csv(stream, index = False)
    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=green_hydrogen_analysis.csv"
    return response


@app.get("/home",response_model=List[Item])
async def all_data(min_count:Optional[int]=200):
    combined_data = tweets(min_count).append(news_data(),ignore_index=True)  
    sentiment_data = analysis_model(list(combined_data['data']))
    score = pd.DataFrame(sentiment_data,columns=['label','score'])
    combined_data['score'] = score.apply(lambda x:getScore(x['label'],x['score']),axis=1)
    return combined_data.to_dict('records')

@app.get("/news_data",response_model=List[Item])
async def google_news_data():
    google_news_data = news_data()
    sentiment_data = analysis_model(list(google_news_data['data']))
    score = pd.DataFrame(sentiment_data,columns=['label','score'])
    google_news_data['score'] = score.apply(lambda x:getScore(x['label'],x['score']),axis=1)
    return google_news_data.to_dict('records')

@app.get("/tweet_data",response_model=List[Item])
async def tweet_data(min_count:Optional[int]=200):
    tweet_data = tweets(min_count) 
    sentiment_data = analysis_model(list(tweet_data['data']))
    score = pd.DataFrame(sentiment_data,columns=['label','score'])
    tweet_data['score'] = score.apply(lambda x:getScore(x['label'],x['score']),axis=1)
    return tweet_data.to_dict('records')