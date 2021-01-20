from numpy.lib.function_base import insert
import pandas as pd
import numpy as np
from pandas import datetime
import math
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt
import yfinance as yf
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
import sys

#quote = ['WMB','PSX', 'FANG', 'COP', 'XEC', 'PXD', 'EPD', 'GLNG', 'NOG', 'DVN']
print("##############")
print("###########") 
def get_historical(ticker):
    end = datetime.now()
    start = datetime(end.year-2,end.month,end.day)
    data = yf.download(ticker, start=start, end=end)
    df = pd.DataFrame(data=data)

    df = df.rename(columns={"Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Adj Close":"adj_close","Volume":"volume"})
    df.to_csv(''+ticker+'.csv')
    #print(df)
    # if(df.empty):
    #     print("Hello")
    #     from alpha_vantage.timeseries import TimeSeries
    #     ts = TimeSeries(key='I8LY0JP5DQ4DECI9',output_format='pandas')
    #     data, meta_data = ts.get_daily_adjusted(symbol='NSE:'+ticker, outputsize='full')
    #     #Format df
    #     #Last 2 yrs rows => 502, in ascending order => ::-1
    #     data=data.head(503).iloc[::-1]
    #     data=data.reset_index()
    #     #Keep Required cols only
    #     df=pd.DataFrame()
    #     print(df)
    #     df['Date']=data['Date']
    #     df['Open']=data['Open']
    #     df['High']=data['High']
    #     df['Low']=data['Low']
    #     df['Close']=data['Close']
    #     df['hello']=data['Adj Close']
    #     df['Volume']=data['Volume']
    #     df.to_csv(''+ticker+'.csv',index=False)
    # else:
    #     print("exit")
    return

# def LIN_REG_ALGO(df):
#         #No of days to be forcasted in future
#         forecast_out = int(7)
#         #Price after n days
#         df['Close after 7 days'] = df['close'].shift(-forecast_out)
#         #New df with only relevant data
#         df_new=df[['close','Close after 7 days']] 

#         #Structure data for train, test & forecast
#         #lables of known data, discard last 35 rows
#         y =np.array(df_new.iloc[:-forecast_out,-1])
#         y=np.reshape(y, (-1,1))
#         #all cols of known data except lables, discard last 35 rows
#         X=np.array(df_new.iloc[:-forecast_out,0:-1])
#         #Unknown, X to be forecasted
#         X_to_be_forecasted=np.array(df_new.iloc[-forecast_out:,0:-1])
        
#         #Traning, testing to plot graphs, check accuracy
#         X_train=X[0:int(0.8*len(df)),:]
#         X_test=X[int(0.2*len(df)):,:]
#         y_train=y[0:int(0.8*len(df)),:]
#         y_test=y[int(0.2*len(df)):,:]
        
#         # Feature Scaling===Normalization
#         #from sklearn.preprocessing import MinMaxScaler
#         sc = MinMaxScaler()
#         X_train = sc.fit_transform(X_train)
#         X_test = sc.transform(X_test)
        
#         X_to_be_forecasted=sc.transform(X_to_be_forecasted)
        
#         #Training
#         clf = DecisionTreeRegressor()
#         clf.fit(X_train, y_train)
      
#         #Testing
#         y_test_pred=clf.predict(X_test)
#         y_test_pred=y_test_pred*(1.04)

#         from sklearn.model_selection import cross_val_score, cross_val_predict
#         from sklearn import metrics
#         predictions = cross_val_predict(clf, X_test, y_test, cv = 5)
#         accuracy = metrics.r2_score(y_test, predictions)
        
#         import matplotlib.pyplot as plt2
#         fig = plt2.figure(figsize=(7.2,4.8),dpi=65)
#         plt2.plot(y_test,label='Actual Price' )
#         plt2.plot(y_test_pred,label='Predicted Price')
        
#         plt2.legend(loc=4)
#         plt2.savefig('static/LR.png')
#         plt2.close(fig)
        
#         error_lr = math.sqrt(mean_squared_error(y_test, y_test_pred))
#         # # Accuracy
#         # from sklearn.metrics import accuracy_score
#         # accuracy = accuracy_score(y_test,y_test_pred)
#         # print("Accuracy " +accuracy)
#         #Forecasting
#         forecast_set = clf.predict(X_to_be_forecasted)
#         forecast_set=forecast_set*(1.04)
#         print(forecast_set)
#         mean=forecast_set.mean()
#         lr_pred=forecast_set[0,0]
#         print()
#         print("##############################################################################")
#         #print("Tomorrow's ",symbols," Closing Price Prediction by Linear Regression: ",lr_pred)
#         print("Linear Regression RMSE:",error_lr)
#         print("##############################################################################")
#         print("Accuracy " +str(accuracy))
#         print()
#         return df, lr_pred, forecast_set, mean, error_lr


# #Try-except to check if valid stock symbol
# def insertintotable(symbol):
#     try:
#         get_historical(symbol)
#     except:
#         return "hello"
#     else:
#         #************** PREPROCESSUNG ***********************
#             df = pd.read_csv(''+symbol+'.csv')
#             #print()
#             print("##############################################################################")
#             print("Today's",symbol,"Stock Data: ")
#             today_stock=df.iloc[-1:]
#             print(today_stock)
#             print("##############################################################################")
#             print()
#             df = df.dropna()
#             code_list=[]
#             for i in range(0,len(df)):
#                 code_list.append(symbol)
#             df2=pd.DataFrame(code_list,columns=['Ticker'])
#             df2 = pd.concat([df2, df], axis=1)
#             df=df2
#             #df, lr_pred, forecast_set,mean,error_lr=LIN_REG_ALGO(df)
#             #print()
#             #df['lr_pred']
#             #df.to_csv(''+symbol+'.csv')
#             #print(df, lr_pred, forecast_set,mean,error_lr)
#             #print(lr_pred)