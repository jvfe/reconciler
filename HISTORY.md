# History

### 0.1.0 (2020-08-30)

* First release on PyPI.

### 0.1.1 (2020-09-04)

* Adds reconciliation_endpoint argument, so the user can define the service (Defaults to Wikidata)
* Changes qid_type argument to be called type_id.

### 0.1.2 (2020-09-24)

* Dataframes with more than 10 rows are now split in multiple dataframes, to avoid timeouts due to large requests.

* Adds a tqdm progress bar for the reconciliation.

### 0.1.3 (2020-09-26)

* Adds a new argument to the main function, has_property, which allows to reconcile against specific property-value pairs.

### 0.1.4 (2020-10-14)

* Makes the type_id argument optional, to allow reconciliation against any term.

### 0.1.5 (2020-10-27)

* Fixes bug on reconciler.reconcile when parsing empty results.

### 0.1.6 (2020-12-20)

* Minor styling fixes, start using isort.