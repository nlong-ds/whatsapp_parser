# -*- coding: utf-8 -*-
"""
Created on 2020-05-25
@author: Niccolò Longoni
Whapparser Class & Methods
"""

import string as s
import re
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords


stop_words_it = stopwords.words("italian")
stop_words_it.extend(x for x in ['comunque', 'allora', 'quando', 'quindi', 'perchè','ancora','qualcosa'])
stop_words_en = stopwords.words("english")
stop_words_all = [stop_words_it, stop_words_en]
stop_words = set().union(*stop_words_all)


class Whapparser() :
    
    def parse_dataframe(self, dataframe):
        idx = int(dataframe.iloc[0].str.find('-') + 2) #find first occurrence of - and count two extra characters to exclude the '- '
        date_time = []
        user_msg = []
       
        for row in dataframe.itertuples():                     
            dt = row[1][0:idx-3] #isolates date and time
            um = row[1][idx:-1] #isolates user and message, excluding /n 
            date_time.append(dt)
            user_msg.append(um)
        
        #add new columns
        dataframe["date_time"] = date_time
        dataframe["good"] = user_msg
        
        #split time column into date and time
        new_cols = dataframe["date_time"].str.split(pat = ', ', n=1, expand = True) #n parameter hits oly the first occurrence
        new_cols = new_cols.rename(columns = {0:'date', 1:'time'})
        dataframe = pd.concat([dataframe,new_cols], axis = 1)         
       
        #parse the good column in two cols: [user,message] 
        pattern = r'(?P<user>[^:]+):\s(?P<message>.+)'
        extra_columns = dataframe["good"].str.extract(pattern, flags = re.IGNORECASE)
        
        output = pd.concat([dataframe, extra_columns], axis = 1)
              
        #strip messy columns
        output = output.drop(columns = ["raw", "date_time", "good"]) 
        
        return output



    def drop_anomalies(self, dataframe):
        #TODO - Handle multiline messages. This is a brute-force method that removes them entirely.
        dataframe = dataframe.dropna()

        #remove all <Media omitted>. Whenever a picture, video or any media content is sent,
        mask = dataframe["message"].str.lower().str.contains(r'<media.+>')
        idx_todrop = dataframe["message"][mask].index
        dataframe = dataframe.drop(idx_todrop).reset_index(drop = True)
        return dataframe
        
    
    
        #2.2. define and apply cleaning function to normalize texts in columns
    def normalize(self, text):
        text = str(text).lower()
        text = text.translate(text.maketrans('','', s.punctuation)) #strip of all punctuation
        return text
    
    
    
    def message_tolist(self, text):
        text = self.normalize(text)
        text_tolist = text.split()
        return text_tolist



    def draw_cloud(self, dataframe, user = None):
        all_words = []
     
        if user != None:
            subset = dataframe[dataframe["user"] == user]["message_tolist"]
        else:
            subset = dataframe["message_tolist"]
    
        for row in subset:
            for word in row:
                if len(word) >= 5:
                    all_words.append(word)
        concatenated_words = ' '.join(all_words)
    
        wc = WordCloud(width = 1200, height = 800, stopwords = stop_words).generate(concatenated_words)
    
        fig = plt.figure(figsize = (12,8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most common words by {}'.format(user))
                
        return fig
        