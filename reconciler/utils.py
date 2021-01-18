from itertools import islice

import pandas as pd


def create_property_array(df_column, property_mapping, current_value):

    prop_mapping_list = []
    for key, value in property_mapping.items():

        prop_value = (
            value.loc[df_column == current_value].to_string(index=False).strip()
        )

        prop_mapping_list.append({"pid": key, "v": prop_value})

    return prop_mapping_list


def chunk_dictionary(data, size=10):
    # https://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}
