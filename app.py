import os
from flask import Flask, render_template
from .models import setup_db, Actor, Movie
from .auth.auth import AuthError 
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__,template_folder='./templates')
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Contro-Allow-Headers','Content-Type ,Authorization')
        response.headers.add('Access-Contro-Allow-Headers','GET, POST ,PATCH , DELETE ,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin' ,  'http://localhost:5000')
        return response 
    return app

app = create_app()

@app.route('/')
def get_greeting():
    greeting = "Hello" 
    return greeting

@app.route('/login', methods=['GET','POST'])
def index():
    return render_template("login.html")

@app.route('/home', methods=['GET','POST'])
def user_logged():
    return render_template("home.html")

if __name__ == '__main__':
    app.run()