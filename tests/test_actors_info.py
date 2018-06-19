import unittest
import os

from src import generate_actor, generate_csv


class TestActorsInfo(unittest.TestCase):
	def test_find_actor_from_username(self):
		username = 'oimundoembr'
		url = f'https://www.instagram.com/{username}/'
		actor = generate_actor.actor_from_url(url)
		self.assertEqual('instagram instagram', actor.full_name)
		self.assertEqual(username, actor.username)
		self.assertEqual(0, actor.followed)
		self.assertEqual(0, actor.follows)
		self.assertEqual(0, actor.posts)

	def test_find_unknown_actor_from_username(self):
		username = 'oimundoembrr'
		url = f'https://www.instagram.com/{username}/'
		actor = generate_actor.actor_from_url(url)
		self.assertEqual(username, actor.full_name)
		self.assertEqual(username, actor.username)
		self.assertEqual(0, actor.followed)
		self.assertEqual(0, actor.follows)
		self.assertEqual(0, actor.posts)

	def test_find_actor_with_broken_url(self):
		username = 'oimundoembr'
		url = f'https://www.inst{username}/'
		actor = generate_actor.actor_from_url(url)
		self.assertFalse(actor)

	#@TODO Criar mais testes para verificar os dados dentro do .csv
	def test_generate_csv_of_all_actors(self):
		filename = generate_csv.generate_actors_info_csv()
		self.assertTrue(os.path.exists(filename))
		os.remove(filename)


if __name__ == '__main__':
    unittest.main()
