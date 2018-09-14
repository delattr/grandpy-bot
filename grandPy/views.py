from flask import render_template, request, json, jsonify
from grandPy import app
from .parser import string_parser
from .api_requests import search_place

app.config.from_object('config')
app.config.from_pyfile('config.py')
key = app.config['API_KEY']

# Convert Json to Object


@app.route("/")
def index():
    return render_template('index.html', key=key)


@app.route('/post', methods=['POST'])
def api_requests():
    question = request.form['user_input']
    place = string_parser(question)
    result = search_place(place, key)
    return jsonify(result)

