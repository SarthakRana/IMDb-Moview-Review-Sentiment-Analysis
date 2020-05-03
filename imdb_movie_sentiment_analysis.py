# -*- coding: utf-8 -*-
"""IMDB_movie_sentiment_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AHOKe2XgJVYel3nNNlqQ270cpw5Su1_A

# Importing relevant libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist

"""# Importing data from Google Drive"""

from google.colab import drive
drive.mount('/content/drive')

train_reviews = []
for line in open('/content/drive/My Drive/movie_data/full_train.txt', 'r', encoding='utf-8'):
  train_reviews.append(line.strip())

test_reviews = []
for line in open('/content/drive/My Drive/movie_data/full_test.txt', 'r', encoding='utf-8'):
  test_reviews.append(line.strip())

"""# Cleaning and Preprocessing

### Remove punctuations, HTML tags, etc.
"""

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
    
    return reviews

train_reviews_clean = preprocess_reviews(train_reviews)
test_reviews_clean = preprocess_reviews(test_reviews)

"""### Tokenizing the data"""

nltk.download('punkt')

train_reviews_clean_tokens = []
for review in train_reviews_clean:
  train_reviews_clean_tokens.append(word_tokenize(review))

test_reviews_clean_tokens = []
for review in test_reviews_clean:
  test_reviews_clean_tokens.append(word_tokenize(review))

"""## Removing stopwords"""

def remove_noise(review_tokens, stop_words = ()):
    return [token for token in review_tokens if token not in stop_words]

nltk.download('stopwords')
stop_words = stopwords.words('english')

cleaned_train_reviews = []
cleaned_test_reviews = []

for tokens in train_reviews_clean_tokens:
  cleaned_train_reviews.append(remove_noise(tokens, stop_words))

for tokens in test_reviews_clean_tokens:
  cleaned_test_reviews.append(remove_noise(tokens, stop_words))

"""## Normalizing the data - Lemmatization"""

def lemmatizeReview(review):
  lemmatizer = WordNetLemmatizer()
  lemmatizedReviews = []
  for token, tag in pos_tag(review):
    if tag.startswith('NN'):
      pos = 'n'
    elif tag.startswith('VB'):
      pos = 'v'
    else:
      pos = 'a'
    token = lemmatizer.lemmatize(token, pos)
    lemmatizedReviews.append(token.lower())
  return lemmatizedReviews

nltk.download('wordnet') # used for stemming pupose inside WordNetLemmatizer
nltk.download('averaged_perceptron_tagger') # User for tagging pupose inside pos_tag
train_reviews_normalized = [lemmatizeReview(review) for review in cleaned_train_reviews]
test_reviews_normalized = [lemmatizeReview(review) for review in cleaned_test_reviews]

"""## Let's have a look at the word count
Instead of simply noting whether a word appears in the review or not, we can include the number of times a given word appears. This can give our sentiment classifier a lot more predictive power. For example, if a movie reviewer says ‘amazing’ or ‘terrible’ multiple times in a review it is considerably more probable that the review is positive or negative, respectively.
"""

# get a single list of tokens - all tokens in a single list
def get_all_words(tokens):
  all_tokens = []
  for token_list in tokens:
    for token in token_list:
      all_tokens.append(token)
  return all_tokens

all_train_tokens_list = get_all_words(train_reviews_normalized)
all_test_tokens_list = get_all_words(test_reviews_normalized)
train_token_frequency = FreqDist(all_train_tokens_list)
test_token_frequency = FreqDist(all_test_tokens_list)

print(train_token_frequency.most_common(10))
print(test_token_frequency.most_common(10))

"""Most common words are same in both training and testing set

# Building the classification model

## Preparing the data for training and testing
"""

def get_train_reviews_tokes(review_normalized):
    for token_list in review_normalized:
        yield dict([token, True] for token in token_list)

train_reviews_for_model = get_train_reviews_tokes(train_reviews_normalized)
test_reviews_for_model = get_train_reviews_tokes(test_reviews_normalized)

COUNT = 1
train_dataset = []
for review_dict in train_reviews_for_model:
  if COUNT <= 12500:
    train_dataset.append((review_dict, 1))
  else:
    train_dataset.append((review_dict, 0))
  COUNT += 1

COUNT = 1
test_dataset = []
for review_dict in test_reviews_for_model:
  if COUNT <= 12500:
    test_dataset.append((review_dict, 1))
  else:
    test_dataset.append((review_dict, 0))
  COUNT += 1

import random
random.shuffle(train_dataset)

train_dataset[24500]

occurence = []
for i in range(1000):
  for tup in train_dataset:
    if tup[1] == 0:
      occurence.append(i)
      break

len(occurence)

