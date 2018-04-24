from django.db import models
import twitter
import time
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib
import json
import os

from urllib.parse import urlparse
import requests
from django.http import Http404

from .account_model import get_user
from .text_model_cnn import get_cnn_predict
from .text_model_tfidf import get_tfidf_predict



script_dir = os.path.dirname(__file__)

from .ignore import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token_key=ACCESS_TOKEN_KEY,
                     access_token_secret=ACCESS_TOKEN_SECRET)
   

def extend_url(url):
    if url is None:
        return None
    try:
        request = requests.get(url)
        return request.url
    except:
        return None

def short_num(num):
    if (num/1000000 > 1):
        return str(int(num/1000000)) + ' M'
    elif (num / 1000 > 1):
        return str(int(num/1000)) + ' K'
    else:
        return str(num)

def get_predict(screen_name):
    # random forest + knn
    with open("predictions/classifier/rf_user_3.pkl", "rb") as file_handler:
        loaded_pickle = joblib.load(file_handler)

    feature = get_user(screen_name=screen_name)

    np_feature = np.asarray((feature))

    pred_account = loaded_pickle.predict_proba(np_feature.tolist())

    data =  api.GetUser(screen_name=screen_name, include_entities=True, return_json=False)
    
    basic_info = data._json
    basic_info['url'] = extend_url(basic_info['url'])
    basic_info['followers_count'] = short_num(basic_info['followers_count'])
    basic_info['friends_count'] = short_num(basic_info['friends_count'])
    basic_info["prediction_account_label"] = float(pred_account[0][1] * 100)
    basic_info["pl"] = "https://twitter.com/"+basic_info["screen_name"]
    if basic_info['default_profile_image']:
	    basic_info["pp"] = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"
    elif 'normal' in basic_info["profile_image_url"]:
        basic_info["pp"] = basic_info["profile_image_url"][:basic_info["profile_image_url"].find("_normal")]+basic_info["profile_image_url"][basic_info["profile_image_url"].find('_normal'):][basic_info["profile_image_url"][basic_info["profile_image_url"].find('_normal'):].find('.'):]
    
    # use cnn text model:
    basic_info = get_cnn_predict(screen_name, basic_info)

    # use tfidf text model:
    # basic_info = get_tfidf_predict(screen_name, basic_info)
    

    return json.dumps(basic_info)


