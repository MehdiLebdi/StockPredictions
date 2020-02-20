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

#Get stock prices for past X days with quandl API

import os
import sys
import quandl
import datetime as dt
import pandas as pd
import numpy as np
import csv

cwd = os.getcwd()

quandl.ApiConfig.api_key = '******'

def get_data_quandl(stock_name):

    today=dt.date.today()
    X_days=dt.timedelta(days=190)
    Xdays_ago=today-X_days

    try:
        df = quandl.get("WIKI/"+stock_name, start_date=str(Xdays_ago), end_date=str(today))
    except:
        print('No Valid '+stock_name+' Stock Found\n')
    new_df=df.drop(['Ex-Dividend', 'Split Ratio','Adj. Open' ,'Adj. High', 'Adj. Low','Adj. Volume'], axis=1)
	
    return new_df

if __name__ == "__main__":
    stock_name = "AAPL"
    file_name=cwd+'/Data/quandl/'+stock_name+" data.csv"
    new_df=get_data_quandl(stock_name)
    new_df.to_csv(file_name, sep=',', encoding='utf-8')

    sys.exit('Quandl data generated successfully')