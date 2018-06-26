import csv
import json
import glob
import re
import os

try:
	os.makedirs('json')
except:
	pass

to_cvt = []
for file in glob.glob("*.csv"):
    to_cvt.append(file)

for f in to_cvt:
	csvfile = open( f , 'r')
	jsonfile = open('./json/' +f[:-4] +'.json', 'w', encoding='utf8')
	fieldnames = ''
	for i in open(f,'r'):
		fieldnames = i.split(',')
		break	
	if not fieldnames:
		print("Problemas com o arquivo " + f)
		pass
	else:
		fieldnames[-1] = fieldnames[-1][:-1]  # retira o '\n' do último nome de coluna
		reader = csv.DictReader( csvfile, fieldnames)
		i = 0
		for row in reader:
			if i == 0:
				i = 1
			else:
				json.dump(row, jsonfile, ensure_ascii=False)
				jsonfile.write('\n')
