import pandas as pd
import numpy as np
import yfinance as yf
import math
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sys

# start date should be within 5 years of current date according to iex API we have used
# The more data we have, the better results we get!

# start = datetime(2019, 1, 1)
# end = date.today()

def get_historical(symbol):
    print(symbol)
    end = datetime.now()
    start = datetime(end.year-2,end.month,end.day)
    data = yf.download(symbol, start=start, end=end)
    df = pd.DataFrame(data=data)
    #df.reset_index(level=0, inplace=True)
    print(df)
    file_name = symbol + '.csv'
    print(file_name)
    df.to_csv(file_name)
    return

    # df['Day'] = df.index
    # prices = df[['Day', 'Close']]
    # #prices.reset_index(level=0, inplace=True)
    # #prices['Date'] = pd.to_datetime(prices['Date']).astype(int) // (10**9)
    # prices = prices.drop(['Date'], axis=1)
    # print(prices)

def LIN_REG_ALGO(df):
  #No of days to be forcasted in future
  forecast_out = int(7)
  #Price after n days
  df['Predicted_Price'] = df['Close'].shift(-forecast_out)
  #New df with only relevant data
  df_new=df[['Close','Predicted_Price']]
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
  X_test=X[int(0.2*len(df)):,:]
  y_train=y[0:int(0.8*len(df)),:]
  y_test=y[int(0.2*len(df)):,:]

  # Feature Scaling===Normalization
  #from sklearn.preprocessing import MinMaxScaler
  sc = MinMaxScaler()
  X_train = sc.fit_transform(X_train)
  X_test = sc.transform(X_test)
  X_to_be_forecasted=sc.transform(X_to_be_forecasted)

  #Training
  Line_Reg = LinearRegression(n_jobs=-1)
  Line_Reg.fit(X_train, y_train)

  #Testing
  y_test_pred=Line_Reg.predict(X_test)
  y_test_pred=y_test_pred*(1.04)

  # Test options and evaluation metric
  num_folds = 10
  seed = 7
  scoring = "r2"

  from sklearn.model_selection import cross_val_score, cross_val_predict
  from sklearn.model_selection import KFold
  kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
  predictions = cross_val_predict(Line_Reg, X_test, y_test, cv = kfold,scoring=scoring)

  import matplotlib.pyplot as plt
  fig = plt.figure(figsize=(24,12))
  plt.plot(y_test,label='Actual Price' )
  plt.plot(y_test_pred,label='Predicted Price')
  plt.legend(loc=4)
  plt.savefig('static/LR.png')
  plt.close(fig)

  from sklearn.metrics import mean_squared_error
  error_lr = math.sqrt(mean_squared_error(y_test, y_test_pred))

    
  #Forecasting
  forecast_set = Line_Reg.predict(X_to_be_forecasted)
  forecast_set=forecast_set*(1.04)
  mean=forecast_set.mean()
  lr_pred=forecast_set[0,0]
  print()
  print("##############################################################################")
  print("Tomorrow's ",symbols," Closing Price Prediction by Linear Regression: ",lr_pred)
  print("Linear Regression RMSE:",error_lr)
  print("##############################################################################")
  return df, lr_pred, forecast_set, mean, error_lr
    

    # prices = df.iloc[:, 0:3]
    # prices = prices.drop(['Open', 'High'], axis=1)
    # prices.reset_index(level=0, inplace=True)
    # print(prices)
    # prices["timestamp"] = prices["Date"].values.astype(float)
    # prices = prices.drop(['Date'], axis=1)

    # dataset = prices.values
    # X = dataset[:,1].reshape(-1,1)
    # print(X)
    # Y = dataset[:,0:1]
    # print(Y)

    # validation_size = 0.2
    # seed = 7

    # X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)

    # from sklearn.linear_model import LinearRegression
    # from sklearn.linear_model import Lasso
    # from sklearn.linear_model import ElasticNet
    # from sklearn.tree import DecisionTreeRegressor
    # from sklearn.neighbors import KNeighborsRegressor
    # from sklearn.svm import SVR

    # # Test options and evaluation metric
    # num_folds = 10
    # seed = 7
    # scoring = "r2"

    # # Spot-Check Algorithms
    # models = []
    # models.append((' LR ', LinearRegression()))
    # models.append((' LASSO ', Lasso()))
    # models.append((' EN ', ElasticNet()))
    # models.append((' KNN ', KNeighborsRegressor()))
    # models.append((' CART ', DecisionTreeRegressor()))
    # models.append((' SVR ', SVR()))

    # from sklearn.model_selection import KFold
    # from sklearn.model_selection import cross_val_score

    # # evaluate each model in turn
    # results = []
    # names = []
    # for name, model in models:
    #     kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
    #     cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    #     #print(cv_results)
    #     #results.append(cv_results)
    #     #names.append(name)
    #     msg = "%s: %f (%f)" % (model, cv_results.mean(), cv_results.std())
    #     print("***********************************" +msg)

    # # Future prediction, add dates here for which you want to predict
    # dates = ["2021-01-18", "2021-01-19", "2021-01-20", "2021-01-21", "2021-01-22"]
    # #convert to time stamp
    # for dt in dates:
    #     datetime_object = datetime.strptime(dt, "%Y-%m-%d")
    #     timestamp = datetime.timestamp(datetime_object)
    #     # to array X
    #     np.append(X, int(timestamp))

    # from matplotlib import pyplot as plt
    # from sklearn.metrics import mean_squared_error

    # # Define model
    # model = DecisionTreeRegressor()
    # # Fit to model
    # model.fit(X_train, Y_train)
    # # predict
    # predictions = model.predict(X)
    # print(mean_squared_error(Y, predictions))

    # # %matplotlib inline 
    # fig= plt.figure(figsize=(24,12))
    # plt.plot(X,Y)
    # plt.plot(X,predictions)
    # plt.show()

    # # GBR
    # from sklearn import ensemble
    # # Fit regression model
    # params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
    #         'learning_rate': 0.01, 'loss': 'ls'}
    # model = ensemble.GradientBoostingRegressor(**params)
    # model.fit(X_train, Y_train)

    # from sklearn.metrics import mean_squared_error, r2_score
    # model_score = model.score(X_train,Y_train)
    # # Have a look at R sq to give an idea of the fit ,
    # # Explained variance score: 1 is perfect prediction
    # print('R2 sq: ',model_score)
    # y_predicted = model.predict(X_validation)

    # # The mean squared error
    # print("Mean squared error: %.2f"% mean_squared_error(Y_validation, y_predicted))
    # # Explained variance score: 1 is perfect prediction
    # print('Test Variance score: %.2f' % r2_score(Y_validation, y_predicted))

    # return predictions
#Try-except to check if valid stock symbol
def insertintotable(symbol):
    try:
        get_historical(symbol)
    except:
        return "hello"
    else:
        #************** PREPROCESSUNG ***********************
            df = pd.read_csv(''+symbol+'.csv')
            #print()
            print("##############################################################################")
            print("Today's",symbol,"Stock Data: ")
            today_stock=df.iloc[-1:]
            print(today_stock)
            print("##############################################################################")
            print()
            df = df.dropna()
            code_list=[]
            for i in range(0,len(df)):
                code_list.append(symbol)
            df2=pd.DataFrame(code_list,columns=['Ticker'])
            df2 = pd.concat([df2, df], axis=1)
            df=df2
            df, lr_pred, forecast_set,mean,error_lr=LIN_REG_ALGO(df)
            print()
            #df['lr_pred']
            #df.to_csv(''+symbol+'.csv')
            print(df, lr_pred, forecast_set,mean,error_lr)
            #print(lr_pred)