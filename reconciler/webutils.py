from collections import defaultdict
from functools import lru_cache
import json
import requests
import pandas as pd


def get_query_dict(df_column, qid_type):
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

        reformatted[idx] = {"query": value, "type": qid_type}

    return input_keys, reformatted


@lru_cache(maxsize=None)
def perform_query(query_string):

    tries = 0
    print("Reconciling...")
    while tries < 3:
        try:
            response = requests.post(
                "https://wikidata.reconci.link/en/api", data=json.loads(query_string)
            )
        except requests.ConnectionError:
            tries += 1
        else:
            query_result = response.json()
            if "status" in query_result and query_result["status"] == "error":
                raise requests.HTTPError(
                    "The query returned an error, check if you mistyped an argument."
                )
            else:
                return query_result
    if tries == 3:
        raise requests.ConnectionError("Couldn't connect to reconciliation client")


def return_reconciled_raw(df_column, qid_type):
    """Send reformatted dict for reconciliation"""

    input_keys, reformatted = get_query_dict(df_column, qid_type)
    reconcilable_data = json.dumps({"queries": json.dumps(reformatted)})
    query_result = perform_query(reconcilable_data)

    return input_keys, query_result