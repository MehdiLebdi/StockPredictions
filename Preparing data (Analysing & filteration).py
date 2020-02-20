#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Artificial Intelligence Stock Market Price Predictor.
   Copyright (C) 2018. Authors: Mehdi Lebdi>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import os
import numpy as np
import csv, json
import datetime
import pandas as pd
import sys

cwd = os.getcwd()
#Perform for each stock by changing the stock symbol
with open(cwd+'/Data/quandl/GOOGL data.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    # Convert csv file reader to a lists 
    data_list = list(spamreader)

# Separating header from the data
header = data_list[0] 
data_list = data_list[1:] 
data_list = np.asarray(data_list)

# Selecting date and close value for each day
selected_data = data_list[:, [0, 4, 5]]
df = pd.DataFrame(data=selected_data[0:,1:],
             index=selected_data[0:,0],
                                columns=['close', 'adj close'],
                                        dtype='float64')

# Adding missing dates to the dataframe
current_date = str(datetime.date.today())
start_date = str(datetime.datetime.now() + datetime.timedelta(-190))
print(start_date)
start_dateTime = start_date[:10]

df1 = df
idx = pd.date_range(start_dateTime, current_date)
df1.index = pd.DatetimeIndex(df1.index)
df1 = df1.reindex(idx, fill_value=np.NaN)

interpolated_df = df1.interpolate()
interpolated_df.count() 

# Removing extra date rows added in data for calculating interpolation
interpolated_df = interpolated_df[3:]

###############################################################################################  
## Preparing NYTimes data

date_format = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S+%f"]
def try_parsing_date(text):
    for fmt in date_format:
        try:
            return datetime.datetime.strptime(text, fmt).strftime('%Y-%m-%d')
        except ValueError:
            pass
    raise ValueError('no valid date format found')

#Get the years and months to analyse
curr_year = int(current_date[:4])
curr_month = int(current_date[5:7])
#month_30ago = int(start_date[5:7])
month_30ago = 1

years = []
months = []
years.append(2017)
years.append(curr_year)
months.append(month_30ago)
months.append(curr_month)

dict_keys = ['pub_date', 'headline']
articles_dict = dict.fromkeys(dict_keys)
# Filtering list for type_of_material
type_of_material_list = ['blog', 'brief', 'news', 'editorial', 'op-ed', 'list','analysis']
# Filtering list for section_name
section_name_list = ['business', 'national', 'world', 'u.s.' , 'politics', 'opinion', 'tech', 'science',  'health']
news_desk_list = ['business', 'national', 'world', 'u.s.' , 'politics', 'opinion', 'tech', 'science',  'health', 'foreign']

current_article_str = ''      

## Adding article column to dataframe
interpolated_df["articles"] = ''
count_articles_filtered = 0
count_total_articles = 0
count_main_not_exist = 0               
count_unicode_error = 0     
count_attribute_error = 0  

for year in years:
    if(year == 2017):
        months=[11,12]   #articles for november/december 2017
    else:
        months=list(range(month_30ago,curr_month+1))  #articles for january 2018 to current month 
    for month in months:
        print(year,month)
        file_str = cwd + '/Data/NYTimes/' + str(year) + '-' + '{:02}'.format(month) + '.json'
        with open(file_str) as data_file:    
            NYTimes_data = json.load(data_file)
        count_total_articles = count_total_articles + len(NYTimes_data["response"]["docs"][:])
        for i in range(len(NYTimes_data["response"]["docs"][:])):
            try:
                if any(substring in NYTimes_data["response"]["docs"][:][i]['type_of_material'].lower() for substring in type_of_material_list):
                    if any(substring in NYTimes_data["response"]["docs"][:][i]['section_name'].lower() for substring in section_name_list):
                        count_articles_filtered += 1
                        articles_dict = { your_key: NYTimes_data["response"]["docs"][:][i][your_key] for your_key in dict_keys }
                        articles_dict['headline'] = articles_dict['headline']['main']
                        date = try_parsing_date(articles_dict['pub_date'])
                        if date == current_date:
                            current_article_str = current_article_str + '. ' + articles_dict['headline']
                        else:  
                            interpolated_df.set_value(current_date, 'articles', interpolated_df.loc[current_date, 'articles'] + '. ' + current_article_str)
                            current_date = date
                            current_article_str = articles_dict['headline']
                        # For last condition in a year
                        if (date == current_date) and (i == len(NYTimes_data["response"]["docs"][:]) - 1): 
                            interpolated_df.set_value(date, 'articles', current_article_str)   
                        
             #Exception for section_name or type_of_material absent
            except AttributeError:
                count_attribute_error += 1
                try:
                    if any(substring in NYTimes_data["response"]["docs"][:][i]['news_desk'].lower() for substring in news_desk_list):
                            count_articles_filtered += 1
                            articles_dict = { your_key: NYTimes_data["response"]["docs"][:][i][your_key] for your_key in dict_keys }
                            articles_dict['headline'] = articles_dict['headline']['main']
                            date = try_parsing_date(articles_dict['pub_date'])
                            if date == current_date:
                                current_article_str = current_article_str + '. ' + articles_dict['headline']
                            else:  
                                interpolated_df.set_value(current_date, 'articles', interpolated_df.loc[current_date, 'articles'] + '. ' + current_article_str)
                                current_date = date
                                current_article_str = articles_dict['headline']
                            # For last condition in a year
                            if (date == current_date) and (i == len(NYTimes_data["response"]["docs"][:]) - 1): 
                                interpolated_df.set_value(date, 'articles', current_article_str)   
                
                except AttributeError:
                    pass
                pass
            except KeyError:
                #print ('key error')
                count_main_not_exist += 1
                pass   
            except TypeError:
                #print ("type error")
                count_main_not_exist += 1
                pass
              
print (count_articles_filtered) 
print (count_total_articles)                    
print (count_main_not_exist)
print (count_unicode_error)

## Putting all articles if no section_name or news_desk not found
for date, row in interpolated_df.T.iteritems():   
    if len(interpolated_df.loc[date, 'articles']) <= 400:
        month = date.month
        year = date.year
        file_str = cwd + '/Data/NYTimes/' + str(year) + '-' + '{:02}'.format(month) + '.json'
        with open(file_str) as data_file:    
            NYTimes_data = json.load(data_file)
        count_total_articles = count_total_articles + len(NYTimes_data["response"]["docs"][:])
        interpolated_df.set_value(date.strftime('%Y-%m-%d'), 'articles', '')
        for i in range(len(NYTimes_data["response"]["docs"][:])):
            try:
                articles_dict = { your_key: NYTimes_data["response"]["docs"][:][i][your_key] for your_key in dict_keys }
                articles_dict['headline'] = articles_dict['headline']['main']
                pub_date = try_parsing_date(articles_dict['pub_date'])
                if date.strftime('%Y-%m-%d') == pub_date: 
                    interpolated_df.set_value(pub_date, 'articles', interpolated_df.loc[pub_date, 'articles'] + '. ' + articles_dict['headline'])  
                
            except KeyError:
                #print ('key error')
                pass   
            except TypeError:
                #print ("type error")
                pass

# Saving the data as pickle file
interpolated_df.to_pickle(cwd+'/Data/pickled_filtered.pkl')  

# Save pandas frame in csv form
#interpolated_df.to_csv(cwd+'/Data/sample_filtered.csv',sep=',', encoding='utf-8')

sys.exit("Pickled file generated Successfully")