# Fantasy Premier League 2021/2022

Inspired by the following tutorial:
https://towardsdatascience.com/fantasy-premier-league-value-analysis-python-tutorial-using-the-fpl-api-8031edfe9910


### Dataset
The dataset from Fantasy Premier League is accessed  by folling this link.
https://fantasy.premierleague.com/api/bootstrap-static/

As of now the dataset is downloaded every 6th hour (UTC) and stored as as Azure blob "snapshot" with the format
```
%Y-%m-%dT%H:%M:%SZ_data.json
```

For now access to the blob demands a "connection string" that can be required by the repo owner. Used together with the azure_storage.py module.
```python
# Download all new data from Azure Blob Storage to disk
$ fantasy download-all -d <PATH_TO_DIR_TO_STORE_DATA>
```


API - Other useful methods

* Fixtures: https://fantasy.premierleague.com/api/fixtures/
* A single teams hostory: https://fantasy.premierleague.com/api/entry/{}/history/
* A single teams score: https://fantasy.premierleague.com/api/entry/{team-id}/
* Score in a specific "classic"-league: https://fantasy.premierleague.com/api/leagues-classic/{league-id}/standings/
* Score in a specific "H2H"-league: https://fantasy.premierleague.com/api/leagues-h2h/{league-id}/standings/
* Latest transfers: https://fantasy.premierleague.com/api/entry/{team-id}/transfers-latest/
* My Team https://fantasy.premierleague.com/api/my-team/{team-id}/ *

*To use the "my team api" authentication is required. See following link
https://medium.com/@bram.vanherle1/fantasy-premier-league-api-authentication-guide-2f7aeb2382e4)

### Other useful links

* Reddit-thread about FPL API
    https://www.reddit.com/r/FantasyPL/comments/c64rrx/fpl_api_url_has_been_changed/
* Blogpost about FPL API (its a little old, but change drf with api and it seems to work)
    https://medium.com/@YourMumSaysWhat/how-to-get-data-from-the-fantasy-premier-league-api-4477d6a334c3
* Historic data for the FPL
    https://github.com/vaastav/Fantasy-Premier-League

