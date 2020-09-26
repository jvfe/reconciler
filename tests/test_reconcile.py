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


def test_long_reconcile():

    us_capitals = {
        "Alabama": "Montgomery",
        "Alaska": "Juneau",
        "Arizona": "Phoenix",
        "Arkansas": "Little Rock",
        "California": "Sacramento",
        "Colorado": "Denver",
        "Connecticut": "Hartford",
        "Delaware": "Dover",
        "Florida": "Tallahassee",
        "Georgia": "Atlanta",
        "Hawaii": "Honolulu",
        "Idaho": "Boise",
        "Illinios": "Springfield",
        "Indiana": "Indianapolis",
        "Iowa": "Des Monies",
        "Kansas": "Topeka",
        "Kentucky": "Frankfort",
        "Louisiana": "Baton Rouge",
        "Maine": "Augusta",
        "Maryland": "Annapolis",
        "Massachusetts": "Boston",
        "Michigan": "Lansing",
        "Minnesota": "St. Paul",
        "Mississippi": "Jackson",
        "Missouri": "Jefferson City",
        "Montana": "Helena",
        "Nebraska": "Lincoln",
        "Neveda": "Carson City",
        "New Hampshire": "Concord",
        "New Jersey": "Trenton",
        "New Mexico": "Santa Fe",
        "New York": "Albany",
        "North Carolina": "Raleigh",
        "North Dakota": "Bismarck",
        "Ohio": "Columbus",
        "Oklahoma": "Oklahoma City",
        "Oregon": "Salem",
        "Pennsylvania": "Harrisburg",
        "Rhoda Island": "Providence",
        "South Carolina": "Columbia",
        "South Dakoda": "Pierre",
        "Tennessee": "Nashville",
        "Texas": "Austin",
        "Utah": "Salt Lake City",
        "Vermont": "Montpelier",
        "Virginia": "Richmond",
        "Washington": "Olympia",
        "West Virginia": "Charleston",
        "Wisconsin": "Madison",
        "Wyoming": "Cheyenne",
        "USA": "Washington DC",
    }
    df = pd.DataFrame.from_dict(us_capitals, orient="index", columns=["Capital"])

    results = reconcile(df["Capital"], type_id="Q515")

    assert results.shape == (51, 7)


def test_reconcile_against_triple():

    gene_df = pd.DataFrame(
        {"gene": ["BRCA1", "MAPK10"], "species": ["Homo sapiens", "Homo sapiens"]}
    )

    results = reconcile(
        gene_df["gene"], type_id="Q7187", has_property=("P703", "Q15978631")
    )

    assert results["id"][0] == "Q227339"


# Edge cases


def test_fake_item():
    with raises(requests.HTTPError):
        reconcile(test_df["City"], type_id="FAKE_ITEM_GIVE_ERROR")


def test_fake_top_res():
    with raises(ValueError):
        reconcile(test_df["City"], type_id="Q515", top_res="I'm such a fake argument")
