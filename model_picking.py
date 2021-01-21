import pandas as pd
import numpy as np
import yfinance as yf
import math
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# start date should be within 5 years of current date according to iex API we have used
# The more data we have, the better results we get!

def get_historical(symbol):
    end = datetime.now()
    start = datetime(end.year-2,end.month,end.day)
    data = yf.download(symbol, start=start, end=end)
    df = pd.DataFrame(data=data)
    df = df.rename(columns={"Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Adj Close":"adj_close","Volume":"volume"})
    df.to_csv(''+symbol+'.csv')
    print(df)

    prices = df.iloc[:, 0:4]
    prices = prices.drop(['open', 'high', 'low'], axis=1)
    prices.reset_index(level=0, inplace=True)
    prices["timestamp"] = prices["Date"].values.astype(float)
    prices = prices.drop(['Date'], axis=1)
    print(prices)


    dataset = prices.values
    X = dataset[:,1].reshape(-1,1)
    #print(X)
    Y = dataset[:,0:1]
    #print(Y)
    #print(dataset)

    validation_size = 0.2
    seed = 7

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)

    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Lasso
    from sklearn.linear_model import ElasticNet
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.svm import SVR

    # Test options and evaluation metric
    num_folds = 10
    seed = 7
    scoring = "r2"

    # Spot-Check Algorithms
    models = []
    models.append((' LR ', LinearRegression()))
    models.append((' LASSO ', Lasso()))
    models.append((' EN ', ElasticNet()))
    models.append((' KNN ', KNeighborsRegressor()))
    models.append((' CART ', DecisionTreeRegressor()))
    models.append((' SVR ', SVR()))

    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_score

    def Average(lst): 
        return sum(lst) / len(lst)

    # evaluate each model in turn
    averages = []
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        #print(cv_results)
        results.append(cv_results)
        names.append(name)
    for result in results:
        averages.append(Average(result))
    print(names)
    print(averages)

    
    # Future prediction, add dates here for which you want to predict
    dates = ["2021-01-22", "2021-01-25", "2021-01-26", "2021-01-27", "2021-01-28"]
    #convert to time stamp
    for dt in dates:
        datetime_object = datetime.strptime(dt, "%Y-%m-%d")
        timestamp = datetime.timestamp(datetime_object)
        # to array X
        np.append(X, int(timestamp))

    from matplotlib import pyplot as plt
    from sklearn.metrics import mean_squared_error

    # Define model
    model = DecisionTreeRegressor()
    # Fit to model
    model.fit(X_train, Y_train)
    # predict
    predictions = model.predict(X)
    df = pd.DataFrame(data=predictions)
    df['Date'] = X
    df['Actual Close Price'] = Y
    print(df)
    # %matplotlib inline 
    fig= plt.figure(figsize=(12,12))
    plt.plot(X,Y)
    plt.plot(X,predictions)
    plt.show()
    #print(type(predictions))
    print(mean_squared_error(Y, predictions))

    # GBR
    from sklearn import ensemble
    # Fit regression model
    params = {'n_estimators': 150, 'max_depth': 4, 'min_samples_split': 2,
            'learning_rate': 0.01, 'loss': 'ls'}
    model = ensemble.GradientBoostingRegressor(**params)
    model.fit(X_train, Y_train)

    from sklearn.metrics import mean_squared_error, r2_score
    model_score = model.score(X_train,Y_train)
    # Have a look at R sq to give an idea of the fit ,
    # Explained variance score: 1 is perfect prediction
    print('R2 sq: ',model_score)
    y_predicted = model.predict(X_validation)

    # The mean squared error
    print("Mean squared error: %.2f"% mean_squared_error(Y_validation, y_predicted))
    # Explained variance score: 1 is perfect prediction
    print('Test Variance score: %.2f' % r2_score(Y_validation, y_predicted))

    return predictions
