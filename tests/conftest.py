import pandas as pd
import pytest

from reconciler.utils import get_query_dict


@pytest.fixture
def city_data():

    test_df = pd.DataFrame(
        {
            "City": [
                "Rio de Janeiro",
                "São Paulo",
                "São Paulo",
                "Natal",
                "FAKE_CITY_HERE",
            ],
        }
    )

    return test_df


@pytest.fixture
def gene_data():

    gene_df = pd.DataFrame(
        {"gene": ["BRCA1", "MAPK10"], "species": ["Q15978631", "Q15978631"]}
    )

    return gene_df


@pytest.fixture
def us_capitals():

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

    return us_capitals


@pytest.fixture
def endpoints():

    test_endpoints = [
        "https://wikidata.reconci.link/en/api",
        "https://services.getty.edu/vocab/reconcile/",
    ]

    return test_endpoints


@pytest.fixture
def reformatted(city_data):

    _, reformatted = get_query_dict(
        city_data["City"], type_id="Q515", property_mapping=None
    )

    return reformatted
