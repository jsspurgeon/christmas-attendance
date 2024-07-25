# convert data into time series.
import pandas as pd
import yaml
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def process_data():
    # Load the data
    with open("./src/config.yml", "r") as f:
        config = yaml.safe_load(f)
        data_file = f"./data/raw/{config['data_source']['attendance']['file_name']}"

    df = pd.read_csv(data_file)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    column_names = [
        "service_date_time",
        "site_description",
        "ministry_description",
        "service_description",
        "activity_type_description",
        "metric_name",
        "entry_note",
        "entry_value",
    ]
    df = df[column_names]

    # Convert data into time series
    df["service_date_time"] = pd.to_datetime(df["service_date_time"])

    # Save the time series file
    output_file = "data/processed/time_series.csv"
    df.to_csv(output_file, index=False)

    logging.info(f"Time series data saved to {output_file}")


def main():
    process_data()


if __name__ == "__main__":
    main()
