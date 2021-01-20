import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import psycopg2

from sqlalchemy.sql import select, func


def output(df, symbol):
    df.to_csv(''+symbol+'.csv')


###################################################################################
def pg_connection(df):

    alchemyEngine   = create_engine("postgresql+psycopg2://postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres", pool_recycle=3600)

    # Connect to PostgreSQL server
    postgreSQLConnection = alchemyEngine.connect()
    postgreSQLTable = "tickers"

    try:
        df.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='append')

    except ValueError as vx:

        print(vx)

    except Exception as ex:  

        print(ex)

    else:

        print("PostgreSQL Table %s has been created successfully."%postgreSQLTable)

    finally:

        postgreSQLConnection.close()