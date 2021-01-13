import pandas as pd
from sqlalchemy import create_engine

def output(df, symbol):
    df.to_csv(''+symbol+'.csv')

## Create PostgreSQL RDS Database Connection

def pg_connection(csv):
    conn_string = "postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres"
    engine = create_engine(f'postgresql://{conn_string}')
    #Check table names
    engine.table_names()
    import csv
    with open(csv) as csvfile:
        myCSVReader = csv.DictReader(csvfile)
        #change names in placeholder to match names in csv file.
        sql = """INSERT INTO postgres(index,type,coordinates,state,total_votes20,votes20_Donald_Trump,votes20_Joe_Biden,cases,deaths,TotalPop,VotingAgeCitizen,Men,Women,Hispanic,White,Black,Native,Asian,Pacific,Biden,Trump,Republican,Democrat,hispanic_pop,white_pop,black_pop,native_pop,asian_pop,pacific_pop,cases_per_100k,deaths_per_100k
    )
            VALUES (%(index)s,%(type)s,%(coordinates)s,%(state)s,%(total_votes20)s,%(votes20_Donald_Trump)s,%(votes20_Joe_Biden)s,%(cases)s,%(deaths)s,%(TotalPop)s, %(VotingAgeCitizen)s,%(Men)s,%(Women)s, %(Hispanic)s,%(White)s,%(Black)s, %(Native)s,%(Asian)s,%(Pacific)s, %(Biden)s,%(Trump)s,%(Republican)s, %(Democrat)s,%(hispanic_pop)s,%(white_pop)s, %(black_pop)s,%(native_pop)s,%(asian_pop)s, %(pacific_pop)s,%(cases_per_100k)s,%(deaths_per_100k)s)"""
        for row in myCSVReader:
            #use row directly
            engine.execute(sql, row)
    pd.read_sql_query('select * from state', con=engine).head()