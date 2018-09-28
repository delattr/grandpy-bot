"""This file is part of GrandPy Bot.

GrandPy Bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GrandPy Bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GrandPy Bot.  If not, see <https://www.gnu.org/licenses/>.
"""

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
