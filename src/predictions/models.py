from django.db import models
import twitter
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from .ignore import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token_key=ACCESS_TOKEN_KEY,
                     access_token_secret=ACCESS_TOKEN_SECRET)


def get_tweets(screen_name):
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """

    return api.GetUserTimeline(screen_name=screen_name, exclude_replies=True, include_rts=False)  # includes entities    

def get_user(user_id=None, screen_name=None):
	json = api.GetUser(user_id=user_id, screen_name=screen_name, include_entities=True, return_json=False)
	json_data = json._json

	Count_of_favorite_tweets = int(json_data['favourites_count'])
	Friends_to_follower_ratio = float(json_data['friends_count']) / json_data['followers_count']
	Total_status_count = int(json_data['statuses_count'])

	if json_data['default_profile_image'] == 'FALSE':
		Default_profile_image = 0
	else:
		Default_profile_image = 1

	if json_data['default_profile'] == 'FALSE':
		Default_profile = 0
	else:
		Default_profile = 1

	created_at = json_data['created_at']
	Account_age = survival_time(created_at)

	User_name = json_data['name']
	Screen_name = json_data['screen_name']

	User_name_digit, User_name_char = counter(User_name)
	Screen_name_digit, Screen_name_char = counter(Screen_name)

	description_pre = json_data['description']
	Description_length, Description_tfidf = preprocess_description(description_pre)

	Average_tweets_per_day = Total_status_count / float(Account_age)

	feature = list()
	feature.append(Count_of_favorite_tweets)
	feature.append(Friends_to_follower_ratio)
	feature.append(Total_status_count)
	feature.append(Default_profile_image)
	feature.append(Default_profile)
	feature.append(Account_age)
	feature.append(User_name_digit)
	feature.append(User_name_char)
	feature.append(Screen_name_digit)
	feature.append(Screen_name_char)
	feature.append(Description_length)
	feature.append(Description_tfidf)
	feature.append(Average_tweets_per_day)

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


def preprocess_description(description):
	description_length = len(description)
	des_list = list()
	des_list.append(description)
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(des_list)
	# X_train_counts.shape
	# tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
	# X_train_tf = tf_transformer.transform(X_train_counts)
	# X_train_tf.shape
	tfidf_transformer = TfidfTransformer()
	des_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	
	return description_length, des_train_tfidf

def measure_running_time(user_id=None, screen_name=None):
	start = time.clock()
	get_user(user_id=user_id, screen_name=screen_name)
	end = time.clock()
	print('function took %0.5f ms' % ((end-start)*1000.0))

