---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import pandas as pd
from fpl.data.azure_storage import AzureStorage
from fpl.data.io import to_csv
from dotenv import load_dotenv
from pathlib import Path
import os
```

```python
#!pip freeze
```

```python
# SETUP and Data Update
AZURE_STORAGE = "https://fantasy1337.blob.core.windows.net"


DATA_DIR_2020 = "../data/raw/fpldata2020/"
DATA_DIR_2021 = "../data/raw/fpldata2021/"
FIXTURES_2020 = "../data/raw/fpl-fixtures-2020/"
FIXTURES_2021 = "../data/raw/fpl-fixtures-2021/"

TRANSFORMED_DATA_2020 = "../data/transformed/transformed_data_2020.csv"
TRANSFORMED_DATA_2021 = "../data/transformed/transformed_data_2021.csv"
TRANSFORMED_DATA_TEAMS_2021 ="../data/transformed/transformed_teams_2021.csv"
TRANSFORMED_DATA_TEAMS_2020 ="../data/transformed/transformed_teams_2020.csv"
# Making sure data dirs exist
Path(DATA_DIR_2020).mkdir(parents=True, exist_ok=True)
Path(DATA_DIR_2021).mkdir(parents=True, exist_ok=True)
Path(TRANSFORMED_DATA_2020).parent.mkdir(parents=True, exist_ok=True)
Path(TRANSFORMED_DATA_2021).parent.mkdir(parents=True, exist_ok=True)


# 2020 data
data_client2020 = AzureStorage(AZURE_STORAGE, "fpldata2020")
data_client2020.download_new_blobs(DATA_DIR_2020)
fixtures_client2020 = AzureStorage(AZURE_STORAGE, "fpl-fixtures-2020")
fixtures_client2020.download_new_blobs(FIXTURES_2020)

# 2021 data
data_client2021 = AzureStorage(AZURE_STORAGE, "fpldata2021")
data_client2021.download_new_blobs(DATA_DIR_2021)
fixtures_client2021 = AzureStorage(AZURE_STORAGE, "fpl-fixtures-2021")
fixtures_client2021.download_new_blobs(FIXTURES_2021)

# Transforming data to .csv
to_csv(data_path = DATA_DIR_2020, save_path = TRANSFORMED_DATA_2020, entity = "elements")
to_csv(data_path = DATA_DIR_2021, save_path = TRANSFORMED_DATA_2021, entity = "elements")
to_csv(data_path = DATA_DIR_2021, save_path = TRANSFORMED_DATA_TEAMS_2021, entity = "teams")
to_csv(data_path = DATA_DIR_2020, save_path = TRANSFORMED_DATA_TEAMS_2020, entity = "teams", fixtures_path = FIXTURES_2020)
```

```python
#Reads final data of 2020 season
df_2020 = pd.read_csv(TRANSFORMED_DATA_2020)
df_2020 = df_2020.iloc[len(df_2020)-df_2020['id'].nunique():]
```

```python
#Reads 2021 player data
df_players = pd.read_csv(TRANSFORMED_DATA_2021)
df_players = df_players.iloc[len(df_players)-df_players['id'].nunique():]

```

```python
#Reads 2021 teams data
df_teams = pd.read_csv(TRANSFORMED_DATA_TEAMS_2021)
df_teams = df_teams.iloc[len(df_teams)-df_teams['id'].nunique():]
```

```python
#Calculate average match difficulty of next 5 matches for each team
df_teams["average_difficulty"] = (df_teams.opponent_0_difficulty +df_teams.opponent_1_difficulty + df_teams.opponent_2_difficulty +df_teams.opponent_3_difficulty +df_teams.opponent_4_difficulty)/5
```

```python
#Show 10 first rows of dataframe
df_players.iloc[:10]
```

```python
#Show all columns available
print(df_players.columns.to_list())
```

```python
#Select id, position, team and cost from players
df_selection = df_players[["id","second_name","element_type","team", "now_cost", "form"]]
```

```python
#Remove players with 0 in form
df_selection = df_selection.loc[df_selection.form > 0.0]
```

```python
#get average difficulty of next 5 games for each player
df_selection['fixtures_difficulty'] = df_selection.team.map(df_teams.set_index('id').average_difficulty)
```

```python
#calculate some self defined metric (let's try form / fixtures_difficulty)
df_selection['value'] = df_selection.form / df_selection.fixtures_difficulty
df_selection['value'] = df_selection['value'].round(2)

```

```python
#Group into different positions
df_goalkeepers = df_selection.loc[df_selection.element_type == 1]
df_defenders = df_selection.loc[df_selection.element_type == 2]
df_midfielders = df_selection.loc[df_selection.element_type == 3]
df_forwards = df_selection.loc[df_selection.element_type == 4]
```

```python
#Show X best rows based on 'value' metric defined above
df_forwards.sort_values([ "value"], ascending = [False]).iloc[:20]
```

```python

```

```python

```

```python

```

```python


