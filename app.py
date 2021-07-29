import os
from flask import Flask, render_template, jsonify, request
from sqlalchemy.sql.operators import exists 
from .models import setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth 
from flask_cors import CORS
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound 

def create_app(test_config=None):
    app = Flask(__name__,template_folder='./templates')
    CORS(app)
    setup_db(app)
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

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def insert_actor(self): 
    try:
        body = request.get_json()
        actor = Actor()
        actor.name= body['name']
        actor.gender= body['gender']
        actor.insert()
        response = {
                'success': True,
                'status_code': 200,
                'actor' : actor.format()
                }
        return jsonify(response)
    except Exception:
        raise Unauthorized()

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('updated:actors')
def update_actor(id):
    try:
        actor = Actor.query.filter(Actor.id == id).first()
        if actor is None:
            return NotFound()
        body = request.get_json()
        actor = Actor()
        if body['name'] is not None:
            actor.name= body['name']

        if body['gender'] is not None:
            actor.gender= body['gender']
        actor.update()
        update_actor = Actor.query.filter(Actor.id == id).first()
        if update_actor is None:
            return NotFound()
        else:
            response = {
                    'success': True,
                    'status_code': 200,
                    'actor_updated' : update_actor.format()
                    }
            return jsonify(response)
    except Exception:
        raise Unauthorized()

@app.route('/actor/<int:id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(id):
    try:
        selected_actor=Actor.query.get(id)
        if selected_actor is None:
            return NotFound()
        selected_actor.delete()

        response = {
                'success': True,
                'status_code': 200,
                'deleted_actor_id' : id
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

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def insert_movies(self): 
    try:
        body = request.get_json()
        movie = Movie()
        movie.title= body['title']
        movie.release_date= body['release_date']
        movie.insert()
        response = {
                'success': True,
                'status_code': 200,
                'movie' : movie.format()
                }
        return jsonify(response)
    except Exception:
        raise Unauthorized()

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('updated:movies')
def update_movie(id):
    try:
        movie = Movie.query.filter(Movie.id == id).first()
        if movie is None:
            return NotFound()
        body = request.get_json()
        movie = Movie()
        if body['title'] is not None:
            movie.title= body['title']

        if body['release_date'] is not None:
            movie.release_date= body['release_date']
        movie.update()
        update_movie = Movie.query.filter(Movie.id == id).first()
        if update_movie is None:
            return NotFound()
        else:
            response = {
                    'success': True,
                    'status_code': 200,
                    'movie_updated' : update_movie.format()
                    }
            return jsonify(response)
    except Exception:
        raise Unauthorized()

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(id):
    try:
        selected_movie=Movie.query.get(id)
        if selected_movie is None:
            return NotFound()
        selected_movie.delete()

        response = {
                'success': True,
                'status_code': 200,
                'deleted_movie_id' : id
                }
        return jsonify(response)
    except Exception:
        raise Unauthorized()

# Error Handling

@app.errorhandler(400)
def bad_request(error):
     return jsonify({
       "success" : False,
       "error" : 400 ,
       "message" : "bad request "
     }) ,400

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
        }), 404

@app.errorhandler(401)
def Unauthorized_client(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized client status"
        }), 401

@app.errorhandler(405)
def method_not_found(error):
     return jsonify({
       "success" : False,
       "error" : 405 ,
       "message" : "Method not found "
     }) ,405

if __name__ == '__main__':
    app.run()