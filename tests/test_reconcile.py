import pandas as pd
import json
from reconciler.reconcile import get_query_dict, perform_query
import pytest

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal"],
        "Inutil": ["bla", "blabla", "blablabla", "blablabla"],
    }
)
input_keys, reformatted = get_query_dict(test_df["City"])


def test_get_query_dict():

    expected = {
        "q0": {"query": "Rio de Janeiro"},
        "q1": {"query": "São Paulo"},
        "q2": {"query": "Natal"},
    }

    assert expected == reformatted


def test_perform_query():

    query_string = json.dumps({"queries": json.dumps(reformatted)})
    query_res = perform_query(query_string)

    assert len(query_res.keys()) == 3
