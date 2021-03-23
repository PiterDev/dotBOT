from flask import Flask
from threading import Thread

stuff = ['sans granie', 'sans gaming', 'snas', 'wig snas', 'sans danaganronpa' ]




app = Flask('')

@app.route('/')
def home():
    return 'Nice, you found the website'

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()