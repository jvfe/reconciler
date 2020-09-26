from reconciler.webutils import get_query_dict, perform_query, return_reconciled_raw
import pandas as pd
import json

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal", "FAKE_CITY_HERE"],
    }
)
input_keys, reformatted = get_query_dict(
    test_df["City"], type_id="Q515", has_property=None
)
test_endpoints = [
    "https://wikidata.reconci.link/en/api",
    "https://services.getty.edu/vocab/reconcile/",
]


def test_get_query_dict():

    expected = {
        0: {"query": "Rio de Janeiro", "type": "Q515"},
        1: {"query": "São Paulo", "type": "Q515"},
        2: {"query": "Natal", "type": "Q515"},
        3: {"query": "FAKE_CITY_HERE", "type": "Q515"},
    }

    assert expected == reformatted


def test_perform_query():

    query_string = json.dumps({"queries": json.dumps(reformatted)})
    query_res = perform_query(query_string, test_endpoints[0])

    assert len(query_res.keys()) == 4


def test_return_raw_results():

    input_keys, raw_res = return_reconciled_raw(
        test_df["City"],
        type_id="Q515",
        reconciliation_endpoint=test_endpoints[0],
        has_property=None,
    )

    input_keys2, raw_res2 = return_reconciled_raw(
        test_df["City"],
        type_id="/ulan",
        reconciliation_endpoint=test_endpoints[1],
        has_property=None,
    )
    assert len(input_keys) and len(raw_res.keys()) == 4
    assert len(input_keys2) and len(raw_res2.keys()) == 4
