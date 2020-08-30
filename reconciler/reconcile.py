from reconciler.webutils import return_reconciled_raw
import numpy as np
import pandas as pd


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
                current_df["type_qid"] = [item[0]["id"] for item in current_df["type"]]
                current_df["type"] = [item[0]["name"] for item in current_df["type"]]
            except IndexError:
                pass

        current_df["input_value"] = input_keys[idx]
        dfs.append(current_df)

    concatenated = pd.concat(dfs)

    return concatenated


def reconcile(column_to_reconcile, qid_type, top_res=1):
    """
    Reconcile a DataFrame column with Wikidata items

    This is the main function of this package, it takes in a Pandas Series,
    that is, a column of a DataFrame, and sends it for reconciliation. In
    order to return more confident results, the parameter qid_type corresponds
    to the type of item you're trying to reconcile against, that is, the item's
    'instance of' property. There is also a top_res argument, to filter the retrieved matches,
    this can be either an int, corresponding to the number of matches you want to
    retrieve for each reconciled item, or 'all', to return all matches.

    The time this function takes to run will depend on the number of unique items
    you have on your column, keep in mind that if you have a very large DataFrame, it
    may be easier to break it up in smaller pieces and reconcile each one individually.

    Args:
        column_to_reconcile (Series): A pandas Series corresponding to
            the column to be reconciled.
        qid_type (str): The Wikidata item type to reconcile against,
            corresponds to the item's 'instance of' property.
        top_res (int or str): The maximum number of matches to return for
            each reconciled item, defaults to one. To retrieve all matches,
            set it to 'all'.

    Returns:
        DataFrame: A Pandas DataFrame with the reconciled results.

    Raises:
        ValueError: top_res argument must be one of either 'all' or an integer.
    """
    input_keys, response = return_reconciled_raw(column_to_reconcile, qid_type)

    parsed = parse_raw_results(input_keys, response)

    full_df = parsed.drop(["features"], axis=1)

    if top_res == "all":
        return full_df
    elif isinstance(top_res, int):
        filtered = full_df.groupby("input_value").head(top_res).reset_index(drop=True)
        return filtered
    else:
        raise ValueError("top_res argument must be one of either 'all' or an integer")
