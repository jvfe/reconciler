import json

import pandas as pd

from reconciler.webutils import perform_query, return_reconciled_raw


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
