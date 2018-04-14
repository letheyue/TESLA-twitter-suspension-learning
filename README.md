Update 04/13/2018

The github url: https://github.com/letheyue/TESLA-twitter-suspension-learning

##### Preparation: This web is built on Python3, if you want to use different python versions on your root, you can choose: 
```Bash
pip install virtualenv
```

To download the library: 
```Bash
cd src 
pip install -Ur requirements.txt
```

##### Attention: If you download some new libs, please do this: 
```Bash
pip freeze >> requirements.txt
```

If you establish a new model, please do this: 
```Bash
python manage.py makemigrations 
python manage.py migrate
```

Everytime git pull from the master, please do this: 
```Bash
pip install -Ur requirements.txt 
python manage.py makemigrations 
python manage.py migrate
```

If you want to write new code, please build a new branch on your local, and merge the branch with master, this is a useful way to avoid conflict!

In src/predictions/models.py, I use twitter access token, this is a private key so I don't pull it on the github. If you run the server, please add the ignore.py(upload in the google drive) into src/predictions/. And do not make the token in public.(I have added it into .gitignore)