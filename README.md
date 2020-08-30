# reconciler

<!-- badges: start -->
[![license](https://img.shields.io/badge/license-BSD%202--Clause-green)](https://github.com/jvfe/reconciler/blob/master/LICENSE)
[![pytest status](https://github.com/jvfe/reconciler/workflows/Python%20package/badge.svg)](https://github.com/jvfe/reconciler/actions)
<!-- badges: end -->

`reconciler` is a python utility package to reconcile tabular data with [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), 
working similarly to what [OpenRefine](https://openrefine.org/) does, but entirely within Python, using Pandas.

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
reconciled = reconcile(test_df["City"], qid_type="Q515")
```

The resulting dataframe would look like this:

| id      | match   | name           |   score | type                   | type_qid   | input_value    |
|:--------|:--------|:---------------|--------:|:-----------------------|:-----------|:---------------|
| Q8678   | True    | Rio de Janeiro |     100 | city                   | Q515       | Rio de Janeiro |
| Q174    | True    | São Paulo      |     100 | city                   | Q515       | São Paulo      |
| Q131620 | True    | Natal          |     100 | municipality of Brazil | Q3184121   | Natal          |

Check out the [documentation](https://jvfe.github.io/reconciler/) for more advanced usage and to learn [how to contribute](https://jvfe.github.io/reconciler/contributing/).
