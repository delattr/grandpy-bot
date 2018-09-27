import requests


def search_place(text, key):
    """ Call Google Place API to get basic information of a place"""

    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    payload = {
        'key': key,
        'input': text,
        'inputtype': 'textquery',
        'language': 'fr',
        'locationbias': 'ipbias',
        'fields': 'place_id,name,formatted_address,geometry'
    }
    try:
        req = requests.get(url, params=payload)
        req.raise_for_status()
        response = req.json()
        print(response)

        if response['status'] == 'OK':
            result = response['candidates'][0]
            # Get place ID from response
            place_id = result['place_id']
            # Get information using place_id
            route = get_detail(place_id, key)
            # Search route name from wikipedia
            wiki = wiki_search(route)
            # Select only necesary data
            data = {'status': response['status'],
                    'name': result['name'],
                    'address': result['formatted_address'],
                    'location': result['geometry']['location'],
                    'route': route,
                    'wiki': wiki}
        else:
            data = {'status': response['status']}
        return data
    except requests.exceptions.HTTPError:
        return {'status': str(req.status_code) + " " + req.reason}


def get_detail(place_id, key):
    """Get route name of a place using Google Place Detail API"""

    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    payload = {'key': key,
               'placeid': place_id,
               'fields': 'address_components,name'}
    try:
        req = requests.get(url, params=payload)
        req.raise_for_status()
        response = req.json()

        address_components = response['result']['address_components']

        for i, v in enumerate(address_components):

            if v['types'][0] == 'route':
                route = address_components[i]['long_name']
                break
            else:  # Get first element from address_compnnents
                route = response['result']['name']
        return route
    except requests.exceptions.HTTPError:
        return {'status': str(req.status_code) + " " + req.reason}


def wiki_search(text):
    """Search route name from Wikipedia"""

    url = "https://fr.wikipedia.org/w/api.php"

    payload = {
        "action": "query",
        "format": "json",
        "prop": "info|extracts",
        "generator": "search",
        "utf8": 1,
        "inprop": "url",
        "exchars": "600",
        "gsrsearch": text,
        "gsrnamespace": "0",
        "gsrlimit": "1"

    }

    try:
        req = requests.get(url, params=payload)
        req.raise_for_status()

    except requests.exceptions.HTTPError:
        return {'status': str(req.status_code) + " " + req.reason}

    else:
        result = req.json()
        print(result)
        for k, v in result['query']['pages'].items():
            if k == -1:
                response = "Oh, mon poussin. Je ne connais pas très bien " \
                    "le quariter."
            else:
                data = v
                response = f'{data["extract"]} <a href = "{data["fullurl"]}"'\
                    ' target="_blank">[En sovir plus sur Wikipedia]</a>'
        return response
