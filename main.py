# from file import CSVConverter
# from file import FileWriter
# from datetime import datetime

# import glob
# import os

# CSV_ACTORS_PATH = './src/atores_dados/csv/'
# CSV_STORIES_PATH = './src/stories/csv/'

# NOW = datetime.now()
# TODAY = str(NOW.day) + '-' + str(NOW.month).zfill(2) + '-' + str(NOW.year)

# JSON_ACTORS_PATH = './resources/json/actors/' + TODAY + '/'
# JSON_STORIES_PATH = './resources/json/stories/' + TODAY + '/'

# if not os.path.exists(JSON_ACTORS_PATH) and not os.path.exists(JSON_STORIES_PATH):
#     os.mkdir(JSON_ACTORS_PATH)
#     os.mkdir(JSON_STORIES_PATH)

# converter = CSVConverter()
# writer = FileWriter(JSON_ACTORS_PATH, 'Nome real da conta')

# def save_each_json(data):
#     for content in data:
#         writer.write_json(content)

# def convert(csvpath):
#     data = converter.convert_to_json(csvpath)
#     save_each_json(data)

# actors_csv = glob.glob(CSV_ACTORS_PATH + '*.csv')
# stories_csv = glob.glob(CSV_STORIES_PATH + '*.csv')

# for csv in actors_csv:
#     convert(csv)

# writer = FileWriter(JSON_STORIES_PATH, 'username')

# for csv in stories_csv:
#     convert(csv)

from core import collect_data

collect_data()