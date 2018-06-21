from src.flask.actors_actor import app
import unittest
import json

class TestActorsActor(unittest,Testcase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True
	
	def test_actors_actor_exist(self):
		result = self.app.get('/actors/renovabr')

	def test_actors_actor_not_exist(self):
		result = self.app.get('/actors/nenhum')


if __name__ == '__main__'
	unittest.main()