import grandPy.parser as parse


def test_string_parsed_with_wordstops_json():
    string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
    assert parse.string_parser(string) == "adresse openclassrooms"
