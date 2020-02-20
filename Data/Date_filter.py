#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

    df_stocks = pd.read_csv(cwd+'/SortDate/finaldf.csv')
    df_st = pd.read_csv(cwd+'/SortDate/NFLX data.csv')


    df = df_stocks   #with all dates
    df2 = df_st      #Without weekends

    #print(df.index[4])
    #print(df.at[df.index[4]])
    #print(df['Date'])
    df2["merge"] = ''

    for i in range(0, len(df2)):
        try:
            #print(df["Date"].loc[i])
            #print(df2["Date"].loc[i])
            if (df["Date"].loc[i] != df2["Date"].loc[i]):
                df2.at[i,'merge']=df["Date"].loc[i]
                
                df.at[date,'status'] 
                print(df["Date"].loc[i])
                print(df["Date"].loc[i])
        except TypeError:
            print('here')
            #print(df.loc[i, "Date"])
    
    #print(df2)

     #Save Prediction into a CSV file

    df2.to_csv(cwd+'/SortDate/Profitability.csv',sep=',', encoding='utf-8')


    print("csv file successfully generated")
    sys.exit("successfully executed")