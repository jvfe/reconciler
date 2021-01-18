from itertools import islice
from collections import defaultdict

import pandas as pd


def create_property_array(df_column, property_mapping, current_value):
    """
    Create a query JSON 'properties' array

    Creates the properties array necessary for when the property_mapping is defined.

    Args:
        df_column (Series): A pandas Series to reconcile.
        property_mapping (dict): The property-column mapping dictionary.
        current_value (str): Current iteration through the input_keys

    Returns:
        list: A list of dictionaries corresponding to the properties.
    """

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
        property_mapping (dict): Property-column mapping of the items you want to
            reconcile against. For example, {"P17": df['country']} to reconcile
            against items that have the property country equals to the values
            in the column country. This is optional and defaults to None.
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
    """
    Split a large dictionary into equal-sized dictionaries

    Args:
        data (dict): The dictionary to be split.
        size (int): The size the smaller dictionaries are supposed to be.

    Returns:
        dict: A subdivision of the larger dictionary, of the
            corresponding size.
    """
    # https://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}
