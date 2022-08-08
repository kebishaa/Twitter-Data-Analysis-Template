import json
import pandas as pd
from textblob import TextBlob
import zipfile

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    with zipfile.ZipFile(json_file, 'r') as zip_ref:
        zip_ref.extractall("data/")
    for tweets in open("data/Economic_Twitter_Data.json", 'r'):
        tweets_data.append(json.loads(tweets))
    return len(tweets_data), tweets_data
class TweetDfExtractor:

    def __init__(self, tweets_list):
        self.tweets_list = tweets_list
    def find_statuses_count(self) -> list:
        statuses_count = []
        for tweet in self.tweets_list:
            statuses_count.append(tweet['user']['statuses_count'])
        return statuses_count
    def find_full_text(self) -> list:
        full_text = []
        for tweet in self.tweets_list:
            try:
                full_text.append(
                    tweet['retweeted_status']['text'])
            except KeyError:
                full_text.append("")
        return full_text        
    def find_original_text(self) -> list:
        original_text = [x['text'] for x in self.tweets_list]
        return original_text  
    def find_sentiments(self, text: list) -> list:
        polarity = []
        subjectivity = []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return polarity, subjectivity    
    def find_sentiment(self, polarity, subjectivity) -> list:
        sentiment = []
        for i in range(len(polarity)):
            if polarity[i] > 0:
                sentiment.append(1)
            elif polarity[i] < 0:
                sentiment.append(0)
            else:
                sentiment.append(-1)
        return sentiment  
    def find_created_time(self) -> list:
        created_at = []
        for time in self.tweets_list:
            created_at.append(time['created_at'])
        return created_at
    def find_created_time(self) -> list:
        created_at = []
        for time in self.tweets_list:
            created_at.append(time['created_at'])
        return created_at
    def find_source(self) -> list:
        source = []
        for x in self.tweets_list:
            source.append(x['source'])
        return source
         