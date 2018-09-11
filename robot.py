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


def searchPlace(text):
   
    place_search = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    # text_search = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    # place_detail = 'https://maps.googleapis.com/maps/api/place/details/json'
    
    place_payload = {'key': app.config['API_KEY'], 
                     'input': text,
                     'inputtype': 'textquery',
                     'language': 'fr', 
                     'locationbias': 'ipbias', 
                     'fields': 'formatted_address,name,geometry'}

    # text_payload = {'key': app.config['API_KEY'], 'query': text +', en france', 'region': 'fr', 'language': 'fr' }
    # detail_payload = {'key': app.config['API_KEY'], 'placeid': ''}

    name = ''
    address = ''
    place_loc = ''
    
    try:
        place_req = requests.get(place_search, params=place_payload)
        place_json = place_req.json()
        place_req.raise_for_status()
        
        if  place_json['status'] == 'OK':
            address = place_json['candidates'][0]['formatted_address']
            place_loc = place_json['candidates'][0]['geometry']['location']
            name = place_json['candidates'][0]['name']
            response = {'status': 'OK', 'name': name, 'address': address, 'location': place_loc}

        else:
            response = {'status': 'ZERO_RESULT'}

    except requests.exceptions.RequestExceptions as error:
        response = str(error)
        
    # try: 
    #     detail_req = requests.get(place_detail, params=detail_payload)
    #     detail_json = detail_req.json()
    #     if  detail_json['status'] == 'OK':
    #         respons2= place_json['address_components'][1]['long_name']
    # except requests.exceptions.RequestExceptions as error:
    #     response2 = error 
    return response

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def post():
    question = request.form['user_input']
    search = stringParser(question)
    place = searchPlace(search)
    return jsonify(place)

if __name__ == '__main__':
    app.run(debug=True)
