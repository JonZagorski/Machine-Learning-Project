import os
import json
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.sql import select, func
from datetime import date, datetime
from psycopg2.extras import RealDictCursor
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_object(os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#test

con = psycopg2.connect("postgresql://postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres")

cursor = con.cursor(cursor_factory=RealDictCursor)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/etl")
def etl():
    return render_template("etl.html")

@app.route("/api")
def api():
     #cursor.execute("select row_to_json(tickers)from  tickers") 
     #cursor.execute("select row_to_json(t)from (select * from tickers) t") 
     cursor.execute("select * from tickers")
     results = cursor.fetchall()
     
     return json.dumps(results, indent=4, sort_keys=True, default=str)
     
@app.route("/api/predictions")
def predictions():
    cursor.execute("select * from predictions")
    results = cursor.fetchall()
    return json.dumps(results, indent =4, sort_keys=True, default=str)

if __name__ == "__main__":
    app.run(debug=True)