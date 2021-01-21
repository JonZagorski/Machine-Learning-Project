<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import models
<<<<<<< HEAD
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
=======
import models2
import features
import output
import finance
import plot 
import sys
=======
=======
>>>>>>> origin/main
=======
>>>>>>> b1700c11035c0289beff651000a9e23d6ddaa8bc
=======
>>>>>>> origin/main
# import models
# import models2
# import features
# import output
# import finance
# import plot 
import model_picking
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/main
=======
>>>>>>> origin/main
=======
>>>>>>> b1700c11035c0289beff651000a9e23d6ddaa8bc
=======
>>>>>>> origin/main
import pandas as pd
import io


#symbols = ['WMB','PSX', 'FANG', 'COP', 'XEC', 'PXD', 'EPD', 'GLNG', 'NOG', 'DVN']

symbol = 'WMB'

model_picking.get_historical(symbol)

# for symbol in symbols: #runs the models on every symbol.

#     #run get_historical to get data on each ticker
#     finance.get_historical(symbol)

#     #load dataset in as a dataframe
#     df = features.loadDataset(symbol)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    final = output.output(df, symbol)
    #plot.dataset_plot(df, symbol)
    connection = output.pg_connection(df)
    #print(f"Scores of models on the dataset {symbol} (Linear, Poly, RBF, Sigmoid, RFC, AdaBoost, VotingClassifier): {[score * 100 for score in scores_models]}")
>>>>>>> origin/main
=======
=======
>>>>>>> origin/main
=======
>>>>>>> b1700c11035c0289beff651000a9e23d6ddaa8bc
=======
>>>>>>> origin/main
#     #train the dataframe using train_test split and run the dataframe through
#     #the Decision Tree Regressor
#     model_prediction =  models.train(df)

#     #add ticker name to each dataframe
#     df["Ticker"] = symbol

#     # Converting the index as date
#     df.index = pd.to_datetime(df.index)

#     # Extracting hour & minute
#     df['hour'] = df.index.hour
#     df['minute'] = df.index.minute

#     #merge both dataframes with predictions and regular data
#     final_df = df.merge(model_prediction, on = ["Date"])

#     #output as CSV
#     final = output.output(final_df, symbol)
#     #plot.dataset_plot(df, symbol)

#     #connect dataframe to PostgreSQL
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
#     connection = output.pg_connection(final_df)
>>>>>>> origin/main
=======
#     connection = output.pg_connection(final_df)
>>>>>>> origin/main
=======
#     connection = output.pg_connection(final_df)
>>>>>>> b1700c11035c0289beff651000a9e23d6ddaa8bc
=======
#     connection = output.pg_connection(final_df)
>>>>>>> origin/main
