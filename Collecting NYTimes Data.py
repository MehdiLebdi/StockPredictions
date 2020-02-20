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

import sys, csv, json
import os
import datetime
import requests
"""
About:
Python wrapper for the New York Times Archive API 
https://developer.nytimes.com/article_search_v2.json
"""

class APIKeyException(Exception):
    def __init__(self, message): self.message = message 

class InvalidQueryException(Exception):
    def __init__(self, message): self.message = message 

class ArchiveAPI(object):
    def __init__(self, key=None):
        """
        Initializes the ArchiveAPI class. Raises an exception if no API key is given.
        :param key: New York Times API Key
        """
        self.key = key
        self.root = 'http://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={}' 
        if not self.key:
            nyt_dev_page = 'http://developer.nytimes.com/docs/reference/keys'
            exception_str = 'Warning: API Key required. Please visit {}'
            raise Exception(exception_str.format(nyt_dev_page))

    def query(self, year=None, month=None, key=None,):
        """
        Calls the archive API and returns the results as a dictionary.
        :param key: Defaults to the API key used to initialize the ArchiveAPI class.
        """
        if not key: key = self.key
        if (year < 1882) or not (0 < month < 13):
            # currently the Archive API only supports year >= 1882
            exception_str = 'Invalid query: See http://developer.nytimes.com/archive_api.json'
            raise InvalidQueryException(exception_str)
        url = self.root.format(year, month, key)
        r = requests.get(url)
        return r.json()

api = ArchiveAPI('********')

today = str(datetime.date.today())
start_date = str(datetime.datetime.now() + datetime.timedelta(-190))
print("start date")
print(start_date)
curr_day = int(today[8:10])
curr_year = int(today[:4])
curr_month = int(today[5:7])

day_30ago = int(start_date[8:10])
year_30ago = int(start_date[:4])
#month_30ago = int(start_date[5:7])
month_30ago = 1

years = []
months = []
years.append(year_30ago)
years.append(curr_year)

cwd = os.getcwd()

#Get articles in JSON format
for year in years:
    if(year == 2017):
        months=[11,12]   #articles for november/december 2017
    else:
        months=list(range(month_30ago,curr_month+1))  #articles for january 2018 to current month 
    for month in months:
        mydict = api.query(year, month)
        file_str = cwd + '/Data/NYTimes/' + str(year) + '-' + '{:02}'.format(month) + '.json'
        with open(file_str, 'w') as fout:
            json.dump(mydict, fout)
        fout.close()

sys.exit("Files Successfully Created")