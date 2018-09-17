import os
import re
import json


def string_parser(text):
    """Parse text input from 'stopwords.json"""

    # Find absolult path to the json file
    SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(SITE_ROOT, 'static', 'stopwords.json')
    # Open json file and convert it into an object
    with open(path_to_json) as f:
        set_stopwords = set(json.load(f))
    # Split phrases into list using RegEx, 're.I' = ignore cases
    parsed_list = re.split(r'\W+', text, flags=re.I)
    # Parse and join the left over words into a string
    parsed_string = ' '.join([w for w in parsed_list
                             if w not in set_stopwords])
    return parsed_string
