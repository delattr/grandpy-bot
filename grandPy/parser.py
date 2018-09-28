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

import os
import re
import json


def string_parser(text):
    """Parse user's question using 'stopwords.json"""
    # Convert text to lowercase
    text = text.lower()

    # Find absolult path to the json file
    SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(SITE_ROOT, 'static', 'stopwords.json')

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
