import pickle
import re
import os
import twitter
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer

import warnings 
warnings.filterwarnings("ignore")

tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')


script_dir = os.path.dirname(__file__)

from .ignore import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token_key=ACCESS_TOKEN_KEY,
                     access_token_secret=ACCESS_TOKEN_SECRET)


# crawl at the text and do pre-process, then change them into vector feature
def get_text(screen_name):
    timeline = api.GetUserTimeline(screen_name=screen_name)

    # get the first 5 text
    list_text = list()
    index = 0
    for item in timeline:
        index += 1
        data = item._json
        clean_data = tweet_cleaner_updated(data['text'])
        list_text.append(clean_data)
        if index == 5:
            break
            
    # pre-processing the data
    with open('predictions/classifier/tvec.pickle', 'rb') as handle:
    	tvec = pickle.load(handle)
        
    test_vec = tvec.transform(list_text)

    return test_vec

# pre-processing the text
def tweet_cleaner_updated(text):
    soup = BeautifulSoup(text, 'html.parser')
    souped = soup.get_text()
    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    stripped = re.sub(combined_pat, '', bom_removed)
    stripped = re.sub(www_pat, '', stripped)
    lower_case = stripped.lower()
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()



def get_tfidf_predict(screen_name, basic_info):
    test_vec = get_text(screen_name)

    with open('predictions/classifier/lr.pickle', 'rb') as handle:
        lr_with_tfidf = pickle.load(handle)

    pred_text = lr_with_tfidf.predict_proba(test_vec)
    basic_info['prediction_text_label'] = list()
    for i in range (0, len(pred_text)):
        basic_info['prediction_text_label'].append(float("{0:.4f}".format(pred_text[i][1])) * 100)
    if (basic_info['prediction_text_label']):
        basic_info['prediction_text_mean'] = sum(basic_info['prediction_text_label']) / float(len(basic_info['prediction_text_label']))
        basic_info['prediction_total'] = (basic_info["prediction_account_label"] + basic_info['prediction_text_mean']) / 2
    else:
        basic_info['prediction_text_mean'] = 0
        basic_info['prediction_total'] = basic_info["prediction_account_label"]

    basic_info['prediction_text_method'] = "Due to the timeout parameter and capacity of Heroku, this is a lighter version using TF-IDF model for predicting the tweets. If you want to see the full version using CNN, please see the code on Github."

    return basic_info

