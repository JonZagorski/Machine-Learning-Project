import models
import models2
import features
import output
import finance
import sys
import pandas as pd

#symbols = ['WMB','PSX', 'FANG', 'COP', 'XEC', 'PXD', 'EPD', 'GLNG', 'NOG', 'DVN']

symbols = sys.argv[1:] #loads symbols from the command line.
for symbol in symbols: #runs the models on every symbol.
    models2.get_historical(symbols)
    #print(score)
    #linreg = finance.insertintotable(symbol)
    #df = features.loadDataset(symbol)
    #scores_models =  models.train(df)
    #final = output.output(df, symbol)
    #connection = output.pg_connection(df)
    #print(f"Scores of models on the dataset {symbol} (Linear, Poly, RBF, Sigmoid, RFC, AdaBoost, VotingClassifier): {[score * 100 for score in scores_models]}")