
import requests


def search_place(text, key):
    """ Call Google Place API to get basic information of a place"""
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    payload = {
        # Reauired fields
        'key': key,
        'input': text,
        'inputtype': 'textquery',
        # Optonal fields
        'locationbias': 'ipbias',
        'fields': 'formatted_address,id,name,geometry'
        }
    try:
        req = requests.get(url, params=payload)
        req.raise_for_status()
        response = req.json()

        if response['status'] == 'OK':
            # Grap the frist result from JSON
            result = response['candidates'][0]
            # Get place ID from response
            name = result['name']
            # Search route name from wikipedia
            wiki = wiki_search(name)
            # Select only necesary data
            data = {'status': response['status'],
                    'name': name,
                    'address': result['formatted_address'],
                    'location': result['geometry']['location'],
                    'wiki': wiki}
        else:
            data = {'status': response['status']}
        return data
    except requests.exceptions.HTTPError:
        return {'status': str(req.status_code) + " " + req.reason}


def wiki_search(text):
    """Search route name from Wikipedia"""

    url = "https://en.wikipedia.org/w/api.php"

    payload = {
        "action": "query",
        "format": "json",
        "prop": "info|extracts",
        "generator": "search",
        "utf8": 1,
        "inprop": "url",
        "exchars": "600",
        "gsrsearch": text,
        "gsrlimit": "1"
    }
    try:
        req = requests.get(url, params=payload)
        req.raise_for_status()

    except requests.exceptions.HTTPError:
        return {'status': str(req.status_code) + " " + req.reason}

    else:
        result = req.json()
        if 'error' in result:
            return result['error']['code']

        else:
            for k, v in result['query']['pages'].items():
                if k == -1:
                    response = "No information was found on Wikipedia.com about this place"
                else:
                    data = v
                    response = f'{data["extract"]} <a href = "{data["fullurl"]}"'\
                        ' target="_blank">[Wikipedia]</a>'
            return response


def get_detail(place_id, key):
    """Get street name of the place using Google Place Detail API"""

    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    payload = {'key': key,
               'placeid': place_id,
               'fields': 'address_components,name'}
    try:
        req = requests.get(url, params=payload)
        req.raise_for_status()
        response = req.json()

        address_components = response['result']['address_components']

        # Iterate over JSON to find the street name
        for i, v in enumerate(address_components):
            if v['types'][0] == 'route':
                route = address_components[i]['long_name']
                break
            else:
                route = response['result']['name']
        return route
    except requests.exceptions.HTTPError:
        # Retrun Status_code if error occurs
        return {'status': str(req.status_code) + " " + req.reason}


