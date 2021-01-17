import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import psycopg2

from sqlalchemy.sql import select, func


def output(df, symbol):
    df.to_csv(''+symbol+'.csv')

## Create PostgreSQL RDS Database Connection

# def pg_connection(symbol):
#     conn_string = "postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres"
#     engine = create_engine(f'postgresql://{conn_string}')
#     #Check table names
#     engine.table_names()
#     import csv
#     with open(''+symbol+'.csv') as csvfile:
#         myCSVReader = csv.DictReader(csvfile)
#         #change names in placeholder to match names in csv file.
#         sql = """INSERT INTO ticker(date,open,high,low,close,adj_close,volume,high_low,pct_change,mdav5,ema5,macd,macd_signalline)
#             VALUES (%(date)s,%(open)s,%(high)s,%(low)s,%(close)s,%(adj_close)s,%(volume)s,%(high_low)s,%(pct_change)s,%(mdav5)s, %(ema5)s,%(macd)s,%(macd_signalline)s)"""
#         for row in myCSVReader:
#             #use row directly
#             engine.execute(sql, row)
#     pd.read_sql_query('select * from ticker', con=engine).head()



###################################################################################
def pg_connection(df):

    alchemyEngine   = create_engine("postgresql+psycopg2://postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres", pool_recycle=3600)

    # Connect to PostgreSQL server
    postgreSQLConnection = alchemyEngine.connect()
    postgreSQLTable = "tickers"

    try:
        df.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='replace')

    except ValueError as vx:

        print(vx)

    except Exception as ex:  

        print(ex)

    else:

        print("PostgreSQL Table %s has been created successfully."%postgreSQLTable)

    finally:

        postgreSQLConnection.close()