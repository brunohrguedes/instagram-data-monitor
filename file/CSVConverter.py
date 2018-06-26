import csv
import json
import os

class CSVConverter:
    """Class to convert CSV to JSON"""

    __delimiter__ = ''
    __fieldnames__ = []

    def convert_to_json(self, csvname):
        """Convert a CSV to a list of JSON"""
        csvfile = open(csvname, 'r')
        self.__obtain_csv_delimiter__(csvfile)
        self.__obtain_csv_fieldnames__(csvfile)
        data = self.__obtain_data_from_csv__(csvfile)
        jsons = self.__convert_data_to_list_of_dict__(data)
        list_of_jsons = self.__transform_list_to_jsons__(jsons)
        csvfile.close()
        return list_of_jsons

    def __obtain_csv_fieldnames__(self, csvfile):
        """Obtain the field names of the CSV file"""
        self.__fieldnames__ = csvfile.readline()
        self.__obtain_csv_delimiter__(self.__fieldnames__)
        self.__fieldnames__ = self.__remove_break_line__(self.__fieldnames__)
        self.__fieldnames__ = self.__split_for_delimiter__(self.__fieldnames__)

    def __obtain_csv_delimiter__(self, string):
        """Dinamically obtain the delimiter of the CSV file"""
        sniffer = csv.Sniffer()
        try:
            self.__delimiter__ = sniffer.sniff(string, [',', ';']).delimiter
        except:
            self.__delimiter__ = ''

    def __obtain_data_from_csv__(self, csvfile):
        """Obtain the data from the CSV file"""
        data = csvfile.readlines()
        data = self.__parse_string_for_delimiter__(data)
        return data

    def __convert_data_to_list_of_dict__(self, data):
        """Return all the data as a list of dictionaries"""
        jsons = list()
        for row in data:
            json_for_row = dict(zip(self.__fieldnames__, row))
            jsons += [json_for_row]
        return jsons
    
    def __transform_list_to_jsons__(self, listofjsons):
        """Return a list of JSONs"""
        jsons = []
        for row in listofjsons:
            jsons += [json.dumps(row)]
        return jsons    


    def __remove_break_line__(self, string):
        """Remove the break line character"""
        return string.rstrip()

    def __split_for_delimiter__(self, string):
        """Split a string based in the delimiter"""
        if not self.__delimiter__ == '':
            return string.split(self.__delimiter__)
        return string.split()

    def __parse_string_for_delimiter__(self, data):
        """Parse the data to a list of strings"""
        parsed = []
        for row in data:
            row = self.__remove_break_line__(row)
            row = self.__split_for_delimiter__(row)
            parsed.append(row)
        return parsed