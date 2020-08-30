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

| cell                      | tissue   | cell_ontology_class   | cell_ontology_term_iri                    | cell_ontology_id   |
|:--------------------------|:---------|:----------------------|:------------------------------------------|:-------------------|
| 10X_P4_3_AAAGTAGAGATGCCAG | Bladder  | mesenchymal cell      | http://purl.obolibrary.org/obo/CL_0008019 | CL:0008019         |
| 10X_P4_3_AACCGCGTCCAACCAA | Bladder  | mesenchymal cell      | http://purl.obolibrary.org/obo/CL_0008019 | CL:0008019         |
| 10X_P4_3_AACTCCCGTCGGGTCT | Bladder  | mesenchymal cell      | http://purl.obolibrary.org/obo/CL_0008019 | CL:0008019         |
| 10X_P4_3_AACTCTTAGTTGCAGG | Bladder  | bladder cell          | http://purl.obolibrary.org/obo/CL_1001319 | CL:1001319         |
| 10X_P4_3_AACTCTTTCATAACCG | Bladder  | mesenchymal cell      | http://purl.obolibrary.org/obo/CL_0008019 | CL:0008019         |

Filtering only the unique pairs:

```python
unique_cells = cell_table.drop_duplicates(subset=['tissue', 'cell_ontology_class'])
```

### Reconciliation

Reconciling, against cell type (Q189118), returning the first 2 matches for each item:

This step will take a while to complete, varying according to your upload speed,
here it took around a minute.

```python
reconciled = reconcile(unique_cells['cell_ontology_class'], qid_type="Q189118", top_res=2)
reconciled.head(10)
```

The output I got:

| id        | match   | name                                          |   score | type      | type_qid   | input_value              |
|:----------|:--------|:----------------------------------------------|--------:|:----------|:-----------|:-------------------------|
| Q1922379  | True    | mesenchymal stem cells                        |   100   | cell type | Q189118    | mesenchymal cell         |
| Q66563456 | False   | epithelial cell of gall bladder               |    28   | []        | nan        | bladder cell             |
| Q66568549 | False   | urothelial cell of trigone of urinary bladder |    21   | []        | nan        | bladder cell             |
| Q11394395 | False   | endothelial cells                             |    50   | []        | nan        | endothelial cell         |
| Q68620792 | False   | human sinusoidal endothelial cell             |    32.5 | []        | nan        | endothelial cell         |
| Q66590632 | False   | basal cell of urothelium                      |    50   | []        | nan        | basal cell of urothelium |
| Q66590636 | False   | basal cell layer of urothelium                |    44.5 | []        | nan        | basal cell of urothelium |
| Q223143   | False   | granulocyte                                   |    67   | cell type | Q189118    | leukocyte                |
| Q1775422  | False   | agranulocyte                                  |    60   | cell type | Q189118    | leukocyte                |
| Q463418   | True    | fibroblast                                    |   100   | cell type | Q189118    | fibroblast               |

Now if you look at the object, you will see the matches retrieved for each item.

Interestingly, as of 30 Aug. 2020, there's not a lot of cell type data present in Wikidata, 
**a lot of the matches didn't even return a "type" value!** That means they don't even have an 
'instance of' property. This could be very interesting to look into, and add this information.