import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

# from datetime import date
from app import create_app
from models.models import setup_db, Actor, Movie

invalid_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVHeVRfMHpqeEdPOExaYWc3bDNONyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRuaGVycmVyYW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmEyMmFlMGY4NjY0MDA2OTJhNjJmNSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjI3Nzc4MTk5LCJleHAiOjE2Mjc3ODUzOTksImF6cCI6IlI3d2dndEVPN1lGZmVGYkwwM0g1ZGg3Snp1djlTOGxmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.ZOwaNseuua966slwwijK27wLJtQH-N4ZdiINDfLCiDq5SfeCG0I57VEftzkU45M3w7CIY9Inj96CWVsMUr3rz6mBC0ex9WBhTOwtpPXH3xvE4CDxJ3QISWyjBxKny7A3SgEN61-Qh5FzNygs0RGaDhA-J4f0I8kUYc0G5a8anw0-YLS4ISJGGXwRkXh7ZU8GdFaVC5vDvjV-7oKFB5Ebr5ST-MJ3wkbcbpmBYA_FQ6o1UKZmCvIb2F9nB-3fdJgF1L15wOLlnILFvJAP_S72uj948ThVdqBYGNznG1yoZFuNpiJ3OEUC1MRHZ9y2SKAJ4IcOvr0hERmKodHe86wd7g'

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_LOCAL']
        self.casting_assistant_token = os.environ['CASTING_ASSISTANT_TOKEN']
        self.casting_director_token = os.environ['CASTING_DIRECTOR_TOKEN']
        self.executive_producer_token = os.environ['EXECUTIVE_PRODUCER_TOKEN']
        setup_db(self.app, self.database_path)

    #----------------------------------------------------------------------------#
    # Tests /actors API
    #----------------------------------------------------------------------------#

    #Testing GET list actors
    def test_get_all_actors_as_casting_assistant_role_200(self):
        res = self.client().get('/actors', headers = {'Authorization' : self.casting_assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_all_actors_without_valid_token_401(self):
        res = self.client().get('/actors', headers = {'Authorization' : invalid_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['success'])


    #Testing POST create actor.
    def test_create_new_actor_as_executive_producer_role_200(self):
        actor = {
            'name' : 'Quentin',
            'gender': 'Male',
        } 
        res = self.client().post('/actors', json = actor, headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_new_actor_as_casting_assistant_role_401(self):
        actor = {
            'name' : 'Martina',
            'gender': 'Female',
        } 
        res = self.client().post('/actors', json = actor, headers = {'Authorization' : self.casting_assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['success'], False)

    #Testing PATCH update actor
    def test_update_actor_as_executive_producer_role_200(self):
        update_actor = {
            'name' : 'Jean Paul'
        } 
        res = self.client().patch('/actors/1', json = update_actor, headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_update_actor_without_id_400(self):
        update_actor = {
            'name' : 'Jean Paul'
        } 
        res = self.client().patch('/actors', json = update_actor, headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    #Testing DELETE remove actor
    def test_delete_actor_as_executive_producer_role_200(self):
        res = self.client().delete('/actors/1', headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor_without_id_400(self):
        res = self.client().delete('/actors', headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['success'], False)

    #----------------------------------------------------------------------------#
        # Tests /movies API
    #----------------------------------------------------------------------------#

    #Testing GET list movies
    def test_get_all_movies_as_casting_assistant_role_200(self):
        res = self.client().get('/movies', headers = {'Authorization' : self.casting_assistant_token})
        print(res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_get_all_movies_without_valid_token_401(self):
        res = self.client().get('/movies', headers = {'Authorization' : invalid_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['success'], False)


    #Testing POST create movie.
    def test_create_new_movie_as_executive_producer_role_200(self):
        movie = {
            'title' : 'Lost',
            'release_date': '2021-11-11 00:00:00',
        } 
        res = self.client().post('/movies', json = movie, headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_new_movie_as_casting_assistant_role_401(self):
        movie = {
            'title' : 'Fango',
            'release_date': '2021-11-11 00:00:00',
        }  
        res = self.client().post('/movies', json = movie, headers = {'Authorization' : self.casting_assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['success'], False)

    #Testing PATCH update movie
    def test_update_movie_as_executive_producer_role_200(self):
        update_movie = {
            'title' : 'Paranoia'
        } 
        res = self.client().patch('/movies/1', json = update_movie, headers = {'Authorization' : self.casting_director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_update_movie_without_id_400(self):
        update_movie = {
            'title' : 'The Rain'
        } 
        res = self.client().patch('/movies', json = update_movie, headers = {'Authorization' : self.casting_director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    #Testing DELETE remove movie
    def test_delete_movie_as_executive_producer_role_200(self):
        res = self.client().delete('/movies/1', headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_delete_movie_without_id_400(self):
        res = self.client().delete('/movies', headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['success'], False)
        
if __name__ == '__main__':
    unittest.main()
