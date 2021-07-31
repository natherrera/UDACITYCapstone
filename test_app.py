import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

# from datetime import date
from app import create_app
from models.models import setup_db, Actor, Movie

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL')
        self.casting_assistant_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVHeVRfMHpqeEdPOExaYWc3bDNONyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRuaGVycmVyYW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmI4MmI2YzcyNDA1MDA3MWI0ZjI1NyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjI3NTIzOTU1LCJleHAiOjE2Mjc1MzExNTUsImF6cCI6IlI3d2dndEVPN1lGZmVGYkwwM0g1ZGg3Snp1djlTOGxmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwicG9zdDphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.A3miCpWJEnlWFtnqpCh1h-EwDPnxwAlbtTeSvJXFr9m_IoOpoqgRRfzU-pGqUJ5_2bIolehMx4oU0QS5B6qosD9d-TbJtPL87yvhOdqVJjbJTgwtkD27gJeSfdZaBanUTk4r9PzxYGja1-MPpjOi8hPouSZEgaFo44StLmQFTJJ-isuivZt1Yi9GTgv1tMXOeN5uRUjlhpmFrwEvfc8NmlMmVeeRnvYRHZ1E23t45-7hm4tOu3RPVdqoy3JWvhBnQU6qqwXAuMyI5I6LySsbZdUI7Wk1r00ecAxCTXCSK-ZrIPKfFycY_LgPt9oZFP0zr8KF48QUqqBQdSVqLTaVtQ'
        self.casting_director_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVHeVRfMHpqeEdPOExaYWc3bDNONyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRuaGVycmVyYW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmI4Mjc2MGY4NjY0MDA2OTJhYWFhMiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjI3NTI0MDEzLCJleHAiOjE2Mjc1MzEyMTMsImF6cCI6IlI3d2dndEVPN1lGZmVGYkwwM0g1ZGg3Snp1djlTOGxmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.Mttet7jybclIQPIVtTkbfH0MMGoiDlu-aHM2NfA60DzVOV8DzucIeIqcDuZJ8R9f6kj4IZLKrdvylJCWVBuG47MNdrTYoYNyOhob6oEGHhlGHGP2t1pArBUDhO0OYv2fLBAw5aREs31QSHRG9Z6UaGP_s2R9jJNfX1vVeuwyou2BZok7OYGHSuBa93PbabPHBpZI7zw1BoykJEPIa-BWGipaEi_iol14cRsPHhHLJI90KRvFrCiZhEs0cPjF7AHNKCcB-NsFdX0Ptm1LpWFp1n2ymqoklsstA3A6wkV1WtJtxlenXK5P2BvcmEQM1oRPxN-RonaahSj2PtajhjacMg'
        self.executive_producer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVHeVRfMHpqeEdPOExaYWc3bDNONyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRuaGVycmVyYW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmEyMmFlMGY4NjY0MDA2OTJhNjJmNSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjI3NTkxMzIzLCJleHAiOjE2Mjc1OTg1MjMsImF6cCI6IlI3d2dndEVPN1lGZmVGYkwwM0g1ZGg3Snp1djlTOGxmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.XWKxOaK6IpVNK7PVZftjmiItm300pRjrq42yHoHvp3sG9y1GzuRCa4P3mizyK9EjfioLVNbDrkk4QIByFKLyJfz6_69_FBsrm3GgxECObARPueTQotoR0PVzWxmziryCMtlQ5adTY2soZCgsdiScpCdeZYQR-d3Z6ms5UcvOKR7c8vGyrXxMCHIWwS0DvgZWI9YHY18uAxLy70H1idJcFzP1Y4Bk_weq2kaR4B0pEPII15ayHmmdIdU6a_caVCVtoOsW5m4VTuBKho6aiCI3zCyGjsd8JgalB5-OtlehG1bu8_K-gzyWm5BsLzY9rExa8glvdSWNEzmRx6ewL7LIxQ'
        setup_db(self.app, self.database_path)

    #----------------------------------------------------------------------------#
    # Tests /actors API
    #----------------------------------------------------------------------------#

    #Testing GET list actors
    def test_get_all_actors_as_casting_assistant_role_200(self):
        res = self.client().get('/actors', headers = {'Authorization' : self.executive_producer_token})
        print(res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    #Testing POST create actor.
    def test_create_new_actor_as_executive_producer_200(self):
        actor = {
            'name' : 'Quentin',
            'gender': 'Male',
        } 
        res = self.client().post('/actors', json = actor, headers = {'Authorization' : self.executive_producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#     #Testing PATCH update actor
#     def test_update_actor_as_executive_producer_200(self):
#         update_actor = {
#             'name' : 'Jean Paul'
#         } 
#         res = self.client().patch('/actors/1', json = update_actor, headers = {'Authorization' : self.executive_producer_token})
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(data['success'])


#     #Testing DELETE remove actor
#     def test_delete_actor_as_executive_producer_200(self):
#         res = self.client().delete('/actors/1', headers = {'Authorization' : self.executive_producer_token})
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(data['success'])
        
if __name__ == '__main__':
    unittest.main()
