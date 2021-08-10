from flask import Flask, session, render_template, Response, request, redirect
from flask_cors import CORS, cross_origin
from datetime import timedelta
import sqlite3
import random
import itertools
import utils
statDir = './static/'
templateDir = './templates/'
# initialize a flask object
app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)

app.config['SECRET_KEY'] = 'abcd12345'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

@app.route('/')
def index():
    return render_template("home.html")

@app.route("/start",methods =['POST','GET'])
def start():
    if request.method == 'POST':
        con = sqlite3.connect('./animeInfo.sqlite3')
        cur = con.cursor()
        print(request.form['diff'] + " " + request.form['num'])
        if not(request.form['diff'] in {"easy","medium","hard"}) or not utils.RepresentsInt(request.form['num']):
            print("bad form")
            print(type(request.form['num']) is int)
            return redirect('/')
        session['game_data'] = utils.queryProcessing(cur,request.form['num'],request.form['diff'])
        session.modified = True
        print(session.get('game_data'))
        return render_template('game.html')
    else:
        return {'data':session.get('game_data')}

@app.route("/roundData",methods=["GET","POST"])
def roundData():
    if request.method == 'POST':
        pass

@app.route("/autocomplete/<term>")
def autocomplete(term):
    con = sqlite3.connect('./animeInfo.sqlite3')
    cur = con.cursor()
    return utils.autocomplete(cur,term)
    
@app.route("/highScore/<int:score>")
def highScore(score):
    if score > session.get('highScore',0):
        session['highScore'] = 0
    return session.get('highScore',0)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)