import pandas as pd

from reconciler.webutils import parse_raw_results, return_reconciled_raw


def reconcile(
    column_to_reconcile,
    type_id=None,
    top_res=1,
    property_mapping=None,
    reconciliation_endpoint="https://wikidata.reconci.link/en/api",
):
    """
    Reconcile a DataFrame column

    This is the main function of this package, it takes in a Pandas Series,
    that is, a column of a DataFrame, and sends it for reconciliation. In
    order to return more confident results, the parameter type_id corresponds
    to the type of item you're trying to reconcile against, that is, in case of a Wikidata item,
    it is the item's 'instance of' property. There is also a top_res argument,
    to filter the retrieved matches, this can be either an int, corresponding to the number of
    matches you want to retrieve for each reconciled item, or 'all', to return all matches.
    The property_mapping argument is an optional argument to denote particular triples to reconcile
    against, so you could, for example, reconcile against items of a particular type, that have
    a specific property equals to some specific value. The reconciliation_endpoint argument corresponds
    to the reconciliation service you're trying to access, if no value is given, it will default to
    the Wikidata reconciliation endpoint. See <https://reconciliation-api.github.io/testbench/> for a
    list of available endpoints.

    Args:
        column_to_reconcile (Series): A pandas Series corresponding to
            the column to be reconciled.
        type_id (str): The item type to reconcile against, in case of a
            wikidata item, it corresponds to the item's 'instance of' QID.
        top_res (int or str): The maximum number of matches to return for
            each reconciled item, defaults to one. To retrieve all matches,
            set it to 'all'.
        property_mapping (dict): Property-column mapping of the items you want to
            reconcile against. For example, {"P17": df['country']} to reconcile
            against items that have the property country equals to the values
            in the column country. This is optional and defaults to None.
        reconciliation_endpoint (str): The reconciliation endpoint, defaults
            to the Wikidata reconciliation endpoint.

    Returns:
        DataFrame: A Pandas DataFrame with the reconciled results.

    Raises:
        ValueError: top_res argument must be one of either 'all' or an integer.
    """

    input_keys, response = return_reconciled_raw(
        column_to_reconcile,
        type_id,
        property_mapping,
        reconciliation_endpoint,
    )

    full_df = parse_raw_results(input_keys, response)

    if top_res == "all":
        return full_df
    elif isinstance(top_res, int):
        filtered = full_df.groupby("input_value").head(top_res).reset_index(drop=True)
        return filtered
    else:
        raise ValueError("top_res argument must be one of either 'all' or an integer")
