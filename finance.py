from flask import Flask, render_template, request, flash, redirect, url_for
from numpy.lib.function_base import insert
import pandas as pd
import numpy as np
from pandas import datetime
import math, random
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt
import yfinance as yf
from sklearn.linear_model import LinearRegression

data = "WMB"

import sys

data = 'VLO'
print("##############")
print(data)
print("###########") 
def get_historical(quote):
    end = datetime.now()
    start = datetime(end.year-2,end.month,end.day)
    data = yf.download(quote, start=start, end=end)
    print(data)
    df = pd.DataFrame(data=data)
    df.to_csv(''+quote+'.csv')
    if(df.empty):
        from alpha_vantage.timeseries import TimeSeries
        ts = TimeSeries(key='I8LY0JP5DQ4DECI9',output_format='pandas')
        data, meta_data = ts.get_daily_adjusted(symbol='NSE:'+quote, outputsize='full')
        #Format df
        #Last 2 yrs rows => 502, in ascending order => ::-1
        data=data.head(503).iloc[::-1]
        data=data.reset_index()
        #Keep Required cols only
        df=pd.DataFrame()
        df['Date']=data['date']
        df['Open']=data['1. open']
        df['High']=data['2. high']
        df['Low']=data['3. low']
        df['Close']=data['4. close']
        df['Adj Close']=data['5. adjusted close']
        df['Volume']=data['6. volume']
        df.to_csv(''+quote+'.csv',index=False)
    return

def LIN_REG_ALGO(df):
        #No of days to be forcasted in future
        forecast_out = int(7)
        #Price after n days
        df['Close after n days'] = df['Close'].shift(-forecast_out)
        #New df with only relevant data
        df_new=df[['Close','Close after n days']]

        #Structure data for train, test & forecast
        #lables of known data, discard last 35 rows
        y =np.array(df_new.iloc[:-forecast_out,-1])
        y=np.reshape(y, (-1,1))
        #all cols of known data except lables, discard last 35 rows
        X=np.array(df_new.iloc[:-forecast_out,0:-1])
        #Unknown, X to be forecasted
        X_to_be_forecasted=np.array(df_new.iloc[-forecast_out:,0:-1])
        
        #Traning, testing to plot graphs, check accuracy
        X_train=X[0:int(0.8*len(df)),:]
        X_test=X[int(0.8*len(df)):,:]
        y_train=y[0:int(0.8*len(df)),:]
        y_test=y[int(0.8*len(df)):,:]
        
        # Feature Scaling===Normalization
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        
        X_to_be_forecasted=sc.transform(X_to_be_forecasted)
        
        #Training
        clf = LinearRegression(n_jobs=-1)
        clf.fit(X_train, y_train)
        
        #Testing
        y_test_pred=clf.predict(X_test)
        y_test_pred=y_test_pred*(1.04)
        import matplotlib.pyplot as plt2
        fig = plt2.figure(figsize=(7.2,4.8),dpi=65)
        plt2.plot(y_test,label='Actual Price' )
        plt2.plot(y_test_pred,label='Predicted Price')
        
        plt2.legend(loc=4)
        plt2.savefig('static/LR.png')
        plt2.close(fig)
        
        error_lr = math.sqrt(mean_squared_error(y_test, y_test_pred))
        
        
        #Forecasting
        forecast_set = clf.predict(X_to_be_forecasted)
        forecast_set=forecast_set*(1.04)
        mean=forecast_set.mean()
        lr_pred=forecast_set[0,0]
        print()
        print("##############################################################################")
        print("Tomorrow's ",quote," Closing Price Prediction by Linear Regression: ",lr_pred)
        print("Linear Regression RMSE:",error_lr)
        print("##############################################################################")
        print()
        return df, lr_pred, forecast_set, mean, error_lr


# ******MOVING AVERAGES*******#
#The variables we will be using at this stage, 
# are the moving averages for the past three and nine days.
#data['MA3'] = data['Value'].shift(1).rolling(window=3).mean()
#data['MA9']= data['Value'].shift(1).rolling(window=9).mean()


#Try-except to check if valid stock symbol
def insertintotable():

    try:
        get_historical(data)
    except:
        return "hello"
    else:
    
        #************** PREPROCESSUNG ***********************
        df = pd.read_csv(''+data+'.csv')
        print()
        print("##############################################################################")
        print("Today's",data,"Stock Data: ")
        today_stock=df.iloc[-1:]
        print(today_stock)
        print("##############################################################################")
        print()
        df = df.dropna()
        code_list=[]
        for i in range(0,len(df)):
            code_list.append(data)
        df2=pd.DataFrame(code_list,columns=['Code'])
        df2 = pd.concat([df2, df], axis=1)
        df=df2

insertintotable()