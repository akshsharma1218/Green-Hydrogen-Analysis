from traceback import print_tb
import requests
import os
import json
import pandas as pd

bearer_token = "AAAAAAAAAAAAAAAAAAAAALiSZwEAAAAAkHH10R4eoiC2D9oNXet748mthmE%3DezQ8QJYDSvIT4Di2zqV54tcMGBWzWFnSvgbVRcfUy1d7XJ0vkm"
search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params = {
    'query': '#green_hydrogen OR green hydrogen',
    'max_results':10,
    # 'start_time':"2022-02-01T00:00:00.000Z",
    'expansions':'author_id',
    'tweet.fields': 'created_at',
    }

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def tweets(count=100):
    params = query_params
    json_response = connect_to_endpoint(search_url, params)
    json_data = {
        'data':json_response['data'],
        'user':json_response['includes']['users']
    }
    while('next_token' in json_response['meta']):
        params['next_token'] = json_response['meta']['next_token']
        json_response = connect_to_endpoint(search_url, params)
        json_data['data'] += json_response['data']
        json_data['user'] += json_response['includes']['users']
        if(count <= len(json_data['data'])):
            break

    df1 = pd.DataFrame.from_records(json_data['data'], columns=['created_at','text','author_id'])
    df2 = pd.DataFrame.from_records(json_data['user'],columns=['id','username'])
    df = pd.merge(df1,df2,left_on="author_id",right_on="id",suffixes=[None,None])
    df.rename(columns={'created_at':'date','text':'data','username':'source'},inplace=True)
    df['date'] = df['date'].apply(lambda x:x[:-5].replace('T'," "))
    return df[['date','data','source']]


if __name__ == "__main__":
    tweets()