import os

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.sql import select, func

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_object(os.environ['DATABASE_URL']
db = SQLAlchemy(app)





con = psycopg2.connect("postgresql://postgres:jh0njr&p3nny@database-1.c84rdrfagztk.us-east-1.rds.amazonaws.com/postgres")

cursor = con.cursor()
#test 
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/etl")
def etl():
    return render_template("etl.html")

@app.route("/api", methods=['GET'])
def api():
     cursor.execute("select array_to_json(array_agg(row_to_json(t))) from (select * from tickers) t")
     result = cursor.fetchall()
     return jsonify(result)




if __name__ == "__main__":
    app.run(debug=True)