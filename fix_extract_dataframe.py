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