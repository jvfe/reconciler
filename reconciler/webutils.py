from collections import defaultdict
from functools import lru_cache
import json
import requests
import numpy as np
import pandas as pd


def get_query_dict(df_column, type_id, has_property):
    """
    Convert a pandas DataFrame column to a query dictionary

    The reconciliation API requires a json request formatted in a
    very particular way. This function takes in a DataFrame column
    and reformats it.

    Args:
        df_column (Series): A pandas Series to reconcile.
        type_id (str): A string specifying the item type to reconcile against,
            in Wikidata this corresponds to the 'instance of' property of an item.

    Returns:
        tuple: A tuple containing the list of the original values
            sent to reconciliation a dictionary with the
            column values reformatted.
    """
    input_keys = df_column.unique()
    reformatted = defaultdict(dict)

    for idx, value in enumerate(input_keys):

        if (type_id and has_property) is not None:
            reformatted[idx] = {
                "query": value,
                "type": type_id,
                "properties": [{"pid": has_property[0], "v": {"id": has_property[1]}}],
            }
        elif type_id is not None:
            reformatted[idx] = {"query": value, "type": type_id}
        else:
            reformatted[idx] = {"query": value}

    return input_keys, reformatted


@lru_cache(maxsize=None)
def perform_query(query_string, reconciliation_endpoint):
    """Make a post request to the reconciliation API

    Args:
        query_string (str): A string corresponding to the query JSON.
        reconciliation_endpoint (str): A url to the reconciliation endpoint.

    Returns:
        dict: A dictionary (JSON) with the query results.

    Raises:
        requests.HTTPError: The query returned an error, check if you mistyped an argument.
        requests.ConnectionError: Couldn't connect to reconciliation client.

    """

    tries = 0
    while tries < 3:
        try:
            response = requests.post(
                reconciliation_endpoint, data=json.loads(query_string)
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


def return_reconciled_raw(df_column, type_id, has_property, reconciliation_endpoint):
    """Send reformatted dict for reconciliation

    This is just a wrapper around the other utility functions. The
    only thing it actually does is convert the query dict to an
    appropriate JSON string.

    Args:
        df_column (Series): A pandas Series to reconcile.
        type_id (str): A string specifying the item type to reconcile against,
            in Wikidata this corresponds to the 'instance of' property of an item.
        reconciliation_endpoint (str): A url to the reconciliation endpoint.

    Returns:
        tuple: A tuple containing the list of the original values
            sent to reconciliation and a dictionary (JSON)
            with the query results.

    """

    input_keys, reformatted = get_query_dict(df_column, type_id, has_property)
    reconcilable_data = json.dumps({"queries": json.dumps(reformatted)})
    query_result = perform_query(reconcilable_data, reconciliation_endpoint)

    return input_keys, query_result


def parse_raw_results(input_keys, response):
    """
    Parse JSON query result

    Args:
        input_keys (list): A list with the original input values
            that were used to reconcile.
        response (dict): A dict corresponding to the raw JSON response
            from the reconciliation API.

    Returns:
        DataFrame: A Pandas DataFrame with all the results.
    """

    res_keys = sorted(response.keys(), key=int)

    dfs = []
    for idx, key in enumerate(res_keys):

        current_df = pd.json_normalize(response[key]["result"])

        if current_df.empty:
            current_df = pd.DataFrame(
                {
                    "id": [np.NaN],
                    "match": [False],
                }
            )
        else:
            try:
                current_df.drop(["features"], axis=1, inplace=True)
                current_df["type_id"] = [item[0]["id"] for item in current_df["type"]]
                current_df["type"] = [item[0]["name"] for item in current_df["type"]]
            except IndexError:
                pass

        current_df["input_value"] = input_keys[idx]
        dfs.append(current_df)

    concatenated = pd.concat(dfs)

    return concatenated
