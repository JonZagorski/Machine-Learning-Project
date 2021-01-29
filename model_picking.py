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

    prices = df.iloc[:, 0:4]
    prices = prices.drop(['open', 'high', 'low'], axis=1)
    prices.reset_index(level=0, inplace=True)
    #prices["timestamp"] = list(map(lambda x: datetime.strptime(x,'%d %m, %Y').strftime('%d/%m/%Y'), prices['Date']))
    #prices["timestamp"] = time.mktime(datetime.strptime(prices["Date"], "%d/%m/%Y").timetuple())
    #prices["timestamp"] = prices["Date"].astype(float)
    #prices = prices.drop(['Date'], axis=1)
    #print(prices.dtypes)

    # shuffle the samples
    prices = prices.sample(n = len(prices), random_state = 42)
    prices = prices.reset_index(drop = True)
    df_valid = prices.sample(frac = 0.2, random_state = 42)
    df_train = prices.drop(df_valid.index)
    #df_train.reshape(-1, 1)

    X_train = df_train['Date'].values
    X_valid = df_valid['Date'].values
    y_train = df_train['close'].values
    y_valid = df_valid['close'].values


    print(f'Training shapes: {X_train.shape} {y_train.shape}')
    print(f'Validation shapes: {X_valid.shape} {y_valid.shape}')

    from sklearn.ensemble import RandomForestRegressor
    rf=RandomForestRegressor(random_state = 42)
    rf.fit(X_train, y_train)

    print(rf.predict_proba(X_train)[:,1])
    print(y_valid_preds = rf.predict_proba(X_valid)[:,1])

    # Test options and evaluation metric

    #Perform Grid-Search
    gsc = GridSearchCV(
        estimator=RandomForestRegressor(),
        param_grid={
            'max_depth': range(3,7),
            'n_estimators': (10, 50, 100, 1000),
        },
        cv=5, scoring='neg_mean_squared_error', verbose=0, n_jobs=-1)

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
