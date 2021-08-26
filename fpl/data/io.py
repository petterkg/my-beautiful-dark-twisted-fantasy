"""IO module."""
import json
import os
from datetime import datetime, timedelta
from json import encoder
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from fpl.data.transformations import (
    add_gw_and_download_time,
    add_unique_id,
    get_game_week,
)


def load_json(file_path: str) -> dict:
    """Load json file.

    Args:
        file_path (str): path to file in format .json

    Returns:
        dict: decoded json
    """
    with open(Path(file_path), encoding="utf-8") as json_file:
        try:
            return json.load(json_file, encoding="UTF-8")
        except json.decoder.JSONDecodeError:
            print("Unable to load json")


def dump_json(file_path: str, data: dict):
    """Dump dict to .json file.

    Args:
        file_path (str): filepath to write
        data (dict): data to write
    """
    with open(Path(file_path), "w", encoding="utf-8") as download_file:
        json.dump(data, download_file, ensure_ascii=False, indent=4)


def load_dataframe_from_json(file_path: str, object_to_grab: str) -> object:
    """Load JSON into dataframe.

    Args:
        file_path (str): Path to .json file
        object_to_grab (stri): Key to object to grab

    Returns:
        pandas.DataFrame: dataframe holding json-object
    """
    json_object = load_json(file_path)
    try:
        return pd.DataFrame(json_object[str(object_to_grab)])
    except KeyError:
        print("Key not found")
    except Exception:
        print("Could not load dataframe")


def list_data_dir(dir_path: str, suffix=".json") -> list:
    """List content of a data directory.

    Args:
        dir_path (str): Path to directory to list
        suffix (str, optional): Filter content based on file suffix. Defaults to ".json".

    Returns:
        list: List holding names of files in directory
    """
    return sorted([Path(dir_path, i) for i in os.listdir(dir_path) if Path(i).suffix == suffix])


def get_description_dict(dataframe: pd.DataFrame) -> dict:
    """Return dict with data descripton fields based on dataframe columns.

    Args:
        dataframe (pandas.DataFrame): Dataframe to generate data description schema for

    Returns:
        dict: Dict holding data description based on df columns
    """
    return {
        i: {
            "change": "None",
            "description": "None",
            "notes": {
                "personal_notes": "None",
                "official_explanation": "None",
                "referance": "None",
            },
            "data_type": "None",
            "type": "None",
            "calculated": "cumulative_sum",
        }
        for i in dataframe.columns
    }


def fix_encoding(data_dir_path: str):
    """Fix files saved in ASCII, overwrites to UTF-8.

    Args:
        data_dir_path (str): Path to directory to fix ascii to utf-8
    """
    for i in list_data_dir(data_dir_path):
        with open(Path(i), "rb", encoding="utf-8") as file:
            json_file = json.load(file, encoding="UTF-8")

        with open(Path("i"), "w", encoding="utf-8") as file:
            json.dump(json_file, file, ensure_ascii=False, indent=4)


def to_csv(
    entity="teams",
    data_path="data",
    save_path="data_transformed.csv",
    fixtures_path="../data/raw/fpl-fixtures-2021/",
):
    """Transform data and save as CSV.

    Args:
        data_path (str, optional): Path to dir holding JSON dumps. Defaults to "data".
        save_path (str, optional): Path to save transformed CSV. Defaults to "data_transformed.csv".
    """
    all_data = []
    print(fixtures_path)
    fixtures_list = list_data_dir(fixtures_path)
    for data in tqdm(list_data_dir(data_path), desc="Compiling DataFrame"):
        # Fails if JSON is malformed.
        try:
            with open(data, encoding="utf-8") as file:
                x = json.load(file, encoding="UTF-8")
                add_gw_and_download_time(x[entity], x["download_time"], get_game_week(x["events"]))
        except json.decoder.JSONDecodeError:
            print(f"cant load data from {data}")

        # Fails if loaded dict does not contain expected keys.
        if entity == "teams":
            fixtures = load_json(_nearest(fixtures_list, x["download_time"]))
            all_fixtures_list = create_opponents(fixtures)
            list(map(lambda y: _add_next_opponents(y, x[entity], all_fixtures_list), x[entity]))
        # Workaround to show progress bar when writing really large DF to CSV.
        all_data.extend(x[entity])
    df = pd.DataFrame(all_data)
    chunks = np.array_split(df.index, 100)
    for chunck, subset in enumerate(tqdm(chunks, desc="Writing CSV")):
        if chunck == 0:  # first row
            df.loc[subset].to_csv(save_path, mode="w", index=True)
        else:
            df.loc[subset].to_csv(save_path, header=None, mode="a", index=True)


def _nearest(items, pivot):
    if isinstance(items[0], str):
        items = [(datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f"), i) for i in items]
    else:
        items = [
            (datetime.strptime(i.name.split(".")[0].split("_")[0], "%Y-%m-%dT%H-%M-%SZ"), i)
            for i in items
        ]
    if isinstance(pivot, str):
        pivot = datetime.strptime(pivot, "%Y-%m-%d %H:%M:%S.%f")

    return min(
        items, key=lambda x: abs(x[0] - pivot) if (x[0] <= pivot) else timedelta(days=100000)
    )[1]


def _elaborate_opponent(opponent, teams_data, num):
    opponent_data = teams_data[opponent["team_id"]]
    return {
        f"opponent_{num}_name": opponent_data["name"],
        f"opponent_{num}_venue": opponent["venue"],
        f"opponent_{num}_difficulty": opponent["difficulty"],
        f"opponent_{num}_strengh_attack": opponent_data["strength_attack_home"]
        if opponent[f"venue"] == "h"
        else opponent_data["strength_attack_away"],
        f"opponent_{num}_strengh_defence": opponent_data["strength_defence_home"]
        if opponent[f"venue"] == "h"
        else opponent_data["strength_defence_away"],
        # Have to check for NaN by comparing NaN == NaN returns False.
        f"opponent_{num}_played_in_gw": int(opponent["gameweek"])
        if isinstance(opponent["gameweek"], (int, float))
        and opponent["gameweek"] == opponent["gameweek"]
        else -1,
    }


def _add_next_opponents(team, teams: dict, all_fixtures: list, num_opponents=5):
    """Add next 5 fixtures to an element.
    Args:
        element (dict): Player element from /bootstrap-static
        all_teams (list): All teams element from /boostrap-static
    """
    if not isinstance(teams, dict):
        teams = {i["id"]: i for i in teams}
    for num, opponent in enumerate(
        all_fixtures[team["id"]][team["gameweek"] : team["gameweek"] + 5]
    ):
        team.update(_elaborate_opponent(opponent, teams, num))


def create_opponents(fixtures: dict, sort=False) -> dict:
    """Return the fixtures list for each PL team.
    Args:
        fixtures (dict, optional): fixtures
        sort (boolean, optional): Sort opponents on gameweek. Defaults to False.
    Returns:
        dict: {team_id: [{team_id: int, difficulty: int, venue: str}]}
    """
    all_teams = {}
    for team_id in range(1, 21):
        opponents = []
        for event in fixtures["fixtures"]:
            if event["team_h"] == team_id:
                opponents.append(
                    {
                        "team_id": event["team_a"],
                        "difficulty": event["team_h_difficulty"],
                        "venue": "h",
                        "gameweek": event["event"],
                    }
                )
            if event["team_a"] == team_id:
                opponents.append(
                    {
                        "team_id": event["team_h"],
                        "difficulty": event["team_a_difficulty"],
                        "venue": "a",
                        "gameweek": event["event"],
                    }
                )

        if sort:
            all_teams[team_id] = sorted(
                opponents, key=lambda i: i["gameweek"] if i["gameweek"] else 99999
            )
        else:
            all_teams[team_id] = opponents
    return all_teams
