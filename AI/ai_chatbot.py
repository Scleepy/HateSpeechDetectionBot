import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import re
import nltk
from nltk.util import pr
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword = set(stopwords.words("english"))

df = pd.read_csv('./AI/tidied_data.csv')

df['labels'] = np.where(df["hate_speech"] > 0, "Hate Speech Detected", np.where(df["offensive_language"] > 0, "Offensive Language Detected", "No Hate Speech or Offensive Language Detected"))

df = df[['tweet', 'labels']]

def clean(text):
    text = str(text).lower()
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text

df['tweet'] = df['tweet'].apply(clean)

x = np.array(df["tweet"])
y = np.array(df["labels"])

cv = CountVectorizer()
x = cv.fit_transform(x)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.33, random_state = 42)
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

def predict_word(test_data):
    df = cv.transform([test_data]).toarray()
    return clf.predict(df)[0]
