from flask import Flask
from flask import render_template
from main import main

app = Flask(__name__, template_folder='template')
user_names = ""
@app.route('/')
def hello_world():
    names = ["Alyssa_Milano", "annakhachiyan", "FINALLEVEL", "kanyewest", "realDonaldTrump"]
    return render_template('index.html', names=names)

@app.route("/submit/<user_1>/<user_2>",  methods=["GET", "POST"])
def left(user_1, user_2):
    print(f"user_1 {user_1}")
    print(f"user_2 {user_2}")

    print('generate tweets')
    main(user_1, user_2)
    return 'ok'

