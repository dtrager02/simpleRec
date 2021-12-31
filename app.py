from google.cloud import bigquery
from flask import Flask, session, render_template, Response, request, redirect
import pandas as pd
from utils import getRecs
statDir = './static/'
templateDir = './templates/'
# initialize a flask object
app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)

client = bigquery.Client()

@app.route('/<str:input>')
def index(input):
    global client
    table = getRecs(client,input)
    return render_template("test.html",table=table)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)