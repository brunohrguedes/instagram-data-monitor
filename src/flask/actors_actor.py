from flask import Flask
from flask import jsonify
import re
import json

app = Flask(__name__)

@app.route('/actors/<actor>', methods=['GET'])
def actors_actor(actor):
	h = {}
	h['name'] = actor
	h['link'] = "http://www.instagram.com/" + actor + "/"
