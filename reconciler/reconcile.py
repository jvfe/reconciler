from collections import defaultdict
import json
import requests
import pandas as pd

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal"],
        "Inutil": ["bla", "blabla", "blablabla", "blablabla"],
    }
)


def get_query_dict(df_column):
    """Convert a pandas DataFrame column to a query dictionary

    The reconciliation API requires a json request formatted in a
    very particular way. This function takes in a DataFrame column
    and reformats it.

    Args:
        df_column: A pandas dataframe column.

    Returns:
        A dict with the column values reformatted.
    """
    values = df_column.unique()
    reformatted = defaultdict(dict)

    for idx, value in enumerate(values):

        reformatted[f"q{idx}"] = {"query": value}

    return reformatted


def reconcile_column(df_column):
    """Send reformatted dict for reconciliation"""

    reformatted = get_query_dict(df_column)
    reconcilable = {"queries": json.dumps(reformatted)}

    response = requests.post("https://wikidata.reconci.link/en/api", data=reconcilable)

    return response.json()