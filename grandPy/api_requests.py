import requests


def search_place(text, key):

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
        response = req.json()
        req.raise_for_status()

        if response['status'] == 'OK':
            result = response['candidates'][0]
            # get place ID from response
            place_id = result['place_id']
            # get information using place_id
            route = getDetail(place_id, key)
            wiki = wiki_search(route)
            data = {'status': response['status'],
                    'name': result['name'],
                    'address': result['formatted_address'],
                    'location': result['geometry']['location'],
                    'route': route,
                    'wiki': wiki}
        else:
            data = {'status': response['status']}

        return data
    except requests.exceptions.HTTPError as err:
        return err


def getDetail(place_id, key):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    payload = {'key': key,
               'placeid': place_id,
               'fields': 'address_components'}
    try:
        req = requests.get(url, params=payload)
        response = req.json()
        req.raise_for_status()

        address_components = response['result']['address_components']
        for i, v in enumerate(address_components):

            if v['types'][0] == 'route':
                route = address_components[i]['long_name']
                break
            else:  # Get first element from address_compnnents
                route = address_components[0]['long_name']
        # Search info from wiki using route name

        return route
    except requests.exceptions.HTTPError as err:
        return err


def wiki_search(text):

    url = "https://fr.wikipedia.org/w/api.php"

    payload = {
        "action": "query",
        "format": "json",
        "prop": "info|extracts",
        "generator": "search",
        "utf8": 1,
        "inprop": "url",
        "exchars": "1200",
        "gsrsearch": text,
        "gsrnamespace": "0",
        "gsrlimit": "1"
    }

    req = requests.get(url, params=payload)
    result = req.json()
    val = result['query']['pages'].values()
    data =list(val)
    return data[0]
