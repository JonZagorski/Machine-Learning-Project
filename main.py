import models
import features
import sys

symbols = sys.argv[1:] #loads symbols from the command line.
for symbol in symbols: #runs the models on every symbol.
    df = features.loadDataset(symbol)
    scores_models =  models.train(df)
    print(f"Scores of models on the dataset {symbol} (Linear, Poly, RBF, Sigmoid, RFC, AdaBoost, VotingClassifier): {[score * 100 for score in scores_models]}")