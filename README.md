# Pandaseda
Functional for exploratory data analysis.

See Example.ipynb for more details

## installation:
```bash
pip install git+https://github.com/Aykhan-sh/pandaseda@master
```
Upgrade:
```bash
pip install --upgrade git+https://github.com/Aykhan-sh/pandaseda@master
```
## Usage
```python
import pandas as pd
from pandaseda.Functional import Describe
titanic = pd.read_csv('train.csv')
desc = Describe(titanic)
desc.display()
```
