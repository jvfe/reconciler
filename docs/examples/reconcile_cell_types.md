# Reconciling cell types

In this showcase we'll try to reconcile some cell-type data from the [Tabula muris](https://tabula-muris.ds.czbiohub.org/)
dataset.

First off, let's load the necessary packages and read in the data using Pandas.
For speed and simplicity, I'll only be reconciling the unique tissue/cell_ontology_class pairs. 

### Pre-processing

```python
from reconciler import reconcile
import pandas as pd

data_url = "https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/10039264/annotations_droplets.csv"

cell_table = pd.read_csv(data_url)
cell_table.head()
```

Filtering only the unique pairs:

```python
unique_cells = cell_table.drop_duplicates(subset=['tissue', 'cell_ontology_class'])
```

### Reconciliation

Reconciling, against type cell (Q7868), returning the first 2 matches for each item:

This step will take a while to complete, varying according to your upload speed,
here it took around a minute.

```python
reconciled = reconcile(unique_cells['cell_ontology_class'], qid_type="Q7868", top_res=2)
reconciled.head(10)
```

The output I got:

| id        | match   | name                              |   score | type      | input_value              | type_qid   |
|:----------|:--------|:----------------------------------|--------:|:----------|:-------------------------|:-----------|
| Q66568500 | False   | mesenchymal cell                  |    50   | []        | mesenchymal cell         | nan        |
| Q66576417 | False   | protoplasm of mesenchymal cell    |    35   | []        | mesenchymal cell         | nan        |
| Q54952164 | False   | SBC-2                             |    25   | cell line | bladder cell             | Q21014462  |
| Q54952183 | False   | SBC-7                             |    25   | cell line | bladder cell             | Q21014462  |
| Q11394395 | False   | endothelial cells                 |    50   | []        | endothelial cell         | nan        |
| Q68620792 | False   | human sinusoidal endothelial cell |    32.5 | []        | endothelial cell         | nan        |
| Q66590632 | False   | basal cell of urothelium          |    50   | []        | basal cell of urothelium | nan        |
| Q66590636 | False   | basal cell layer of urothelium    |    44.5 | []        | basal cell of urothelium | nan        |
| Q42395    | False   | white blood cells                 |    50   | []        | leukocyte                | nan        |
| Q71228927 | False   | Leukocyte Rolling                 |    34.5 | []        | leukocyte                | nan        |

Now if you look at the object, you will see the matches retrieved for each item.

Interestingly, as of 30 aug. 2020, there's not a lot of cell type data present in Wikidata, 
**a lot of the matches didn't even return a "type" value!** That means they don't even have an 
'instance of' property. This could be very interesting to look into, and add this information.