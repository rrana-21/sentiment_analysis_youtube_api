#!/usr/bin/env python
# coding: utf-8

# # Sentiment Analysis of Most Popular Videos on Youtube

# ## Why is sentiment analysis necesary on youtube videos?

# Sentiment analysis of the titles of popular YouTube videos can be helpful in gaining insights into the emotions and opinions associated with those titles. Analyzing the sentiment of the words used in the titles can provide an understanding of how viewers might feel about the content before watching it. A positive sentiment can indicate that the video is likely to be well-received, while a negative sentiment can suggest that the video is potentially controversial or disliked. This information can be used by marketers and content creators to create more engaging and successful video content.
# 
# The following analysis is done in three parts:
# 1) Data collection and preparation 
# 
# 2) Sentiment analysis algorithm selection and implementation
# 
# 3) Evaluation and interpretation of results

# ## Import Libraries/Packages

# In[99]:


#data retrivial
from googleapiclient.discovery import build
import pandas as pd 
import numpy as np 

#progress bar 
from tqdm.notebook import tqdm

#Huggingface pipeline (pip install if needed)
from transformers import pipeline

#datetime 
import datetime

#visuals
import matplotlib.pyplot as plt


# ## 1) Data collection and preparation 

# The YouTube Data API v3 is used to collect video metadata of the most popular Youtube videos. To ensure the maximum number of the most popular videos (200), pagination is used to iterate through the API's response and retrieve all available results. 
# 
# The results are stored in a List and converted into a pandas DataFrame for easier manipulation and analysis. Before applying any sentiment analysis algorithms or models, I needed to further clean and pre-process the data to ensure that it was accurate and meaningful. This involved ensuring the presence of an 'id' to avoid duplication, dropping unnecessary columns, and structuring the DataFrame for sentiment analysis.
# 
# More information for Youtube Data API v3 can be found [here](https://developers.google.com/youtube/v3). 

# In[112]:


apikey = 'xxxx'


# In[101]:


# Set parameters
max_results = 50
region_code = 'CA'

#build call 
youtube = build("youtube", "v3", developerKey=apikey)

#calling the API and storing the video data in the "videos" list, while pagnating responses to get max results of 200
videos = []
pageToken = ""
while True:
    requests = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        maxResults=max_results,
        pageToken=pageToken if pageToken != "" else "").execute()
    
    v = requests.get('items', [])
    if v:
        videos.extend(v)
    pageToken = requests.get('nextPageToken')
    if not pageToken:
        break

#create dataframe from the "videos list"
vid_df = pd.DataFrame(videos)

#id is outside of snippet, create a dictionary and apply pd.series to the snippet column to explode the dictionary /
#and store the values as columns
contents_df = vid_df['snippet'].apply(pd.Series)
vid_df = vid_df.join(contents_df)

#drop snippet column 
vid_df = vid_df.drop(columns=['snippet'])


# In[102]:


#check for max results, which should be 200
len(vid_df)


# ## 2) Sentiment analysis algorithm selection and implementation

# #### What is sentiment analysis?

# Sentiment analysis is the process of analyzing text, speech, or other forms of communication to determine the emotional tone or sentiment expressed. It involves using natural language processing (NLP) techniques and machine learning algorithms to identify and extract sentiment-related features such as positive or negative language, sarcasm, and irony. Sentiment analysis is used in a variety of applications, including marketing, customer service, product development, and social media monitoring. It helps businesses and organizations gain insights into how their customers feel about their products or services, identify potential issues, and respond to feedback more effectively.

# #### Approach to conducting sentiment analysis

# I'll be using Hugging Face's sentiment analysis model, DistilBERT-base-uncased-finetuned-sst-2-English, which is a pre-trained deep learning model that is capable of analyzing text and classifying it into sentiment categories - positive or negative. The model is trained on a large dataset called the Stanford Sentiment Treebank (SST-2) and has been fine-tuned for the English language. This model is particularly useful for analyzing short-form text, such as social media posts or headlines, and has been shown to achieve state-of-the-art performance on a variety of sentiment analysis tasks.
# 
# We will be running this model for each title of the 200 most popular youtube videos to extract a sentiment "label" and a "score".
# 
# "***label***": refers to the sentiment category assigned to the text being analyzed - typically, positive or negative. The label indicates the overall sentiment of the text, based on the sentiment classification model's analysis.
# 
# "***score***": represents the degree of confidence that the model has in its classification. The score is typically a probability value between 0 and 1, where a higher score indicates a greater level of confidence in the assigned sentiment label.

# In[103]:


#specifiy and use the 'distilbert-base-uncased-finetuned-sst-2-english' model for sentiment analysis
sent_pipeline = pipeline(model="distilbert-base-uncased-finetuned-sst-2-english")


# In[105]:


#run sent_pipeline on title atribute of dataframe, response stored as list of dictionaries in sent_scores attribute
vid_df['sent_scores'] = vid_df['title'].apply(lambda x: sent_pipeline(x))


# In[106]:


#remove sent_score values from list and store them only as dictionaries, i.e. explode to store only dictionary
results_df = vid_df.explode('sent_scores')

#split sent_score dictonaries into it's seperate columns
results_df['label'],results_df['conf_score'] = [v['label'] for k,v in results_df['sent_scores'].items()],[v['score'] for k,v in results_df['sent_scores'].items()]


# In[107]:


#drop sent_scores column 
results_df = results_df.drop('sent_scores', axis=1)

#results_df


# ## Evaluation and interpretation of results

# #### Binary Mapping

# A new column ("***binary_label***") was added to the dataset to map sentiment scores to a binary label. Specifically, scores indicating a positive sentiment were labeled as 1, while scores indicating a negative sentiment were labeled as -1. 
# 

# In[108]:


#create "label_score" column which assigns 1 for positive or 0 for negative, this will help us get an average for the sentiment
results_df['binary_label'] = results_df['label'].apply(lambda x: 1 if x == 'POSITIVE' else -1)


# #### Weighted Voting System

# For each record, multiply the sentiment category by its confidence score. If the sentiment category is "positive", multiply by 1. If it is "negative", multiply by -1. This will give you a score for each record, with higher scores indicating stronger sentiment.

# In[109]:


results_df['sentiment_scores'] = results_df['binary_label'] * results_df['conf_score']


# The label_score was used to calculate an average sentiment score for each video in the dataset. Videos with scores positive sentiment scores were interpreted as having a more positive sentiment, while videos with negative sentiment scores were interpreted as having a more negative sentiment. 

# In[110]:


#get sum of sentiment_scores
sum_of_score = results_df['sentiment_scores'].sum()

#sum_of_score


# #### Evaluation and Results

# By employing this binary mapping and weighted voting system, we can accurately use the predict a sentiment score by taking into account both the label (*binary_label*) and the confidence score (*conf_score*) for each video title, giving more weight to video titles with higher confidence scores. This approach can help to produce more accurate results than a simple majority vote or a binary classification based on a fixed threshold.
# 
# This overall sentiment can provide a nuanced understanding of the sentiment of these videos, which can be used to better inform creators of attractive and meaningful titles. 

# In[111]:


today = datetime.date.today()

sentiment =''
if sum_of_score >= 0:
    sentiment = 'positive'
else:
    sentiment = 'negative'

print(r'The overall sentiment for the most popular 200 videos on {0} is {1}.'.format(today, sentiment))


# #### Further Research/Findings

# With the sentiment scores now calculated and mapped to the videos, further research can be conducted to explore the relationship between sentiment and video performance. For example, by examining whether videos with more positive sentiment tend to receive more views or engagement, one can gain insight into the types of titles and topics that are most appealing to YouTube viewers. This information can then be used to assist with title selection, ensuring that titles are not only attention-grabbing but also convey a positive sentiment that resonates with viewers. By analyzing the relationship between sentiment and video performance, researchers can continue to refine and improve their understanding of the factors that contribute to successful YouTube content.
