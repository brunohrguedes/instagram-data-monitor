import unittest
from file import CSVConverter

class TestCSVConverter(unittest.TestCase):
	
    path = './resources/test_files/converter/'
    converter = CSVConverter()

    ##########
    # Test convert CSV
    ##########

    def test_convert_empty_csv(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'empty.csv'), [])

    def test_convert_one_field_csv(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'one_field.csv'), ['{"nome": "joao"}'])

    def test_convert_one_field_csv_with_various_data(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'one_field_with_multiple_lines_of_data.csv'), \
                          ['{"nome": "joao"}', '{"nome": "jose"}', \
                          '{"nome": "maria"}'])

    def test_convert_multiple_fields_csv(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'multiple_fields.csv'), \
                         ['{"nome": "maria", "idade": "21", "sexo": "feminino"}'])

    def test_convert_multiple_fields_csv_with_various_data(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'multiple_fields_with_multiple_lines_of_data.csv'), \
                          ['{"nome": "joao", "idade": "17", "sexo": "m"}', \
                          '{"nome": "jose", "idade": "30", "sexo": "m"}', \
                          '{"nome": "maria", "idade": "21", "sexo": "f"}'])

    def test_convert_multiple_fields_in_semicolon_csv(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'multiple_fields.csv'), \
                         ['{"nome": "maria", "idade": "21", "sexo": "feminino"}'])
        
    def test_convert_multiple_fields_in_semicolon_csv_with_various_data(self):
        self.assertEqual(self.converter.convert_to_json(self.path + \
                         'multiple_fields_with_multiple_lines_of_data.csv'), \
                          ['{"nome": "joao", "idade": "17", "sexo": "m"}', \
                          '{"nome": "jose", "idade": "30", "sexo": "m"}', \
                          '{"nome": "maria", "idade": "21", "sexo": "f"}'])