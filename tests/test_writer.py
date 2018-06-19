import unittest
from file import FileWriter

class TestFileWriter(unittest.TestCase):
	
    path = './resources/test_files/writer/'
    writer = FileWriter(path)
    writer_with_field = FileWriter(path, 'sexo')

    ##########
    # Test file writer
    ##########

    def test_write_empty_json(self):
        self.assertRaises(Exception, self.writer.write_json, '')

    def test_write_single_field_json(self):
        data = '{"name": "joao"}'
        self.writer.write_json(data)
        content = self.__read_file_content__('joao.json')
        self.assertEqual(content, data)

    def test_write_multiple_field_json(self):
        data = '{"name": "maria", "idade": "21", "sexo": "feminino"}'
        self.writer.write_json(data)
        content = self.__read_file_content__('maria.json')
        self.assertEqual(content, data)

    def test_write_single_field_no_default_values_json(self):
        data = '{"sexo": "masculino"}'
        self.writer_with_field.write_json(data)
        content = self.__read_file_content__('masculino.json')
        self.assertEqual(content, data)

    def test_write_multiple_field_no_default_values_json(self):
        data = '{"name": "maria", "idade": "21", "sexo": "feminino"}'
        self.writer_with_field.write_json(data)
        content = self.__read_file_content__('feminino.json')
        self.assertEqual(content, data)

    def __read_file_content__(self, filename):
        file = open(self.path + filename, 'r')
        content = file.read()
        file.close()
        return content
