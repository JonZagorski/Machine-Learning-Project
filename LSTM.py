#Dependencies
import math
import numpy as np
import pandas_datareader as web
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import psycopg2
from sqlalchemy.sql import select, func

symbols = ['WMB','PSX', 'FANG', 'COP', 'XEC', 'PXD', 'EPD', 'GLNG', 'NOG', 'DVN']

for symbol in symbols:

    df = web.DataReader(symbol, data_source = 'yahoo', start = '2012-01-01', end= '2021-2-11')

    #Get the number of rows and columns in dataset
    #df.shape

    #Visualize the closing price history 
    # plt.figure(figsize=(16,8))
    # plt.title('Close Price History')
    # plt.plot(df['Close'])
    # plt.xlabel('Date', fontsize =18)
    # plt.ylabel('Close Price USD ($)', fontsize=18)
    # plt.show()

    #Create a new dataframe with only the close column
    data = df.filter(['Close'])

    #Convert the dataframe to numpy array
    dataset = data.values

    #Compute the number of rows to train the model on
    training_data_len = math.ceil(len(dataset) * .8)
    print(training_data_len)
    #Scale the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    print(scaled_data)

    #Create the training dataset

    #Create the scaled training dataset
    train_data = scaled_data[0:training_data_len, :]
    #Split the data into x_train and y_train datasets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        if i<= 60:
            print(x_train)
            print(y_train)
            print()

    #convert the x_train and y_train dataset to numpy arrays to train LSTM model
    x_train, y_train = np.array(x_train), np.array(y_train)

    #reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train.shape

    #build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    #compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    #train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    #Create the testing dataset 
    #create a new array containing scaled values from index 1774 to 2292 
    test_data = scaled_data[training_data_len - 60: , :]
    #Create the datasets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])
    
    #convert the data to a numpy array
    x_test = np.array(x_test)

    #reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    #get the models predicted price values for x_test dataset
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    #get the root mean squared error (RMSE)
    rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
    print(rmse)

    #plot the data 
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    valid['Ticker'] = symbol
    # #visualize the data
    # plt.figure(figsize=(16,8))
    # plt.title('Model')
    # plt.xlabel('Date', fontsize = 18)
    # plt.ylabel('Close Price USD ($)', fontsize=18)
    # plt.plot(train['Close'])
    # plt.plot(valid[['Close', 'Predictions']])
    # plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    # plt.show()

    print(valid)

    #get the quote 
    price_quote = web.DataReader(symbol, data_source='yahoo', start='2012-01-01', end='2021-02-11')
    #create a new dataframe 
    new_df = price_quote.filter(['Close'])
    #get the last 60 day closing price values and convert the df to an array
    last_60_days = new_df[-60:].values
    #scale the data to be values between 0 and 1
    last_60_days_scaled = scaler.transform(last_60_days)
    #create an empty list
    X_test = []
    #append the last 60 days to X_test list
    X_test.append(last_60_days_scaled)
    #Convert the X_test dataset to a numpy array
    X_test = np.array(X_test)
    #reshape the data 
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    
    #Get the predicted scaled price
    pred_price = model.predict(X_test)
    #undo the scaling
    pred_price = scaler.inverse_transform(pred_price)
    print(pred_price)

    price_quote_2 = web.DataReader(symbol, data_source='yahoo', start='2021-02-12', end='2021-02-12')
    print(price_quote_2['Close'])

    # alchemyEngine   = create_engine("postgresql+psycopg2://postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres", pool_recycle=3600)

    # # Connect to PostgreSQL server
    # postgreSQLConnection = alchemyEngine.connect()
    # postgreSQLTable = "LSTM_predictions"

    # try:
    #     valid.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='append')

    # except ValueError as vx:

    #     print(vx)

    # except Exception as ex:  

    #     print(ex)

    # else:

    #     print("PostgreSQL Table %s has been created successfully."%postgreSQLTable)

    # finally:

    #     postgreSQLConnection.close()