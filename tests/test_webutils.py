import json

import pandas as pd

from reconciler.webutils import get_query_dict, perform_query, return_reconciled_raw


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


def test_perform_query(reformatted, endpoints):

    query_string = json.dumps({"queries": json.dumps(reformatted)})
    query_res = perform_query(query_string, endpoints[0])

    assert len(query_res.keys()) == 4


def test_return_raw_results(city_data, endpoints):

    input_keys, raw_res = return_reconciled_raw(
        city_data["City"],
        type_id="Q515",
        reconciliation_endpoint=endpoints[0],
        property_mapping=None,
    )

    input_keys2, raw_res2 = return_reconciled_raw(
        city_data["City"],
        type_id="/ulan",
        reconciliation_endpoint=endpoints[1],
        property_mapping=None,
    )

    assert len(input_keys) and len(raw_res.keys()) == 4
    assert len(input_keys2) and len(raw_res2.keys()) == 4
