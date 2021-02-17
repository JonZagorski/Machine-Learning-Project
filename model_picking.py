import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

# start date should be within 5 years of current date according to iex API we have used
# The more data we have, the better results we get!

def get_historical(symbol):
    end = datetime.now()
    start = datetime(end.year-1,end.month,end.day)
    data = yf.download(symbol, start=start, end=end)
    df = pd.DataFrame(data=data)
    df = df.rename(columns={"Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Adj Close":"adj_close","Volume":"volume"})
    df.to_csv(''+symbol+'.csv')
    print(df)

    #Split data into training set and test set
    dataset_train=df.iloc[0:int(0.8*len(df)),:]
    dataset_test=df.iloc[int(0.8*len(df)):,:]
    ############# NOTE #################
    #TO PREDICT STOCK PRICES OF NEXT N DAYS, STORE PREVIOUS N DAYS IN MEMORY WHILE TRAINING
    # HERE N=7
    ###dataset_train=pd.read_csv('Google_Stock_Price_Train.csv')
    training_set=df.iloc[:,4].values# 1:2, to store as numpy array else Series obj will be stored
    #select cols using above manner to select as float64 type, view in var explorer

    #Feature Scaling
    from sklearn.preprocessing import MinMaxScaler
    sc=MinMaxScaler(feature_range=(0,1))#Scaled values btween 0,1
    training_set_scaled=sc.fit_transform(training_set)
    #In scaling, fit_transform for training, transform for test
    
    #Creating data stucture with 7 timesteps and 1 output. 
    #7 timesteps meaning storing trends from 7 days before current day to predict 1 next output
    X_train=[]#memory with 7 days from day i
    y_train=[]#day i
    for i in range(7,len(training_set_scaled)):
        X_train.append(training_set_scaled[i-7:i,0])
        y_train.append(training_set_scaled[i,0])
    #Convert list to numpy arrays
    X_train=np.array(X_train)
    y_train=np.array(y_train)
    X_forecast=np.array(X_train[-1,1:])
    X_forecast=np.append(X_forecast,y_train[-1])
    #Reshaping: Adding 3rd dimension
    X_train=np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))#.shape 0=row,1=col
    X_forecast=np.reshape(X_forecast, (1,X_forecast.shape[0],1))
    #For X_train=np.reshape(no. of rows/samples, timesteps, no. of cols/features)
    
    #Building RNN
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import Dropout
    from keras.layers import LSTM
    
    #Initialise RNN
    regressor=Sequential()
    
    #Add first LSTM layer
    regressor.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1],1)))
    #units=no. of neurons in layer
    #input_shape=(timesteps,no. of cols/features)
    #return_seq=True for sending recc memory. For last layer, retrun_seq=False since end of the line
    regressor.add(Dropout(p=0.1))
    
    #Add 2nd LSTM layer
    regressor.add(LSTM(units=50,return_sequences=True))
    regressor.add(Dropout(p=0.1))
    
    #Add 3rd LSTM layer
    regressor.add(LSTM(units=50,return_sequences=True))
    regressor.add(Dropout(p=0.1))
    
    #Add 4th LSTM layer
    regressor.add(LSTM(units=50))
    regressor.add(Dropout(p=0.1))
    
    #Add o/p layer
    regressor.add(Dense(units=1))
    
    #Compile
    regressor.compile(optimizer='adam',loss='mean_squared_error')
    
    #Training
    regressor.fit(X_train,y_train,epochs=25,batch_size=32 )
    #For lstm, batch_size=power of 2
    
    #Testing
    ###dataset_test=pd.read_csv('Google_Stock_Price_Test.csv')
    real_stock_price=dataset_test.iloc[:,4:5].values
    
    #To predict, we need stock prices of 7 days before the test set
    #So combine train and test set to get the entire data set
    dataset_total=pd.concat((dataset_train['Close'],dataset_test['Close']),axis=0) 
    testing_set=dataset_total[ len(dataset_total) -len(dataset_test) -7: ].values
    testing_set=testing_set.reshape(-1,1)
    #-1=till last row, (-1,1)=>(80,1). otherwise only (80,0)
    
    #Feature scaling
    testing_set=sc.transform(testing_set)
    
    #Create data structure
    X_test=[]
    for i in range(7,len(testing_set)):
        X_test.append(testing_set[i-7:i,0])
        #Convert list to numpy arrays
    X_test=np.array(X_test)
    
    #Reshaping: Adding 3rd dimension
    X_test=np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    
    #Testing Prediction
    predicted_stock_price=regressor.predict(X_test)
    
    #Getting original prices back from scaled values
    predicted_stock_price=sc.inverse_transform(predicted_stock_price)
    fig = plt.figure(figsize=(7.2,4.8),dpi=65)
    plt.plot(real_stock_price,label='Actual Price')  
    plt.plot(predicted_stock_price,label='Predicted Price')
        
    plt.legend(loc=4)
    plt.savefig('static/LSTM.png')
    plt.close(fig)
    
    
    error_lstm = math.sqrt(mean_squared_error(real_stock_price, predicted_stock_price))
    
    
    #Forecasting Prediction
    forecasted_stock_price=regressor.predict(X_forecast)
    
    #Getting original prices back from scaled values
    forecasted_stock_price=sc.inverse_transform(forecasted_stock_price)
    
    lstm_pred=forecasted_stock_price[0,0]
    print()
    print("##############################################################################")
    print("Tomorrow's ",quote," Closing Price Prediction by LSTM: ",lstm_pred)
    print("LSTM RMSE:",error_lstm)
    print("##############################################################################")
    print()

    # prices = df.iloc[:, 0:4]
    # prices = prices.drop(['open', 'high', 'low'], axis=1)
    # prices.reset_index(level=0, inplace=True)
    #prices["timestamp"] = list(map(lambda x: datetime.strptime(x,'%d %m, %Y').strftime('%d/%m/%Y'), prices['Date']))
    #prices["timestamp"] = time.mktime(datetime.strptime(prices["Date"], "%d/%m/%Y").timetuple())
    #prices["timestamp"] = prices["Date"].astype(float)
    #prices = prices.drop(['Date'], axis=1)
    #print(prices.dtypes)

    # # shuffle the samples
    # prices = prices.sample(n = len(prices), random_state = 42)
    # prices = prices.reset_index(drop = True)
    # df_valid = prices.sample(frac = 0.2, random_state = 42)
    # df_train = prices.drop(df_valid.index)
    # #df_train.reshape(-1, 1)

    # X_train = df_train['Date'].values
    # X_valid = df_valid['Date'].values
    # y_train = df_train['close'].values
    # y_valid = df_valid['close'].values


    # print(f'Training shapes: {X_train.shape} {y_train.shape}')
    # print(f'Validation shapes: {X_valid.shape} {y_valid.shape}')

    # from sklearn.ensemble import RandomForestRegressor
    # rf=RandomForestRegressor(random_state = 42)
    # rf.fit(X_train, y_train)

    # print(rf.predict_proba(X_train)[:,1])
    # print(y_valid_preds = rf.predict_proba(X_valid)[:,1])

    # # Test options and evaluation metric

    # #Perform Grid-Search
    # gsc = GridSearchCV(
    #     estimator=RandomForestRegressor(),
    #     param_grid={
    #         'max_depth': range(3,7),
    #         'n_estimators': (10, 50, 100, 1000),
    #     },
    #     cv=5, scoring='neg_mean_squared_error', verbose=0, n_jobs=-1)

    # evaluate model


    # # Future prediction, add dates here for which you want to predict
    # dates = ["2021-01-25", "2021-01-26", "2021-01-27", "2021-01-28","2021-01-29"]
    # #convert to time stamp
    # for dt in dates:
    #     datetime_object = datetime.strptime(dt, "%Y-%m-%d")
    #     timestamp = datetime.timestamp(datetime_object)
    #     print(timestamp)
    #     # to array X
    #     np.append(X, int(timestamp))
    # #print(X)
        

    # from matplotlib import pyplot as plt
    # from sklearn.metrics import mean_squared_error

    # # Define model
    # model = DecisionTreeRegressor()
    # # Fit to model
    # model.fit(X_train, Y_train)
    # # predict
    # predictions = model.predict(X)
    # print(predictions)
    # df = pd.DataFrame(data=predictions)
    # df['Date'] = X
    # df['Actual Close Price'] = Y
    # #df[0] = Z
    # print(df)
    # # %matplotlib inline 
    # fig= plt.figure(figsize=(12,12))
    # plt.plot(X,Y)
    # plt.plot(X,predictions)
    # plt.show()
    # #print(type(predictions))
    # print(mean_squared_error(Y, predictions))

    # # GBR
    # from sklearn import ensemble
    # # Fit regression model
    # params = {'n_estimators': 150, 'max_depth': 4, 'min_samples_split': 2,
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
