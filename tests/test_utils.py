import pandas as pd

from reconciler.utils import get_query_dict


def test_get_query_dict(reformatted):

    expected = {
        0: {"query": "Rio de Janeiro", "type": "Q515"},
        1: {"query": "São Paulo", "type": "Q515"},
        2: {"query": "Natal", "type": "Q515"},
        3: {"query": "FAKE_CITY_HERE", "type": "Q515"},
    }

    assert expected == reformatted


def test_query_dict_w_mapping():

    expected = {
        0: {
            "query": "Quercus robur",
            "properties": [
                {"pid": "epithet_1", "v": "Quercus"},
                {"pid": "epithet_2", "v": "robur"},
                {"pid": "publishing_author", "v": "L."},
            ],
        }
    }

    data = pd.DataFrame(
        {
            "scientific_name": ["Quercus robur"],
            "genus": ["Quercus"],
            "species": ["robur"],
            "author": ["L."],
        }
    )

    _, reformatted = get_query_dict(
        data["scientific_name"],
        type_id=None,
        property_mapping={
            "epithet_1": data["genus"],
            "epithet_2": data["species"],
            "publishing_author": data["author"],
        },
    )

    assert expected == reformatted