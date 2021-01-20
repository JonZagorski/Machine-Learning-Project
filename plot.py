import numpy as np
import matplotlib.pyplot as plt

def dataset_plot(df, symbol):
    x = df.index
<<<<<<< HEAD
    y = df.loc[:, 'Adj Close']
    plt.plot(x, y)
    plt.xlabel('Dates')
    plt.ylabel('Adj Close')
=======
>>>>>>> origin/main
    y = df.loc[:, 'adj_close']
    plt.plot(x, y)
    plt.xlabel('dates')
    plt.ylabel('adj_close')
    plt.title(f'Adj Close Price trend for {symbol}')
    plt.show()

def feature_plot(df):
    x = df.index
<<<<<<< HEAD
    y_mdav5 = df.loc[:, 'MDAV5']
    y_macd = df.loc[:, 'MACD']
    y_macd_sline = df.loc[:, 'MACD_SignalLine']

    plt.subplot(3,1,1)
    plt.plot(x, y_mdav5)
    plt.title('MDAV5')

    plt.subplot(3,1,2)
    plt.plot(x, y_macd)
    plt.title('MACD')
=======
>>>>>>> origin/main
    y_mdav5 = df.loc[:, 'mdav5']
    y_macd = df.loc[:, 'macd']
    y_macd_sline = df.loc[:, 'macd_signalline']

    plt.subplot(3,1,1)
    plt.plot(x, y_mdav5)
    plt.title('mdav5')

    plt.subplot(3,1,2)
    plt.plot(x, y_macd)
    plt.title('macd')

    plt.subplot(3,1,3)
    plt.plot(x, y_macd_sline)

    plt.title('MACD_SignalLine')
    plt.show()