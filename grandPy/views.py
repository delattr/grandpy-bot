from flask import render_template, request, json, jsonify
from grandPy import app
from .parser import string_parser
from .api_requests import search_place
import os


app.config.from_object(os.environ.get('APP_ENV'))
maps_key = app.config['MAPS_API_KEY']
place_key = app.config['PLACE_API_KEY']


@app.route("/")
def index():
    return render_template('index.html', key=maps_key)


@app.route('/post', methods=['POST'])
def api_requests():
    question = request.form['user_input']
    # Get place from google api
    place = string_parser(question)
    print(place)
    # Search place form Wiki api
    result = search_place(place, place_key)
    print(result)
    return jsonify(result)
