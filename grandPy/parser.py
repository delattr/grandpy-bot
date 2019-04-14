import os
import re
import json


def string_parser(text):
    """Parse user's question using 'stopwords.json"""
    # Convert text to lowercase
    text = text.lower()

    # Find absolult path to the json file
    SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(SITE_ROOT, 'static', 'stopwords_en.json')

    # Open json file and convert it into an object
    with open(path_to_json) as f:
        stopwords = set(json.load(f))

    # Split phrases into list using RegEx
    parsed_list = re.split(r'\W+', text)

    # remove empty elements
    parsed_list = [i for i in parsed_list if i != ""]

    # Parse and join the left over words into a string
    parsed_string = ' '.join([w for w in parsed_list if w not in stopwords])

    return parsed_string
