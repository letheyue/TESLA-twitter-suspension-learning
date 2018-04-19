from django.db import models
import twitter
import time
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib
import json
import os

import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
# from keras.models import load_model
# from keras import backend as be
from django.http import Http404
# import boto3
# from Tesla.aws.conf import AWS_STORAGE_BUCKET_NAME
# from Tesla.aws.ignore import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r"(?P<url>https?://[^\s]+)"
combined_pat = r'|'.join((pat1, pat2))

script_dir = os.path.dirname(__file__)

from .ignore import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token_key=ACCESS_TOKEN_KEY,
                     access_token_secret=ACCESS_TOKEN_SECRET)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def get_tweets(screen_name):
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """

    return api.GetUserTimeline(screen_name=screen_name, exclude_replies=True, include_rts=False)  # includes entities    

def get_user(user_id=None, screen_name=None):
    json = api.GetUser(user_id=user_id, screen_name=screen_name, include_entities=True, return_json=False)
    json_data = json._json
    
    # feature Count of favorite tweets
    Count_of_favorite_tweets = int(json_data['favourites_count'])
    # feature Friends to follower ratio
    if json_data['followers_count'] == 0:
        Friends_to_follower_ratio = float(100000)
    else:
        Friends_to_follower_ratio = (float(json_data['friends_count']) / json_data['followers_count'])
    # feature Total status count
    Total_status_count = int(json_data['statuses_count'])
    
    # feature Default profile image & Default profile
    # def_p_na','def_p_false','def_p_true'
    if json_data['default_profile_image'] == 'FALSE':
        Def_p_img_false = 1.0
        Def_p_img_true = 0.0
        Def_p_img_na = 0.0
    elif json_data['default_profile_image'] == 'True':
        Def_p_img_false = 0.0
        Def_p_img_true = 1.0
        Def_p_img_na = 0.0
    else:
        Def_p_img_false = 0.0
        Def_p_img_true = 0.0
        Def_p_img_na = 1.0

    if json_data['default_profile'] == 'FALSE':
        Def_p_false = 1.0
        Def_p_true = 0.0
        Def_p_na = 0.0
    elif json_data['default_profile'] == 'True':
        Def_p_false = 0.0
        Def_p_true = 1.0
        Def_p_na = 0.0
    else:
        Def_p_false = 0.0
        Def_p_true = 0.0
        Def_p_na = 1.0
    
    # feature Account ages
    created_at = json_data['created_at']
    Account_age = survival_time(created_at)

    # feature User name and screen_name
    User_name = json_data['name']
    Screen_name = json_data['screen_name']
    User_name_digit, User_name_char = counter(User_name)
    Screen_name_digit, Screen_name_char = counter(Screen_name)

    # feature Length of description and Description text
    description_pre = json_data['description']
    Description_length = len(description_pre)
    
    # feature Average tweet per day
    # Average_tweets_per_day = Total_status_count / float(Account_age)

    # feature listed count
    Listed_count = json_data['listed_count']

    # feature of description, the number of hashtag, @ and url
    Bio_hashtag = json_data['description'].count('#')
    Bio_at = json_data['description'].count('@')
    Bio_url = json_data['description'].count('http')

    feature = pd.DataFrame(index=[0])
    feature['favorite_count'] = Count_of_favorite_tweets
    feature['friends_to_followers'] = Friends_to_follower_ratio
    feature['statuses_count'] = Total_status_count
    feature['def_p_img_na'] = Def_p_img_na
    feature['def_p_img_false'] = Def_p_img_false
    feature['def_p_img_true'] = Def_p_img_true
    feature['def_p_na'] = Def_p_na
    feature['def_p_false'] = Def_p_false
    feature['def_p_true'] = Def_p_true
    feature['age'] = Account_age
    feature['name_letter'] = User_name_char
    feature['name_num'] = User_name_digit
    feature['screen_letter'] = Screen_name_char
    feature['screen_num'] = Screen_name_digit
    feature['des_len'] = Description_length
#     feature['avg_tweet_per_day'] = Average_tweets_per_day
#     feature['des_text'] = Description_tfidf
    feature['listed_count'] = Listed_count
    feature['bio_hashtag'] = Bio_hashtag
    feature['bio_at'] = Bio_at
    feature['bio_url'] = Bio_url

    return feature



def survival_time(created_at):
	# get the account ages: crawl at time - created at time 
	current_time = time.localtime(time.time())
	current_year = current_time.tm_year
	current_month = current_time.tm_mon
	current_day = current_time.tm_mday

	meta = created_at.split(" ")
	created_month = meta[1]
	if created_month == 'Jan':
		created_month = int(1)
	elif created_month == 'Feb':
		created_month = int(2)
	elif created_month == 'Mar':
		created_month = int(3)
	elif created_month == 'Apr':
		created_month = int(4)
	elif created_month == 'May':
		created_month = int(5)
	elif created_month == 'Jun':
		created_month = int(6)
	elif created_month == 'Jul':
		created_month = int(7)
	elif created_month == 'Aug':
		created_month = int(8)
	elif created_month == 'Sep':
		created_month = int(9)
	elif created_month == 'Oct':
		created_month = int(10)
	elif created_month == 'Nov':
		created_month = int(11)
	elif created_month == 'Dec':
		created_month = int(12)
	created_day = int(meta[2])
	created_year = int(meta[5])

	Account_age = (current_year - created_year) * 365 + (current_month - created_month) * 30 + (current_day - created_day)

	return Account_age

def counter(name):
	# counter of char & counter of digit
	numbers = sum(c.isdigit() for c in name)
	words   = sum(c.isalpha() for c in name)

	return numbers, words


def preprocess_description(user_id=None, screen_name=None):
    # preprocess the description text
    json = api.GetUser(user_id=user_id, screen_name=screen_name, include_entities=True, return_json=False)
    json_data = json._json
    description = json_data["description"]
    
    des_list = list()
    des_list.append(description)
    
    tfidf_transformer = TfidfVectorizer()
    des_text = tfidf_transformer.fit_transform(des_list)
    
    return des_text

def measure_running_time(user_id=None, screen_name=None):
	start = time.clock()
	get_user(user_id=user_id, screen_name=screen_name)
	end = time.clock()
	print('function took %0.5f ms' % ((end-start)*1000.0))

# crawl at the text and do pre-process, then change them into vector feature
def get_text(screen_name):
    timeline = api.GetUserTimeline(screen_name=screen_name)
    # check if it has timeline
    if len(timeline) is 0:
        raise Http404("This user doesn't have any tweets!")
    # get the first 1 tweets
    index = 0
    list_text = list()
    for item in timeline:
        index += 1
        data = item._json
        list_text.append(data['text'])
        break

    text = tweet_cleaner_updated(list_text[0])

    with open('predictions/classifier/pos_hmean.p', 'rb') as fp:
        w2v_pos_hmean_01 = pickle.load(fp, encoding='latin1')

    text = get_w2v_general(text, 200, w2v_pos_hmean_01)

    return text

# make the str text to vector feature
def get_w2v_general(tweet, size, vectors):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in tweet.split():
        try:
            vec += vectors[word].reshape((1, size))
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec

# pre-processing the text
def tweet_cleaner_updated(text):
    try:
        mention = re.search(pat1, text).group()
    except:
        mention = ''
    try:
        url = re.search(pat2, text).group("url")
        o = urlparse(url)
        netloc = o.netloc
        path = p.path
    except:
        netloc = ''
        path = ''
    soup = BeautifulSoup(text, 'html.parser')
    souped = soup.get_text()
    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\u2026", "?")
    except:
        bom_removed = souped
    stripped = re.sub(combined_pat, '', bom_removed)
    lower_case = stripped.lower()
    letters_only = re.sub("[^a-zA-Z]", " ", lower_case)
    letters_only = letters_only + netloc + path + mention
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()

def get_predict(screen_name):
    # random forest + knn
    with open("predictions/classifier/rf_user_3.pkl", "rb") as file_handler:
        loaded_pickle = joblib.load(file_handler)
    # s3 = boto3.resource('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # local_file = 'predictions/tmp/rf_user_2.pkl'
    # obj = s3.Bucket(AWS_STORAGE_BUCKET_NAME).download_file('media/rf_user_2.pkl', local_file)
    # loaded_pickle = joblib.load(local_file)
    # os.remove(local_file)

    feature = get_user(screen_name=screen_name)

    np_feature = np.asarray((feature))

    pred_account = loaded_pickle.predict_proba(np_feature.tolist())

    data =  api.GetUser(screen_name=screen_name, include_entities=True, return_json=False)


    # word2vec for text
    
    # text_feature = get_text(screen_name)
    # loaded_w2v_model = load_model('predictions/classifier/w2v_01_best_weights.10-0.9346.hdf5')
    # pred_text = loaded_w2v_model.predict(text_feature) # label is pred_text[0][0]
    # be.clear_session()

    basic_info = data._json
    basic_info["prediction_account_label"] = float(pred_account[0][1] * 100)
    # basic_info["prediction_text_label"] = float(pred_text[0][0] * 100)

    return json.dumps(basic_info)


