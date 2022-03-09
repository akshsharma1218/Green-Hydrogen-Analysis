from fastapi import FastAPI
from fastapi_models import *
from utils.google_news import news_data
from utils.tweet_data import tweets
from transformers import pipeline
from fastapi.responses import StreamingResponse
import io

analysis_model = pipeline("sentiment-analysis")

app = FastAPI()

def getScore(x):
    result = analysis_model(x)[0]
    if result['label'] == "POSITIVE":
        return result['score']
    return -(result['score'])


@app.get("/")
async def download_csv(min_count:Optional[int]=200):
    df = tweets(min_count).append(news_data(),ignore_index=True) 
    df['score'] = df['data'].apply(lambda x:getScore(x))
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
    combined_data['score'] = combined_data['data'].apply(lambda x:getScore(x))
    return combined_data.to_dict('records')

@app.get("/news_data",response_model=List[Item])
async def google_news_data():
    google_news_data = news_data()
    google_news_data['score'] = google_news_data['data'].apply(lambda x:getScore(x))
    return google_news_data.to_dict('records')

@app.get("/tweet_data",response_model=List[Item])
async def tweet_data(min_count:Optional[int]=200):
    tweet_data = tweets(min_count)
    tweet_data['score'] = tweet_data['data'].apply(lambda x:getScore(x))
    return tweet_data.to_dict('records')