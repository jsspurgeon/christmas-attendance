import logging
import pandas as pd
import holidays

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def add_time_features(time_series: pd.DataFrame) -> None:
    time_series['day_of_week'] = pd.to_datetime(time_series['service_date_time']).dt.day_name()
    time_series['day_of_month'] = pd.to_datetime(time_series['service_date_time']).dt.day
    time_series['hour'] = pd.to_datetime(time_series['service_date_time']).dt.hour
    time_series['month'] = pd.to_datetime(time_series['service_date_time']).dt.month
    time_series['year'] = pd.to_datetime(time_series['service_date_time']).dt.year
    time_series['quarter'] = pd.to_datetime(time_series['service_date_time']).dt.quarter
    time_series['day_of_year'] = pd.to_datetime(time_series['service_date_time']).dt.dayofyear
    return time_series

def add_holiday_feature(time_series: pd.DataFrame) -> None:
    us_holidays = holidays.US(observed=False)
    time_series['holiday'] = time_series['service_date_time'].apply(lambda x: us_holidays.get(x))
    return time_series

def main():
    time_series = pd.read_csv('./data/processed/time_series.csv')
    time_series = add_time_features(time_series)
    logging.info("Temporal features added to the time series data.")
    time_series = add_holiday_feature(time_series)
    logging.info("Holiday feature added to the time series data.")
    time_series.to_csv('data/processed/time_series_with_features.csv', index=False)
    logging.info("Time series data with features saved to data/processed folder.")

if __name__ == "__main__":
    main()