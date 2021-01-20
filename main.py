import models
import features
<<<<<<< HEAD
import sys
=======
>>>>>>> main
import output
import sys
import pandas as pd

symbols = sys.argv[1:] #loads symbols from the command line.
for symbol in symbols: #runs the models on every symbol.
    df = features.loadDataset(symbol)
    scores_models =  models.train(df)
    final = output.output(df, symbol)
    #connection = output.pg_connection(symbol)
    #print(f"Scores of models on the dataset {symbol} (Linear, Poly, RBF, Sigmoid, RFC, AdaBoost, VotingClassifier): {[score * 100 for score in scores_models]}")
