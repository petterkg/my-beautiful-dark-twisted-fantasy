---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import pandas as pd
from fpl.data.azure_storage import AzureStorage
from fpl.data.io import to_csv
from dotenv import load_dotenv
from pathlib import Path
```

```python
# SETUP

DATA_DIR_2020 = "../data/2020"
DATA_DIR_2021 = "../data/2021"
TRANSFORMED_DATA_2020 = "../transformed_2020.csv"
TRANSFORMED_DATA_2021 = "..//transformed_2021.csv"

# Making sure data dirs exist
Path(DATA_DIR_2020).mkdir(parents=True, exist_ok=True)
Path(DATA_DIR_2021).mkdir(parents=True, exist_ok=True)

# loading secrets from .env
load_dotenv()

# 2020 data
client2020 = AzureStorage(os.getenv("AZURE_STORAGE_CONNECTION_STRING"), "fpldata2020")
client2020.download_new_blobs(DATA_DIR_2020)

# 2021 data
client2021 = AzureStorage(os.getenv("AZURE_STORAGE_CONNECTION_STRING"), "fpldata2021")
client2021.download_new_blobs(DATA_DIR_2021)

# Transforming data to .csv
to_csv(DATA_DIR_2020, TRANSFORMED_DATA_2020)
to_csv(DATA_DIR_2021, TRANSFORMED_DATA_2021)
```

```python

```

```python
df = pd.read_csv(TRANSFORMED_DATA_2020)
```

```python
# Last inn data om lag

import json

with open("../data/2020-09-12T08-24-34Z_data.json") as file:
    data = json.load(file)
teams = pd.DataFrame(data["teams"])
teams = teams.sort_values(by=['strength_overall_home'], ascending=False)
teams

with open("../data/2021-06-28T06-01-19Z_data.json") as file:
    data = json.load(file)
teams = pd.DataFrame(data["teams"])
teams = teams.sort_values(by=['strength_overall_home'], ascending=False)
teams
```

```python
# Last inn sortert liste over tilgjengelige data dumps

from fpl.data.io import list_data_dir

# Selvskrevet metode
all_data_list = list_data_dir("../data")

# Første data dump
all_data_list[0]

# Siste data dump
all_data_list[-1]

# Midterste data dump
all_data_list[int(len(all_data_list)/2)]

with open(all_data_list[-1]) as file:
    data = json.load(file)



```

```python

```

```python
df
```

```python
# Select columns
selected_df = df[["id", "gameweek"]]
selected_df
```

```python
# Filtrer datafram
filter = df[df["player_id"] > 40]
filter
```

```python

```

```python
from fpl.visualization.exploration import reorder_elements

df = reorder_elements(df)
df
```

```python

```
