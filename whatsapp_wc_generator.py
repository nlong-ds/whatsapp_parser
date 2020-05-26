# -*- coding: utf-8 -*-
"""
Created on 2020-05-25
@author: Niccolò Longoni
Whapparser WordCloud generator
"""

import os
import pandas as pd
import sys
from whapparser_class import Whapparser


if __name__ == '__main__': 
    

##### Handle file selection and user input ######
    
    print(70 * '-')
    print('Looking for .txts in the script folder\n')
    txts = [item for item in os.listdir() if item.endswith('txt')]
    print(txts)
    
    if len(txts) == 0:
        print('No txts files found in directory. Please add some.')
        sys.exit('Exiting program')
        
    elif len(txts) > 1:
        print('More than one file retrieved. which do you want to test?\nPlease include .txt. suffix.')
        

        while True:
            to_read = input()
            if to_read not in txts:
                print('This file does not exist in the folder. Please insert valid input.')
                continue
            else:
                break

    else:
        to_read = txts[0]

    
    try:
        f = open(f"{to_read}", "r", errors='ignore', encoding = 'UTF-8')
        lines = f.readlines()
        starting_df = pd.DataFrame(lines, columns = ['raw'])
    
    
    except Exception as e:
                
        print (70 * ('-'))
        print ("Error found in reading the Txts: " + str(e))
        sys.exit('Exiting program')

            
        
##### Applying class methods and parsing data ######

    print('Parsing the dataframe...')    
    try:
        conversation = Whapparser()
        df = conversation.parse_dataframe(starting_df)   

    except Exception as e:              
        print (70 * ('-'))
        print ("Error found in Parsing the dataframe" + str(e))
        sys.exit('Exiting program')


    print('Removing anomalies and normalizing text (null rows and media)...')
    df = conversation.drop_anomalies(df)
    df["message"] = df["message"].apply(conversation.normalize) 
    df["message_tolist"] = df["message"].apply(conversation.message_tolist)
   
    
    
##### Generating wordcloud ######

    print('Generating wordcloud...')
    
    wc_type = input("Do you wish to generate a user-specific wordcloud? [Y/n]")
    if wc_type.lower() == 'y' :
        user_input = input("Specify a user if you want to generate a specific wordcloud")
    else:
        user_input = None
        print('Generating conversation wordcloud...')
    
    figure = conversation.draw_cloud(df, user=user_input)

    

##### Create folder to store output #####
    
    if not os.path.exists('output'):
        os.makedirs('output')
    output_directory = os.getcwd() + '\\output\\'
 
    
    try:    
        df.to_csv(output_directory + 'conversation.csv')
        figure.savefig(output_directory + 'wordcloud.jpg', format="jpg")

    except Exception as e:
                
        print (70 * ('-'))
        print ("Error found while creating Dataframe/saving worcloud: " + str(e))
        
