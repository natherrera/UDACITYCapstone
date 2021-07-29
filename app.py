import os
from flask import Flask, render_template, jsonify 
from .models import setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth 
from flask_cors import CORS
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound

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

#----------------------------------------------------------------------------#
# /actors API
#----------------------------------------------------------------------------#

@app.route('/actors', methods=['GET'])
@requires_auth('view:actors')
def get_actors(payload):
    try:
        actors_list = Actor.query.all()
        actors = [actor.format() for actor in actors_list]
        if len(actors) == 0:
            return NotFound()
        else:
            response = {
            'success': True,
            'status_code': 200,
            'actors' : actors ,
            }
            return jsonify(response)
    except Exception:
        raise Unauthorized()

#----------------------------------------------------------------------------#
# /movies API
#----------------------------------------------------------------------------#

@app.route('/movies', methods=['GET'])
@requires_auth('view:movies')
def get_movies(payload):
    try:
        movies_list = Movie.query.all()
        movies = [movie.format() for movie in movies_list]
        if len(movies) == 0:
            return NotFound()
        else:
            response = {
            'success': True,
            'status_code': 200,
            'movies' : movies ,
            }
            return jsonify(response)
    except Exception:
        raise Unauthorized()

if __name__ == '__main__':
    app.run()