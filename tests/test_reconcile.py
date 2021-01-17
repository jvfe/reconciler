import numpy as np
import pandas as pd
import pytest
from pytest import raises

from reconciler import reconcile


def test_basic_reconcile(city_data):

    expected_last_column = pd.Series(city_data["City"].unique())
    results = reconcile(city_data["City"], type_id="Q515")

    assert results.shape == (4, 7)
    pd.testing.assert_series_equal(
        expected_last_column, results["input_value"], check_names=False
    )


def test_reconcile_without_type(city_data):

    results = reconcile(city_data["City"])

    expected_names = ["Rio de Janeiro", "São Paulo", "Christmas"]

    retrieved = results["name"].to_list()[0:3]

    assert retrieved == expected_names


def test_reconcile_against_triple(gene_data):

    results = reconcile(
        gene_data["gene"], property_mapping={"P703": gene_data["species"]}
    )

    assert results["id"][0] == "Q227339"


@pytest.mark.skip(reason="Not working as of yet.")
def test_long_reconcile(us_capitals):

    df = pd.DataFrame.from_dict(
        us_capitals, orient="index", columns=["Capital"]
    ).reset_index()

    results = reconcile(
        df["Capital"], type_id="Q515", property_mapping={"P1376": df["index"]}
    )

    assert results.shape == (51, 7)


def test_no_results():
    """Tests if parsing with absent results still works"""

    test_series = pd.Series(["Querula rubricollis", "Querula rubricollis"])

    reconciled = reconcile(test_series, type_id="Q16521")

    expected_results = pd.DataFrame(
        {
            "id": [np.NaN],
            "match": [False],
            "input_value": ["Querula rubricollis"],
        }
    )

    pd.testing.assert_frame_equal(expected_results, reconciled)


# Edge cases


def test_fake_top_res(city_data):
    with raises(ValueError):
        reconcile(city_data["City"], type_id="Q515", top_res="I'm such a fake argument")
