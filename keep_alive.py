from flask import Flask
from threading import Thread
from flask_cors import CORS


app = Flask('')
CORS(app)

@app.route("/")
def home():
    return "nhk bot 1 is running !"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    Thread(target=run).start()

