import unittest
from core.dict import to_utf8 as utf8_to_utf8_right

class TesteAtor(unittest.TestCase):
	def teste_kahlo(self):
		self.assertEqual(utf8_to_utf8_right('N\u00e3o Me Kahlo'), "Não Me Kahlo" )
	def teste_midiaNinja(self):
		self.assertEqual(utf8_to_utf8_right('M\u00eddia NINJA'), "Mídia NINJA" )
	def teste_stringNormal(self):
		self.assertEqual(utf8_to_utf8_right('nada de errado'), "nada de errado" )
