# Green-Hydrogen-Analysis
FastApi server for analysing data from google news and twitter on Green Hydrogen using huggingface sentiment analysis model.

# How to setup?

Run following commands:
```
  git clone https://github.com/akshsharma1218/Green-Hydrogen-Analysis.git
  cd Green-Hydrogen-Analysis     # or cd <Name of Folder>
  pip install -r requirements.txt
  uvicorn main:app --reload
```

# About Project
- Go to [docs](http://127.0.0.1:8000/docs) route to see all available route and schema. 
- Go to [news_data](http://127.0.0.1:8000/news_data) route to analyse only google news data.
- Go to [tweet_data](http://127.0.0.1:8000/tweet_data) route to analyse only twitter data.
- Go to [all_data](http://127.0.0.1:8000/home) route to analyse data from both google news and twitter.
- Go to [download_csv](http://127.0.0.1:8000/) route to download all data as csv. 
- One can also add `min_count` query parameter in `home, download_csv and tweet_data` route to reduce the amount of tweets to be scraped.  

# Images
  ## Available routes
  ![Screenshot (122)](https://user-images.githubusercontent.com/73122223/157450238-73a7938f-d237-4bc2-871d-ff6d8277e19d.png)
  ## Response
  ![Screenshot (120)](https://user-images.githubusercontent.com/73122223/157443545-a15377e4-0156-4e01-8a56-73be15527616.png)
