import pandas as pd
import yaml
from pandas import DataFrame
import sys


try:
    data_source = sys.argv[1]
except IndexError:
    raise ValueError("Missing argument. Please provide a data source.") from None

with open("./src/config.yml") as file:
    config = yaml.safe_load(file)


def generate_column_json(df: DataFrame) -> dict:
    """
    Generate a json string with the column names and types from df.
    """

    columns = df.columns
    column_types = df.dtypes
    column_json = {}
    for i in range(len(columns)):
        column_json[columns[i]] = str(column_types[i])
    return column_json


def update_config_columns(data_source: str, column_json: dict, path: str) -> None:
    """
    Update the config.yml file with the column names and types for the specified data source.

    Parameters:
    data_source (str): The data source to update.
    column_json (dict): A dictionary with the column names and types.
    path (str): The path to the config.yml file.

    Returns:
    None
    """
    with open(path) as file:
        config = yaml.safe_load(file)

    config["data_source"][data_source]["columns"] = column_json

    with open(path, "w") as file:
        yaml.dump(config, file)


def main():
    file_path = f"./data/raw/{config['data_source'][data_source]['file_name']}"
    df = pd.read_csv(file_path)
    column_json = generate_column_json(df)
    update_config_columns(data_source, column_json, path="./src/config.yml")


if __name__ == "__main__":
    main()
