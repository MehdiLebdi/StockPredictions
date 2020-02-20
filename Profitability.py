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
import unicodedata

cwd = os.getcwd()

#Status = Buy | Sell | Hold | Pass as 0,1,2,3

if __name__ == "__main__":

	# Reading the saved data from csv or excel file

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM/NetflixAnalysis.xlsx')

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/NetflixAnalysis.xlsx')

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/NetflixAnalysis.xlsx')

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/NetflixAnalysis.xlsx')

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/NetflixAnalysis.xlsx')

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/NetflixAnalysis.xlsx')

    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Sentiment/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Sentiment/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Sentiment/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Sentiment/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/Sentiment/NetflixAnalysis.xlsx')
    
    df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/AppleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/FacebookAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/GoogleAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/MicrosoftAnalysis.xlsx')
    #df_stocks = pd.read_excel(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/NetflixAnalysis.xlsx')

    df = df_stocks

    for date in range(1, len(df)):
        try:
            #if prediction is less than open and previous status is Buy then we Sell at open
            if (df["prediction"].at[date] < df["open"].at[date]) and df.at[date-1,'status'] == 0:
                df.at[date,'status'] = 1 # new status updated to Sell
                df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Sell at open 
                # number of shares stays same as previous
                df.at[date,'number shares'] = df.at[date-1,'number shares']

            #if prediction is less than open and previous status is Sell then we Pass at open
            elif (df["prediction"].at[date] < df["open"].at[date]) and df.at[date-1,'status'] == 1:
                df.at[date,'status'] = 3 # new status updated to Pass
                df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Pass at open 
                # number of shares is same as previous
                df.at[date,'number shares'] = df.at[date-1,'number shares']

            #if prediction is less than open and previous status is Pass then we Pass at open
            elif (df["prediction"].at[date] < df["open"].at[date]) and df.at[date-1,'status'] == 3:
                df.at[date,'status'] = 3 # status stays at Pass
                df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Pass at open 
                # number of shares is same as previous
                df.at[date,'number shares'] = df.at[date-1,'number shares']

            #if prediction is more than open and previous status is Pass then we Buy at open
            elif (df["prediction"].at[date] > df["open"].at[date]) and df.at[date-1,'status'] == 3:
                df.at[date,'status'] = 0 # new status updated to Buy
                # number of shares = round to lowest integer for (balance/open)
                df.at[date,'number shares'] = int(df.loc[date-1,'balance']/df['open'].at[date])
                df.at[date,'balance'] = df.loc[date,'number shares'] * df['open'].at[date] # Balance after Buy at open 

            #if prediction is more than open and previous status is Buy then we Hold at open
            elif (df["prediction"].at[date] > df["open"].at[date]) and df.at[date-1,'status'] == 0:
                df.at[date,'status'] = 2 # new status updated to Hold
                df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Hold at open 
                # number of shares is same as previous
                df.at[date,'number shares'] = df.at[date-1,'number shares']

            #if prediction is more than open and previous status is Hold then we Hold at open
            elif (df["prediction"].at[date] > df["open"].at[date]) and df.at[date-1,'status'] == 2:
                df.at[date,'status'] = 2 # status stays at Hold
                df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Hold at open 
                # number of shares is same as previous
                df.at[date,'number shares'] = df.at[date-1,'number shares']

            #if prediction is more than open and previous status is Sell then we Buy at open
            elif (df["prediction"].at[date] > df["open"].at[date]) and df.at[date-1,'status'] == 1:
                df.at[date,'status'] = 0 # new status updated to Buy
                # number of shares = round to lowest integer for (balance/open)
                df.at[date,'number shares'] = int(df.loc[date-1,'balance']/df['open'].at[date])
                df.at[date,'balance'] = df.loc[date,'number shares'] * df['open'].at[date] # Balance after Buy at open 

            #if prediction is less than open and previous status is Hold then we Sell at open
            elif (df["prediction"].at[date] < df["open"].at[date]) and df.at[date-1,'status'] == 2:
                df.at[date,'status'] = 1 # new status updated to Sell
                df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Sell at open 
                # number of shares stays same as previous
                df.at[date,'number shares'] = df.at[date-1,'number shares']

            else:
                print(date)
                print(df.loc[date, 'open'])
                print(df.loc[date, 'prediction'])

            df.at[date,'profit/loss'] = df.at[date,'balance'] - df.at[0,'balance']

            #If the losses are more than $1000 and we're still holding then we cut losses and sell at market price
            #if df.at[date,'profit/loss'] < -1000 and df.at[date,'status'] == 2:  #Don't be a Bag Holder
            #    df.at[date,'status'] = 1 # new status updated to Sell
            #    df.at[date,'balance'] = df.loc[date-1,'number shares'] * df['open'].at[date] # Balance after Sell at open 
                # number of shares stays same as previous
            #    df.at[date,'number shares'] = df.at[date-1,'number shares']
            
        except TypeError:
            print(df.loc[date, 'open'])
            print(date)

    for date in range(len(df)):
        try:
            if df.at[date,'status'] == 0:
                df.at[date,'Actual Status']  = 'Buy'

            elif df.at[date,'status'] == 1:
                df.at[date,'Actual Status']  = 'Sell'

            elif df.at[date,'status'] == 2:
                df.at[date,'Actual Status']  = 'Hold'

            else:
                df.at[date,'Actual Status']  = 'Pass'
                
        except TypeError:
            print(df.loc[date, 'open'])
            print(date)


    #Save Prediction into a CSV file

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree1/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree2/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree3/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree4/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Polynomial/degree5/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Sentiment/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Sentiment/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Sentiment/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Sentiment/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/Sentiment/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')

    df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/profit/Apple Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/profit/Facebook Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/profit/Google Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/profit/Microsoft Stock Profitability.csv',sep=',', encoding='utf-8')
    #df.to_csv(cwd+'/Data/ProfitsAnalysis/LSTM+Sentiment/profit/Netflix Stock Profitability.csv',sep=',', encoding='utf-8')


    print("csv files successfully generated")
    sys.exit("Profitability Analysis successfully executed")