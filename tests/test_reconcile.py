import pandas as pd
from reconciler.reconcile import get_query_dict
import pytest

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal"],
        "Inutil": ["bla", "blabla", "blablabla", "blablabla"],
    }
)


def test_get_query_dict():

    expected = {
        "q0": {"query": "Rio de Janeiro"},
        "q1": {"query": "São Paulo"},
        "q2": {"query": "Natal"},
    }

    assert expected == get_query_dict(test_df["City"])