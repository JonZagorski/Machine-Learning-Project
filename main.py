# import models
# import models2
# import features
# import output
# import finance
# import plot 
import model_picking
import pandas as pd


symbols = ['WMB','PSX', 'FANG', 'COP', 'XEC', 'PXD', 'EPD', 'GLNG', 'NOG', 'DVN']


for symbol in symbols: #runs the models on every symbol.
    model_picking.get_historical(symbol)

    # #run get_historical to get data on each ticker
    # finance.get_historical(symbol)

    # #load dataset in as a dataframe
    # df = features.loadDataset(symbol)

    # #train the dataframe using train_test split and run the dataframe through
    # #the Decision Tree Regressor
    # model_prediction =  models.train(df)

    # #add ticker name to each dataframe
    # df["Ticker"] = symbol

    # # Converting the index as date
    # df.index = pd.to_datetime(df.index)

    # # Extracting hour & minute
    # df['hour'] = df.index.hour
    # df['minute'] = df.index.minute

    # #merge both dataframes with predictions and regular data
    # final_df = df.merge(model_prediction, on = ["Date"])

    # #output as CSV
    # final = output.output(final_df, symbol)
    # #plot.dataset_plot(df, symbol)

    # #connect dataframe to PostgreSQL
    # connection = output.pg_connection(final_df)