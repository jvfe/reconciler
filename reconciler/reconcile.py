from collections import defaultdict
from functools import lru_cache
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
    input_keys = df_column.unique()
    reformatted = defaultdict(dict)

    for idx, value in enumerate(input_keys):

        reformatted[f"q{idx}"] = {"query": value}

    return input_keys, reformatted


@lru_cache(maxsize=32)
def perform_query(query_string):

    tries = 0
    while tries < 3:
        try:
            response = requests.post(
                "https://wikidata.reconci.link/en/api", data=json.loads(query_string)
            )
        except requests.ConnectionError:
            tries += 1
        else:
            return response.json()
    if tries == 3:
        raise requests.ConnectionError("Couldn't connect to reconciliation client")


def return_reconciled_raw(df_column):
    """Send reformatted dict for reconciliation"""

    input_keys, reformatted = get_query_dict(df_column)
    reconcilable_data = json.dumps({"queries": json.dumps(reformatted)})
    query_result = perform_query(reconcilable_data)

    return input_keys, query_result


def reconcile(column_to_reconcile, top_res=1):

    input_keys, response = return_reconciled_raw(column_to_reconcile)
    res_keys = sorted(response.keys())

    dfs = []
    for idx, key in enumerate(res_keys):
        current_df = pd.json_normalize(response[key]["result"])
        current_df["input_value"] = input_keys[idx]
        dfs.append(current_df)

    full_df = pd.concat(dfs).drop(["features"], axis=1)
    full_df["type"] = [item[0]["name"] for item in full_df["type"]]

    filtered = full_df.groupby("input_value").head(top_res).reset_index(drop=True)

    return filtered