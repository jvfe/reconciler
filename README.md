# reconciler

<!-- badges: start -->
[![license](https://img.shields.io/badge/license-BSD%202--Clause-green)](https://github.com/jvfe/reconciler/blob/master/LICENSE)
[![pytest status](https://github.com/jvfe/reconciler/workflows/pytest/badge.svg)](https://github.com/jvfe/reconciler/actions)
[![documentation status](https://github.com/jvfe/reconciler/workflows/docs/badge.svg)](https://jvfe.github.io/reconciler/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4088488.svg)](https://doi.org/10.5281/zenodo.4088488)
<!-- badges: end -->

`reconciler` is a python package to reconcile tabular data with various reconciliation services, such as 
[Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), working similarly to what [OpenRefine](https://openrefine.org/) 
does, but entirely within Python, using Pandas.

## Quickstart

You can install the latest version of reconciler from PyPI with:

``` bash
pip install reconciler
```

Then to use it:

```python
from reconciler import reconcile
import pandas as pd

# A DataFrame with a column you want to reconcile.
test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal"],
    }
)

# Reconcile against type city (Q515), getting the best match for each item.
reconciled = reconcile(test_df["City"], type_id="Q515")
```

The resulting dataframe would look like this:

| id      | match   | name           |   score | type                   | type_id   | input_value    |
|:--------|:--------|:---------------|--------:|:-----------------------|:-----------|:---------------|
| Q8678   | True    | Rio de Janeiro |     100 | city                   | Q515       | Rio de Janeiro |
| Q174    | True    | São Paulo      |     100 | city                   | Q515       | São Paulo      |
| Q131620 | True    | Natal          |     100 | municipality of Brazil | Q3184121   | Natal          |

In case you want to ensure the results are cities from Brazil, you can specify the has_property argument with
a specific property-value pair:

```python
# Reconcile against type city (Q515) and items have the country (P17) property equals to Brazil (Q155)
reconciled = reconcile(test_df["City"], type_id="Q515", has_property=("P17", "Q155"))
```

## Other very useful packages

Although my opinion may be biased, I think `reconciler` is a pretty nice package.
But the thing is, it probably won't fulfill all your Wikidata-related needs.
Here are other packages that could help with that:

* [WikidataIntegrator](https://github.com/SuLab/WikidataIntegrator) has a lot of very nice, low-level, functions 
    for dealing with various wikidata-related activities, such as item acquisition and programmatic editing.

* [wikidata2df](https://github.com/jvfe/wikidata2df) is a very simple utility package for quickly and easily
    turning wikidata SPARQL queries into Pandas DataFrames.