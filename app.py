import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "appointment_scheduler"
app.config["MONGO_URI"] = "mongodb+srv://philiph80:delrod123@myfirstcluster-yuvii.mongodb.net/appointment_scheduler?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
