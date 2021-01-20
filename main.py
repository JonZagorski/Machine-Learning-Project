import models
import models2
import features
import output
import finance
import plot 
import pandas as pd


symbols = ['WMB','PSX', 'FANG', 'COP', 'XEC', 'PXD', 'EPD', 'GLNG', 'NOG', 'DVN']

#symbol = 'WMB'

#models2.get_historical(symbol)


#symbols = sys.argv[1:] #loads symbols from the command line.
for symbol in symbols: #runs the models on every symbol.
    #models2.get_historical(symbol)
    #print(score)
    finance.get_historical(symbol)
    df = features.loadDataset(symbol)
    model_prediction =  models.train(df)
    df["Ticker"] = symbol
    # Converting the index as date
    df.index = pd.to_datetime(df.index)

    # Extracting hour & minute
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute

    final_df = df.merge(model_prediction, on = ["Date"])
    final = output.output(final_df, symbol)
    #plot.dataset_plot(df, symbol)
    connection = output.pg_connection(final_df)
    #print(f"Scores of models on the dataset {symbol} (Linear, Poly, RBF, Sigmoid, RFC, AdaBoost, VotingClassifier): {[score * 100 for score in scores_models]}")