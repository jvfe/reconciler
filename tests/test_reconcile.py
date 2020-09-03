from reconciler.reconcile import reconcile
from pytest import raises
import pandas as pd
import requests

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal", "FAKE_CITY_HERE"],
    }
)


def test_basic_reconcile():

    expected_last_column = pd.Series(test_df["City"].unique())
    results = reconcile(test_df["City"], type_id="Q515")

    assert results.shape == (4, 7)
    pd.testing.assert_series_equal(
        expected_last_column, results["input_value"], check_names=False
    )


# Edge cases


def test_fake_item():
    with raises(requests.HTTPError):
        reconcile(test_df["City"], type_id="FAKE_ITEM_GIVE_ERROR")


def test_fake_top_res():
    with raises(ValueError):
        reconcile(test_df["City"], type_id="Q515", top_res="I'm such a fake argument")
