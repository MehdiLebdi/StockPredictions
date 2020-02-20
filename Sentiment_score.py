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
import sys
import numpy as np
import pandas as pd
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
import nltk.sentiment.util
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

sid = SentimentIntensityAnalyzer()

cwd = os.getcwd()

def bbands(price, length=30, numsd=1):
    """ returns average, upper band, and lower band"""
    
    ave = price.rolling(length).mean()
    sd = price.rolling(length).std()
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return np.round(ave,3), np.round(upband,3), np.round(dnband,3)

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


if __name__ == "__main__":
	# Reading the saved data pickle file
    df_stocks = pd.read_pickle(cwd+'/Data/pickled_filtered.pkl')

    df_stocks['prices'] = df_stocks['adj close']

    # selecting the prices and articles
    df_stocks = df_stocks[['prices', 'articles']]

    df_stocks['articles'] = df_stocks['articles'].map(lambda x: x.lstrip('.-'))

    df = df_stocks[['prices']].copy()

    # Adding new columns to the data frame
    df["compound"] = ''
    df["neg"] = ''
    df["neu"] = ''
    df["pos"] = ''
    df["prediction"] = ''

    df["ave"], df["upper"], df["lower"] = bbands(df.prices, length=30, numsd=1)

    for date, row in df_stocks.T.iteritems():
        try:
            sentence = unicodedata.normalize('NFKD', df_stocks.loc[date, 'articles'])
            ss = sid.polarity_scores(sentence)
            df.at[date,'compound'] = ss['compound']
            df.at[date,'neg'] = ss['neg']
            df.at[date,'neu'] = ss['neu']
            df.at[date,'pos'] = ss['pos']
            if df["neg"].at[date] < df["pos"].at[date]:
                df.at[date,'prediction'] = ((df["lower"].at[date]+df["ave"].at[date])/2)
            else:
                df.at[date,'prediction'] = ((df["upper"].at[date]+df["ave"].at[date])/2)
        except TypeError:
            print(df_stocks.loc[date, 'articles'])
            print(date)

    PredictPrice = df["prediction"].iloc[-1]
    
    print("\n\nSentiment Analysis\n")
    print("=========================================================")
    print(("The next day price is: $%s \n") %(PredictPrice))

    y_true=[] #npArray of Actual Price for past month
    y_pred=[] #npArray of Predicted Price for past month
    y_true = df['prices'].values.tolist()
    y_true_previous = y_true[-159:]
    y_pred = df['prediction'].tolist()
    y_pred_previous = y_pred[-159:]

    #plot of prediction and actual prices
    plt.figure(figsize=(15, 5), facecolor='w', edgecolor='k')
    plt.plot(df["prices"].iloc[-159:], color='blue', linewidth=3, label= 'Actual')
    plt.scatter(df.index, df["prediction"], color='red', label='Predicted')
    plt.title("Apple Closing Prices(Over 5-month period)")
    plt.xlabel("Dates")
    plt.ylabel("Prices ($)")
    plt.legend(loc='upper left')
    plt.show()

    #Save Prediction into a CSV file
    df["prediction"].to_csv(cwd+'/Data/Googl Stock Prediction.csv',sep=',', encoding='utf-8')

    #Benchmark metrics of success
    print("Metrics of Success:")

    #Mean Absolute Percentage Error
    MAPE = mean_absolute_percentage_error(y_true_previous,y_pred_previous)
    print(("The Mean Absolute Percentage Error is: %.2f percent")%(MAPE))
    #Mean Squared Error
    mse = mean_squared_error(y_true_previous, y_pred_previous)
    print(("The Mean Squared Error is: %.2f")%(mse))
    
    sys.exit("Code Executed Successfully")