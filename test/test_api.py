import grandPy.api_requests as api
import pytest
import requests


class FakeResponse:
    """Mocking requests.get"""

    def raise_for_status(self):
        pass

    def json(self):
        pass


def fake_get(*args, **kargs):
    response = FakeResponse()
    return response


def test_results_from_google_place_api_and_mediawiki_api(monkeypatch):
    def fake_json(self):
        self.data = {
            'candidates': [{
                'formatted_address': '7 Cité Paradis, 75010 Paris, France',
                'geometry': {
                    'location': {
                        'lat': 48.8747578,
                        'lng': 2.350564700000001}},
                'name': 'OpenClassrooms',
                'place_id': 'ChIJIZX8lhRu5kcRGwYk8Ce3Vc8'
            }],
            'status': 'OK',
            'result': {
                'address_components': [{
                    'long_name': 'route name',
                    'types': ['route']
                }]
            },
            'query': {
                'pages': {
                    1: {
                        'extract': 'wiki_extracts',
                        'fullurl': 'http://fr.wikipedia.org/'}
                }
            }
        }
        return self.data

    FakeResponse.json = fake_json

    data = {'status': 'OK',
            'name': 'OpenClassrooms',
            'address': '7 Cité Paradis, 75010 Paris, France',
            'location': {'lat': 48.8747578,
                         'lng': 2.350564700000001},
            'route': 'route name',
            'wiki': 'wiki_extracts <a href = "http://fr.wikipedia.org/"'
            ' target="_blank">[En sovir plus sur Wikipedia]</a>'}

    monkeypatch.setattr(requests, 'get', fake_get)
    assert api.search_place('openclassrooms', 'api_key') == data


def test_requests_HTTP_error(monkeypatch):

    def status(self):
        raise requests.exceptions.HTTPError
    original_satus = FakeResponse.raise_for_status
    FakeResponse.raise_for_status = status
    FakeResponse.status_code = '404'
    FakeResponse.reason = 'Page Not Found'
    result = {'status': '404 Page Not Found'}
    monkeypatch.setattr('grandPy.api_requests.requests.get', fake_get)

    assert api.search_place('text', 'api_key') == result
    assert api.get_detail('place_id', 'api_key') == result
    assert api.wiki_search('query') == result
    FakeResponse.raise_for_status = original_satus


def test_place_api_returns_no_results(monkeypatch):

    def fake_json(self):
        return {'status': 'ZERO_RESULTS'}
    FakeResponse.json = fake_json
    monkeypatch.setattr('grandPy.api_requests.requests.get', fake_get)
    assert api.search_place('text', 'api_key') == {'status': 'ZERO_RESULTS'}


def test_wiki_api_retuns_no_results(monkeypatch):
    def fake_json(self):
        self.data = {'query': {
            'pages': {
                -1: {
                    'extract': 'wiki_extracts',
                    'fullurl': 'http://fr.wikipedia.org/'}
            }
        }}
        return self.data
    FakeResponse.json = fake_json
    monkeypatch.setattr('grandPy.api_requests.requests.get', fake_get)
    result = "Oh, mon poussin. Je ne connais pas très bien le quariter."
    assert api.wiki_search('query',) == result
