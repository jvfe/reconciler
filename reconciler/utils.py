from itertools import islice
from collections import defaultdict

import pandas as pd


def create_property_array(df_column, property_mapping, current_value):

    prop_mapping_list = []
    for key, value in property_mapping.items():

        prop_value = (
            value.loc[df_column == current_value].to_string(index=False).strip()
        )

        prop_mapping_list.append({"pid": key, "v": prop_value})

    return prop_mapping_list


def get_query_dict(df_column, type_id, property_mapping):
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

        reformatted[idx]["query"] = value

        if type_id is not None:
            reformatted[idx]["type"] = type_id
        if property_mapping is not None:
            reformatted[idx]["properties"] = create_property_array(
                df_column, property_mapping, value
            )

    return input_keys, reformatted


def chunk_dictionary(data, size=10):
    # https://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}
