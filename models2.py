import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, date

# start date should be within 5 years of current date according to iex API we have used
# The more data we have, the better results we get!

start = datetime(2019, 1, 1)
end = date.today()

def get_historical(symbol):
    end = datetime.now()
    start = datetime(end.year-2,end.month,end.day)
    data = yf.download(symbol, start=start, end=end)
    df = pd.DataFrame(data=data)
    print(df)
    from sklearn.model_selection import train_test_split

    # df['Day'] = df.index
    # prices = df[['Day', 'Close']]
    # #prices.reset_index(level=0, inplace=True)
    # #prices['Date'] = pd.to_datetime(prices['Date']).astype(int) // (10**9)
    # prices = prices.drop(['Date'], axis=1)
    # print(prices)

    prices = df.iloc[:, 0:3]
    prices = prices.drop(['Open', 'High'], axis=1)
    prices.reset_index(level=0, inplace=True)
    print(prices)
    prices["timestamp"] = prices["Date"].values.astype(float)
    prices = prices.drop(['Date'], axis=1)

    dataset = prices.values
    X = dataset[:,1].reshape(-1,1)
    print(X)
    Y = dataset[:,0:1]
    print(Y)

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

    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        #print(cv_results)
        results.append(cv_results)
        names.append(name)
    msg = "%s: %f (%f)" % (names, results.mean(), results.std())
    print(msg)

    # Future prediction, add dates here for which you want to predict
    dates = ["2021-01-18", "2021-01-19", "2021-01-20", "2021-01-21", "2021-01-22"]
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
    print(mean_squared_error(Y, predictions))

    # %matplotlib inline 
    fig= plt.figure(figsize=(24,12))
    plt.plot(X,Y)
    plt.plot(X,predictions)
    plt.show()

    # GBR
    from sklearn import ensemble
    # Fit regression model
    params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
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