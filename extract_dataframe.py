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
    def find_screen_name(self) -> list:
        screen_name = []
        for x in self.tweets_list:
            screen_name.append(x['user']['screen_name'])
        return screen_name
    def find_followers_count(self) -> list:
        followers_count = []

        for x in self.tweets_list:
            if 'retweeted_status' in x.keys():
                followers_count.append(
                    x['retweeted_status']['user']['followers_count'])
            else:
                followers_count.append(0)
        return followers_count

    def find_friends_count(self) -> list:
        friends_count = []
        for x in self.tweets_list:
            friends_count.append(x['user']['friends_count'])
        return friends_count
    def is_sensitive(self) -> list:
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else:
                is_sensitive.append(None)
        return is_sensitive
    def find_favourite_count(self) -> list:
        favorite_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                favorite_count.append(
                    tweet['retweeted_status']['favorite_count'])
            else:
                favorite_count.append(0)
        return favorite_count
    def find_retweet_count(self) -> list:
        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(
                    tweet['retweeted_status']['retweet_count'])
            else:
                retweet_count.append(0)
        return retweet_count
      # Improved the functionality of hashtags
    def find_hashtags(self) -> list:
        hashtags = []
        for tweet in self.tweets_list:
            try:
                hashtags.append(tweet['entities']['hashtags'][0]['text'])
            except KeyError:
                hashtags.append(None)
            except IndexError:
                hashtags.append(None)

        return hashtags
    
    def find_mentions(self) -> list:
        mentions = []
        for hs in self.tweets_list:
            mentions.append(", ".join(
                [mention['screen_name'] for mention in hs['entities']['user_mentions']]))
        return mentions

    def find_lang(self) -> list:
        lang = []
        for x in self.tweets_list:
            lang.append(x['lang'])
        return lang
    
    def find_location(self) -> list:
        location = []
        for tweet in self.tweets_list:
            location.append(tweet['user']['location'])
        return location
    
    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity',
                   'subjectivity', 'lang', 'statuses_count', 'favorite_count', 'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive',
                   'hashtags', 'user_mentions', 'place']
    
        created_at = self.find_created_time()
        source = self.find_source()
        original_text = self.find_original_text()
        clean_text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(clean_text)
        sentiment = self.find_sentiment(polarity, subjectivity)
        lang = self.find_lang()
        statuses_count = self.find_statuses_count()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, original_text, clean_text, sentiment, polarity, subjectivity, lang, statuses_count,
                   fav_count, retweet_count, screen_name, follower_count,
                   friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('data/economic_clean.csv', index=False)
            print('File Successfully Saved.!!!')
        return df

if __name__ == "__main__":
    _, tweet_list = read_json("data/Economic_Twitter_Data.zip")
    tweet = TweetDfExtractor(tweet_list)
    df = tweet.get_tweet_df(True)
    

         