from .webutils import return_reconciled_raw
import numpy as np
import pandas as pd


def parse_raw_results(input_keys, response):

    res_keys = sorted(response.keys())

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
            current_df["type_qid"] = [item[0]["id"] for item in current_df["type"]]
            current_df["type"] = [item[0]["name"] for item in current_df["type"]]

        current_df["input_value"] = input_keys[idx]
        dfs.append(current_df)

    concatenated = pd.concat(dfs)

    return concatenated


def reconcile(column_to_reconcile, qid_type, top_res=1):

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
