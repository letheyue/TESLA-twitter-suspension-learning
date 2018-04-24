# TESLA: TwittEr Spam LeArning
## CSCE 670 Spring 2018, Course Project

### Intro
Welcome to our code base, where the magic happens! We'd love to introduce our web application that can detect if a user is a spam or not in real-time. For technical details, please keep on reading or refer to the [about](https://tesla-twitter-spammer-learning.herokuapp.com/about/) section. Our app is live on [Heroku](https://tesla-twitter-spammer-learning.herokuapp.com), check it out!

### Installation guide (local server mode)
Our application is built entirely on Python 3. Sorry 2.7 - it's time for an upgrade! (Tensorflow doesn't work with 2.7 anyways. SAD.)

* For Windows users who are using Anaconda, please make sure that you have Python 3.5 environment installed. You can check out this awesome post [here](https://conda.io/docs/user-guide/tasks/manage-python.html) for Python version control with Conda. 
* For Mac users: as long as your Python version >= 3.5, you should be fine.

To play around with our code, please do **fork** first. Then **clone** it to your local machine. Install the required libraries by typing the command below:
```Bash
cd src 
pip install -Ur requirements.txt
```
(Again, for Windows users - if you have an issue with cache files, try
```Python
pip install -Ur requirements.txt --no-cache-dir
```
instead.)

Once everything is installed, stay in the *src* folder and type:
```Python
python manage.py runserver
```

Note: you might encounter an **ImportError** claiming that there's no module called 'Tesla.aws'. That is because our team uses AWS as part of the storage. Simply uncomment the following line in the **\src\Tesla\settings\base.py** file:

```Python
# Comment this line please
from Tesla.aws.conf import *
```

You should be able to access our application in a local mode.
### Switching between different text models
We have trained two models for the tweet feature: **TF-IDF** and **CNN**. The latter one is too big to load on a Heroku free dyno. Thus, our online app runs the **TF-IDF** model by default. When you download our repository and run it in the local server mode, it's defaulted to run **CNN**. If you'd like to switch to another model, change the following lines in the **\src\predictions\models.py**:

```Python
# use cnn text model:
#basic_info = get_cnn_predict(screen_name, basic_info)

# use tfidf text model:
basic_info = get_tfidf_predict(screen_name, basic_info)
```

Uncomment the one that you'd like to use. (Please, do not uncomment/comment both. We have no guarantee on how the application will behave. DANGER ZONE!)
### Something technical
As promised above - here is something technical.

Our website was built upon Django 1.9 with Python 3.6. It accepts screennames (aka handler, e.g. [@realDonaldTrump](https://twitter.com/realDonaldTrump)) as input and communicates with the Twitter API to gather basic account and tweet information. 

Our framework consists of two parts: account and tweet models. 
* Account model focuses on [User](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object) based features, such as the count of favorite tweets, account ages, etc. 
* Tweet model, on the other hand, uses text from the [Tweet](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object) object exclusively. We've trained two text-based models, namely TF-IDF and CNN. Each text-based model accepts the latest 5 tweets as input. (If a user tweets less than 5 times, then the text model would predict based on the number of actual tweets available.) 

Our models were pre-trained offline for online prediction. Once the results are ready for both models, we use a simple weighted function to aggregate them together and get a final "spam" score. If the score is greater than 50%, then we believe that this user is a spammer.

If you'd like to know more details on how we actually built our models, check out the [classifiers](https://github.com/letheyue/TESLA-twitter-suspension-learning/tree/master/classifiers) that we've tried and [data visualization](https://github.com/letheyue/TESLA-twitter-suspension-learning/tree/master/data%20visualization) plots.

### If you've encountered any issues...
Please, please, please DO NOT HESITATE to let us know! Send us a pull request and we'll manage to get back to you ASAP. Bug reports welcome!

### Special shout-out!
* Thanks [Yue](https://github.com/letheyue) for building the website and merging everything together. 
* Thanks [Rose](https://github.com/mekomlusa) for training the account model and providing guidance on how to run traditional classifiers in general.
* Thanks [Weitong](https://github.com/harry08010) for his specialization in front-end design and edition work.
* Thanks [Bowen](https://github.com/lanbowen23) for training the text model and fiddling with deep learning.

~~And finally, thanks Cav and Parisa. You are just simply too nice to read this through, so we think you deserve some credits here.~~

