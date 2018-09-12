from flask import Flask, render_template, request, url_for, json, jsonify
import os
import re
import requests


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


# Convert Json to Object
def getJson():
    path_json = os.path.join(app.root_path, 'static', 'stopwords.json')
    path_json = os.path.join(app.root_path, 'static', 'stopwords.json')
    with open(path_json) as f:
        data = json.load(f)
    return set(data)


def stringParser(text):
    text = request.form['user_input']
    text = text.lower()
    text = re.split(r'[^-\w+]', text)
    wordstops = getJson()
    string_parsed = ' '.join([w for w in text if w not in wordstops])
    return string_parsed


def getPlace(text):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    payload = {'key': app.config['API_KEY'],
               'input': text,
               'inputtype': 'textquery',
               'language': 'fr',
               'locationbias': 'ipbias',
               'fields': 'place_id,formatted_address,name,geometry'}
    try:
        req = requests.get(url, params=payload)
        response = req.json()
        req.raise_for_status()

        if response['status'] == 'OK':
            results = response['candidates'][0]
            status = response['status']
            address = results['formatted_address']
            location = results['geometry']['location']
            name = results['name']
            place_id = results['place_id']
            voie = getRouteName(place_id)
        else:
            data = {'status': response['status']}

        data = {'status': status,
                'name': name,
                'address': address,
                'location': location,
                'route': voie}

        return data
    except requests.exceptions.HTTPError as err:
        return err


def getRouteName(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    payload = {'key': app.config['API_KEY'],
               'placeid': place_id,
               'fields': 'address_components'}
    try:
        req = requests.get(url, params=payload)
        response = req.json()
        req.raise_for_status()
        print(response)
        address_components = response['result']['address_components']
        for i, v in enumerate(address_components):
            if v['types'][0] == 'route':
                voie = address_components[i]['long_name']
        return voie
    except requests.exceptions.HTTPError as err:
        return err


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def post():
    question = request.form['user_input']
    search = stringParser(question)
    place = getPlace(search)
    return jsonify(place)


if __name__ == '__main__':
    app.run(debug=True)
