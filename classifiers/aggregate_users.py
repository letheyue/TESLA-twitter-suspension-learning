# Aggregate all available data, user part
import pandas as pd
import os
import random
import datetime
cwd = os.getcwd()

# from the varol data
user_column_header = ['business_profile_state', 'can_media_tag', 'contributors_enabled', 'created_at', 'default_profile', 'default_profile_image', 'description', 'fast_followers_count', 'favourites_count', 'follow_request_sent', 'followed_by', 'followers_count', 'following', 'friends_count', 'geo_enabled', 'has_custom_timelines', 'has_extended_profile', 'id', 'id_str', 'is_translation_enabled', 'is_translator', 'lang', 'listed_count', 'location', 'media_count', 'name', 'normal_followers_count', 'notifications', 'profile_background_color', 'profile_background_image_url', 'profile_background_image_url_https', 'profile_background_tile', 'profile_banner_url', 'profile_image_url', 'profile_image_url_https', 'profile_link_color', 'profile_location', 'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color', 'profile_use_background_image', 'protected', 'screen_name', 'statuses_count', 'time_zone', 'translator_type', 'url', 'user_type', 'utc_offset', 'verified', 'withheld_in_countries','crawled_at']
#tweet_column_header = ['contributors', 'conversation_id', 'conversation_id_str', 'coordinates', 'created_at', 'entities', 'extended_entities', 'favorite_count', 'favorited', 'geo', 'id', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'place', 'possibly_sensitive', 'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count', 'retweeted', 'retweeted_status', 'self_thread', 'source', 'supplemental_language', 'text', 'truncated', 'user', 'user_type', 'withheld_in_countries']

# loading all the cresci data
ss1 = pd.read_csv(cwd+"/social_spambots_1.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ss1.columns.values.tolist()) - set(user_column_header)
ss1 = ss1.drop(user_diff_feature, axis=1)
ss1['user_type'] = 1
user_column_header = ss1.columns.values.tolist()

ss2 = pd.read_csv(cwd+"/social_spambots_2.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ss2.columns.values.tolist()) - set(user_column_header)
ss2 = ss2.drop(user_diff_feature, axis=1)
ss2['user_type'] = 1

ss3 = pd.read_csv(cwd+"/social_spambots_3.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ss3.columns.values.tolist()) - set(user_column_header)
ss3 = ss3.drop(user_diff_feature, axis=1)
ss3['user_type'] = 1

ts1 = pd.read_csv(cwd+"/traditional_spambots_1.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ts1.columns.values.tolist()) - set(user_column_header)
ts1 = ts1.drop(user_diff_feature, axis=1)
ts1['user_type'] = 1

ts2 = pd.read_csv(cwd+"/traditional_spambots_2.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ts2.columns.values.tolist()) - set(user_column_header)
ts2 = ts2.drop(user_diff_feature, axis=1)
ts2['user_type'] = 1

ts3 = pd.read_csv(cwd+"/traditional_spambots_3.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ts3.columns.values.tolist()) - set(user_column_header)
ts3 = ts3.drop(user_diff_feature, axis=1)
ts3['user_type'] = 1

ts4 = pd.read_csv(cwd+"/traditional_spambots_4.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(ts4.columns.values.tolist()) - set(user_column_header)
ts4 = ts4.drop(user_diff_feature, axis=1)
ts4['user_type'] = 1

genuine = pd.read_csv(cwd+"/genuine_accounts.csv/users.csv",sep=',',header='infer')
user_diff_feature = set(genuine.columns.values.tolist()) - set(user_column_header)
genuine = genuine.drop(user_diff_feature, axis=1)
genuine['user_type'] = 0

#fakefoers = pd.read_csv(cwd+"/fake_followers.csv/users.csv",sep=',',header='infer')
#user_diff_feature = set(fakefoers.columns.values.tolist()) - set(user_column_header)
#fakefoers = fakefoers.drop(user_diff_feature, axis=1)
#fakefoers['user_type'] = 1

# loading varol
varol = pd.read_csv(cwd+"/user_varol.csv",sep=',',header='infer')
user_diff_feature = set(varol.columns.values.tolist()) - set(user_column_header)
varol = varol.drop(user_diff_feature, axis=1)
varol['crawled_at'] = datetime.datetime(2016,4,30)

# loading trump
trump_circle = pd.read_csv(cwd+"/user_data_trump.csv",sep=',',header='infer')
user_diff_feature = set(trump_circle.columns.values.tolist()) - set(user_column_header)
trump_circle = trump_circle.drop(user_diff_feature, axis=1)
trump_circle['crawled_at'] = datetime.datetime.today()
trump_circle['user_type'] = 0

# adding all datas up
#all_user = [ss1,ss2,ss3,ts2,ts3,ts4,genuine,fakefoers,varol]
all_user = [ss1,ss2,ss3,ts2,ts3,ts4,genuine,varol,trump_circle]
df = pd.DataFrame()
for dataset in all_user:
    df = pd.concat([df, dataset], ignore_index=True)
        
# Output the sampled spam dataframe
print "Outputing all aggregated user dataframe..."
today = datetime.datetime.today()
outputname = "all_users_"+str(today).replace(':','-')+".csv"
df.to_csv(outputname,sep=',', na_rep=" ", encoding='utf-8', index_label=False, index=False)